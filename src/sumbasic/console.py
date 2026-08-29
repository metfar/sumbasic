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
from sumtui import Application, CommandWindow, FunctionBar, Menu, MenuBar, MenuDesktop, MenuItem, Panel, Separator, StatusBar, VBox;
from . import __version__;
from .interpreter import BasicInterpreter;


class SumBasicConsoleApp:
    def __init__(self, interpreter=None, theme=None):
        self.interpreter = interpreter or BasicInterpreter(output_func=self._output);
        self.app = Application("sumBASIC", theme=theme);
        self.command = CommandWindow(prompt="> ", on_submit=self._submit);
        self.status = StatusBar("Ready.");
        self.command.write("sumBASIC {} - educational BASIC".format(__version__));
        self.command.write("Numbered lines are stored. RUN, LIST, NEW, LOAD, SAVE, RENUM. F10 exits.");
        self.menu = MenuBar([
            Menu("File", [MenuItem("New", lambda: self._run_command("NEW")), MenuItem("Exit", self.app.stop, "F10")]),
            Menu("Run", [MenuItem("Run", lambda: self._run_command("RUN"), "F5"), MenuItem("List", lambda: self._run_command("LIST"))]),
            Menu("Help", [MenuItem("About", self._about, "F1")]),
        ]);
        self.bar = FunctionBar([("f1", "Help", self._about), ("f5", "Run", lambda: self._run_command("RUN")), ("f9", "Menu", lambda: self.desktop.open_menu(0)), ("f10", "Exit", self.app.stop)]);
        self.bar.install(self.app);
        body = VBox(Panel(self.command, title="sumBASIC Command", content_style="command"), self.status, self.bar, sizes=[None, 1, 1]);
        self.desktop = MenuDesktop(self.menu, body);
        self.app.set_root(self.desktop);
        self.app.focus.set(self.command);

    def _output(self, text, end="\n"):
        value = str(text) + ("" if end == "" else "\n");
        for line in value.splitlines(): self.command.write(line);
        if end == "" and value and not value.endswith("\n"): self.command.write(value);

    def _submit(self, line, window):
        try:
            self.interpreter.execute_immediate(line);
            self.status.set_text("Ready. {} line(s)".format(len(self.interpreter.program.source_lines())));
        except Exception as exc:
            self.command.write_error("Error: {}".format(exc));
            self.status.set_text("Error");
        self.app.invalidate();
        return None;

    def _run_command(self, command):
        return self._submit(command, self.command);

    def _about(self):
        self.command.write("sumBASIC {} | console BASIC frontend for the Sum ecosystem".format(__version__));
        return True;

    def run(self):
        return self.app.run();
