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
#
"""sumBASIC language backend for the common sumIDE shell.

The editor/workspace/preferences implementation lives in :mod:`sumide`.  This
module deliberately keeps only BASIC-specific execution services so old
``SumBasicIDE`` imports continue to work without reviving a second IDE.
""";
import queue;
import re;
import threading;

from sumide.app import ScriptIDE;
from sumtui.events import Key, KeyEvent;

from .interpreter import BasicError, BasicInterpreter;
from .shell import run_interactive_shell;


class _VirtualRunScreen:
    """Small ANSI-aware screen for CLS/LOCATE output in the IDE pane.""";
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
                    target = ((self._col // 4) + 1) * 4;
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


class SumBasicIDE(ScriptIDE):
    """Common sumIDE shell plus the cooperative/in-process BASIC backend.""";
    def __init__(self, path=None, theme=None, interpreter=None, **kwargs):
        self._basic_output_buffer = "";
        self._run_screen = _VirtualRunScreen();
        self._run_thread = None;
        self._run_dirty = False;
        self._run_finished = False;
        self._run_error = None;
        self._run_lock = threading.Lock();
        self._inkey_queue = queue.Queue();
        self._direct_basic_thread = None;
        self._direct_basic_output_buffer = "";
        self._direct_basic_finished = False;
        self._direct_basic_error = None;
        self._shell_output_pending = False;
        self.basic_interpreter = interpreter;
        kwargs.pop("config", None);
        kwargs.pop("config_path", None);
        super().__init__(path=path, language="basic", theme=theme, **kwargs);
        self.command_view.on_submit = self._submit_direct_command;
        if self.basic_interpreter is None:
            self.basic_interpreter = BasicInterpreter(
                input_func=self._ide_input,
                output_func=self._basic_output,
                inkey_func=self._ide_inkey,
                shell_interactive_func=self._interactive_shell,
                shell_output_func=self._shell_output,
            );
        else:
            self.basic_interpreter.output_func = self._basic_output;
            self.basic_interpreter.inkey_func = self._ide_inkey;
            self.basic_interpreter.shell_interactive_func = self._interactive_shell;
            self.basic_interpreter.shell_output_func = self._shell_output;
        self._application_dispatch = self.app.dispatch;
        self.app.dispatch = self._dispatch_event;
        self.app.add_idle(self._poll_run_state);
        self.output_view.set_text("Ready. Press F5 to run the current BASIC buffer.");
        self._update_status("BASIC IDE");

    def _register_keybindings(self):
        super()._register_keybindings();
        self.keys.register("basic.run", "Run / Stop BASIC", ["f5", "ctrl+r"], context="editor", callback=self.toggle_run);
        return self.keys;

    def _basic_output(self, text, end="\n"):
        piece = str(text) + ("" if end == "" else end);
        with self._run_lock:
            self._basic_output_buffer += piece;
            self._run_dirty = True;
        self._run_screen.write(text, end=end);
        return None;

    def _shell_output(self, text, end=""):
        self._basic_output(text, end=end);
        with self._run_lock:
            self._shell_output_pending = True;
        return None;

    def _interactive_shell(self):
        return self.app.run_external(run_interactive_shell);

    def _ide_input(self, prompt=""):
        raise BasicError("Interactive INPUT from the source IDE is not implemented yet; run this program in the sumBASIC console for interactive input");

    def _ide_inkey(self):
        try:
            return self._inkey_queue.get_nowait();
        except queue.Empty:
            return "";

    def _queue_program_key(self, value):
        if value:
            self._inkey_queue.put(str(value));
        return True;

    def _dispatch_event(self, event):
        running = self._run_thread is not None and self._run_thread.is_alive();
        if running and isinstance(event, KeyEvent):
            if event.key == Key.ESCAPE:
                return self._queue_program_key(chr(27));
            if event.text and not event.ctrl and not event.alt:
                return self._queue_program_key(event.text);
        return self._application_dispatch(event);

    def _prepare_run(self):
        while True:
            try:
                self._inkey_queue.get_nowait();
            except queue.Empty:
                break;
        with self._run_lock:
            self._basic_output_buffer = "";
            self._run_dirty = True;
            self._run_finished = False;
            self._run_error = None;
        self._run_screen.clear();
        self.output_view.set_text("Running...");
        self._update_status("Running BASIC. F5 stops; F6 switches windows.");
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
            self._update_status("Run error");
        elif self.basic_interpreter.stopped_by_statement:
            self.output_view.set_text(rendered if rendered else "Program stopped by STOP.");
            self._update_status("BASIC STOP. CONTINUE or F5 resumes from the next statement.");
        elif self.basic_interpreter.stopped_by_request:
            self.output_view.set_text(rendered if rendered else "Program stopped.");
            self._update_status("Run stopped");
        else:
            self.output_view.set_text(rendered if rendered else "Program finished with no text output.");
            self._update_status("Run complete. F5 executes the current editor buffer, saved or not.");
        self._scroll_output_end();
        self.app.invalidate();
        return True;

    def _basic_direct_output(self, text, end="\n"):
        piece = str(text) + ("" if end == "" else end);
        with self._run_lock:
            self._direct_basic_output_buffer += piece;
        return None;

    def _direct_worker_basic(self, source):
        previous_output = self.basic_interpreter.output_func;
        try:
            self.basic_interpreter.output_func = self._basic_direct_output;
            self.basic_interpreter.execute_direct(source);
        except Exception as exc:
            with self._run_lock:
                self._direct_basic_error = exc;
        finally:
            self.basic_interpreter.output_func = previous_output;
            with self._run_lock:
                self._direct_basic_finished = True;
        return None;

    def _submit_direct_command(self, line, window):
        source = str(line or "").strip();
        if not source:
            return None;
        if self._run_thread is not None and self._run_thread.is_alive():
            window.write_error("A BASIC program is running; stop it before using direct mode.");
            return None;
        if self._direct_basic_thread is not None and self._direct_basic_thread.is_alive():
            window.write_error("A direct command is already running.");
            return None;
        with self._run_lock:
            self._direct_basic_output_buffer = "";
            self._direct_basic_error = None;
            self._direct_basic_finished = False;
        self._update_status("Direct BASIC command running...");
        if not self.app.running:
            self._direct_worker_basic(source);
            self._finish_direct_command();
            return None;
        self._direct_basic_thread = threading.Thread(target=self._direct_worker_basic, args=(source,), name="sumBASIC-direct", daemon=True);
        self._direct_basic_thread.start();
        return None;

    def _finish_direct_command(self):
        with self._run_lock:
            output = self._direct_basic_output_buffer;
            error = self._direct_basic_error;
            self._direct_basic_finished = False;
        if output:
            for line in output.rstrip("\n").splitlines():
                self.command_view.write(line, style="command");
        if error is not None:
            self.command_view.write_error("Error: {}".format(error));
            self._update_status("Direct command error");
        else:
            self._update_status("Direct command complete");
        self._direct_basic_thread = None;
        self.app.invalidate();
        return True;

    def toggle_run(self):
        if self._run_thread is not None and self._run_thread.is_alive():
            return self.stop_program();
        if self._direct_basic_thread is not None and self._direct_basic_thread.is_alive():
            self.basic_interpreter.request_stop();
            self._update_status("Stopping direct BASIC command...");
            return True;
        if self.basic_interpreter.can_continue:
            return self.continue_program();
        return self.run_program();

    def _continue_worker(self):
        try:
            self.basic_interpreter.continue_run();
        except Exception as exc:
            with self._run_lock:
                self._run_error = exc;
        finally:
            with self._run_lock:
                self._run_finished = True;
                self._run_dirty = True;
        return None;

    def continue_program(self):
        if self._run_thread is not None and self._run_thread.is_alive():
            self._update_status("Program is already running.");
            return True;
        if not self.basic_interpreter.can_continue:
            self._update_status("No BASIC STOP to continue from.");
            return True;
        with self._run_lock:
            self._run_finished = False;
            self._run_error = None;
            self._run_dirty = True;
        self._update_status("Continuing after STOP. F5 stops; F6 switches windows.");
        if not self.app.running:
            self._continue_worker();
            return self._finish_sync();
        self._run_thread = threading.Thread(target=self._continue_worker, name="sumBASIC-continue", daemon=True);
        self._run_thread.start();
        self.app.invalidate();
        return True;

    def run_program(self):
        if self._run_thread is not None and self._run_thread.is_alive():
            self._update_status("Program already running. Press F5 to stop it.");
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
            self._update_status("No BASIC program is running.");
            return True;
        self.basic_interpreter.request_stop();
        self._update_status("Stopping BASIC program...");
        return True;

    def _poll_run_state(self):
        with self._run_lock:
            dirty = self._run_dirty;
            finished = self._run_finished;
            error = self._run_error;
            shell_output_pending = self._shell_output_pending;
            self._run_dirty = False;
            self._shell_output_pending = False;
        if dirty:
            rendered = self._run_screen.text();
            if rendered:
                self.output_view.set_text(rendered);
                self._scroll_output_end();
        if shell_output_pending:
            self.workspace.show(self.output_window);
            dirty = True;
        with self._run_lock:
            direct_finished = self._direct_basic_finished;
        if direct_finished:
            self._finish_direct_command();
            dirty = True;
        if finished:
            rendered = self._run_screen.text();
            if error is not None:
                message = "Error: {}".format(error);
                self.output_view.set_text((rendered + "\n" if rendered else "") + message);
                self._update_status("Run error");
            elif self.basic_interpreter.stopped_by_statement:
                self.output_view.set_text(rendered if rendered else "Program stopped by STOP.");
                self._update_status("BASIC STOP. CONTINUE or F5 resumes from the next statement.");
            elif self.basic_interpreter.stopped_by_request:
                self.output_view.set_text(rendered if rendered else "Program stopped.");
                self._update_status("Run stopped");
            else:
                self.output_view.set_text(rendered if rendered else "Program finished with no text output.");
                self._update_status("Run complete. F5 executes the current editor buffer, saved or not.");
            self._scroll_output_end();
            self._run_thread = None;
            with self._run_lock:
                self._run_finished = False;
            return True;
        return dirty;
