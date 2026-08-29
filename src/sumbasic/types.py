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
from decimal import Decimal;
from itertools import product;


SUFFIX_TYPES = {
    "$": "STRING",
    "!": "INTEGER",
    "&": "LONG",
    "%": "DOUBLE",
};

SCALAR_TYPES = {
    "ANY", "BOOLEAN", "INTEGER", "LONG", "SINGLE", "DOUBLE", "DECIMAL", "STRING", "BYTES",
};

COLLECTION_TYPES = {"ARRAY", "LIST", "DICT", "SET", "TUPLE"};


class BasicTypeError(RuntimeError):
    pass;


class BasicArrayError(RuntimeError):
    pass;


def suffix_type(name):
    text = str(name);
    return SUFFIX_TYPES.get(text[-1:]);


def normalize_type(type_name):
    if type_name is None:
        return None;
    text = " ".join(str(type_name).strip().upper().split());
    if not text:
        return None;
    base = text.split("[", 1)[0].strip();
    aliases = {
        "BOOL": "BOOLEAN",
        "INT": "INTEGER",
        "FLOAT": "DOUBLE",
        "STR": "STRING",
        "BYTE": "BYTES",
    };
    base = aliases.get(base, base);
    if "[" in text:
        return base + "[" + text.split("[", 1)[1];
    return base;


def base_type(type_name):
    normalized = normalize_type(type_name) or "ANY";
    return normalized.split("[", 1)[0].strip();


def default_value(type_name):
    kind = base_type(type_name);
    if kind == "STRING": return "";
    if kind == "BOOLEAN": return False;
    if kind in ("INTEGER", "LONG"): return 0;
    if kind in ("SINGLE", "DOUBLE"): return 0.0;
    if kind == "DECIMAL": return Decimal("0");
    if kind == "BYTES": return b"";
    if kind == "LIST": return [];
    if kind == "DICT": return {};
    if kind == "SET": return set();
    if kind == "TUPLE": return ();
    return 0;


def coerce_value(value, type_name):
    kind = base_type(type_name);
    if kind == "ANY": return value;
    if kind == "STRING": return str(value);
    if kind == "BOOLEAN": return bool(value);
    if kind in ("INTEGER", "LONG"): return int(float(value));
    if kind in ("SINGLE", "DOUBLE"): return float(value);
    if kind == "DECIMAL": return Decimal(str(value));
    if kind == "BYTES":
        if isinstance(value, bytes): return value;
        if isinstance(value, bytearray): return bytes(value);
        return str(value).encode("utf-8");
    if kind == "LIST":
        if isinstance(value, list): return value;
        if isinstance(value, (tuple, set)): return list(value);
        raise BasicTypeError("LIST value required");
    if kind == "DICT":
        if isinstance(value, dict): return value;
        raise BasicTypeError("DICT value required");
    if kind == "SET":
        if isinstance(value, set): return value;
        if isinstance(value, (list, tuple)): return set(value);
        raise BasicTypeError("SET value required");
    if kind == "TUPLE":
        if isinstance(value, tuple): return value;
        if isinstance(value, (list, set)): return tuple(value);
        raise BasicTypeError("TUPLE value required");
    raise BasicTypeError("Unknown BASIC type: {}".format(type_name));


class BasicArray:
    def __init__(self, name, bounds, type_name="ANY", shared=False):
        self.name = str(name);
        self.bounds = [(int(low), int(high)) for low, high in bounds];
        if not self.bounds: raise BasicArrayError("Array requires at least one dimension");
        for low, high in self.bounds:
            if high < low: raise BasicArrayError("Invalid array bounds {} TO {}".format(low, high));
        self.type_name = normalize_type(type_name) or suffix_type(name) or "ANY";
        self.shared = bool(shared);
        size = 1;
        for low, high in self.bounds: size *= (high - low + 1);
        self.data = [default_value(self.type_name) for _ in range(size)];

    @property
    def dimensions(self):
        return len(self.bounds);

    def lbound(self, dimension=1):
        index = int(dimension) - 1;
        if not 0 <= index < len(self.bounds): raise BasicArrayError("Invalid array dimension: {}".format(dimension));
        return self.bounds[index][0];

    def ubound(self, dimension=1):
        index = int(dimension) - 1;
        if not 0 <= index < len(self.bounds): raise BasicArrayError("Invalid array dimension: {}".format(dimension));
        return self.bounds[index][1];

    def _offset(self, indices):
        values = [int(value) for value in indices];
        if len(values) != len(self.bounds):
            raise BasicArrayError("{} expects {} indices, got {}".format(self.name, len(self.bounds), len(values)));
        offset = 0;
        stride = 1;
        for value, (low, high) in reversed(list(zip(values, self.bounds))):
            if value < low or value > high:
                raise BasicArrayError("Subscript out of range for {}: {} not in {} TO {}".format(self.name, value, low, high));
            offset += (value - low) * stride;
            stride *= (high - low + 1);
        return offset;

    def get(self, indices):
        return self.data[self._offset(indices)];

    def set(self, indices, value):
        self.data[self._offset(indices)] = coerce_value(value, self.type_name);
        return value;

    def resize(self, bounds, preserve=False):
        replacement = BasicArray(self.name, bounds, self.type_name, shared=self.shared);
        if preserve:
            overlap = [];
            for old, new in zip(self.bounds, replacement.bounds):
                overlap.append(range(max(old[0], new[0]), min(old[1], new[1]) + 1));
            if len(overlap) == len(self.bounds) == len(replacement.bounds):
                for indices in product(*overlap): replacement.set(indices, self.get(indices));
        self.bounds = replacement.bounds;
        self.data = replacement.data;
        return self;
