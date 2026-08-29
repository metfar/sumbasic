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
from sumtui import FunctionAction, Menu, MenuItem, Panel, TextView, VBox;
from sumtui.tools.edit import EditApp;

from .interpreter import BasicError, BasicInterpreter;


class SumBasicIDE(EditApp):
    """sumTUI source editor with sumBASIC-aware F5 execution."""
    def __init__(self, path=None, theme=None, interpreter=None, **kwargs):
        self._basic_output_buffer = "";
        self.basic_interpreter = interpreter;
        super().__init__(path=path, theme=theme, **kwargs);
        self.output_view = TextView("Ready. Press F5 to run the current editor buffer.");
        self.output_panel = Panel(self.output_view, title="Run output", content_style="viewer");
        body = VBox(self.panel, self.output_panel, self.status, self.bar, sizes=[None, 8, 1, 1]);
        self.desktop.body = body;
        self.app.set_root(self.desktop);
        if self.basic_interpreter is None:
            self.basic_interpreter = BasicInterpreter(input_func=self._ide_input, output_func=self._basic_output);
        else:
            self.basic_interpreter.output_func = self._basic_output;
        self._update_status();

    def _register_keybindings(self):
        super()._register_keybindings();
        self.keys.register("basic.run", "Run BASIC", ["f5"], context="editor", callback=self.run_program);
        return self.keys;

    def _make_function_bar(self):
        bar = super()._make_function_bar();
        key = self.keys.primary("basic.run");
        if key:
            insert_at = min(2, len(bar.actions));
            bar.actions.insert(insert_at, FunctionAction(key, "Run", None));
        return bar;

    def _menus(self):
        menus = super()._menus();
        menus.append(Menu("Run", [MenuItem("Run current buffer", self.run_program, self._ks("basic.run"))]));
        return menus;

    def _basic_output(self, text, end="\n"):
        self._basic_output_buffer += str(text) + ("" if end == "" else end);
        return None;

    def _ide_input(self, prompt=""):
        raise BasicError("Interactive INPUT from the source IDE is not implemented yet; run this program in the sumBASIC console for interactive input");

    def run_program(self):
        self._basic_output_buffer = "";
        self.output_view.set_text("");
        try:
            self.basic_interpreter.program.load_text(self.editor.text);
            self.basic_interpreter.run();
            rendered = self._basic_output_buffer.rstrip("\n");
            self.output_view.set_text(rendered if rendered else "Program finished with no text output.");
            self.status.set("Run complete. F5 executes the current editor buffer, saved or not.");
        except Exception as exc:
            rendered = self._basic_output_buffer.rstrip("\n");
            message = "Error: {}".format(exc);
            self.output_view.set_text((rendered + "\n" if rendered else "") + message);
            self.status.set("Run error");
        self.app.invalidate();
        return True;
