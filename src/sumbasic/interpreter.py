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
from pathlib import Path;

from .channels import ChannelError, ChannelManager, channel_number;
from .database import BasicDatabase;
from .expressions import ExpressionEvaluator;
from .program import BasicProgram;


class BasicError(RuntimeError):
    pass;


class _StopProgram(Exception):
    pass;


class BasicInterpreter:
    def __init__(self, input_func=input, output_func=print):
        self.program = BasicProgram();
        self.variables = {};
        self.channels = ChannelManager();
        self.database = None;
        self.expr = ExpressionEvaluator(self.variables, extra_functions={
            "EOF": lambda channel: self.channels.eof(channel),
            "LOF": lambda channel: self.channels.lof(channel),
            "LOC": lambda channel: self.channels.loc(channel),
            "FREEFILE": lambda: self.channels.freefile(),
            "DBRECNO": lambda: self._db().recno(),
            "DBRECCOUNT": lambda: self._db().reccount(),
        });
        self.input_func = input_func;
        self.output_func = output_func;
        self.gosub_stack = [];
        self.for_stack = [];
        self.data = [];
        self.data_index = 0;
        self.arrays = {};

    def reset_runtime(self):
        self.channels.close_all();
        self.variables.clear();
        self.gosub_stack = [];
        self.for_stack = [];
        self.data = [];
        self.data_index = 0;
        self.arrays = {};


    def _db(self):
        if self.database is None:
            self.database = BasicDatabase(max_areas=10);
        return self.database;

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

    def _emit(self, text="", end="\n"):
        try:
            self.output_func(str(text), end=end);
        except TypeError:
            self.output_func(str(text) + ("" if end == "" else end.rstrip("\n")));

    def _split_colon(self, source):
        out = [];
        current = [];
        quote = None;
        depth = 0;
        for char in str(source):
            if quote:
                current.append(char);
                if char == quote: quote = None;
                continue;
            if char == '"': quote = char; current.append(char);
            elif char == "(": depth += 1; current.append(char);
            elif char == ")": depth -= 1; current.append(char);
            elif char == ":" and depth == 0:
                out.append("".join(current).strip()); current = [];
            else: current.append(char);
        out.append("".join(current).strip());
        return [item for item in out if item];

    def _split_print(self, source):
        items = [];
        current = [];
        quote = None;
        depth = 0;
        sep = None;
        for char in str(source):
            if quote:
                current.append(char);
                if char == quote: quote = None;
                continue;
            if char == '"': quote = char; current.append(char);
            elif char == "(": depth += 1; current.append(char);
            elif char == ")": depth -= 1; current.append(char);
            elif char in ";," and depth == 0:
                items.append(("".join(current).strip(), char)); current = [];
            else: current.append(char);
        items.append(("".join(current).strip(), None));
        return items;

    def _coerce_input(self, name, text):
        if str(name).endswith("$"): return str(text);
        value = str(text).strip();
        if value == "": return 0;
        try: return float(value) if any(c in value for c in ".eE") else int(value);
        except ValueError: return value;

    def _build_execution(self):
        execution = [];
        line_to_pc = {};
        for number, source in self.program.source_lines():
            line_to_pc[int(number)] = len(execution);
            for statement in self._split_colon(source):
                execution.append((int(number), statement));
        return execution, line_to_pc;

    def _scan_data(self, execution):
        data = [];
        for _, statement in execution:
            match = re.match(r"^DATA\s+(.+)$", statement, re.I);
            if not match: continue;
            for item in self._split_print(match.group(1).replace(";", ",")):
                source = item[0];
                if source:
                    try: data.append(self.expr.eval(source));
                    except Exception: data.append(source.strip().strip('"'));
        self.data = data;
        self.data_index = 0;

    def run(self):
        self.reset_runtime();
        execution, line_to_pc = self._build_execution();
        self._scan_data(execution);
        block_if = self._match_blocks(execution, "IF", "END IF", else_word="ELSE");
        while_blocks = self._match_blocks(execution, "WHILE", "WEND");
        do_blocks = self._match_blocks(execution, "DO", "LOOP");
        pc = 0;
        try:
            while pc < len(execution):
                number, statement = execution[pc];
                pc = self._execute_statement(statement, pc, number, execution, line_to_pc, block_if, while_blocks, do_blocks);
        except _StopProgram:
            pass;
        return dict(self.variables);

    def _match_blocks(self, execution, start_word, end_word, else_word=None):
        stack = [];
        mapping = {};
        for pc, (_, stmt) in enumerate(execution):
            upper = stmt.strip().upper();
            is_start = upper.startswith(start_word + " ") or upper == start_word;
            if start_word == "IF":
                is_start = is_start and upper.endswith("THEN");
            if is_start:
                stack.append((pc, None));
            elif else_word and upper == else_word and stack:
                start, _ = stack[-1]; stack[-1] = (start, pc);
            elif upper.startswith(end_word) and stack:
                start, middle = stack.pop();
                mapping[start] = (middle, pc); mapping[pc] = start;
                if middle is not None: mapping[middle] = pc;
        return mapping;

    def _jump_line(self, target, line_to_pc):
        number = int(target);
        if number not in line_to_pc: raise BasicError("Undefined line {}".format(number));
        return line_to_pc[number];

    def _execute_statement(self, source, pc, line_number, execution, line_to_pc, block_if, while_blocks, do_blocks):
        text = source.strip();
        upper = text.upper();
        if not text or upper.startswith("REM ") or upper == "REM" or text.startswith("'"): return pc + 1;
        if upper in ("END", "SYSTEM"): raise _StopProgram();
        if upper == "STOP": raise _StopProgram();
        if upper.startswith("DATA "): return pc + 1;
        if upper == "CLS": self._emit("\033[2J\033[H", end=""); return pc + 1;
        match = re.match(r'^OPEN\s+(.+?)\s+FOR\s+(INPUT|OUTPUT|APPEND|BINARY|RANDOM)\s+AS\s+#?([A-Ja-j]|\d+)(?:\s+LEN\s*=\s*(.+))?$', text, re.I);
        if match:
            source_name = self._parse_open_source(match.group(1)); mode = match.group(2).lower(); channel = self._channel_value(match.group(3));
            length = int(self.expr.eval(match.group(4))) if match.group(4) else 0; self.channels.open(source_name, mode, channel, record_length=length); return pc + 1;
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
            channel = self.channels.get(self._channel_value(match.group(1))); data = self.channels.get_record(channel.number, int(self.expr.eval(match.group(2))));
            for field in channel.fields: self.expr.set(field.name, data[field.offset:field.offset + field.width].decode("latin-1").rstrip());
            return pc + 1;
        match = re.match(r'^PUT\s+#([A-Ja-j]|\d+)\s*,\s*(.+)$', text, re.I);
        if match:
            channel = self.channels.get(self._channel_value(match.group(1))); payload = bytearray(b" " * channel.record_length);
            for field in channel.fields:
                raw = str(self.expr.get(field.name)).encode("latin-1", errors="replace")[:field.width].ljust(field.width, b" "); payload[field.offset:field.offset + field.width] = raw;
            self.channels.put_record(channel.number, int(self.expr.eval(match.group(2))), payload); return pc + 1;
        match = re.match(r'^LINE\s+INPUT\s+#([A-Ja-j]|\d+)\s*,\s*([A-Za-z_][A-Za-z0-9_]*\$)$', text, re.I);
        if match:
            self.expr.set(match.group(2), self.channels.readline(self._channel_value(match.group(1)))); return pc + 1;
        match = re.match(r'^INPUT\s+#([A-Ja-j]|\d+)\s*,\s*(.+)$', text, re.I);
        if match:
            names = [item.strip() for item in match.group(2).split(",")]; values = self.channels.input_values(self._channel_value(match.group(1)));
            if len(values) < len(names): raise BasicError("INPUT # returned fewer values than variables");
            for name, raw in zip(names, values): self.expr.set(name, self._coerce_input(name, raw));
            return pc + 1;
        match = re.match(r'^WRITE\s+#([A-Ja-j]|\d+)\s*,?\s*(.*)$', text, re.I);
        if match:
            import csv; import io;
            values = [self.expr.eval(item[0]) for item in self._split_print(match.group(2)) if item[0]]; buffer = io.StringIO(); writer = csv.writer(buffer, lineterminator="\n"); writer.writerow(values);
            self.channels.print(self._channel_value(match.group(1)), buffer.getvalue().rstrip("\n"), end="\n"); return pc + 1;
        match = re.match(r'^PRINT\s+#([A-Ja-j]|\d+)\s*,?\s*(.*)$', text, re.I);
        if match:
            body = match.group(2); items = self._split_print(body); trailing = body.rstrip().endswith((";", ",")); rendered = "";
            for expr, sep in items:
                if expr: rendered += str(self.expr.eval(expr));
                if sep == ",": rendered += "\t";
            self.channels.print(self._channel_value(match.group(1)), rendered, end="" if trailing else "\n"); return pc + 1;
        match = re.match(r'^DB\.SELECT\s+(.+)$', text, re.I);
        if match: self._db().select(self.expr.eval(match.group(1)) if not re.fullmatch(r'[A-Ja-j]', match.group(1).strip()) else match.group(1).strip()); return pc + 1;
        match = re.match(r'^DB\.USE(?:\s+(.+?))?(?:\s+ALIAS\s+([A-Za-z_][A-Za-z0-9_]*))?$', text, re.I);
        if match:
            table = self.expr.eval(match.group(1)) if match.group(1) else None; self._db().use(table, alias=match.group(2)); return pc + 1;
        match = re.match(r'^DB\.GO\s+(.+)$', text, re.I);
        if match: self._db().go(self.expr.eval(match.group(1)) if match.group(1).strip().upper() not in ("TOP", "BOTTOM") else match.group(1).strip().upper()); return pc + 1;
        match = re.match(r'^DB\.SKIP(?:\s+(.+))?$', text, re.I);
        if match: self._db().skip(int(self.expr.eval(match.group(1)))) if match.group(1) else self._db().skip(1); return pc + 1;
        if upper == "DB.CLOSE": self._db().close(); self.database = None; return pc + 1;
        match = re.match(r"^LOCATE\s+(.+?)\s*,\s*(.+)$", text, re.I);
        if match:
            row = int(self.expr.eval(match.group(1))); col = int(self.expr.eval(match.group(2)));
            self._emit("\033[{};{}H".format(row, col), end=""); return pc + 1;
        if upper.startswith("PRINT") or text.startswith("?"):
            body = text[1:].strip() if text.startswith("?") else text[5:].strip();
            if body.upper().startswith("USING "):
                return self._print_using(body[6:].strip(), pc);
            items = self._split_print(body);
            trailing = body.rstrip().endswith((";", ","));
            rendered = "";
            for expr, sep in items:
                if expr: rendered += str(self.expr.eval(expr));
                if sep == ",": rendered += "\t";
                elif sep == ";": rendered += "";
            self._emit(rendered, end="" if trailing else "\n");
            return pc + 1;
        match = re.match(r"^(LINE\s+INPUT|INPUT)\s*(?:\"([^\"]*)\"\s*[;,])?\s*([A-Za-z_][A-Za-z0-9_]*[$%&!#]?)$", text, re.I);
        if match:
            prompt = match.group(2) or ("? " if match.group(1).upper() == "INPUT" else "");
            raw = self.input_func(prompt);
            value = str(raw) if match.group(1).upper().startswith("LINE") else self._coerce_input(match.group(3), raw);
            self.expr.set(match.group(3), value); return pc + 1;
        match = re.match(r"^(?:LET\s+)?([A-Za-z_][A-Za-z0-9_]*[$%&!#]?)\s*=\s*(.+)$", text, re.I);
        if match:
            self.expr.set(match.group(1), self.expr.eval(match.group(2))); return pc + 1;
        match = re.match(r"^IF\s+(.+?)\s+THEN(?:\s+(.*))?$", text, re.I);
        if match:
            condition = bool(self.expr.eval(match.group(1))); tail = (match.group(2) or "").strip();
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
        match = re.match(r"^GOTO\s+(\d+)$", text, re.I);
        if match: return self._jump_line(match.group(1), line_to_pc);
        match = re.match(r"^GOSUB\s+(\d+)$", text, re.I);
        if match:
            self.gosub_stack.append(pc + 1); return self._jump_line(match.group(1), line_to_pc);
        if upper == "RETURN":
            if not self.gosub_stack: raise BasicError("RETURN without GOSUB");
            return self.gosub_stack.pop();
        match = re.match(r"^FOR\s+([A-Za-z_][A-Za-z0-9_]*[$%&!#]?)\s*=\s*(.+?)\s+TO\s+(.+?)(?:\s+STEP\s+(.+))?$", text, re.I);
        if match:
            name = match.group(1); start = self.expr.eval(match.group(2)); end = self.expr.eval(match.group(3)); step = self.expr.eval(match.group(4)) if match.group(4) else 1;
            self.expr.set(name, start); next_pc = self._find_next(execution, pc);
            self.for_stack.append({"name": name, "end": end, "step": step, "for_pc": pc, "next_pc": next_pc});
            return pc + 1;
        match = re.match(r"^NEXT(?:\s+([A-Za-z_][A-Za-z0-9_]*[$%&!#]?))?$", text, re.I);
        if match:
            if not self.for_stack: raise BasicError("NEXT without FOR");
            frame = self.for_stack[-1]; value = self.expr.get(frame["name"]) + frame["step"]; self.expr.set(frame["name"], value);
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
                condition = bool(self.expr.eval(match.group(2))); condition = (not condition) if match.group(1).upper() == "UNTIL" else condition;
                if not condition:
                    pair = do_blocks.get(pc);
                    return (pair[1] + 1) if isinstance(pair, tuple) else pc + 1;
            return pc + 1;
        match = re.match(r"^LOOP(?:\s+(WHILE|UNTIL)\s+(.+))?$", text, re.I);
        if match:
            start = do_blocks.get(pc, pc);
            if match.group(1):
                condition = bool(self.expr.eval(match.group(2))); condition = (not condition) if match.group(1).upper() == "UNTIL" else condition;
                return start if condition else pc + 1;
            return start;
        match = re.match(r"^READ\s+(.+)$", text, re.I);
        if match:
            for name in [item.strip() for item in match.group(1).split(",")]:
                if self.data_index >= len(self.data): raise BasicError("Out of DATA");
                self.expr.set(name, self.data[self.data_index]); self.data_index += 1;
            return pc + 1;
        if upper.startswith("RESTORE"):
            self.data_index = 0; return pc + 1;
        match = re.match(r"^SWAP\s+([^,]+),\s*(.+)$", text, re.I);
        if match:
            a = match.group(1).strip(); b = match.group(2).strip(); va = self.expr.get(a); vb = self.expr.get(b); self.expr.set(a, vb); self.expr.set(b, va); return pc + 1;
        match = re.match(r"^DIM\s+([A-Za-z_][A-Za-z0-9_]*[$%&!#]?)\s*\((.+)\)$", text, re.I);
        if match:
            size = int(self.expr.eval(match.group(2))); self.arrays[match.group(1).casefold()] = [0] * (size + 1); return pc + 1;
        raise BasicError("Unsupported statement at line {}: {}".format(line_number, text));

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
                mask = token.group(0); decimals = len(mask.split(".", 1)[1]) if "." in mask else 0; width = len(mask);
                replacement = ("{:>%d.%df}" % (width, decimals)).format(float(value)) if decimals else ("{:>%dd}" % width).format(int(value));
                rendered = rendered[:token.start()] + replacement + rendered[token.end():];
            else: rendered += str(value);
        self._emit(rendered); return pc + 1;

    def execute_immediate(self, source):
        text = str(source).strip();
        numbered = re.match(r"^(\d+)\s*(.*)$", text);
        if numbered:
            self.program.set_numbered_line(int(numbered.group(1)), numbered.group(2)); return None;
        upper = text.upper();
        if upper == "RUN": return self.run();
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
        # Execute one immediate BASIC statement by using a temporary free-form program while preserving variables.
        old_program = self.program; temp = BasicProgram(); temp.free_lines = [text]; self.program = temp;
        execution, line_to_pc = self._build_execution();
        try:
            self._execute_statement(text, 0, 1, execution, line_to_pc, {}, {}, {});
        finally:
            self.program = old_program;
        return None;
