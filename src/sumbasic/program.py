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
        self.path = None;

    def clear(self):
        self.lines.clear();
        self.free_lines = [];
        self.path = None;

    def set_numbered_line(self, number, source):
        number = int(number);
        text = str(source).rstrip();
        if text:
            self.lines[number] = text;
        else:
            self.lines.pop(number, None);

    def delete_range(self, start, end=None):
        start = int(start);
        end = start if end is None else int(end);
        for number in list(self.lines):
            if start <= number <= end:
                del self.lines[number];

    def renumber(self, start=10, step=10):
        start = int(start);
        step = int(step);
        old = sorted(self.lines);
        mapping = {number: start + index * step for index, number in enumerate(old)};
        rewritten = {};
        jump_re = re.compile(r"\b(GOTO|GOSUB|THEN|ELSE)\s+(\d+)\b", re.I);
        for old_number in old:
            text = self.lines[old_number];
            def replace(match):
                target = int(match.group(2));
                return "{} {}".format(match.group(1), mapping.get(target, target));
            rewritten[mapping[old_number]] = jump_re.sub(replace, text);
        self.lines = rewritten;
        return mapping;

    def load_text(self, source):
        self.clear();
        free = [];
        numbered = False;
        for physical in str(source).splitlines():
            match = re.match(r"^\s*(\d+)\s*(.*)$", physical);
            if match:
                numbered = True;
                self.set_numbered_line(int(match.group(1)), match.group(2));
            elif physical.strip() or free:
                free.append(physical.rstrip());
        if numbered and any(line.strip() for line in free):
            next_number = (max(self.lines) + 10) if self.lines else 10;
            for line in free:
                if line.strip():
                    self.lines[next_number] = line;
                    next_number += 10;
        elif not numbered:
            self.free_lines = free;
        return self;

    def source_lines(self):
        if self.lines:
            return [(number, self.lines[number]) for number in sorted(self.lines)];
        return [(index + 1, line) for index, line in enumerate(self.free_lines)];

    def source_text(self, numbered=None):
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
