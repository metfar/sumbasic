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


class BasicProgram:
    def __init__(self):
        self.lines = {};
        self.free_lines = [];
        self.mixed_lines = [];
        self.path = None;

    def clear(self):
        self.lines.clear();
        self.free_lines = [];
        self.mixed_lines = [];
        self.path = None;

    def _comment_only(self, source):
        text = str(source).lstrip();
        if not text:
            return True;
        if text.startswith("#") or text.startswith("'"):
            return True;
        return bool(re.match(r"^REM(?:\s|$)", text, re.I));

    def set_numbered_line(self, number, source):
        number = int(number);
        text = str(source).rstrip();
        if self.mixed_lines:
            found = False;
            rebuilt = [];
            for label, line in self.mixed_lines:
                if label == number:
                    if text and not found:
                        rebuilt.append((number, text));
                    found = True;
                else:
                    rebuilt.append((label, line));
            if text and not found:
                rebuilt.append((number, text));
            self.mixed_lines = rebuilt;
            return None;
        if text:
            self.lines[number] = text;
        else:
            self.lines.pop(number, None);
        return None;

    def delete_range(self, start, end=None):
        start = int(start);
        end = start if end is None else int(end);
        if self.mixed_lines:
            self.mixed_lines = [(label, text) for label, text in self.mixed_lines if label is None or not (start <= label <= end)];
            return None;
        for number in list(self.lines):
            if start <= number <= end:
                del self.lines[number];
        return None;

    def _rewrite_jumps(self, text, mapping):
        jump_re = re.compile(r"\b(GOTO|GOSUB|THEN|ELSE|RESTORE)\s+(\d+)\b", re.I);
        def replace(match):
            target = int(match.group(2));
            return "{} {}".format(match.group(1), mapping.get(target, target));
        return jump_re.sub(replace, text);

    def renumber(self, start=10, step=10):
        start = int(start);
        step = int(step);
        if self.mixed_lines:
            old = [];
            for label, _ in self.mixed_lines:
                if label is not None and label not in old:
                    old.append(label);
            mapping = {number: start + index * step for index, number in enumerate(old)};
            rebuilt = [];
            for label, text in self.mixed_lines:
                new_label = mapping.get(label, label) if label is not None else None;
                rebuilt.append((new_label, self._rewrite_jumps(text, mapping)));
            self.mixed_lines = rebuilt;
            return mapping;
        old = sorted(self.lines);
        mapping = {number: start + index * step for index, number in enumerate(old)};
        rewritten = {};
        for old_number in old:
            rewritten[mapping[old_number]] = self._rewrite_jumps(self.lines[old_number], mapping);
        self.lines = rewritten;
        return mapping;

    def _logical_lines(self, source):
        """Join modern BASIC continuation lines ending in backslash or ``_``.

        Continuation is resolved before numbered/free-form detection so a
        multiline statement remains one executable statement.  The marker is
        recognized only as the final non-space character of a physical line.
        """;
        logical = [];
        pending = "";
        for physical in str(source).splitlines():
            text = str(physical).rstrip();
            continued = bool(text) and text[-1:] in ("\\", "_");
            if continued:
                text = text[:-1].rstrip();
            if pending:
                pending = pending + " " + text.lstrip();
            else:
                pending = text;
            if not continued:
                logical.append(pending);
                pending = "";
        if pending:
            logical.append(pending);
        return logical;

    def load_text(self, source):
        self.clear();
        records = [];
        has_numbered = False;
        has_free_code = False;
        for physical in self._logical_lines(source):
            match = re.match(r"^\s*(\d+)\s*(.*)$", physical);
            if match:
                has_numbered = True;
                records.append((int(match.group(1)), match.group(2).rstrip()));
            else:
                text = physical.rstrip();
                records.append((None, text));
                if text.strip() and not self._comment_only(text):
                    has_free_code = True;
        if has_numbered and has_free_code:
            self.mixed_lines = records;
        elif has_numbered:
            for label, text in records:
                if label is not None:
                    self.set_numbered_line(label, text);
        else:
            self.free_lines = [text for _, text in records];
        return self;

    def execution_records(self):
        """Return (display_line, source, explicit_line_label) in execution order.

        Pure classic numbered programs execute in numeric line-number order.
        Free-form programs execute in physical order.  Hybrid programs preserve
        physical order and treat any explicit numeric line as a jump label,
        allowing modern source to use classic GOTO/GOSUB targets without moving
        the surrounding unnumbered statements.
        """
        if self.mixed_lines:
            out = [];
            for physical, (label, text) in enumerate(self.mixed_lines, start=1):
                display = label if label is not None else physical;
                out.append((display, text, label));
            return out;
        if self.lines:
            return [(number, self.lines[number], number) for number in sorted(self.lines)];
        return [(index + 1, line, None) for index, line in enumerate(self.free_lines)];

    def source_lines(self):
        return [(display, source) for display, source, _ in self.execution_records()];

    def source_text(self, numbered=None):
        if self.mixed_lines:
            lines = [];
            for label, text in self.mixed_lines:
                lines.append("{} {}".format(label, text) if label is not None else text);
            return "\n".join(lines) + ("\n" if lines else "");
        if numbered is None:
            numbered = bool(self.lines);
        if self.lines and numbered:
            return "\n".join("{} {}".format(number, self.lines[number]) for number in sorted(self.lines)) + ("\n" if self.lines else "");
        return "\n".join(line for _, line in self.source_lines()) + ("\n" if self.source_lines() else "");

    def load_file(self, path):
        path = Path(path);
        self.load_text(path.read_text(encoding="utf-8", errors="replace"));
        self.path = path;
        return self;

    def save_file(self, path=None):
        target = Path(path) if path is not None else self.path;
        if target is None:
            raise ValueError("SAVE requires a filename");
        target.write_text(self.source_text(), encoding="utf-8");
        self.path = target;
        return target;
