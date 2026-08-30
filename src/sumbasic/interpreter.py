#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#pylint:disable=W0301
#  
#  Copyright 2018- William Martinez Bas <metfar@gmail.com>
#  
#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 2 of the License, or
#  (at your option) any later version.
#  
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#  
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software
#  Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#  MA 02110-1301, USA.
#  
import re;
import threading;
import time;
from pathlib import Path;

from .audio import AudioEngine, GW_BASIC_SOUND_MAX_HZ, GW_BASIC_SOUND_MIN_HZ, MusicParseError, gw_ticks_to_seconds, spectrum_frequency_pitch, spectrum_pitch_frequency;
from .channels import ChannelManager, channel_number;
from .database import BasicDatabase;
from .expressions import ExpressionEvaluator;
from .program import BasicProgram;
from .types import BasicArray, base_type, coerce_value, default_value, normalize_type, suffix_type;
from .vocabulary import GRAPHICS_FUNCTION_STUBS, GRAPHICS_STUBS;


class BasicError(RuntimeError):
    pass;


class _StopProgram(Exception):
    pass;


class _BasicStop(Exception):
    def __init__(self, next_pc, line_number=None):
        super().__init__(next_pc, line_number);
        self.next_pc = int(next_pc);
        self.line_number = line_number;


class BasicInterpreter:
    def __init__(self, input_func=input, output_func=print, inkey_func=None, sleep_func=None, now_func=None, tone_func=None):
        self.program = BasicProgram();
        self.variables = {};
        self.variable_types = {};
        self.arrays = {};
        self.shared_variables = set();
        self.channels = ChannelManager();
        self.database = None;
        self.input_func = input_func;
        self.output_func = output_func;
        self.inkey_func = inkey_func if inkey_func is not None else (lambda: "");
        self.sleep_func = sleep_func if sleep_func is not None else time.sleep;
        self.audio = AudioEngine(tone_func=tone_func, sleep_func=self.sleep_func);
        self.tone_player = self.audio.sound_player;
        self.tone_func = tone_func if tone_func is not None else self.audio.sound;
        self.expr = ExpressionEvaluator(self.variables, self.variable_types, self.arrays, extra_functions={
            "EOF": lambda channel: self.channels.eof(channel),
            "LOF": lambda channel: self.channels.lof(channel),
            "LOC": lambda channel: self.channels.loc(channel),
            "FREEFILE": lambda: self.channels.freefile(),
            "DBRECNO": lambda: self._db().recno(),
            "DBRECCOUNT": lambda: self._db().reccount(),
            "INKEY$": lambda: self.inkey_func(),
            "POINT": lambda *args: self._stub_function("POINT", 0),
            "SCREEN$": lambda *args: self._stub_function("SCREEN$", ""),
            "ATTR": lambda *args: self._stub_function("ATTR", 0),
            "PEEK": lambda *args: 0,
            "IN": lambda *args: 0,
            "USR": lambda *args: 0,
        }, now_func=now_func);
        self.gosub_stack = [];
        self.for_stack = [];
        self.data = [];
        self.data_index = 0;
        self.data_line_index = {};
        self.option_base = 0;
        self.stop_requested = threading.Event();
        self.stopped_by_request = False;
        self.stopped_by_statement = False;
        self._resume_context = None;

    def reset_runtime(self):
        self.channels.close_all();
        self.variables.clear();
        self.variable_types.clear();
        self.arrays.clear();
        self.shared_variables.clear();
        self.gosub_stack = [];
        self.for_stack = [];
        self.data = [];
        self.data_index = 0;
        self.data_line_index = {};
        self.option_base = 0;
        self._resume_context = None;
        self.stopped_by_statement = False;

    def _db(self):
        if self.database is None: self.database = BasicDatabase(max_areas=10);
        return self.database;

    def _stub_function(self, name, default):
        self._emit("{}: NOT IMPLEMENTED YET".format(name));
        return default;

    def _channel_value(self, token):
        raw = str(token).strip();
        if raw.startswith("#"): raw = raw[1:].strip();
        if len(raw) == 1 and raw.isalpha(): return channel_number(raw);
        try: return channel_number(int(self.expr.eval(raw)));
        except Exception: return channel_number(raw);

    def _parse_open_source(self, raw):
        text = str(raw).strip();
        if text.upper() in ("STDIN", "STDOUT", "STDERR"): return text.lower() + ":";
        return str(self.expr.eval(text));

    def _format_value(self, value):
        if isinstance(value, complex):
            real = value.real;
            imag = value.imag;
            real_text = str(int(real)) if float(real).is_integer() else str(real);
            imag_text = str(int(abs(imag))) if float(abs(imag)).is_integer() else str(abs(imag));
            if imag == 0: return real_text;
            if real == 0: return ("-" if imag < 0 else "") + imag_text + "i";
            return real_text + ("-" if imag < 0 else "+") + imag_text + "i";
        if isinstance(value, float) and value.is_integer(): return str(int(value));
        return str(value);

    def _emit(self, text="", end="\n"):
        try:
            self.output_func(str(text), end=end);
        except TypeError:
            self.output_func(str(text) + ("" if end == "" else end.rstrip("\n")));

    def _hash_is_channel(self, source, position):
        rest = str(source)[position + 1:];
        if not re.match(r"\s*(?:[A-Ja-j]|\d+)", rest): return False;
        before = str(source)[:position].rstrip();
        return bool(re.search(r"(?:\bAS|\bOPEN|\bCLOSE|\bFIELD|\bGET|\bPUT|\bPRINT|\bWRITE|\bINPUT|\bLINE\s+INPUT)\s*$", before, re.I));

    def _strip_comment(self, source):
        text = str(source);
        output = [];
        quote = False;
        index = 0;
        while index < len(text):
            char = text[index];
            if char == '"':
                quote = not quote;
                output.append(char);
                index += 1;
                continue;
            if not quote and char == "'": break;
            if not quote and char == "#" and not self._hash_is_channel(text, index): break;
            output.append(char);
            index += 1;
        return "".join(output).rstrip();

    def _split_top_level(self, source, separators=",", keep_empty=False):
        items = [];
        current = [];
        quote = False;
        depth = 0;
        for char in str(source):
            if char == '"':
                quote = not quote;
                current.append(char);
                continue;
            if not quote and char in "([{": depth += 1;
            elif not quote and char in ")]}": depth -= 1;
            if not quote and depth == 0 and char in separators:
                value = "".join(current).strip();
                if value or keep_empty: items.append(value);
                current = [];
            else:
                current.append(char);
        value = "".join(current).strip();
        if value or keep_empty: items.append(value);
        return items;

    def _split_colon(self, source):
        return self._split_top_level(source, separators=":", keep_empty=False);

    def _split_print(self, source):
        items = [];
        current = [];
        quote = False;
        depth = 0;
        for char in str(source):
            if char == '"':
                quote = not quote;
                current.append(char);
                continue;
            if not quote and char in "([{": depth += 1;
            elif not quote and char in ")]}": depth -= 1;
            if not quote and depth == 0 and char in ";,":
                items.append(("".join(current).strip(), char));
                current = [];
            else:
                current.append(char);
        items.append(("".join(current).strip(), None));
        return items;

    def _coerce_input(self, name, text):
        if suffix_type(name) == "STRING": return str(text);
        value = str(text).strip();
        if value == "": return 0;
        try: return float(value) if any(char in value for char in ".eE") else int(value);
        except ValueError: return value;

    def _build_execution(self):
        execution = [];
        line_to_pc = {};
        self.execution_label_by_pc = {};
        self.execution_named_label_by_pc = {};
        self.named_label_pc = {};
        pending_named = [];
        for number, source, explicit_label in self.program.execution_records():
            first_pc = len(execution);
            if explicit_label is not None:
                line_to_pc[int(explicit_label)] = first_pc;
            clean = self._strip_comment(source);
            label_match = re.match(r"^\s*:([A-Za-z_][A-Za-z0-9_]*)(?::|$)(.*)$", clean);
            if label_match:
                label = label_match.group(1).upper();
                if label in line_to_pc:
                    raise BasicError("Duplicate label {}".format(label));
                line_to_pc[label] = len(execution);
                self.named_label_pc[label] = len(execution);
                pending_named.append(label);
                clean = (label_match.group(2) or "").strip();
            for statement in self._split_colon(clean):
                statement_pc = len(execution);
                execution.append((int(number), statement));
                if explicit_label is not None:
                    self.execution_label_by_pc[statement_pc] = int(explicit_label);
                if pending_named:
                    self.execution_named_label_by_pc[statement_pc] = tuple(pending_named);
                    pending_named = [];
        return execution, line_to_pc;

    def _parse_data_value(self, source):
        text = str(source).strip();
        if text == "": return "";
        if len(text) >= 2 and text[0] == text[-1] == '"': return text[1:-1].replace('""', '"');
        if re.fullmatch(r"[+-]?&H[0-9A-Fa-f]+", text):
            sign = -1 if text.startswith("-") else 1;
            raw = text.lstrip("+-")[2:];
            return sign * int(raw, 16);
        if re.fullmatch(r"[+-]?&O[0-7]+", text):
            sign = -1 if text.startswith("-") else 1;
            raw = text.lstrip("+-")[2:];
            return sign * int(raw, 8);
        if re.fullmatch(r"[+-]?&B[01]+", text):
            sign = -1 if text.startswith("-") else 1;
            raw = text.lstrip("+-")[2:];
            return sign * int(raw, 2);
        if re.fullmatch(r"[+-]?\d+", text): return int(text);
        if re.fullmatch(r"[+-]?(?:\d+\.\d*|\d*\.\d+)(?:[Ee][+-]?\d+)?", text) or re.fullmatch(r"[+-]?\d+[Ee][+-]?\d+", text): return float(text);
        return text;

    def _scan_data(self, execution):
        data = [];
        lines = {};
        data_positions = [];
        for pc, (_, statement) in enumerate(execution):
            match = re.match(r"^DATA(?:\s+(.*))?$", statement, re.I);
            if not match: continue;
            explicit_label = getattr(self, "execution_label_by_pc", {}).get(pc);
            if explicit_label is not None and explicit_label not in lines:
                lines[explicit_label] = len(data);
            data_positions.append((pc, len(data)));
            for item in self._split_top_level(match.group(1) or "", separators=",", keep_empty=True): data.append(self._parse_data_value(item));
        for label, label_pc in getattr(self, "named_label_pc", {}).items():
            for data_pc, data_index in data_positions:
                if data_pc >= label_pc:
                    lines[label] = data_index;
                    break;
        self.data = data;
        self.data_line_index = lines;
        self.data_index = 0;

    def request_stop(self):
        """Request cooperative termination of the currently running BASIC program."""
        self.stop_requested.set();
        self.audio.stop_all();
        return True;

    def _stop_if_requested(self):
        if self.stop_requested.is_set():
            self.stopped_by_request = True;
            raise _StopProgram();
        return None;

    @property
    def can_continue(self):
        return self._resume_context is not None;

    def _execute_context(self, context, pc):
        execution, line_to_pc, block_if, while_blocks, do_blocks = context;
        self.stopped_by_statement = False;
        try:
            while pc < len(execution):
                self._stop_if_requested();
                number, statement = execution[pc];
                pc = self._execute_statement(statement, pc, number, execution, line_to_pc, block_if, while_blocks, do_blocks);
        except _BasicStop as stopped:
            self.stopped_by_statement = True;
            self._resume_context = (context, stopped.next_pc);
            where = stopped.line_number;
            self._emit("Break" if where is None else "Break in {}".format(where));
        except _StopProgram:
            self._resume_context = None;
        else:
            self._resume_context = None;
        return dict(self.variables);

    def _validate_statement_syntax(self, source, line_number):
        """Validate statement recognition without executing program side effects.

        This is intentionally a syntax/recognition pass, not a type checker.  It
        catches commands that the runtime would reject (the gap that made an
        older cached a14 report PLAY as OK under --check) while allowing
        expressions whose values are only known at run time.
        """
        text = str(source).strip();
        upper = text.upper();
        if not text or upper.startswith("REM ") or upper == "REM": return True;
        if upper in ("END", "SYSTEM", "STOP", "CLS", "RETURN", "WEND", "ELSE", "END IF", "ENDIF"):
            return True;
        if upper.startswith("DATA") and (upper == "DATA" or upper.startswith("DATA ")): return True;
        patterns = (
            r"^OPTION\s+BASE\s+[01]$",
            r"^DIM\s+(?:SHARED\s+)?.+$",
            r"^REDIM\s+(?:PRESERVE\s+)?.+$",
            r'^OPEN\s+.+?\s+FOR\s+(?:INPUT|OUTPUT|APPEND|BINARY|RANDOM)\s+AS\s+#?(?:[A-Ja-j]|\d+)(?:\s+LEN\s*=\s*.+)?$',
            r'^OPEN\s+.+?\s+MODE\s+["\'][^"\']+["\']\s+AS\s+#?(?:[A-Ja-j]|\d+)$',
            r'^CLOSE(?:\s+#?(?:[A-Ja-j]|\d+))?$',
            r'^FIELD\s+#(?:[A-Ja-j]|\d+)\s*,\s*.+$',
            r'^GET\s+#(?:[A-Ja-j]|\d+)\s*,\s*.+$',
            r'^PUT\s+#(?:[A-Ja-j]|\d+)\s*,\s*.+$',
            r'^LINE\s+INPUT\s+#(?:[A-Ja-j]|\d+)\s*,\s*[A-Za-z_][A-Za-z0-9_]*\$$',
            r'^INPUT\s+#(?:[A-Ja-j]|\d+)\s*,\s*.+$',
            r'^WRITE\s+#(?:[A-Ja-j]|\d+)\s*,?.*$',
            r'^PRINT\s+#(?:[A-Ja-j]|\d+)\s*,?.*$',
            r'^DB\.SELECT\s+.+$', r'^DB\.USE(?:\s+.+?)?(?:\s+ALIAS\s+[A-Za-z_][A-Za-z0-9_]*)?$',
            r'^DB\.GO\s+.+$', r'^DB\.SKIP(?:\s+.+)?$', r'^DB\.CLOSE$',
            r'^LOCATE\s+.+?\s*,\s*.+$',
            r'^(?:LINE\s+INPUT|INPUT)\s*(?:"[^"]*"\s*[;,])?\s*[A-Za-z_][A-Za-z0-9_]*[$%&!]?$',
            r'^GOTO\s+(?:[A-Za-z_][A-Za-z0-9_]*|\d+)$', r'^GOSUB\s+(?:[A-Za-z_][A-Za-z0-9_]*|\d+)$',
            r'^FOR\s+EACH\s+.+?\s+IN\s+.+$',
            r'^FOR\s+[A-Za-z_][A-Za-z0-9_]*[$%&!]?\s*=\s*.+?\s+TO\s+.+?(?:\s+STEP\s+.+)?$',
            r'^NEXT(?:\s+[A-Za-z_][A-Za-z0-9_]*[$%&!]?)?$', r'^WHILE\s+.+$',
            r'^DO(?:\s+(?:WHILE|UNTIL)\s+.+)?$', r'^LOOP(?:\s+(?:WHILE|UNTIL)\s+.+)?$',
            r'^READ\s+.+$', r'^RESTORE(?:\s+.+)?$', r'^SWAP\s+.+?,\s*.+$',
            r'^RANDOMIZE(?:\s+.+)?$', r'^PAUSE\s+.+$', r'^BEEP\s+.+$', r'^SOUND\s+.+$',
            r'^(?:PLAY|ZXPLAY|GWPLAY)\s+.+$',
        );
        if upper.startswith("PRINT") or text.startswith("?"): return True;
        if any(re.match(pattern, text, re.I) for pattern in patterns):
            if re.match(r"^(?:PLAY|ZXPLAY|GWPLAY)\s+", text, re.I):
                command, body = re.match(r"^(PLAY|ZXPLAY|GWPLAY)\s+(.+)$", text, re.I).groups();
                body = body.strip();
                if body.upper() not in ("OFF", "STOP"):
                    mode_match = re.match(r"^(FOREGROUND|BACKGROUND)\b\s*(.*)$", body, re.I);
                    if mode_match: body = mode_match.group(2).strip();
                    args = self._split_top_level(body, separators=",", keep_empty=False);
                    limit = 3 if command.upper() in ("PLAY", "ZXPLAY") else 1;
                    if not 1 <= len(args) <= limit:
                        raise BasicError("{} requires {} music string{} at line {}".format(command.upper(), "one to three" if limit == 3 else "one", "s" if limit == 3 else "", line_number));
            return True;
        if re.match(r"^IF\s+.+?\s+THEN(?:\s+.*)?$", text, re.I):
            match = re.match(r"^IF\s+(.+?)\s+THEN(?:\s+(.*))?$", text, re.I);
            tail = (match.group(2) or "").strip();
            if tail:
                then_part, else_part = self._split_inline_else(tail);
                for part in (then_part, else_part):
                    if part and not re.fullmatch(r"\d+", part): self._validate_statement_syntax(part, line_number);
            return True;
        assignment = re.match(r"^(?:LET\s+)?(.+?)\s*=\s*(.+)$", text, re.I);
        if assignment:
            target = assignment.group(1).strip();
            if re.fullmatch(r"[A-Za-z_][A-Za-z0-9_]*[$%&!]?", target) or re.fullmatch(r"[A-Za-z_][A-Za-z0-9_]*[$%&!]?\s*[\[(].*[\])]", target): return True;
        if re.match(r"^[A-Za-z_][A-Za-z0-9_]*[$%&!]?\s*\.", text): return True;
        if self._graphics_stub_name(text) is not None: return True;
        raise BasicError("Unsupported statement at line {}: {}".format(line_number, text));

    def check(self):
        """Validate block structure and runtime statement recognition without executing."""
        execution, line_to_pc = self._build_execution();
        self._match_blocks(execution, "IF", "END IF", else_word="ELSE");
        self._match_blocks(execution, "WHILE", "WEND");
        self._match_blocks(execution, "DO", "LOOP");
        for line_number, statement in execution:
            self._validate_statement_syntax(statement, line_number);
        # Jump targets are cheap to validate statically and make --check useful.
        for line_number, statement in execution:
            jump = re.match(r"^(?:GOTO|GOSUB)\s+([A-Za-z_][A-Za-z0-9_]*|\d+)$", statement.strip(), re.I);
            if jump:
                raw = jump.group(1); target = int(raw) if raw.isdigit() else raw.upper();
                if target not in line_to_pc: raise BasicError("Undefined target {} at line {}".format(raw, line_number));
        return True;

    def run(self):
        self.stop_requested.clear();
        self.stopped_by_request = False;
        self.stopped_by_statement = False;
        self._resume_context = None;
        self.reset_runtime();
        execution, line_to_pc = self._build_execution();
        self._scan_data(execution);
        context = (
            execution,
            line_to_pc,
            self._match_blocks(execution, "IF", "END IF", else_word="ELSE"),
            self._match_blocks(execution, "WHILE", "WEND"),
            self._match_blocks(execution, "DO", "LOOP"),
        );
        return self._execute_context(context, 0);

    def continue_run(self):
        if self._resume_context is None:
            raise BasicError("Cannot CONTINUE: no program is stopped");
        context, pc = self._resume_context;
        self._resume_context = None;
        self.stop_requested.clear();
        self.stopped_by_request = False;
        return self._execute_context(context, pc);

    def _match_blocks(self, execution, start_word, end_word, else_word=None):
        stack = [];
        mapping = {};
        for pc, (_, stmt) in enumerate(execution):
            upper = stmt.strip().upper();
            is_start = upper.startswith(start_word + " ") or upper == start_word;
            if start_word == "IF": is_start = is_start and upper.endswith("THEN");
            if is_start:
                stack.append((pc, None));
            elif else_word and upper == else_word and stack:
                start, _ = stack[-1];
                stack[-1] = (start, pc);
            elif upper.startswith(end_word) and stack:
                start, middle = stack.pop();
                mapping[start] = (middle, pc);
                mapping[pc] = start;
                if middle is not None: mapping[middle] = pc;
        return mapping;

    def _jump_line(self, target, line_to_pc):
        raw = str(target).strip();
        key = int(raw) if re.fullmatch(r"\d+", raw) else raw.upper();
        if key not in line_to_pc:
            kind = "line" if isinstance(key, int) else "label";
            raise BasicError("Undefined {} {}".format(kind, raw));
        return line_to_pc[key];

    def _parse_dimensions(self, source):
        bounds = [];
        for dimension in self._split_top_level(source, separators=",", keep_empty=False):
            explicit = re.match(r"^(.+?)\s+TO\s+(.+)$", dimension, re.I);
            if explicit:
                low = int(self.expr.eval(explicit.group(1)));
                high = int(self.expr.eval(explicit.group(2)));
            else:
                low = self.option_base;
                high = int(self.expr.eval(dimension));
            bounds.append((low, high));
        return bounds;

    def _declare_one(self, declaration, shared=False, redim=False, preserve=False):
        match = re.match(r"^([A-Za-z_][A-Za-z0-9_]*[$%&!]?)(?:\s*\((.*)\))?(?:\s+AS\s+(.+))?$", declaration.strip(), re.I);
        if not match: raise BasicError("Invalid DIM declaration: {}".format(declaration));
        name = match.group(1);
        dimensions = match.group(2);
        explicit_type = normalize_type(match.group(3));
        suffix = suffix_type(name);
        if explicit_type and suffix and base_type(explicit_type) != suffix:
            raise BasicError("Type conflict for {}: suffix specifies {}, AS specifies {}".format(name, suffix, explicit_type));
        type_name = explicit_type or suffix or "ANY";
        key = name.casefold();
        if name.upper() == "PI": raise BasicError("PI is a built-in constant and cannot be declared");
        if dimensions is not None:
            bounds = self._parse_dimensions(dimensions);
            if redim and key in self.arrays:
                self.arrays[key].resize(bounds, preserve=preserve);
            else:
                self.arrays[key] = BasicArray(name, bounds, type_name=type_name, shared=shared);
            if shared: self.shared_variables.add(key);
            return;
        if redim: raise BasicError("REDIM requires an array");
        self.variable_types[key] = type_name;
        self.expr.set(name, default_value(type_name));
        if shared: self.shared_variables.add(key);

    def _declare(self, body, shared=False, redim=False, preserve=False):
        for declaration in self._split_top_level(body, separators=",", keep_empty=False): self._declare_one(declaration, shared=shared, redim=redim, preserve=preserve);

    def _assign_target(self, target, value):
        text = str(target).strip();
        array_match = re.match(r"^([A-Za-z_][A-Za-z0-9_]*[$%&!]?)\s*\((.*)\)$", text);
        if array_match and array_match.group(1).casefold() in self.arrays:
            indices = [self.expr.eval(item) for item in self._split_top_level(array_match.group(2), separators=",", keep_empty=False)];
            self.arrays[array_match.group(1).casefold()].set(indices, value);
            return value;
        subscript = re.match(r"^([A-Za-z_][A-Za-z0-9_]*[$%&!]?)\s*\[(.*)\]$", text);
        if subscript:
            container = self.expr.get(subscript.group(1));
            key = self.expr.eval(subscript.group(2));
            container[key] = value;
            return value;
        if re.fullmatch(r"[A-Za-z_][A-Za-z0-9_]*[$%&!]?", text): return self.expr.set(text, value);
        raise BasicError("Invalid assignment target: {}".format(target));

    def _target_value(self, target):
        text = str(target).strip();
        array_match = re.match(r"^([A-Za-z_][A-Za-z0-9_]*[$%&!]?)\s*\((.*)\)$", text);
        if array_match and array_match.group(1).casefold() in self.arrays:
            indices = [self.expr.eval(item) for item in self._split_top_level(array_match.group(2), separators=",", keep_empty=False)];
            return self.arrays[array_match.group(1).casefold()].get(indices);
        subscript = re.match(r"^([A-Za-z_][A-Za-z0-9_]*[$%&!]?)\s*\[(.*)\]$", text);
        if subscript: return self.expr.get(subscript.group(1))[self.expr.eval(subscript.group(2))];
        return self.expr.get(text);

    def _restore(self, target=None):
        if target is None or str(target).strip() == "":
            self.data_index = 0;
            return;
        raw = str(target).strip();
        if re.fullmatch(r"[A-Za-z_][A-Za-z0-9_]*", raw):
            label = raw.upper();
            if label not in self.data_line_index: raise BasicError("RESTORE {} has no DATA at or after that label".format(raw));
            self.data_index = self.data_line_index[label];
            return;
        number = int(self.expr.eval(target));
        candidates = sorted(line for line in self.data_line_index if isinstance(line, int) and line >= number);
        if not candidates: raise BasicError("RESTORE {} has no DATA at or after that line".format(number));
        self.data_index = self.data_line_index[candidates[0]];

    def _execute_statement(self, source, pc, line_number, execution, line_to_pc, block_if, while_blocks, do_blocks):
        text = source.strip();
        upper = text.upper();
        if not text or upper.startswith("REM ") or upper == "REM": return pc + 1;
        if upper in ("END", "SYSTEM"): raise _StopProgram();
        if upper == "STOP": raise _BasicStop(pc + 1, line_number);
        if upper.startswith("DATA") and (upper == "DATA" or upper.startswith("DATA ")): return pc + 1;
        if upper == "CLS": self._emit("\033[2J\033[H", end=""); return pc + 1;
        match = re.match(r"^OPTION\s+BASE\s+([01])$", text, re.I);
        if match: self.option_base = int(match.group(1)); return pc + 1;
        match = re.match(r"^DIM\s+(SHARED\s+)?(.+)$", text, re.I);
        if match:
            self._declare(match.group(2), shared=bool(match.group(1))); return pc + 1;
        match = re.match(r"^REDIM\s+(PRESERVE\s+)?(.+)$", text, re.I);
        if match:
            self._declare(match.group(2), redim=True, preserve=bool(match.group(1))); return pc + 1;
        match = re.match(r'^OPEN\s+(.+?)\s+FOR\s+(INPUT|OUTPUT|APPEND|BINARY|RANDOM)\s+AS\s+#?([A-Ja-j]|\d+)(?:\s+LEN\s*=\s*(.+))?$', text, re.I);
        if match:
            source_name = self._parse_open_source(match.group(1));
            mode = match.group(2).lower();
            channel = self._channel_value(match.group(3));
            length = int(self.expr.eval(match.group(4))) if match.group(4) else 0;
            self.channels.open(source_name, mode, channel, record_length=length);
            return pc + 1;
        match = re.match(r'^OPEN\s+(.+?)\s+MODE\s+["\']([^"\']+)["\']\s+AS\s+#?([A-Ja-j]|\d+)$', text, re.I);
        if match:
            self.channels.open(self._parse_open_source(match.group(1)), match.group(2), self._channel_value(match.group(3))); return pc + 1;
        match = re.match(r'^CLOSE(?:\s+#?([A-Ja-j]|\d+))?$', text, re.I);
        if match:
            self.channels.close(self._channel_value(match.group(1))) if match.group(1) else self.channels.close_all(); return pc + 1;
        match = re.match(r'^FIELD\s+#([A-Ja-j]|\d+)\s*,\s*(.+)$', text, re.I);
        if match:
            definitions = [];
            for item in self._split_print(match.group(2).replace(";", ",")):
                part = item[0];
                if not part: continue;
                field_match = re.match(r'^(.+?)\s+AS\s+([A-Za-z_][A-Za-z0-9_]*\$)$', part, re.I);
                if not field_match: raise BasicError("Invalid FIELD definition: {}".format(part));
                definitions.append((int(self.expr.eval(field_match.group(1))), field_match.group(2)));
            self.channels.define_fields(self._channel_value(match.group(1)), definitions);
            for _, name in definitions: self.expr.set(name, "");
            return pc + 1;
        match = re.match(r'^GET\s+#([A-Ja-j]|\d+)\s*,\s*(.+)$', text, re.I);
        if match:
            channel = self.channels.get(self._channel_value(match.group(1)));
            data = self.channels.get_record(channel.number, int(self.expr.eval(match.group(2))));
            for field in channel.fields: self.expr.set(field.name, data[field.offset:field.offset + field.width].decode("latin-1").rstrip());
            return pc + 1;
        match = re.match(r'^PUT\s+#([A-Ja-j]|\d+)\s*,\s*(.+)$', text, re.I);
        if match:
            channel = self.channels.get(self._channel_value(match.group(1)));
            payload = bytearray(b" " * channel.record_length);
            for field in channel.fields:
                raw = str(self.expr.get(field.name)).encode("latin-1", errors="replace")[:field.width].ljust(field.width, b" ");
                payload[field.offset:field.offset + field.width] = raw;
            self.channels.put_record(channel.number, int(self.expr.eval(match.group(2))), payload);
            return pc + 1;
        match = re.match(r'^LINE\s+INPUT\s+#([A-Ja-j]|\d+)\s*,\s*([A-Za-z_][A-Za-z0-9_]*\$)$', text, re.I);
        if match:
            self.expr.set(match.group(2), self.channels.readline(self._channel_value(match.group(1)))); return pc + 1;
        match = re.match(r'^INPUT\s+#([A-Ja-j]|\d+)\s*,\s*(.+)$', text, re.I);
        if match:
            names = [item.strip() for item in match.group(2).split(",")];
            values = self.channels.input_values(self._channel_value(match.group(1)));
            if len(values) < len(names): raise BasicError("INPUT # returned fewer values than variables");
            for name, raw in zip(names, values): self._assign_target(name, self._coerce_input(name, raw));
            return pc + 1;
        match = re.match(r'^WRITE\s+#([A-Ja-j]|\d+)\s*,?\s*(.*)$', text, re.I);
        if match:
            import csv;
            import io;
            values = [self.expr.eval(item[0]) for item in self._split_print(match.group(2)) if item[0]];
            buffer = io.StringIO();
            writer = csv.writer(buffer, lineterminator="\n");
            writer.writerow(values);
            self.channels.print(self._channel_value(match.group(1)), buffer.getvalue().rstrip("\n"), end="\n");
            return pc + 1;
        match = re.match(r'^PRINT\s+#([A-Ja-j]|\d+)\s*,?\s*(.*)$', text, re.I);
        if match:
            body = match.group(2);
            items = self._split_print(body);
            trailing = body.rstrip().endswith((";", ","));
            rendered = "";
            for expression, separator in items:
                if expression: rendered += self._format_value(self.expr.eval(expression));
                if separator == ",": rendered += "\t";
            self.channels.print(self._channel_value(match.group(1)), rendered, end="" if trailing else "\n");
            return pc + 1;
        match = re.match(r'^DB\.SELECT\s+(.+)$', text, re.I);
        if match: self._db().select(self.expr.eval(match.group(1)) if not re.fullmatch(r'[A-Ja-j]', match.group(1).strip()) else match.group(1).strip()); return pc + 1;
        match = re.match(r'^DB\.USE(?:\s+(.+?))?(?:\s+ALIAS\s+([A-Za-z_][A-Za-z0-9_]*))?$', text, re.I);
        if match:
            table = self.expr.eval(match.group(1)) if match.group(1) else None;
            self._db().use(table, alias=match.group(2)); return pc + 1;
        match = re.match(r'^DB\.GO\s+(.+)$', text, re.I);
        if match: self._db().go(self.expr.eval(match.group(1)) if match.group(1).strip().upper() not in ("TOP", "BOTTOM") else match.group(1).strip().upper()); return pc + 1;
        match = re.match(r'^DB\.SKIP(?:\s+(.+))?$', text, re.I);
        if match: self._db().skip(int(self.expr.eval(match.group(1)))) if match.group(1) else self._db().skip(1); return pc + 1;
        if upper == "DB.CLOSE": self._db().close(); self.database = None; return pc + 1;
        match = re.match(r"^LOCATE\s+(.+?)\s*,\s*(.+)$", text, re.I);
        if match:
            row = int(self.expr.eval(match.group(1)));
            col = int(self.expr.eval(match.group(2)));
            self._emit("\033[{};{}H".format(row, col), end=""); return pc + 1;
        if upper.startswith("PRINT") or text.startswith("?"):
            body = text[1:].strip() if text.startswith("?") else text[5:].strip();
            if body.upper().startswith("USING "): return self._print_using(body[6:].strip(), pc);
            items = self._split_print(body);
            trailing = body.rstrip().endswith((";", ","));
            rendered = "";
            for expression, separator in items:
                if expression: rendered += self._format_value(self.expr.eval(expression));
                if separator == ",": rendered += "\t";
            self._emit(rendered, end="" if trailing else "\n");
            return pc + 1;
        match = re.match(r"^(LINE\s+INPUT|INPUT)\s*(?:\"([^\"]*)\"\s*([;,]))?\s*([A-Za-z_][A-Za-z0-9_]*[$%&!]?)$", text, re.I);
        if match:
            command = match.group(1).upper();
            prompt_text = match.group(2);
            separator = match.group(3);
            variable = match.group(4);
            if command == "INPUT":
                if prompt_text is None: prompt = "? ";
                elif separator == ";": prompt = prompt_text + "? ";
                else: prompt = prompt_text;
            else:
                prompt = prompt_text or "";
            raw = self.input_func(prompt);
            value = str(raw) if command.startswith("LINE") else self._coerce_input(variable, raw);
            self._assign_target(variable, value); return pc + 1;
        match = re.match(r"^IF\s+(.+?)\s+THEN(?:\s+(.*))?$", text, re.I);
        if match:
            condition = bool(self.expr.eval(match.group(1)));
            tail = (match.group(2) or "").strip();
            if tail:
                then_part, else_part = self._split_inline_else(tail);
                chosen = then_part if condition else else_part;
                if not chosen: return pc + 1;
                if re.fullmatch(r"\d+", chosen): return self._jump_line(chosen, line_to_pc);
                return self._execute_statement(chosen, pc, line_number, execution, line_to_pc, block_if, while_blocks, do_blocks) if chosen.upper() != text.upper() else pc + 1;
            middle, end = block_if.get(pc, (None, None));
            if end is None: raise BasicError("IF without END IF at line {}".format(line_number));
            if not condition: return (middle + 1) if middle is not None else end + 1;
            return pc + 1;
        if upper == "ELSE": return block_if.get(pc, pc) + 1;
        if upper in ("END IF", "ENDIF"): return pc + 1;
        match = re.match(r"^GOTO\s+([A-Za-z_][A-Za-z0-9_]*|\d+)$", text, re.I);
        if match: return self._jump_line(match.group(1), line_to_pc);
        match = re.match(r"^GOSUB\s+([A-Za-z_][A-Za-z0-9_]*|\d+)$", text, re.I);
        if match:
            self.gosub_stack.append(pc + 1); return self._jump_line(match.group(1), line_to_pc);
        if upper == "RETURN":
            if not self.gosub_stack: raise BasicError("RETURN without GOSUB");
            return self.gosub_stack.pop();
        match = re.match(r"^FOR\s+EACH\s+(.+?)\s+IN\s+(.+)$", text, re.I);
        if match:
            names = [item.strip() for item in self._split_top_level(match.group(1), separators=",", keep_empty=False)];
            collection = self.expr.eval(match.group(2));
            values = list(collection.items()) if isinstance(collection, dict) and len(names) == 2 else list(collection);
            next_pc = self._find_next(execution, pc);
            if not values: return next_pc + 1;
            frame = {"kind": "each", "names": names, "values": values, "index": 0, "for_pc": pc, "next_pc": next_pc};
            self.for_stack.append(frame);
            self._assign_each_frame(frame);
            return pc + 1;
        match = re.match(r"^FOR\s+([A-Za-z_][A-Za-z0-9_]*[$%&!]?)\s*=\s*(.+?)\s+TO\s+(.+?)(?:\s+STEP\s+(.+))?$", text, re.I);
        if match:
            name = match.group(1);
            start = self.expr.eval(match.group(2));
            end = self.expr.eval(match.group(3));
            step = self.expr.eval(match.group(4)) if match.group(4) else 1;
            self.expr.set(name, start);
            next_pc = self._find_next(execution, pc);
            self.for_stack.append({"kind": "numeric", "name": name, "end": end, "step": step, "for_pc": pc, "next_pc": next_pc});
            return pc + 1;
        match = re.match(r"^NEXT(?:\s+([A-Za-z_][A-Za-z0-9_]*[$%&!]?))?$", text, re.I);
        if match:
            if not self.for_stack: raise BasicError("NEXT without FOR");
            frame = self.for_stack[-1];
            if frame.get("kind") == "each":
                frame["index"] += 1;
                if frame["index"] < len(frame["values"]):
                    self._assign_each_frame(frame); return frame["for_pc"] + 1;
                self.for_stack.pop(); return pc + 1;
            value = self.expr.get(frame["name"]) + frame["step"];
            self.expr.set(frame["name"], value);
            keep = value <= frame["end"] if frame["step"] >= 0 else value >= frame["end"];
            if keep: return frame["for_pc"] + 1;
            self.for_stack.pop(); return pc + 1;
        match = re.match(r"^WHILE\s+(.+)$", text, re.I);
        if match:
            if bool(self.expr.eval(match.group(1))): return pc + 1;
            pair = while_blocks.get(pc);
            return (pair[1] + 1) if isinstance(pair, tuple) else pc + 1;
        if upper == "WEND": return while_blocks.get(pc, pc);
        match = re.match(r"^DO(?:\s+(WHILE|UNTIL)\s+(.+))?$", text, re.I);
        if match:
            if match.group(1):
                condition = bool(self.expr.eval(match.group(2)));
                condition = (not condition) if match.group(1).upper() == "UNTIL" else condition;
                if not condition:
                    pair = do_blocks.get(pc);
                    return (pair[1] + 1) if isinstance(pair, tuple) else pc + 1;
            return pc + 1;
        match = re.match(r"^LOOP(?:\s+(WHILE|UNTIL)\s+(.+))?$", text, re.I);
        if match:
            start = do_blocks.get(pc, pc);
            if match.group(1):
                condition = bool(self.expr.eval(match.group(2)));
                condition = (not condition) if match.group(1).upper() == "UNTIL" else condition;
                return start if condition else pc + 1;
            return start;
        match = re.match(r"^READ\s+(.+)$", text, re.I);
        if match:
            for name in self._split_top_level(match.group(1), separators=",", keep_empty=False):
                if self.data_index >= len(self.data): raise BasicError("Out of DATA");
                self._assign_target(name, self.data[self.data_index]);
                self.data_index += 1;
            return pc + 1;
        match = re.match(r"^RESTORE(?:\s+(.+))?$", text, re.I);
        if match:
            self._restore(match.group(1)); return pc + 1;
        match = re.match(r"^SWAP\s+(.+?),\s*(.+)$", text, re.I);
        if match:
            first = match.group(1).strip();
            second = match.group(2).strip();
            first_value = self._target_value(first);
            second_value = self._target_value(second);
            self._assign_target(first, second_value);
            self._assign_target(second, first_value);
            return pc + 1;
        match = re.match(r"^RANDOMIZE(?:\s+(.+))?$", text, re.I);
        if match:
            seed = self.expr.eval(match.group(1)) if match.group(1) else None;
            self.expr.random.seed(seed); return pc + 1;
        match = re.match(r"^PAUSE\s+(.+)$", text, re.I);
        if match:
            frames = float(self.expr.eval(match.group(1)));
            if frames < 0: raise BasicError("PAUSE requires a non-negative frame count");
            if frames == 0:
                while not self.inkey_func():
                    self._stop_if_requested();
                    self.sleep_func(0.01);
            else:
                self.sleep_func(frames / 50.0);
                self._stop_if_requested();
            return pc + 1;
        match = re.match(r"^BEEP\s+(.+)$", text, re.I);
        if match:
            args = self._split_top_level(match.group(1), separators=",", keep_empty=False);
            if len(args) != 2: raise BasicError("BEEP requires: duration, pitch");
            duration = float(self.expr.eval(args[0]));
            pitch = float(self.expr.eval(args[1]));
            if duration < 0: raise BasicError("BEEP duration must be non-negative");
            frequency = spectrum_pitch_frequency(pitch);
            self.audio.beep(frequency, duration);
            return pc + 1;
        match = re.match(r"^SOUND\s+(.+)$", text, re.I);
        if match:
            args = self._split_top_level(match.group(1), separators=",", keep_empty=False);
            if len(args) != 2: raise BasicError("SOUND requires: frequency, duration");
            frequency = float(self.expr.eval(args[0]));
            ticks = float(self.expr.eval(args[1]));
            if frequency < GW_BASIC_SOUND_MIN_HZ or frequency > GW_BASIC_SOUND_MAX_HZ:
                raise BasicError("SOUND frequency must be between 37 and 32767 Hz");
            if ticks < 0: raise BasicError("SOUND duration must be non-negative");
            # SOUND speaks in Hertz, but the actual tone is rendered by the same
            # fractional-semitone generator as BEEP.  The round trip is deliberate:
            # it preserves SOUND syntax/units while keeping one monophonic backend.
            pitch = spectrum_frequency_pitch(frequency);
            tone_frequency = spectrum_pitch_frequency(pitch);
            self.audio.sound(tone_frequency, gw_ticks_to_seconds(ticks));
            return pc + 1;
        match = re.match(r"^(PLAY|ZXPLAY|GWPLAY)\s+(.+)$", text, re.I);
        if match:
            command = match.group(1).upper();
            body = match.group(2).strip();
            if body.upper() in ("OFF", "STOP"):
                self.audio.stop_music(); return pc + 1;
            mode = None;
            mode_match = re.match(r"^(FOREGROUND|BACKGROUND)\b\s*(.*)$", body, re.I);
            if mode_match:
                mode = mode_match.group(1).upper();
                body = mode_match.group(2).strip();
            args = self._split_top_level(body, separators=",", keep_empty=False);
            try:
                if command in ("PLAY", "ZXPLAY"):
                    if not 1 <= len(args) <= 3: raise BasicError("{} requires one to three music strings".format(command));
                    strings = [str(self.expr.eval(arg)) for arg in args];
                    self.audio.zxplay(strings, background=(mode == "BACKGROUND"));
                else:
                    if len(args) != 1: raise BasicError("GWPLAY requires one music string");
                    self.audio.gwplay(str(self.expr.eval(args[0])), mode=mode);
            except MusicParseError as exc:
                raise BasicError(str(exc)) from exc;
            return pc + 1;
        assignment = re.match(r"^(?:LET\s+)?(.+?)\s*=\s*(.+)$", text, re.I);
        if assignment:
            target = assignment.group(1).strip();
            if re.fullmatch(r"[A-Za-z_][A-Za-z0-9_]*[$%&!]?", target) or re.fullmatch(r"[A-Za-z_][A-Za-z0-9_]*[$%&!]?\s*[\[(].*[\])]", target):
                self._assign_target(target, self.expr.eval(assignment.group(2))); return pc + 1;
        if re.match(r"^[A-Za-z_][A-Za-z0-9_]*[$%&!]?\s*\.", text):
            self.expr.eval(text); return pc + 1;
        command = self._graphics_stub_name(text);
        if command is not None:
            self._emit("{}: NOT IMPLEMENTED YET".format(command)); return pc + 1;
        raise BasicError("Unsupported statement at line {}: {}".format(line_number, text));

    def _assign_each_frame(self, frame):
        value = frame["values"][frame["index"]];
        names = frame["names"];
        if len(names) == 1:
            self._assign_target(names[0], value); return;
        if not isinstance(value, (tuple, list)) or len(value) < len(names): raise BasicError("FOR EACH value cannot be unpacked");
        for name, item in zip(names, value): self._assign_target(name, item);

    def _graphics_stub_name(self, text):
        upper = str(text).strip().upper();
        for command in sorted(GRAPHICS_STUBS, key=len, reverse=True):
            if upper == command or upper.startswith(command + " "): return command;
        return None;

    def _split_inline_else(self, tail):
        match = re.match(r"^(.*?)(?:\s+ELSE\s+)(.*)$", tail, re.I);
        return (match.group(1).strip(), match.group(2).strip()) if match else (tail.strip(), "");

    def _find_next(self, execution, pc):
        depth = 0;
        for index in range(pc + 1, len(execution)):
            upper = execution[index][1].strip().upper();
            if upper.startswith("FOR "): depth += 1;
            elif upper.startswith("NEXT"):
                if depth == 0: return index;
                depth -= 1;
        raise BasicError("FOR without NEXT");

    def _print_using(self, body, pc):
        parts = self._split_print(body);
        if not parts or not parts[0][0]: raise BasicError("PRINT USING requires a format");
        fmt = str(self.expr.eval(parts[0][0]));
        values = [self.expr.eval(item[0]) for item in parts[1:] if item[0]];
        rendered = fmt;
        for value in values:
            token = re.search(r"[#]+(?:\.[#]+)?", rendered);
            if token:
                mask = token.group(0);
                decimals = len(mask.split(".", 1)[1]) if "." in mask else 0;
                width = len(mask);
                replacement = ("{:>%d.%df}" % (width, decimals)).format(float(value)) if decimals else ("{:>%dd}" % width).format(int(value));
                rendered = rendered[:token.start()] + replacement + rendered[token.end():];
            else:
                rendered += self._format_value(value);
        self._emit(rendered); return pc + 1;

    def execute_immediate(self, source):
        text = self._strip_comment(str(source).strip());
        if not text: return None;
        numbered = re.match(r"^(\d+)\s*(.*)$", text);
        if numbered:
            self.program.set_numbered_line(int(numbered.group(1)), numbered.group(2)); return None;
        upper = text.upper();
        if upper == "RUN": return self.run();
        if upper in ("CONTINUE", "CONT"): return self.continue_run();
        if upper == "LIST": self._emit(self.program.source_text(), end=""); return None;
        if upper == "NEW": self.program.clear(); self.reset_runtime(); return None;
        match = re.match(r'^LOAD\s+"?([^\"]+)"?$', text, re.I);
        if match: self.program.load_file(match.group(1)); return None;
        match = re.match(r'^SAVE(?:\s+"?([^\"]+)"?)?$', text, re.I);
        if match: self.program.save_file(match.group(1) or None); return None;
        match = re.match(r"^DELETE\s+(\d+)(?:-(\d+))?$", text, re.I);
        if match: self.program.delete_range(match.group(1), match.group(2)); return None;
        match = re.match(r"^RENUM(?:\s+(\d+)(?:\s*,\s*(\d+))?)?$", text, re.I);
        if match: self.program.renumber(match.group(1) or 10, match.group(2) or 10); return None;
        old_program = self.program;
        temp = BasicProgram();
        temp.free_lines = [text];
        self.program = temp;
        execution, line_to_pc = self._build_execution();
        try:
            self._execute_statement(text, 0, 1, execution, line_to_pc, {}, {}, {});
        finally:
            self.program = old_program;
        return None;
