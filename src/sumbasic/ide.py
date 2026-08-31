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
import queue;
import re;
import threading;

from sumtui import CommandWindow, CommandWindowPane, FunctionAction, Menu, MenuItem, Separator, TextView, TextViewPane, VBox, Workspace, WorkspaceWindow;
from sumtui.events import Key, KeyEvent;
from sumtui.tools.edit import EditApp;

from .interpreter import BasicError, BasicInterpreter;
from .shell import run_interactive_shell;


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
        self._inkey_queue = queue.Queue();
        self._direct_thread = None;
        self._direct_output_buffer = "";
        self._direct_finished = False;
        self._direct_error = None;
        self._shell_output_pending = False;
        self.basic_interpreter = interpreter;
        super().__init__(path=path, theme=theme, **kwargs);
        self.output_view = TextView("Ready. Press F5 to run the current editor buffer.");
        self.command_view = CommandWindow(prompt="> ", on_submit=self._submit_direct_command);
        self.output_pane = TextViewPane(self.output_view);
        self.command_pane = CommandWindowPane(self.command_view);
        title = self.document.path.name if self.document.path is not None else "Untitled";
        available_width = max(40, int(self.app.width));
        available_height = max(12, int(self.app.height) - 3);
        code_width = max(30, min(available_width - 2, int(available_width * 0.78)));
        code_height = max(9, min(available_height - 1, int(available_height * 0.72)));
        output_width = max(28, min(available_width - 4, int(available_width * 0.68)));
        output_height = max(7, min(available_height - 2, 10));
        command_width = max(28, min(available_width - 2, 44));
        command_height = max(7, min(available_height - 2, 11));
        self.code_window = WorkspaceWindow(self.panel.child, title="Code - {}".format(title), name="code", left=1, top=0, width=code_width, height=code_height, content_style="viewer");
        self.output_window = WorkspaceWindow(self.output_pane, title="Output", name="output", left=3, top=max(1, available_height - output_height), width=output_width, height=output_height, content_style="viewer");
        self.command_window = WorkspaceWindow(self.command_pane, title="Command", name="command", left=max(0, available_width - command_width - 1), top=max(1, available_height - command_height - 1), width=command_width, height=command_height, content_style="command");
        self.workspace = Workspace(
            self.output_window,
            self.command_window,
            self.code_window,
            layout_id="sumbasic",
            layout_path=self._workspace_layout_path(),
            viewport_width=available_width,
            viewport_height=available_height,
        );
        body = VBox(self.workspace, self.status, self.bar, sizes=[None, 1, 1]);
        self.desktop.body = body;
        self.app.set_root(self.desktop);
        self.workspace.activate(self.code_window);
        if self.basic_interpreter is None:
            self.basic_interpreter = BasicInterpreter(input_func=self._ide_input, output_func=self._basic_output, inkey_func=self._ide_inkey, shell_interactive_func=self._interactive_shell, shell_output_func=self._shell_output);
        else:
            self.basic_interpreter.output_func = self._basic_output;
            self.basic_interpreter.inkey_func = self._ide_inkey;
            self.basic_interpreter.shell_interactive_func = self._interactive_shell;
            self.basic_interpreter.shell_output_func = self._shell_output;
        self._application_dispatch = self.app.dispatch;
        self.app.dispatch = self._dispatch_event;
        self.app.add_idle(self._poll_run_state);
        self.menu.menus = self._menus();
        self._update_status();

    def _register_keybindings(self):
        super()._register_keybindings();
        self.keys.register("basic.run", "Run / Stop BASIC", ["f5", "ctrl+r"], context="editor", callback=self.toggle_run);
        self.keys.register("menu.run", "Run menu", ["alt+r"], context="editor", callback=lambda: self.open_menu(6));
        self.keys.register("menu.help", "Help menu", ["alt+h"], context="editor", callback=lambda: self.open_menu(7));
        return self.keys;

    def _make_function_bar(self):
        bar = super()._make_function_bar();
        run_key = self.keys.primary("basic.run");
        insert_at = min(2, len(bar.actions));
        if run_key:
            bar.actions.insert(insert_at, FunctionAction(run_key, "Run/Stop", None));
        return bar;

    def _menus(self):
        menus = super()._menus();
        run_menu = Menu("Run", [
            MenuItem("Run / Stop current buffer", self.toggle_run, self._ks("basic.run")),
            MenuItem("Continue after BASIC STOP", self.continue_program),
        ]);
        help_index = next((index for index, menu in enumerate(menus) if menu.title == "Help"), len(menus));
        menus.insert(help_index, run_menu);
        return menus;

    def _menu_closed(self):
        workspace = getattr(self, "workspace", None);
        if workspace is not None and workspace.active_window is not None:
            focus = workspace.active_window.primary_focus();
            if focus is not None:
                self.app.focus.set(focus);
                self.app.invalidate();
                return True;
        return super()._menu_closed();

    def _set_document(self, document):
        result = super()._set_document(document);
        if hasattr(self, "code_window"):
            self.code_window.title = "Code - {}".format(document.path.name if document.path is not None else "Untitled");
        return result;

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
        try: return self._inkey_queue.get_nowait();
        except queue.Empty: return "";

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
            try: self._inkey_queue.get_nowait();
            except queue.Empty: break;
        with self._run_lock:
            self._basic_output_buffer = "";
            self._run_dirty = True;
            self._run_finished = False;
            self._run_error = None;
        self._run_screen.clear();
        self.output_view.set_text("Running...");
        self.status.set("Running. F5 stops; F6 switches windows.");
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
        elif self.basic_interpreter.stopped_by_statement:
            self.output_view.set_text(rendered if rendered else "Program stopped by STOP.");
            self.status.set("BASIC STOP. CONTINUE or F5 resumes from the next statement.");
        elif self.basic_interpreter.stopped_by_request:
            self.output_view.set_text(rendered if rendered else "Program stopped.");
            self.status.set("Run stopped");
        else:
            self.output_view.set_text(rendered if rendered else "Program finished with no text output.");
            self.status.set("Run complete. F5 executes the current editor buffer, saved or not.");
        self._scroll_output_end();
        self.app.invalidate();
        return True;

    def window_targets(self):
        return [self.editor, self.output_view, self.command_view];

    def _direct_output(self, text, end="\n"):
        piece = str(text) + ("" if end == "" else end);
        with self._run_lock:
            self._direct_output_buffer += piece;
        return None;

    def _direct_worker(self, source):
        previous_output = self.basic_interpreter.output_func;
        try:
            self.basic_interpreter.output_func = self._direct_output;
            self.basic_interpreter.execute_direct(source);
        except Exception as exc:
            with self._run_lock:
                self._direct_error = exc;
        finally:
            self.basic_interpreter.output_func = previous_output;
            with self._run_lock:
                self._direct_finished = True;
        return None;

    def _submit_direct_command(self, line, window):
        source = str(line or "").strip();
        if not source:
            return None;
        if self._run_thread is not None and self._run_thread.is_alive():
            window.write_error("A BASIC program is running; stop it before using direct mode.");
            return None;
        if self._direct_thread is not None and self._direct_thread.is_alive():
            window.write_error("A direct command is already running.");
            return None;
        with self._run_lock:
            self._direct_output_buffer = "";
            self._direct_error = None;
            self._direct_finished = False;
        self.status.set("Direct BASIC command running...");
        if not self.app.running:
            self._direct_worker(source);
            self._finish_direct_command();
            return None;
        self._direct_thread = threading.Thread(target=self._direct_worker, args=(source,), name="sumBASIC-direct", daemon=True);
        self._direct_thread.start();
        return None;

    def _finish_direct_command(self):
        with self._run_lock:
            output = self._direct_output_buffer;
            error = self._direct_error;
            self._direct_finished = False;
        if output:
            for line in output.rstrip("\n").splitlines():
                self.command_view.write(line, style="command");
        if error is not None:
            self.command_view.write_error("Error: {}".format(error));
            self.status.set("Direct command error");
        else:
            self.status.set("Direct command complete");
        self._direct_thread = None;
        self.app.invalidate();
        return True;

    def toggle_run(self):
        if self._run_thread is not None and self._run_thread.is_alive():
            return self.stop_program();
        if self._direct_thread is not None and self._direct_thread.is_alive():
            self.basic_interpreter.request_stop();
            self.status.set("Stopping direct BASIC command...");
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
            self.status.set("Program is already running.");
            return True;
        if not self.basic_interpreter.can_continue:
            self.status.set("No BASIC STOP to continue from.");
            return True;
        with self._run_lock:
            self._run_finished = False;
            self._run_error = None;
            self._run_dirty = True;
        self.status.set("Continuing after STOP. F5 stops; F6 switches windows.");
        if not self.app.running:
            self._continue_worker();
            return self._finish_sync();
        self._run_thread = threading.Thread(target=self._continue_worker, name="sumBASIC-continue", daemon=True);
        self._run_thread.start();
        self.app.invalidate();
        return True;

    def run_program(self):
        if self._run_thread is not None and self._run_thread.is_alive():
            self.status.set("Program already running. Press F5 to stop it.");
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
            direct_finished = self._direct_finished;
        if direct_finished:
            self._finish_direct_command();
            dirty = True;
        if finished:
            rendered = self._run_screen.text();
            if error is not None:
                message = "Error: {}".format(error);
                self.output_view.set_text((rendered + "\n" if rendered else "") + message);
                self.status.set("Run error");
            elif self.basic_interpreter.stopped_by_statement:
                self.output_view.set_text(rendered if rendered else "Program stopped by STOP.");
                self.status.set("BASIC STOP. CONTINUE or F5 resumes from the next statement.");
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
