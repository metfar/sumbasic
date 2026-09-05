#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#pylint:disable=W0301
#  
#  Copyright 2018- William Martinez Bas <metfar@gmail.com>
#  
import argparse;
import sys;
from pathlib import Path;

from sumui import add_backend_arguments, backend_from_args;
from sumtui import TerminalTextScreen;

from . import __version__;
from .console import SumBasicConsoleApp;
from .interpreter import BasicError, BasicInterpreter;
from .graphics import GraphicsBackendError, SumGuiGraphicsHandler;
from .shell import run_interactive_shell;
from .terminal_input import TerminalInput;


def _stdout_output(text="", end="\n"):
    print(str(text), end=end, flush=True);


def _plain_repl(interpreter):
    print("sumBASIC {} - Ready.".format(__version__));
    while True:
        try: line = input("> ");
        except (EOFError, KeyboardInterrupt): print(); return 0;
        if line.strip().upper() in ("QUIT", "SYSTEM", "EXIT"): return 0;
        try: interpreter.execute_immediate(line);
        except Exception as exc: print("Error: {}".format(exc), file=sys.stderr);




def _source_uses_graphics(path):
    """Return True when a BASIC source owns a pixel graphics display.

    A GUI graphics program must not be executed inside the same Pygame display
    that presents sumIDE: Pygame exposes one process-global display surface.
    Standalone graphical --run therefore owns the display directly, while
    text-only GUI programs continue to use the common IDE/application shell.
    """;
    try:
        source=Path(path).read_text(encoding="utf-8",errors="replace");
    except OSError:
        return False;
    import re;
    pattern=re.compile(r"^\s*(?:DISPLAY\b|SCREEN\s+(?!0(?:\s|$))|PLOT\b|CIRCLE\b|RECTANGLE\b|ARC\b|ELLIPSE\b|PAINT\b|FILL\b|CHART\b|TABLE\b|OUTTEXTXY\b|BSAVE\s+.+,\s*SCREEN\b)",re.I|re.M);
    return bool(pattern.search(source));

def _edit_file(path=None, backend="tui", run=False):
    from sumide.app import main_basic;
    argv = [] if path is None else [str(path)];
    if run:
        argv.insert(0, "--run");
    if backend == "gui":
        argv.insert(0, "--gui");
    return int(main_basic(argv) or 0);


def _finish_audio(interpreter):
    interpreter.audio.wait_for_background();
    return None;


def _finish_graphics(interpreter, wait=False):
    handler = getattr(getattr(interpreter, "graphics", None), "handler", None);
    finish = getattr(handler, "finish", None);
    if finish is not None:
        finish(wait=bool(wait));
    return None;


def _run_loaded(interpreter, interactive_terminal=False):
    try:
        if interactive_terminal:
            with TerminalInput() as terminal:
                terminal.pointer_callback = interpreter.queue_pointer;
                interpreter.input_func = terminal.input;
                interpreter.inkey_func = terminal.inkey;
                interpreter.shell_interactive_func = lambda: terminal.run_external(run_interactive_shell);
                interpreter.run();
                _finish_audio(interpreter);
            _finish_graphics(interpreter, wait=True);
            return 0;
        interpreter.run();
        _finish_audio(interpreter);
        _finish_graphics(interpreter, wait=False);
        return 0;
    except (BasicError, GraphicsBackendError) as exc:
        print("sumBASIC error: {}".format(exc), file=sys.stderr);
        return 1;




def _check_loaded(interpreter, label):
    try:
        interpreter.check();
    except BasicError as exc:
        print("{}: ERROR: {}".format(label, exc), file=sys.stderr);
        return 1;
    print("{}: OK".format(label));
    return 0;

def build_parser():
    parser = argparse.ArgumentParser(prog="sumbasic", description="Educational console BASIC for the Sum ecosystem.");
    parser.add_argument("file", nargs="?", help="BASIC source file; opens in the sumBASIC IDE unless --run/--check is used");
    parser.add_argument("-c", "--command", dest="command", help="execute BASIC source supplied directly on the command line");
    parser.add_argument("--run", action="store_true", help="run a BASIC program");
    parser.add_argument("--check", action="store_true", help="validate program structure and recognized statements without running it");
    parser.add_argument("--plain", action="store_true", help="use the plain terminal REPL instead of the Sum UI");
    add_backend_arguments(parser);
    parser.add_argument("--version", action="store_true", help="show version");
    return parser;


def main(argv=None):
    parser = build_parser();
    args = parser.parse_args(argv);
    ui_backend = backend_from_args(args);
    if args.plain and ui_backend == "gui":
        parser.error("--plain and --gui are mutually exclusive");
    if args.version:
        print("sumBASIC {}".format(__version__)); return 0;
    if args.file and args.command is not None:
        parser.error("a source file and --command/-c cannot be used together");
    if args.file and not (args.run or args.check): return _edit_file(args.file, backend=ui_backend);
    if args.file and args.run and ui_backend == "gui" and not _source_uses_graphics(args.file): return _edit_file(args.file, backend="gui", run=True);
    if not args.file and args.command is None and not args.run and not args.check and not args.plain and (ui_backend == "gui" or bool(getattr(sys.stdin, "isatty", lambda: False)())):
        return _edit_file(None, backend=ui_backend);
    interpreter = BasicInterpreter(output_func=_stdout_output, graphics_handler=SumGuiGraphicsHandler(), text_screen=TerminalTextScreen());
    if args.command is not None:
        interpreter.program.load_text(str(args.command) + ("" if str(args.command).endswith("\n") else "\n"));
        if args.check: return _check_loaded(interpreter, "command");
        return _run_loaded(interpreter, interactive_terminal=bool(getattr(sys.stdin, "isatty", lambda: False)()));
    if args.file:
        interpreter.program.load_file(Path(args.file));
        if args.check: return _check_loaded(interpreter, str(args.file));
        if args.run:
            return _run_loaded(interpreter, interactive_terminal=bool(getattr(sys.stdin, "isatty", lambda: False)()));
    if not args.plain and not bool(getattr(sys.stdin, "isatty", lambda: False)()):
        source = sys.stdin.read();
        if source.strip():
            interpreter.program.load_text(source);
            if args.check: return _check_loaded(interpreter, "stdin");
            return _run_loaded(interpreter, interactive_terminal=False);
    if args.plain: return _plain_repl(interpreter);
    return int(SumBasicConsoleApp(interpreter=interpreter).run(backend=ui_backend) or 0);
