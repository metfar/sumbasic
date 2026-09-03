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

from sumui import GraphicsCommand, GraphicsMode, GraphicsProgram, ImageSpec, basic_mode, display_mode, modern_mode, screen_mode, spectrum_mode;


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

    def text_mode(self):
        had_mode = self.mode is not None;
        self.mode = None;
        self.commands = [];
        if had_mode and self.handler is not None:
            self.handler(GraphicsCommand("close"));
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
        return self.set_mode(basic_mode(int(width), int(height), scaling=scaling, refresh="auto", pages=1, active_page=0, visible_page=0));

    def historical_screen(self, number, colorswitch=0, active_page=0, visible_page=0):
        return self.set_mode(screen_mode(int(number), colorswitch=colorswitch, active_page=active_page, visible_page=visible_page));

    def display(self, width, height, color_spec=32, refresh="auto", pages=1, active_page=0, visible_page=0):
        return self.set_mode(display_mode(width, height, color_spec=color_spec, refresh=refresh, pages=pages, active_page=active_page, visible_page=visible_page, palette_profile="basic"));

    def set_active_page(self, page):
        return self.emit("active_page", (int(page),));

    def set_visible_page(self, page):
        return self.emit("visible_page", (int(page),));

    def set_refresh(self, mode):
        return self.emit("refresh_mode", (str(mode).lower(),));

    def update(self):
        return self.emit("update");

    def copy_page(self, source, destination):
        return self.emit("copy_page", (int(source), int(destination)));

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

    def query(self, operation, arguments=(), **options):
        self.ensure_mode();
        if self.handler is None:
            raise GraphicsBackendError("graphics query requires an active graphical backend");
        command = GraphicsCommand(operation, tuple(arguments or ()), tuple(options.items()));
        return self.handler(command);

    def capture(self, x=0, y=0, width=None, height=None):
        mode = self.ensure_mode();
        width = mode.logical_width - int(x) if width is None else int(width);
        height = mode.logical_height - int(y) if height is None else int(height);
        image = self.query("capture", (int(x), int(y), width, height));
        if not isinstance(image, ImageSpec):
            raise GraphicsBackendError("graphics backend did not return a portable image");
        return image;

    def save_image(self, filename, image=None):
        return self.query("save_image", (str(filename),) if image is None else (str(filename), image));

    def load_image(self, filename):
        image = self.query("load_image", (str(filename),));
        if not isinstance(image, ImageSpec):
            raise GraphicsBackendError("graphics backend did not return a portable image");
        return image;

    def clear(self, color=None):
        options = {} if color is None else {"color": color};
        return self.emit("clear", (), **options);

    def service(self, seconds=0.0):
        callback = getattr(self.handler, "service", None) if self.handler is not None else None;
        if callback is None:
            return False;
        return bool(callback(float(seconds)));

    def program(self):
        mode = self.ensure_mode();
        return GraphicsProgram(mode, tuple(self.commands), background=self.background);


class GraphicsBackendError(RuntimeError):
    """Raised when a requested graphics backend cannot be started.""";


class SumGuiGraphicsHandler:
    """Lazy sumGUI bridge used by the BASIC CLI and IDE.

    Importing ``sumbasic`` stays Pygame-free until the first graphics command.
    The concrete renderer remains backend-neutral from the interpreter's point
    of view: it receives only ``GraphicsMode`` and ``GraphicsCommand`` values.
    """;
    def __init__(self, title="sumBASIC graphics", fit_display=True):
        self.title = str(title);
        self.fit_display = bool(fit_display);
        self.window = None;

    def _ensure_window(self):
        if self.window is not None:
            return self.window;
        try:
            from sumgui.graphics import GraphicsWindow;
        except (ImportError, ModuleNotFoundError) as exc:
            raise GraphicsBackendError("sumBASIC graphics require sumGUI/Pygame; install the graphics extra with: pip install 'sumbasic[graphics]'") from exc;
        self.window = GraphicsWindow(title=self.title, fit_display=self.fit_display);
        return self.window;

    def __call__(self, item):
        return self._ensure_window().handle(item);

    def finish(self, wait=False):
        if self.window is None:
            return 0;
        return self.window.finish(wait=wait);

    def service(self, seconds=0.0):
        if self.window is None:
            return False;
        return bool(self.window.service(float(seconds)));

    def close(self):
        if self.window is not None:
            self.window.close();
        return None;
