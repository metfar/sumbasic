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
import builtins;
import os;
import select;
import sys;


class TerminalInput:
    """Immediate terminal keyboard input for command-line BASIC programs.

    POSIX terminals stay in cbreak mode while a program runs so INKEY$ can
    see a key without Enter.  INPUT temporarily restores the normal terminal
    mode, preserving ordinary line editing and echo.
    """
    def __init__(self, stream=None):
        self.stream = stream if stream is not None else sys.stdin;
        self.fd = None;
        self.enabled = False;
        self._windows = os.name == "nt";
        self._saved_attributes = None;
        self._termios = None;
        self._tty = None;
        try:
            self.fd = self.stream.fileno();
            self.enabled = bool(self.stream.isatty());
        except (AttributeError, OSError, ValueError):
            self.fd = None;
            self.enabled = False;

    def __enter__(self):
        if self.enabled and not self._windows:
            import termios;
            import tty;
            self._termios = termios;
            self._tty = tty;
            self._saved_attributes = termios.tcgetattr(self.fd);
            tty.setcbreak(self.fd);
        return self;

    def __exit__(self, exc_type, exc_value, traceback):
        self.restore();
        return False;

    def restore(self):
        if self.enabled and not self._windows and self._saved_attributes is not None:
            try:
                self._termios.tcsetattr(self.fd, self._termios.TCSADRAIN, self._saved_attributes);
            except (OSError, ValueError):
                pass;

    def _resume_cbreak(self):
        if self.enabled and not self._windows and self._tty is not None:
            try:
                self._tty.setcbreak(self.fd);
            except (OSError, ValueError):
                pass;

    def input(self, prompt=""):
        if not self.enabled or self._windows:
            return builtins.input(prompt);
        self.restore();
        try:
            return builtins.input(prompt);
        finally:
            self._resume_cbreak();

    def run_external(self, callback):
        """Temporarily restore normal terminal mode for an external program.""";
        if not callable(callback):
            raise TypeError("callback must be callable");
        if not self.enabled or self._windows:
            return callback();
        self.restore();
        try:
            return callback();
        finally:
            self._resume_cbreak();

    def _read_posix_bytes(self, timeout=0.0, maximum=16):
        if not self.enabled or self.fd is None:
            return b"";
        ready, _, _ = select.select([self.fd], [], [], max(0.0, float(timeout)));
        if not ready:
            return b"";
        data = os.read(self.fd, 1);
        while len(data) < maximum:
            ready, _, _ = select.select([self.fd], [], [], 0.0);
            if not ready:
                break;
            data += os.read(self.fd, 1);
        return data;

    def _decode_key(self, data):
        if not data:
            return "";
        encoding = getattr(self.stream, "encoding", None) or "utf-8";
        try:
            return data.decode(encoding);
        except UnicodeDecodeError:
            try:
                return data.decode("utf-8");
            except UnicodeDecodeError:
                return data.decode(encoding, errors="ignore");

    def _read_posix(self):
        data = self._read_posix_bytes(0.0);
        if not data:
            return "";
        # A bare Escape is a key in its own right, while cursor/function keys
        # normally begin with ESC.  Give an escape sequence a tiny opportunity
        # to arrive so an arrow does not look like the Escape key to BASIC.
        if data == b"\x1b":
            tail = self._read_posix_bytes(0.015);
            if tail:
                data += tail;
        return self._decode_key(data);

    def _read_windows(self):
        if not self.enabled:
            return "";
        import msvcrt;
        if not msvcrt.kbhit():
            return "";
        value = msvcrt.getwch();
        if value in ("\x00", "\xe0") and msvcrt.kbhit():
            value += msvcrt.getwch();
        return value;

    def inkey(self):
        if not self.enabled:
            return "";
        if self._windows:
            return self._read_windows();
        return self._read_posix();
