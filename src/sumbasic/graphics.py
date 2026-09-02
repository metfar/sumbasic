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

from sumui import GraphicsCommand, GraphicsMode, GraphicsProgram, modern_mode, spectrum_mode;


class GraphicsRuntime:
    """Backend-neutral BASIC graphics command stream.

    Language semantics live in sumBASIC; drawing lives in a Sum UI backend.
    A handler, when installed, receives either a ``GraphicsMode`` when SCREEN
    changes the logical display or a ``GraphicsCommand`` for a drawing op.
    """
    def __init__(self, handler=None):
        self.handler = handler if callable(handler) else None;
        self.mode = None;
        self.commands = [];
        self.background = (0, 0, 0, 255);

    def set_handler(self, handler):
        self.handler = handler if callable(handler) else None;
        return self.handler;

    def reset(self):
        self.mode = None;
        self.commands = [];
        return self;

    def set_mode(self, mode):
        if not isinstance(mode, GraphicsMode):
            mode = GraphicsMode.from_dict(mode);
        self.mode = mode;
        self.commands = [];
        if self.handler is not None:
            self.handler(mode);
        return mode;

    def modern(self, width, height, scaling="fit"):
        return self.set_mode(modern_mode(int(width), int(height), scaling=scaling));

    def spectrum(self):
        return self.set_mode(spectrum_mode());

    def ensure_mode(self):
        if self.mode is None:
            self.modern(640, 480);
        return self.mode;

    def emit(self, operation, arguments=(), **options):
        self.ensure_mode();
        command = GraphicsCommand(operation, tuple(arguments or ()), tuple(options.items()));
        self.commands.append(command);
        if self.handler is not None:
            self.handler(command);
        return command;

    def clear(self, color=None):
        options = {} if color is None else {"color": color};
        return self.emit("clear", (), **options);

    def program(self):
        mode = self.ensure_mode();
        return GraphicsProgram(mode, tuple(self.commands), background=self.background);
