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
from collections import deque;
import os;
import select;
import sys;
import re;


class TerminalInput:
    """Immediate terminal keyboard input for command-line BASIC programs.

    POSIX terminals stay in cbreak mode while a program runs so INKEY$ can
    see a key without Enter.  INPUT temporarily restores the normal terminal
    mode, preserving ordinary line editing and echo.
    """
    _SGR_MOUSE_RE = re.compile(br"^\x1b\[<(\d+);(\d+);(\d+)([Mm])$");
    _KITTY_KEY_RE = re.compile(br"^\x1b\[([0-9:]+)(?:;([0-9]+)(?::([123]))?)?(?:;([0-9:]*))?u$");

    def __init__(self, stream=None, pointer_callback=None, keyup_callback=None):
        self.stream = stream if stream is not None else sys.stdin;
        self.fd = None;
        self.enabled = False;
        self._windows = os.name == "nt";
        self._saved_attributes = None;
        self._termios = None;
        self._tty = None;
        self.pointer_callback = pointer_callback;
        self.keyup_callback = keyup_callback;
        self._mouse_reporting = False;
        self._keyboard_reporting = False;
        self._inkey_queue = deque();
        self._keyup_queue = deque();
        self.key_repeat = True;
        self._last_event_extended = False;
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
            self._enable_keyboard();
            self._enable_mouse();
        return self;

    def __exit__(self, exc_type, exc_value, traceback):
        self.restore();
        return False;

    def restore(self):
        self._disable_mouse();
        self._disable_keyboard();
        if self.enabled and not self._windows and self._saved_attributes is not None:
            try:
                self._termios.tcsetattr(self.fd, self._termios.TCSADRAIN, self._saved_attributes);
            except (OSError, ValueError):
                pass;

    def _resume_cbreak(self):
        if self.enabled and not self._windows and self._tty is not None:
            try:
                self._tty.setcbreak(self.fd);
                self._enable_keyboard();
                self._enable_mouse();
            except (OSError, ValueError):
                pass;


    def _enable_keyboard(self):
        """Request Kitty progressive keyboard events when the terminal supports them.

        Flags 27 request disambiguated press/repeat/release events for all keys
        plus associated text.  Unsupported terminals safely ignore the CSI.
        """;
        if self.enabled and not self._windows and self.fd is not None and not self._keyboard_reporting:
            try:
                # Push the caller's mode and then set the requested flags explicitly.
                # Some terminals implement the progressive-enhancement setter more
                # completely than the stack form; sending both remains valid for
                # Kitty-compatible terminals and improves interoperability.
                os.write(self.fd, b"\x1b[>27u\x1b[=27u");
                self._keyboard_reporting = True;
            except (OSError, ValueError):
                self._keyboard_reporting = False;

    def _disable_keyboard(self):
        if self._keyboard_reporting and self.fd is not None:
            try:
                # Reset first for terminals that implement SET but not the stack,
                # then pop so fully compatible terminals restore the caller's mode.
                os.write(self.fd, b"\x1b[=0u\x1b[<u");
            except (OSError, ValueError): pass;
        self._keyboard_reporting = False;

    def _enable_mouse(self):
        if self.enabled and not self._windows and self.fd is not None and not self._mouse_reporting:
            try:
                os.write(self.fd, b"\x1b[?1000h\x1b[?1006h");
                self._mouse_reporting = True;
            except (OSError, ValueError):
                self._mouse_reporting = False;

    def _disable_mouse(self):
        if self._mouse_reporting and self.fd is not None:
            try: os.write(self.fd, b"\x1b[?1006l\x1b[?1000l");
            except (OSError, ValueError): pass;
        self._mouse_reporting = False;

    def set_key_repeat(self, enabled=True):
        """Enable/disable delivery of distinguishable repeat events.

        Legacy terminals send repeated printable bytes without an event type.
        With repeat disabled Sum therefore treats INKEY$ as a real-time sample:
        it returns the newest pending character and discards stale typematic
        backlog, while Kitty release events remain untouched.
        """;
        self.key_repeat = bool(enabled);
        if not self.key_repeat:
            self._inkey_queue.clear();
            self._discard_legacy_pending_input();
        return self.key_repeat;

    def _discard_legacy_pending_input(self):
        if not self.enabled: return None;
        if self._windows:
            try:
                import msvcrt;
                while msvcrt.kbhit(): msvcrt.getwch();
            except Exception: pass;
            return None;
        if self.fd is not None and self._termios is not None:
            try: self._termios.tcflush(self.fd, self._termios.TCIFLUSH);
            except (AttributeError, OSError, ValueError): pass;
        return None;

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

    def _decode_kitty_key(self, data):
        """Return ``(legacy_value, event_type)`` for a Kitty CSI-u event.""";
        match = self._KITTY_KEY_RE.match(data);
        if match is None:
            return None;
        key_field, modifiers_field, event_field, text_field = match.groups();
        try:
            key_code = int(key_field.split(b":", 1)[0]);
            modifiers = int(modifiers_field or b"1");
            event_type = int(event_field or b"1");
        except (TypeError, ValueError):
            return None;
        modifier_bits = max(0, modifiers - 1);
        if event_type == 1 and key_code in (67, 99) and (modifier_bits & 4):
            raise KeyboardInterrupt();
        text = "";
        if text_field:
            try:
                text = "".join(chr(int(item)) for item in text_field.split(b":") if item);
            except (TypeError, ValueError, OverflowError):
                text = "";
        if event_type in (1, 2) and text:
            return text, event_type;
        if key_code == 27:
            return chr(27), event_type;
        if key_code == 13:
            return "\r", event_type;
        if key_code == 9:
            return "\t", event_type;
        if key_code == 127:
            return "\x7f", event_type;
        if 32 <= key_code <= 0x10ffff and not 0xe000 <= key_code <= 0xf8ff:
            try: return chr(key_code), event_type;
            except (ValueError, OverflowError): pass;
        # Keep non-text functional keys compatible with historical INKEY$: the
        # raw CSI remains visible instead of inventing a new BASIC key name.
        if event_type in (1, 2):
            return self._decode_key(data), event_type;
        return "", event_type;

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

    def _poll_key_event(self):
        """Return ``(action, value)`` without losing the opposite event kind.""";
        self._last_event_extended = False;
        if not self.enabled:
            return "none", "";
        if self._windows:
            value = self._read_windows();
            return ("press", value) if value else ("none", "");
        data = self._read_posix_bytes(0.0);
        if not data:
            return "none", "";
        if data == b"\x1b":
            tail = self._read_posix_bytes(0.015);
            if tail:
                data += tail;
        if data.startswith(b"\x1b[<"):
            while not data.endswith((b"M", b"m")) and len(data) < 64:
                tail = self._read_posix_bytes(0.002, maximum=64 - len(data));
                if not tail: break;
                data += tail;
            match = self._SGR_MOUSE_RE.match(data);
            if match:
                code, x, y, ending = match.groups();
                code = int(code);
                button = 1 if (code & 3) == 0 and ending == b"M" else 0;
                if callable(self.pointer_callback):
                    self.pointer_callback(int(x), int(y), button);
                return "none", "";
        if data.startswith(b"\x1b[") and not data.endswith(b"u"):
            while len(data) < 96:
                tail = self._read_posix_bytes(0.002, maximum=96 - len(data));
                if not tail: break;
                data += tail;
                if data.endswith(b"u"): break;
        kitty = self._decode_kitty_key(data);
        if kitty is not None:
            self._last_event_extended = True;
            value, event_type = kitty;
            return {1: "press", 2: "repeat", 3: "release"}.get(event_type, "press"), value;
        return "press", self._decode_key(data);

    def inkey(self):
        if self._inkey_queue:
            return self._inkey_queue.popleft();
        action, value = self._poll_key_event();
        if action == "release":
            if value:
                self._keyup_queue.append(value);
                if callable(self.keyup_callback): self.keyup_callback(value);
            return "";
        if action == "repeat" and not self.key_repeat:
            return "";
        if action in ("press", "repeat"):
            if not self.key_repeat and not self._last_event_extended and not self._windows:
                # _read_posix_bytes intentionally drains the currently ready
                # kernel bytes.  For real-time KEYREPEAT OFF semantics keep only
                # the newest decoded character, then flush any typematic bytes
                # that arrived while the sequence was being decoded.
                if len(value) > 1 and not value.startswith("\x1b"): value = value[-1];
                self._inkey_queue.clear();
                self._discard_legacy_pending_input();
                return value;
            if len(value) > 1 and not value.startswith("\x1b"):
                for char in value[1:]: self._inkey_queue.append(char);
                return value[0];
            return value;
        return "";

    def keyup(self):
        if self._keyup_queue:
            return self._keyup_queue.popleft();
        action, value = self._poll_key_event();
        if action == "release":
            return value;
        if action == "repeat" and not self.key_repeat:
            return "";
        if action in ("press", "repeat") and value:
            if not self.key_repeat and not self._last_event_extended and not self._windows:
                if len(value) > 1 and not value.startswith("\x1b"): value = value[-1];
                self._inkey_queue.clear();
                self._inkey_queue.append(value);
                self._discard_legacy_pending_input();
            else:
                self._inkey_queue.append(value);
        return "";
