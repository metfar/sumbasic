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
import cmath;
import math;
import random;
import re;
from datetime import datetime;
from decimal import Decimal;

from .types import coerce_value, suffix_type;
from .vocabulary import ZX_SPECTRUM_PI;


class BasicExpressionError(RuntimeError):
    pass;


class ExpressionEvaluator:
    def __init__(self, variables=None, variable_types=None, arrays=None, extra_functions=None, now_func=None):
        self.variables = variables if variables is not None else {};
        self.variable_types = variable_types if variable_types is not None else {};
        self.arrays = arrays if arrays is not None else {};
        self.extra_functions = extra_functions if extra_functions is not None else {};
        self.now_func = now_func if now_func is not None else datetime.now;
        self.random = random.Random();
        self._encoded_names = {};

    @staticmethod
    def key(name):
        return str(name).casefold();

    @staticmethod
    def _basic_round(value, digits=0):
        digits = int(digits);
        scale = 10.0 ** digits;
        scaled = float(value) * scale;
        rounded = math.floor(scaled + 0.5) if scaled >= 0 else math.ceil(scaled - 0.5);
        result = rounded / scale;
        return int(result) if digits == 0 else result;

    @staticmethod
    def _root(value, degree=2):
        degree_value = float(degree);
        if degree_value == 0: raise BasicExpressionError("ROOT degree cannot be zero");
        if isinstance(value, complex): return value ** (1.0 / degree_value);
        value = float(value);
        if value < 0:
            degree_int = int(degree_value);
            if degree_value != degree_int or degree_int % 2 == 0: raise BasicExpressionError("ROOT domain error");
            return -((-value) ** (1.0 / degree_int));
        return value ** (1.0 / degree_value);

    @staticmethod
    def _cbrt(value):
        if isinstance(value, complex): return value ** (1.0 / 3.0);
        value = float(value);
        return math.copysign(abs(value) ** (1.0 / 3.0), value);

    @staticmethod
    def _frac(value):
        value = float(value);
        return value - math.trunc(value);

    @staticmethod
    def _clamp(value, low, high):
        if low > high: raise BasicExpressionError("CLAMP lower bound is greater than upper bound");
        return max(low, min(high, value));

    @staticmethod
    def _band(*values):
        if not values: return 0;
        result = int(values[0]);
        for value in values[1:]: result &= int(value);
        return result;

    @staticmethod
    def _bor(*values):
        if not values: return 0;
        result = int(values[0]);
        for value in values[1:]: result |= int(value);
        return result;

    @staticmethod
    def _bxor(*values):
        if not values: return 0;
        result = int(values[0]);
        for value in values[1:]: result ^= int(value);
        return result;

    @staticmethod
    def _numeric_pair(first, second):
        if isinstance(first, complex) or isinstance(second, complex):
            return complex(first), complex(second);
        if isinstance(first, Decimal) or isinstance(second, Decimal):
            if not isinstance(first, Decimal): first = Decimal(str(first));
            if not isinstance(second, Decimal): second = Decimal(str(second));
        return first, second;

    @staticmethod
    def _real_or_complex(value, real_function, complex_function):
        return complex_function(value) if isinstance(value, complex) else real_function(value);

    @staticmethod
    def _log_base(value, base):
        if isinstance(value, complex) or isinstance(base, complex):
            return cmath.log(value) / cmath.log(base);
        return math.log(value, base);

    def _time_string(self):
        return self.now_func().strftime("%H:%M:%S");

    def _timer_value(self):
        now = self.now_func();
        return (now.hour * 3600) + (now.minute * 60) + now.second + (now.microsecond / 1000000.0);

    @staticmethod
    def _complex_sign(value):
        if isinstance(value, complex):
            magnitude = abs(value);
            return 0 if magnitude == 0 else value / magnitude;
        return -1 if value < 0 else (1 if value > 0 else 0);

    @staticmethod
    def _complex_predicate(value, real_predicate):
        if isinstance(value, complex): return real_predicate(value.real) or real_predicate(value.imag);
        return real_predicate(value);

    @staticmethod
    def _finite_predicate(value):
        if isinstance(value, complex): return math.isfinite(value.real) and math.isfinite(value.imag);
        return math.isfinite(value);

    @staticmethod
    def _val_first_number(value):
        """Extract the first BASIC-style number from arbitrary text.

        sumBASIC deliberately keeps the tolerant data-import semantics agreed
        for VAL(): English numeric format, comma thousands separators,
        scientific notation, and an optional accounting sign before *or* after
        the number.  The first exterior sign wins; exponent signs are part of
        the exponent and do not count as exterior signs.
        """;
        source = str(value);
        pattern = re.compile(
            r"(?P<lead>[+-])?\s*"
            r"(?P<num>(?:(?:\d{1,3}(?:,\d{3})+|\d+)(?:\.\d*)?|\.\d+)(?:[eE][+-]?\d+)?)"
            r"(?P<trail>[+-])?"
        );
        match = pattern.search(source);
        if not match: return 0;
        number_text = match.group("num").replace(",", "");
        number = float(number_text);
        lead = match.group("lead");
        trail = match.group("trail");
        sign = lead if lead is not None else trail;
        if sign == "-": number = -abs(number);
        elif sign == "+": number = abs(number);
        return int(number) if number.is_integer() else number;

    @staticmethod
    def _format_base(value, base, width=0, uppercase=False):
        number = int(value);
        sign = "-" if number < 0 else "";
        digits = format(abs(number), {2: "b", 8: "o", 16: "X" if uppercase else "x"}[int(base)]);
        digits = digits.rjust(max(0, int(width)), "0");
        return sign + digits;

    @staticmethod
    def _basic_boolean(value):
        return -1 if bool(value) else 0;

    @staticmethod
    def _basic_string(value):
        if isinstance(value, complex):
            real = value.real;
            imag = value.imag;
            real_text = str(int(real)) if float(real).is_integer() else str(real);
            imag_text = str(int(abs(imag))) if float(abs(imag)).is_integer() else str(abs(imag));
            if imag == 0: return real_text;
            if real == 0: return ("-" if imag < 0 else "") + imag_text + "i";
            return real_text + ("-" if imag < 0 else "+") + imag_text + "i";
        return str(value);

    def get(self, name):
        upper = str(name).upper();
        if upper == "PI": return ZX_SPECTRUM_PI;
        if upper in ("TRUE", "__BASIC_TRUE"): return -1;
        if upper in ("FALSE", "__BASIC_FALSE"): return 0;
        if upper in ("NULL", "NIL", "NONE", "__BASIC_NULL"): return None;
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
            "SGN": lambda x: self._complex_sign(x),
            "SIGN": lambda x: self._complex_sign(x),
            "SQR": lambda x: self._real_or_complex(x, math.sqrt, cmath.sqrt),
            "SQRT": lambda x: self._real_or_complex(x, math.sqrt, cmath.sqrt),
            "CBRT": lambda x: self._cbrt(x),
            "ROOT": lambda x, n=2: self._root(x, n),
            "POW": lambda x, y: x ** y,
            "SQUARE": lambda x: x * x,
            "CUBE": lambda x: x * x * x,
            "SIN": lambda x: self._real_or_complex(x, math.sin, cmath.sin),
            "COS": lambda x: self._real_or_complex(x, math.cos, cmath.cos),
            "TAN": lambda x: self._real_or_complex(x, math.tan, cmath.tan),
            "COT": lambda x: 1.0 / self._real_or_complex(x, math.tan, cmath.tan),
            "SEC": lambda x: 1.0 / self._real_or_complex(x, math.cos, cmath.cos),
            "CSC": lambda x: 1.0 / self._real_or_complex(x, math.sin, cmath.sin),
            "ASN": lambda x: self._real_or_complex(x, math.asin, cmath.asin),
            "ASIN": lambda x: self._real_or_complex(x, math.asin, cmath.asin),
            "ACS": lambda x: self._real_or_complex(x, math.acos, cmath.acos),
            "ACOS": lambda x: self._real_or_complex(x, math.acos, cmath.acos),
            "ATN": lambda x: self._real_or_complex(x, math.atan, cmath.atan),
            "ATAN": lambda x: self._real_or_complex(x, math.atan, cmath.atan),
            "ATN2": lambda y, x: math.atan2(y, x),
            "ATAN2": lambda y, x: math.atan2(y, x),
            "SINH": lambda x: self._real_or_complex(x, math.sinh, cmath.sinh),
            "COSH": lambda x: self._real_or_complex(x, math.cosh, cmath.cosh),
            "TANH": lambda x: self._real_or_complex(x, math.tanh, cmath.tanh),
            "ASNH": lambda x: self._real_or_complex(x, math.asinh, cmath.asinh),
            "ASINH": lambda x: self._real_or_complex(x, math.asinh, cmath.asinh),
            "ACSH": lambda x: self._real_or_complex(x, math.acosh, cmath.acosh),
            "ACOSH": lambda x: self._real_or_complex(x, math.acosh, cmath.acosh),
            "ATNH": lambda x: self._real_or_complex(x, math.atanh, cmath.atanh),
            "ATANH": lambda x: self._real_or_complex(x, math.atanh, cmath.atanh),
            "LN": lambda x: self._real_or_complex(x, math.log, cmath.log),
            "LOG": lambda x: self._real_or_complex(x, math.log10, cmath.log10),
            "LOGB": lambda x, base: self._log_base(x, base),
            "LOGBASE": lambda x, base: self._log_base(x, base),
            "LOG10": lambda x: self._real_or_complex(x, math.log10, cmath.log10),
            "LOG2": lambda x: self._log_base(x, 2),
            "EXP": lambda x: self._real_or_complex(x, math.exp, cmath.exp),
            "INT": lambda x: math.floor(x),
            "FIX": lambda x: math.trunc(x),
            "TRUNC": lambda x: math.trunc(x),
            "FLOOR": lambda x: math.floor(x),
            "CEIL": lambda x: math.ceil(x),
            "ROUND": lambda x, digits=0: self._basic_round(x, digits),
            "FRAC": lambda x: self._frac(x),
            "MIN": lambda *values: min(values),
            "MAX": lambda *values: max(values),
            "CLAMP": lambda x, low, high: self._clamp(x, low, high),
            "HYPOT": lambda *values: math.hypot(*values),
            "RAD": lambda x: math.radians(x),
            "RADIANS": lambda x: math.radians(x),
            "DEG": lambda x: math.degrees(x),
            "DEGREES": lambda x: math.degrees(x),
            "GCD": lambda *values: math.gcd(*(int(value) for value in values)),
            "LCM": lambda *values: math.lcm(*(int(value) for value in values)),
            "FACT": lambda x: math.factorial(int(x)),
            "FACTORIAL": lambda x: math.factorial(int(x)),
            "COMB": lambda n, k: math.comb(int(n), int(k)),
            "PERM": lambda n, k=None: math.perm(int(n), None if k is None else int(k)),
            "GAMMA": lambda x: math.gamma(x),
            "LGAMMA": lambda x: math.lgamma(x),
            "ERF": lambda x: math.erf(x),
            "ERFC": lambda x: math.erfc(x),
            "ISFINITE": lambda x: self._finite_predicate(x),
            "ISINF": lambda x: self._complex_predicate(x, math.isinf),
            "ISNAN": lambda x: self._complex_predicate(x, math.isnan),
            "BAND": lambda *values: self._band(*values),
            "BOR": lambda *values: self._bor(*values),
            "BXOR": lambda *values: self._bxor(*values),
            "BNOT": lambda x: ~int(x),
            "SHL": lambda x, n: int(x) << int(n),
            "SHR": lambda x, n: int(x) >> int(n),
            "IDIV": lambda x, y: x // y,
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
            "STR$": lambda x: self._basic_string(x),
            "VAL": lambda x: self._val_first_number(x),
            "EVAL": lambda x: self.eval(str(x)),
            "VAL$": lambda x: str(x),
            "BIN": lambda x: self._format_base(x, 2),
            "BIN$": lambda x, width=0: self._format_base(x, 2, width),
            "HEX$": lambda x, width=0: self._format_base(x, 16, width, uppercase=True),
            "OCT$": lambda x, width=0: self._format_base(x, 8, width),
            "DECIMAL": lambda x=0: Decimal(str(x)),
            "COMPLEX": lambda real=0, imag=0: complex(real, imag),
            "CMPLX": lambda real=0, imag=0: complex(real, imag),
            "REAL": lambda z: complex(z).real,
            "IMAG": lambda z: complex(z).imag,
            "CONJ": lambda z: complex(z).conjugate(),
            "CONJUGATE": lambda z: complex(z).conjugate(),
            "PHASE": lambda z: cmath.phase(complex(z)),
            "ARG": lambda z: cmath.phase(complex(z)),
            "MAG": lambda z: abs(z),
            "NORM": lambda z: abs(z) ** 2,
            "POLAR": lambda radius, angle: cmath.rect(radius, angle),
            "ISCOMPLEX": lambda z: isinstance(z, complex),
            "TIME$": lambda: self._time_string(),
            "TIMER": lambda: self._timer_value(),
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
        if upper in table:
            try: return table[upper](*args);
            except BasicExpressionError: raise;
            except (ArithmeticError, TypeError, ValueError, OverflowError) as exc: raise BasicExpressionError("{}: {}".format(upper, exc)) from exc;
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
        # Normalize language aliases before Python's parser can reinterpret
        # True/False/None using Python's own numeric semantics.
        segment = re.sub(r"\bTRUE\b", "__BASIC_TRUE", segment, flags=re.I);
        segment = re.sub(r"\bFALSE\b", "__BASIC_FALSE", segment, flags=re.I);
        segment = re.sub(r"\b(?:NULL|NIL|NONE)\b", "__BASIC_NULL", segment, flags=re.I);
        # Classic Spectrum BIN plus Sum's modern binary literal alias.
        segment = re.sub(r"\bBIN\s+([01]+)\b", lambda m: str(int(m.group(1), 2)), segment, flags=re.I);
        segment = re.sub(r"(?<![A-Za-z0-9_])%([01]+)\b", lambda m: str(int(m.group(1), 2)), segment);
        segment = re.sub(r"\bXOR\b", " __SUMBASIC_XOR__ ", segment, flags=re.I);
        segment = re.sub(r"<>", " != ", segment);
        segment = re.sub(r"(?<![<>=!])=(?!=)", "==", segment);
        segment = re.sub(r"\bAND\b", " and ", segment, flags=re.I);
        segment = re.sub(r"\bOR\b", " or ", segment, flags=re.I);
        segment = re.sub(r"\bNOT\b", " not ", segment, flags=re.I);
        segment = re.sub(r"\bMOD\b", " % ", segment, flags=re.I);
        segment = re.sub(r"\bDIV\b", " // ", segment, flags=re.I);
        segment = re.sub(r"\\", "//", segment);
        segment = re.sub(r"\bDB\.(RECNO|RECCOUNT)\s*\(", lambda m: "DB" + m.group(1).upper() + "(", segment, flags=re.I);
        segment = re.sub(r"(?<![A-Za-z0-9_])RND(?!\s*\()", "RND()", segment, flags=re.I);
        segment = re.sub(r"(?<![A-Za-z0-9_])INKEY\$(?!\s*\()", "INKEY$()", segment, flags=re.I);
        segment = re.sub(r"(?<![A-Za-z0-9_])TIME\$(?!\s*\()", "TIME$()", segment, flags=re.I);
        segment = re.sub(r"(?<![A-Za-z0-9_])TIMER(?![A-Za-z0-9_$%&!]|\s*\()", "TIMER()", segment, flags=re.I);
        for builtin in ("COLS", "ROWS", "GWIDTH", "GHEIGHT", "GCOLORS", "CURSOR", "MOUSEX", "MOUSEY", "MOUSEBUTTON"):
            # Preserve backward compatibility with variables such as Rows.
            # A user variable shadows the bare convenience spelling; the
            # explicit ROWS()/COLS() function form always remains available.
            if self.key(builtin) not in self.variables and self.key(builtin) not in self.arrays:
                segment = re.sub(r"(?<![A-Za-z0-9_])" + builtin + r"(?![A-Za-z0-9_$%&!]|\s*\()", builtin + "()", segment, flags=re.I);
        segment = segment.replace("^", "**");
        segment = segment.replace("__SUMBASIC_XOR__", "^");
        segment = re.sub(r"&H([0-9A-Fa-f]+)", lambda m: str(int(m.group(1), 16)), segment);
        segment = re.sub(r"&O([0-7]+)", lambda m: str(int(m.group(1), 8)), segment);
        segment = re.sub(r"&B([01]+)", lambda m: str(int(m.group(1), 2)), segment);
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
        text = "".join(pieces).strip();
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
        if isinstance(node, ast.Constant):
            if isinstance(node.value, bool): return self._basic_boolean(node.value);
            return node.value;
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
            first, second = self._numeric_pair(a, b);
            ops = {
                ast.Add: lambda: first + second,
                ast.Sub: lambda: first - second,
                ast.Mult: lambda: first * second,
                ast.Div: lambda: first / second,
                ast.FloorDiv: lambda: first // second,
                ast.Mod: lambda: first % second,
                ast.Pow: lambda: first ** second,
                ast.LShift: lambda: int(a) << int(b),
                ast.RShift: lambda: int(a) >> int(b),
                ast.BitXor: lambda: self._basic_boolean(bool(a) ^ bool(b)) if isinstance(a, complex) or isinstance(b, complex) else (int(a) ^ int(b)),
                ast.BitAnd: lambda: int(a) & int(b),
                ast.BitOr: lambda: int(a) | int(b),
            };
            for kind, function in ops.items():
                if isinstance(node.op, kind): return function();
        if isinstance(node, ast.UnaryOp):
            value = self._node(node.operand);
            if isinstance(node.op, ast.USub): return -value;
            if isinstance(node.op, ast.UAdd): return +value;
            if isinstance(node.op, ast.Not):
                if isinstance(value, (int, bool)) and not isinstance(value, complex): return ~int(value);
                return self._basic_boolean(not bool(value));
            if isinstance(node.op, ast.Invert): return ~int(value);
        if isinstance(node, ast.BoolOp):
            values = [self._node(item) for item in node.values];
            integral = all(isinstance(value, (int, bool)) and not isinstance(value, complex) for value in values);
            if integral:
                result = int(values[0]) if values else 0;
                for value in values[1:]:
                    result = (result & int(value)) if isinstance(node.op, ast.And) else (result | int(value));
                return result;
            truth = [bool(value) for value in values];
            return self._basic_boolean(all(truth) if isinstance(node.op, ast.And) else any(truth));
        if isinstance(node, ast.Compare):
            left = self._node(node.left);
            for op, comparator in zip(node.ops, node.comparators):
                right = self._node(comparator);
                ok = ((isinstance(op, ast.Eq) and left == right) or (isinstance(op, ast.NotEq) and left != right) or (isinstance(op, ast.Lt) and left < right) or (isinstance(op, ast.LtE) and left <= right) or (isinstance(op, ast.Gt) and left > right) or (isinstance(op, ast.GtE) and left >= right));
                if not ok: return 0;
                left = right;
            return -1;
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
