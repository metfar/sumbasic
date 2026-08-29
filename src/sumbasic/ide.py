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
import threading;

from sumtui import FunctionAction, Menu, MenuItem, Panel, TextView, VBox;
from sumtui.tools.edit import EditApp;

from .interpreter import BasicError, BasicInterpreter;


class _VirtualRunScreen:
    """Small ANSI-aware text screen used by the IDE run pane.

    sumBASIC text programs use CLS and LOCATE through ordinary ANSI cursor
    sequences.  A plain TextView would otherwise display those sequences as
    text.  This buffer understands the small subset emitted by the interpreter
    and keeps a terminal-like screen that can be refreshed while the program
    is still running.
    """
    _LOCATE_RE = re.compile(r"^\x1b\[(\d+);(\d+)H");

    def __init__(self):
        self._lock = threading.Lock();
        self.clear();

    def clear(self):
        with getattr(self, "_lock", threading.Lock()):
            self._rows = [""];
            self._row = 0;
            self._col = 0;
        return None;

    def _ensure_row(self, row):
        while len(self._rows) <= row:
            self._rows.append("");
        return None;

    def _put(self, char):
        self._ensure_row(self._row);
        line = self._rows[self._row];
        if len(line) < self._col:
            line += " " * (self._col - len(line));
        if self._col < len(line):
            line = line[:self._col] + char + line[self._col + 1:];
        else:
            line += char;
        self._rows[self._row] = line;
        self._col += 1;
        return None;

    def write(self, text, end="\n"):
        data = str(text) + ("" if end == "" else end);
        with self._lock:
            index = 0;
            while index < len(data):
                if data.startswith("\x1b[2J", index):
                    self._rows = [""];
                    self._row = 0;
                    self._col = 0;
                    index += 4;
                    continue;
                if data.startswith("\x1b[H", index):
                    self._row = 0;
                    self._col = 0;
                    index += 3;
                    continue;
                if data.startswith("\x1b[", index):
                    match = self._LOCATE_RE.match(data[index:]);
                    if match:
                        self._row = max(0, int(match.group(1)) - 1);
                        self._col = max(0, int(match.group(2)) - 1);
                        self._ensure_row(self._row);
                        index += match.end();
                        continue;
                char = data[index];
                if char == "\n":
                    self._row += 1;
                    self._col = 0;
                    self._ensure_row(self._row);
                elif char == "\r":
                    self._col = 0;
                elif char == "\t":
                    target = ((self._col // 8) + 1) * 8;
                    while self._col < target:
                        self._put(" ");
                else:
                    self._put(char);
                index += 1;
        return None;

    def text(self):
        with self._lock:
            rows = list(self._rows);
        while len(rows) > 1 and rows[-1] == "":
            rows.pop();
        return "\n".join(rows);


class SumBasicIDE(EditApp):
    """sumTUI source editor with non-blocking sumBASIC F5 execution."""
    def __init__(self, path=None, theme=None, interpreter=None, **kwargs):
        self._basic_output_buffer = "";
        self._run_screen = _VirtualRunScreen();
        self._run_thread = None;
        self._run_dirty = False;
        self._run_finished = False;
        self._run_error = None;
        self._run_lock = threading.Lock();
        self.basic_interpreter = interpreter;
        super().__init__(path=path, theme=theme, **kwargs);
        self.output_view = TextView("Ready. Press F5 to run the current editor buffer.");
        self.output_panel = Panel(self.output_view, title="Run output", content_style="viewer");
        body = VBox(self.panel, self.output_panel, self.status, self.bar, sizes=[None, 12, 1, 1]);
        self.desktop.body = body;
        self.app.set_root(self.desktop);
        if self.basic_interpreter is None:
            self.basic_interpreter = BasicInterpreter(input_func=self._ide_input, output_func=self._basic_output);
        else:
            self.basic_interpreter.output_func = self._basic_output;
        self.app.add_idle(self._poll_run_state);
        self._update_status();

    def _register_keybindings(self):
        super()._register_keybindings();
        self.keys.register("basic.run", "Run BASIC", ["f5"], context="editor", callback=self.run_program);
        self.keys.register("basic.stop", "Stop BASIC", ["f6"], context="editor", callback=self.stop_program);
        return self.keys;

    def _make_function_bar(self):
        bar = super()._make_function_bar();
        run_key = self.keys.primary("basic.run");
        stop_key = self.keys.primary("basic.stop");
        insert_at = min(2, len(bar.actions));
        if run_key:
            bar.actions.insert(insert_at, FunctionAction(run_key, "Run", None));
            insert_at += 1;
        if stop_key:
            bar.actions.insert(insert_at, FunctionAction(stop_key, "Stop", None));
        return bar;

    def _menus(self):
        menus = super()._menus();
        menus.append(Menu("Run", [
            MenuItem("Run current buffer", self.run_program, self._ks("basic.run")),
            MenuItem("Stop running program", self.stop_program, self._ks("basic.stop")),
        ]));
        return menus;

    def _basic_output(self, text, end="\n"):
        piece = str(text) + ("" if end == "" else end);
        with self._run_lock:
            self._basic_output_buffer += piece;
            self._run_dirty = True;
        self._run_screen.write(text, end=end);
        return None;

    def _ide_input(self, prompt=""):
        raise BasicError("Interactive INPUT from the source IDE is not implemented yet; run this program in the sumBASIC console for interactive input");

    def _prepare_run(self):
        with self._run_lock:
            self._basic_output_buffer = "";
            self._run_dirty = True;
            self._run_finished = False;
            self._run_error = None;
        self._run_screen.clear();
        self.output_view.set_text("Running...");
        self.status.set("Running. F6 stops the current BASIC program.");
        return None;

    def _run_worker(self, source):
        try:
            self.basic_interpreter.program.load_text(source);
            self.basic_interpreter.run();
        except Exception as exc:
            with self._run_lock:
                self._run_error = exc;
        finally:
            with self._run_lock:
                self._run_finished = True;
                self._run_dirty = True;
        return None;

    def _scroll_output_end(self):
        self.output_view.offset = max(0, len(self.output_view.lines) - self.output_view.page_size);
        return None;

    def _finish_sync(self):
        rendered = self._run_screen.text();
        error = self._run_error;
        if error is not None:
            message = "Error: {}".format(error);
            self.output_view.set_text((rendered + "\n" if rendered else "") + message);
            self.status.set("Run error");
        elif self.basic_interpreter.stopped_by_request:
            self.output_view.set_text(rendered if rendered else "Program stopped.");
            self.status.set("Run stopped");
        else:
            self.output_view.set_text(rendered if rendered else "Program finished with no text output.");
            self.status.set("Run complete. F5 executes the current editor buffer, saved or not.");
        self._scroll_output_end();
        self.app.invalidate();
        return True;

    def run_program(self):
        if self._run_thread is not None and self._run_thread.is_alive():
            self.status.set("Program already running. Press F6 to stop it.");
            return True;
        source = self.editor.text;
        self._prepare_run();
        if not self.app.running:
            self._run_worker(source);
            return self._finish_sync();
        self._run_thread = threading.Thread(target=self._run_worker, args=(source,), name="sumBASIC-run", daemon=True);
        self._run_thread.start();
        self.app.invalidate();
        return True;

    def stop_program(self):
        if self._run_thread is None or not self._run_thread.is_alive():
            self.status.set("No BASIC program is running.");
            return True;
        self.basic_interpreter.request_stop();
        self.status.set("Stopping BASIC program...");
        return True;

    def _poll_run_state(self):
        with self._run_lock:
            dirty = self._run_dirty;
            finished = self._run_finished;
            error = self._run_error;
            self._run_dirty = False;
        if dirty:
            rendered = self._run_screen.text();
            if rendered:
                self.output_view.set_text(rendered);
                self._scroll_output_end();
        if finished:
            rendered = self._run_screen.text();
            if error is not None:
                message = "Error: {}".format(error);
                self.output_view.set_text((rendered + "\n" if rendered else "") + message);
                self.status.set("Run error");
            elif self.basic_interpreter.stopped_by_request:
                self.output_view.set_text(rendered if rendered else "Program stopped.");
                self.status.set("Run stopped");
            else:
                self.output_view.set_text(rendered if rendered else "Program finished with no text output.");
                self.status.set("Run complete. F5 executes the current editor buffer, saved or not.");
            self._scroll_output_end();
            self._run_thread = None;
            with self._run_lock:
                self._run_finished = False;
            return True;
        return dirty;
