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
import ast;
import math;
import random;
import re;

from .types import coerce_value, suffix_type;
from .vocabulary import ZX_SPECTRUM_PI;


class BasicExpressionError(RuntimeError):
    pass;


class ExpressionEvaluator:
    def __init__(self, variables=None, variable_types=None, arrays=None, extra_functions=None):
        self.variables = variables if variables is not None else {};
        self.variable_types = variable_types if variable_types is not None else {};
        self.arrays = arrays if arrays is not None else {};
        self.extra_functions = extra_functions if extra_functions is not None else {};
        self.random = random.Random();
        self._encoded_names = {};

    @staticmethod
    def key(name):
        return str(name).casefold();

    def get(self, name):
        upper = str(name).upper();
        if upper == "PI": return ZX_SPECTRUM_PI;
        if upper == "TRUE": return True;
        if upper == "FALSE": return False;
        key = self.key(name);
        if key in self.variables: return self.variables[key];
        if str(name).endswith("$"): return "";
        return 0;

    def set(self, name, value):
        if str(name).upper() == "PI": raise BasicExpressionError("Cannot assign to built-in constant PI");
        key = self.key(name);
        declared = self.variable_types.get(key);
        inferred = suffix_type(name);
        type_name = declared or inferred;
        if type_name is not None: value = coerce_value(value, type_name);
        self.variables[key] = value;
        return value;

    def _func(self, name, args):
        upper = name.upper();
        table = {
            "ABS": lambda x: abs(x),
            "ASN": lambda x: math.asin(x),
            "ACS": lambda x: math.acos(x),
            "ATN": lambda x: math.atan(x),
            "COS": lambda x: math.cos(x),
            "EXP": lambda x: math.exp(x),
            "FIX": lambda x: math.trunc(x),
            "INT": lambda x: math.floor(x),
            "LN": lambda x: math.log(x),
            "LOG": lambda x: math.log(x),
            "SGN": lambda x: -1 if x < 0 else (1 if x > 0 else 0),
            "SIN": lambda x: math.sin(x),
            "SQR": lambda x: math.sqrt(x),
            "TAN": lambda x: math.tan(x),
            "LEN": lambda x: len(x) if hasattr(x, "__len__") else len(str(x)),
            "ASC": lambda x: ord(str(x)[0]) if str(x) else 0,
            "CODE": lambda x: ord(str(x)[0]) if str(x) else 0,
            "CHR$": lambda x: chr(int(x) & 0xff),
            "LCASE$": lambda x: str(x).lower(),
            "UCASE$": lambda x: str(x).upper(),
            "LEFT$": lambda x, n: str(x)[:int(n)],
            "RIGHT$": lambda x, n: str(x)[-int(n):] if int(n) else "",
            "LTRIM$": lambda x: str(x).lstrip(),
            "RTRIM$": lambda x: str(x).rstrip(),
            "SPACE$": lambda n: " " * int(n),
            "STR$": lambda x: str(x),
            "VAL": lambda x: float(str(x).strip()) if any(c in str(x) for c in ".eE") else int(str(x).strip() or "0"),
            "VAL$": lambda x: str(x),
            "BIN": lambda x: format(int(x), "b"),
            "HEX$": lambda x: format(int(x), "X"),
            "OCT$": lambda x: format(int(x), "o"),
        };
        if upper == "RND": return self.random.random();
        if upper == "MID$":
            text = str(args[0]);
            start = max(1, int(args[1])) - 1;
            length = int(args[2]) if len(args) > 2 else None;
            return text[start:] if length is None else text[start:start + length];
        if upper == "INSTR":
            if len(args) == 2:
                start, haystack, needle = 1, str(args[0]), str(args[1]);
            else:
                start, haystack, needle = int(args[0]), str(args[1]), str(args[2]);
            pos = haystack.find(needle, max(0, start - 1));
            return pos + 1 if pos >= 0 else 0;
        if upper == "STRING$":
            n = int(args[0]);
            value = args[1];
            char = chr(int(value) & 0xff) if isinstance(value, (int, float)) else str(value)[:1];
            return char * n;
        if upper in table: return table[upper](*args);
        if upper in self.extra_functions: return self.extra_functions[upper](*args);
        raise BasicExpressionError("Unknown function: {}".format(name));

    def _encode_suffix_names(self, segment, encoded):
        def encode_suffix(match):
            name = match.group(0);
            token = "__basic_" + name.encode("utf-8").hex();
            encoded[token] = name;
            return token;
        return re.sub(r"\b[A-Za-z_][A-Za-z0-9_]*[$%&!]", encode_suffix, segment);

    def _transform(self, segment, encoded):
        segment = re.sub(r"<>", "!=", segment);
        segment = re.sub(r"(?<![<>=])=(?!=)", "==", segment);
        segment = re.sub(r"\bAND\b", " and ", segment, flags=re.I);
        segment = re.sub(r"\bOR\b", " or ", segment, flags=re.I);
        segment = re.sub(r"\bNOT\b", " not ", segment, flags=re.I);
        segment = re.sub(r"\bMOD\b", " % ", segment, flags=re.I);
        segment = re.sub(r"\bDB\.(RECNO|RECCOUNT)\s*\(", lambda m: "DB" + m.group(1).upper() + "(", segment, flags=re.I);
        segment = re.sub(r"(?<![A-Za-z0-9_])RND(?!\s*\()", "RND()", segment, flags=re.I);
        segment = re.sub(r"(?<![A-Za-z0-9_])INKEY\$(?!\s*\()", "INKEY$()", segment, flags=re.I);
        segment = segment.replace("^", "**");
        segment = re.sub(r"&H([0-9A-Fa-f]+)", lambda m: str(int(m.group(1), 16)), segment);
        segment = re.sub(r"&O([0-7]+)", lambda m: str(int(m.group(1), 8)), segment);
        return self._encode_suffix_names(segment, encoded);

    def eval(self, source):
        text = str(source).strip();
        encoded = {};
        pieces = [];
        current = [];
        quote = False;
        for char in text:
            if char == '"':
                if quote:
                    current.append(char);
                    pieces.append("".join(current));
                    current = [];
                    quote = False;
                else:
                    if current:
                        pieces.append(self._transform("".join(current), encoded));
                        current = [];
                    current.append(char);
                    quote = True;
            else:
                current.append(char);
        if current: pieces.append("".join(current) if quote else self._transform("".join(current), encoded));
        text = "".join(pieces);
        self._encoded_names = encoded;
        try:
            tree = ast.parse(text, mode="eval");
        except SyntaxError as exc:
            raise BasicExpressionError("Invalid expression: {}".format(source)) from exc;
        return self._node(tree.body);

    def _array_name(self, node):
        if not isinstance(node, ast.Name): return None;
        return getattr(self, "_encoded_names", {}).get(node.id, node.id);

    def _node(self, node):
        if isinstance(node, ast.Constant): return node.value;
        if isinstance(node, ast.Name): return self.get(getattr(self, "_encoded_names", {}).get(node.id, node.id));
        if isinstance(node, ast.List): return [self._node(item) for item in node.elts];
        if isinstance(node, ast.Tuple): return tuple(self._node(item) for item in node.elts);
        if isinstance(node, ast.Set): return set(self._node(item) for item in node.elts);
        if isinstance(node, ast.Dict): return {self._node(key): self._node(value) for key, value in zip(node.keys, node.values)};
        if isinstance(node, ast.Subscript):
            container = self._node(node.value);
            key = self._node(node.slice);
            return container[key];
        if isinstance(node, ast.BinOp):
            a = self._node(node.left);
            b = self._node(node.right);
            ops = {
                ast.Add: lambda: a + b,
                ast.Sub: lambda: a - b,
                ast.Mult: lambda: a * b,
                ast.Div: lambda: a / b,
                ast.FloorDiv: lambda: a // b,
                ast.Mod: lambda: a % b,
                ast.Pow: lambda: a ** b,
                ast.LShift: lambda: int(a) << int(b),
                ast.RShift: lambda: int(a) >> int(b),
            };
            for kind, function in ops.items():
                if isinstance(node.op, kind): return function();
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
            key = self.key(name);
            if key in self.arrays: return self.arrays[key].get([self._node(arg) for arg in node.args]);
            upper = str(name).upper();
            if upper in ("LBOUND", "UBOUND") and node.args:
                array_name = self._array_name(node.args[0]);
                if array_name is None or self.key(array_name) not in self.arrays: raise BasicExpressionError("{} requires an array".format(upper));
                dimension = self._node(node.args[1]) if len(node.args) > 1 else 1;
                array = self.arrays[self.key(array_name)];
                return array.lbound(dimension) if upper == "LBOUND" else array.ubound(dimension);
            return self._func(name, [self._node(arg) for arg in node.args]);
        if isinstance(node, ast.Call) and isinstance(node.func, ast.Attribute):
            owner = self._node(node.func.value);
            method = node.func.attr.upper();
            args = [self._node(arg) for arg in node.args];
            if isinstance(owner, list):
                if method == "APPEND": owner.append(args[0]); return None;
                if method == "INSERT": owner.insert(int(args[0]), args[1]); return None;
                if method == "REMOVE": owner.remove(args[0]); return None;
                if method == "CLEAR": owner.clear(); return None;
                if method == "POP": return owner.pop(int(args[0])) if args else owner.pop();
            if isinstance(owner, dict):
                if method == "HASKEY": return args[0] in owner;
                if method == "KEYS": return list(owner.keys());
                if method == "VALUES": return list(owner.values());
                if method == "ITEMS": return list(owner.items());
                if method == "GET": return owner.get(*args);
                if method == "CLEAR": owner.clear(); return None;
            if isinstance(owner, set):
                if method == "ADD": owner.add(args[0]); return None;
                if method == "REMOVE": owner.remove(args[0]); return None;
                if method == "DISCARD": owner.discard(args[0]); return None;
                if method == "CLEAR": owner.clear(); return None;
            raise BasicExpressionError("Unsupported collection method: {}".format(method));
        raise BasicExpressionError("Unsupported expression: {}".format(ast.dump(node)));
