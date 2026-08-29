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
import io;
import os;
import subprocess;
import sys;
from dataclasses import dataclass, field;


class ChannelError(RuntimeError):
    pass;


def channel_number(value):
    raw = str(value).strip();
    if raw.startswith("#"): raw = raw[1:].strip();
    if len(raw) == 1 and raw.isalpha():
        number = ord(raw.upper()) - ord("A") + 1;
    else:
        try: number = int(raw);
        except ValueError as exc: raise ChannelError("Invalid channel: {}".format(value)) from exc;
    if not 1 <= number <= 10:
        raise ChannelError("Channel must be 1..10 (A..J aliases are accepted)");
    return number;


@dataclass
class RandomField:
    width: int;
    name: str;
    offset: int;


@dataclass
class BasicChannel:
    number: int;
    stream: object;
    mode: str;
    source: str;
    binary: bool = False;
    random: bool = False;
    record_length: int = 0;
    fields: list = field(default_factory=list);
    process: object = None;
    owned: bool = True;

    def close(self):
        if self.owned and self.stream is not None:
            try: self.stream.close();
            except Exception: pass;
        if self.process is not None:
            try: self.process.wait(timeout=1.0);
            except Exception: pass;
        self.stream = None;


class ChannelManager:
    def __init__(self, stdin=None, stdout=None, stderr=None):
        self.stdin = stdin if stdin is not None else sys.stdin;
        self.stdout = stdout if stdout is not None else sys.stdout;
        self.stderr = stderr if stderr is not None else sys.stderr;
        self.channels = {};

    def close_all(self):
        for number in list(self.channels): self.close(number);

    def close(self, spec):
        number = channel_number(spec);
        channel = self.channels.pop(number, None);
        if channel is not None: channel.close();

    def get(self, spec):
        number = channel_number(spec);
        if number not in self.channels: raise ChannelError("Channel #{} is not open".format(number));
        return self.channels[number];

    def freefile(self):
        for number in range(1, 11):
            if number not in self.channels: return number;
        raise ChannelError("No free channel (1..10)");

    @staticmethod
    def _python_mode(mode, binary=False):
        key = str(mode).strip().lower();
        aliases = {
            "input": "r", "output": "w", "append": "a", "binary": "r+b", "random": "r+b",
            "r": "r", "w": "w", "a": "a", "r+": "r+", "w+": "w+", "a+": "a+",
            "rb": "rb", "wb": "wb", "ab": "ab", "r+b": "r+b", "w+b": "w+b", "a+b": "a+b",
        };
        if key not in aliases: raise ChannelError("Unsupported file mode: {}".format(mode));
        result = aliases[key];
        if binary and "b" not in result: result += "b";
        return result;

    def open(self, source, mode, number, record_length=0, encoding="utf-8"):
        number = channel_number(number);
        if number in self.channels: raise ChannelError("Channel #{} is already open".format(number));
        raw_source = str(source);
        key_source = raw_source.strip().casefold();
        key_mode = str(mode).strip().lower();
        random_access = key_mode == "random";
        binary = random_access or key_mode == "binary" or "b" in key_mode;
        stream = None; process = None; owned = True;
        if key_source in ("stdin", "stdin:"):
            if key_mode not in ("input", "r", "rb"): raise ChannelError("STDIN is input-only");
            stream = getattr(self.stdin, "buffer", self.stdin) if binary else self.stdin; owned = False;
        elif key_source in ("stdout", "stdout:"):
            if key_mode in ("input", "r", "rb"): raise ChannelError("STDOUT is output-only");
            stream = getattr(self.stdout, "buffer", self.stdout) if binary else self.stdout; owned = False;
        elif key_source in ("stderr", "stderr:"):
            if key_mode in ("input", "r", "rb"): raise ChannelError("STDERR is output-only");
            stream = getattr(self.stderr, "buffer", self.stderr) if binary else self.stderr; owned = False;
        elif raw_source.startswith("|") or raw_source.endswith("|"):
            command = raw_source.strip("|").strip();
            if not command: raise ChannelError("Pipeline command is empty");
            if key_mode in ("input", "r", "rb"):
                process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, text=not binary);
                stream = process.stdout;
            elif key_mode in ("output", "append", "w", "a", "wb", "ab"):
                process = subprocess.Popen(command, shell=True, stdin=subprocess.PIPE, text=not binary);
                stream = process.stdin;
            else:
                raise ChannelError("Pipeline supports INPUT/OUTPUT modes");
        else:
            py_mode = self._python_mode(key_mode, binary=binary);
            if random_access and not os.path.exists(raw_source): py_mode = "w+b";
            stream = open(raw_source, py_mode, encoding=None if "b" in py_mode else encoding);
        channel = BasicChannel(number, stream, key_mode, raw_source, binary=binary, random=random_access, record_length=max(0, int(record_length or 0)), process=process, owned=owned);
        self.channels[number] = channel;
        return channel;

    def define_fields(self, spec, definitions):
        channel = self.get(spec);
        if not channel.random: raise ChannelError("FIELD requires a RANDOM channel");
        offset = 0; fields = [];
        for width, name in definitions:
            width = int(width);
            if width <= 0: raise ChannelError("FIELD width must be positive");
            fields.append(RandomField(width, str(name), offset)); offset += width;
        if channel.record_length <= 0: channel.record_length = offset;
        if offset > channel.record_length: raise ChannelError("FIELD definitions exceed record length {}".format(channel.record_length));
        channel.fields = fields;
        return fields;

    def print(self, spec, text, end="\n"):
        channel = self.get(spec);
        if channel.binary: raise ChannelError("PRINT # requires a text channel");
        channel.stream.write(str(text) + str(end)); channel.stream.flush();

    def readline(self, spec):
        channel = self.get(spec);
        if channel.binary: raise ChannelError("LINE INPUT # requires a text channel");
        value = channel.stream.readline();
        if value == "": return "";
        return value.rstrip("\r\n");

    def input_values(self, spec):
        line = self.readline(spec);
        values = [];
        current = []; quote = False;
        for ch in line:
            if ch == '"': quote = not quote; current.append(ch);
            elif ch == "," and not quote: values.append("".join(current).strip()); current = [];
            else: current.append(ch);
        values.append("".join(current).strip());
        return [item[1:-1] if len(item) >= 2 and item[0] == item[-1] == '"' else item for item in values];

    def eof(self, spec):
        channel = self.get(spec); stream = channel.stream;
        if not hasattr(stream, "tell") or not hasattr(stream, "seek"):
            return False;
        try:
            here = stream.tell(); data = stream.read(1); stream.seek(here); return data in ("", b"");
        except (OSError, io.UnsupportedOperation): return False;

    def lof(self, spec):
        channel = self.get(spec); stream = channel.stream;
        try:
            here = stream.tell(); stream.seek(0, os.SEEK_END); size = stream.tell(); stream.seek(here); return size;
        except (OSError, io.UnsupportedOperation): return 0;

    def loc(self, spec):
        channel = self.get(spec);
        try:
            pos = channel.stream.tell();
            if channel.random and channel.record_length: return (pos // channel.record_length) + 1;
            return pos;
        except (OSError, io.UnsupportedOperation): return 0;

    def get_record(self, spec, record_number):
        channel = self.get(spec);
        if not channel.random: raise ChannelError("GET requires a RANDOM channel");
        if channel.record_length <= 0: raise ChannelError("RANDOM channel requires LEN or FIELD definitions");
        record = max(1, int(record_number)); channel.stream.seek((record - 1) * channel.record_length);
        data = channel.stream.read(channel.record_length);
        if len(data) < channel.record_length: data += b" " * (channel.record_length - len(data));
        return data;

    def put_record(self, spec, record_number, data):
        channel = self.get(spec);
        if not channel.random: raise ChannelError("PUT requires a RANDOM channel");
        if channel.record_length <= 0: raise ChannelError("RANDOM channel requires LEN or FIELD definitions");
        record = max(1, int(record_number)); payload = bytes(data[:channel.record_length]).ljust(channel.record_length, b" ");
        channel.stream.seek((record - 1) * channel.record_length); channel.stream.write(payload); channel.stream.flush();
