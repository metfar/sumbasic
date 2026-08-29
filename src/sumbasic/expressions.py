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
import ast;
import math;
import random;
import re;


class BasicExpressionError(RuntimeError):
    pass;


def _split_args(text):
    parts = [];
    current = [];
    quote = None;
    depth = 0;
    for char in str(text):
        if quote:
            current.append(char);
            if char == quote:
                quote = None;
            continue;
        if char in "\"'":
            quote = char;
            current.append(char);
        elif char == "(":
            depth += 1;
            current.append(char);
        elif char == ")":
            depth -= 1;
            current.append(char);
        elif char == "," and depth == 0:
            parts.append("".join(current).strip());
            current = [];
        else:
            current.append(char);
    parts.append("".join(current).strip());
    return parts;


class ExpressionEvaluator:
    def __init__(self, variables=None, extra_functions=None):
        self.variables = variables if variables is not None else {};
        self.extra_functions = extra_functions if extra_functions is not None else {};
        self.random = random.Random();

    @staticmethod
    def key(name):
        return str(name).casefold();

    def get(self, name):
        key = self.key(name);
        if key in self.variables:
            return self.variables[key];
        if str(name).endswith("$"):
            return "";
        return 0;

    def set(self, name, value):
        suffix = str(name)[-1:] if str(name) else "";
        if suffix == "$":
            value = str(value);
        elif suffix in ("%", "&"):
            value = int(float(value));
        elif suffix in ("!", "#"):
            value = float(value);
        self.variables[self.key(name)] = value;
        return value;

    def _func(self, name, args):
        upper = name.upper();
        table = {
            "ABS": lambda x: abs(x), "ATN": lambda x: math.atan(x), "COS": lambda x: math.cos(x),
            "EXP": lambda x: math.exp(x), "FIX": lambda x: math.trunc(x), "INT": lambda x: math.floor(x),
            "LOG": lambda x: math.log(x), "SGN": lambda x: -1 if x < 0 else (1 if x > 0 else 0),
            "SIN": lambda x: math.sin(x), "SQR": lambda x: math.sqrt(x), "TAN": lambda x: math.tan(x),
            "LEN": lambda x: len(str(x)), "ASC": lambda x: ord(str(x)[0]) if str(x) else 0,
            "CHR$": lambda x: chr(int(x) & 0xff), "LCASE$": lambda x: str(x).lower(), "UCASE$": lambda x: str(x).upper(),
            "LEFT$": lambda x, n: str(x)[:int(n)], "RIGHT$": lambda x, n: str(x)[-int(n):] if int(n) else "",
            "LTRIM$": lambda x: str(x).lstrip(), "RTRIM$": lambda x: str(x).rstrip(), "SPACE$": lambda n: " " * int(n),
            "STR$": lambda x: str(x), "VAL": lambda x: float(str(x).strip()) if any(c in str(x) for c in ".eE") else int(str(x).strip() or "0"),
            "HEX$": lambda x: format(int(x), "X"), "OCT$": lambda x: format(int(x), "o"),
        };
        if upper == "RND":
            return self.random.random();
        if upper == "MID$":
            text = str(args[0]); start = max(1, int(args[1])) - 1; length = int(args[2]) if len(args) > 2 else None;
            return text[start:] if length is None else text[start:start + length];
        if upper == "INSTR":
            if len(args) == 2:
                start, haystack, needle = 1, str(args[0]), str(args[1]);
            else:
                start, haystack, needle = int(args[0]), str(args[1]), str(args[2]);
            pos = haystack.find(needle, max(0, start - 1));
            return pos + 1 if pos >= 0 else 0;
        if upper == "STRING$":
            n = int(args[0]); value = args[1]; char = chr(int(value) & 0xff) if isinstance(value, (int, float)) else str(value)[:1];
            return char * n;
        if upper in table:
            return table[upper](*args);
        if upper in self.extra_functions:
            return self.extra_functions[upper](*args);
        raise BasicExpressionError("Unknown function: {}".format(name));

    def eval(self, source):
        text = str(source).strip();
        encoded = {};
        def transform(segment):
            segment = re.sub(r"<>", "!=", segment);
            segment = re.sub(r"(?<![<>=])=(?!=)", "==", segment);
            segment = re.sub(r"\bAND\b", " and ", segment, flags=re.I);
            segment = re.sub(r"\bOR\b", " or ", segment, flags=re.I);
            segment = re.sub(r"\bNOT\b", " not ", segment, flags=re.I);
            segment = re.sub(r"\bMOD\b", " % ", segment, flags=re.I);
            segment = re.sub(r"\bDB\.(RECNO|RECCOUNT)\s*\(", lambda m: "DB" + m.group(1).upper() + "(", segment, flags=re.I);
            segment = segment.replace("^", "**");
            segment = re.sub(r"&H([0-9A-Fa-f]+)", lambda m: str(int(m.group(1), 16)), segment);
            segment = re.sub(r"&O([0-7]+)", lambda m: str(int(m.group(1), 8)), segment);
            def encode_suffix(match):
                name = match.group(0);
                token = "__basic_" + name.encode("utf-8").hex();
                encoded[token] = name;
                return token;
            return re.sub(r"\b[A-Za-z_][A-Za-z0-9_]*[$%&!#]", encode_suffix, segment);
        pieces = [];
        current = [];
        quote = False;
        for char in text:
            if char == '"':
                if quote:
                    current.append(char); pieces.append("".join(current)); current = []; quote = False;
                else:
                    if current: pieces.append(transform("".join(current))); current = [];
                    current.append(char); quote = True;
            else:
                current.append(char);
        if current:
            pieces.append("".join(current) if quote else transform("".join(current)));
        text = "".join(pieces);
        self._encoded_names = encoded;
        try:
            tree = ast.parse(text, mode="eval");
        except SyntaxError as exc:
            raise BasicExpressionError("Invalid expression: {}".format(source)) from exc;
        return self._node(tree.body);

    def _node(self, node):
        if isinstance(node, ast.Constant): return node.value;
        if isinstance(node, ast.Name): return self.get(getattr(self, "_encoded_names", {}).get(node.id, node.id));
        if isinstance(node, ast.BinOp):
            a = self._node(node.left); b = self._node(node.right);
            ops = {ast.Add: lambda: a + b, ast.Sub: lambda: a - b, ast.Mult: lambda: a * b, ast.Div: lambda: a / b, ast.FloorDiv: lambda: a // b, ast.Mod: lambda: a % b, ast.Pow: lambda: a ** b};
            for kind, fn in ops.items():
                if isinstance(node.op, kind): return fn();
        if isinstance(node, ast.UnaryOp):
            value = self._node(node.operand);
            if isinstance(node.op, ast.USub): return -value;
            if isinstance(node.op, ast.UAdd): return +value;
            if isinstance(node.op, ast.Not): return not value;
        if isinstance(node, ast.BoolOp):
            values = [bool(self._node(item)) for item in node.values];
            return all(values) if isinstance(node.op, ast.And) else any(values);
        if isinstance(node, ast.Compare):
            left = self._node(node.left);
            for op, comparator in zip(node.ops, node.comparators):
                right = self._node(comparator);
                ok = ((isinstance(op, ast.Eq) and left == right) or (isinstance(op, ast.NotEq) and left != right) or (isinstance(op, ast.Lt) and left < right) or (isinstance(op, ast.LtE) and left <= right) or (isinstance(op, ast.Gt) and left > right) or (isinstance(op, ast.GtE) and left >= right));
                if not ok: return False;
                left = right;
            return True;
        if isinstance(node, ast.Call) and isinstance(node.func, ast.Name):
            name = getattr(self, "_encoded_names", {}).get(node.func.id, node.func.id);
            return self._func(name, [self._node(arg) for arg in node.args]);
        raise BasicExpressionError("Unsupported expression node: {}".format(type(node).__name__));
