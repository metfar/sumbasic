#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#pylint:disable=W0301
#  
#  Copyright 2018- William Martinez Bas <metfar@gmail.com>
#  
import argparse;
import sys;
from pathlib import Path;

from . import __version__;
from .console import SumBasicConsoleApp;
from .ide import SumBasicIDE;
from .interpreter import BasicInterpreter;
from .terminal_input import TerminalInput;


def _plain_repl(interpreter):
    print("sumBASIC {} - Ready.".format(__version__));
    while True:
        try: line = input("> ");
        except (EOFError, KeyboardInterrupt): print(); return 0;
        if line.strip().upper() in ("QUIT", "SYSTEM", "EXIT"): return 0;
        try: interpreter.execute_immediate(line);
        except Exception as exc: print("Error: {}".format(exc), file=sys.stderr);


def _edit_file(path):
    return int(SumBasicIDE(path=path).run() or 0);


def build_parser():
    parser = argparse.ArgumentParser(prog="sumbasic", description="Educational console BASIC for the Sum ecosystem.");
    parser.add_argument("file", nargs="?", help="BASIC source file; opens in the sumBASIC IDE unless --run/--check is used");
    parser.add_argument("--run", action="store_true", help="run a BASIC program");
    parser.add_argument("--check", action="store_true", help="parse/load the program without running it");
    parser.add_argument("--plain", action="store_true", help="use the plain terminal REPL instead of sumTUI");
    parser.add_argument("--version", action="store_true", help="show version");
    return parser;


def main(argv=None):
    args = build_parser().parse_args(argv);
    if args.version:
        print("sumBASIC {}".format(__version__)); return 0;
    if args.file and not (args.run or args.check): return _edit_file(args.file);
    interpreter = BasicInterpreter();
    if args.file:
        interpreter.program.load_file(Path(args.file));
        if args.check:
            interpreter._build_execution(); print("{}: OK".format(args.file)); return 0;
        if args.run:
            with TerminalInput() as terminal:
                interpreter.input_func = terminal.input;
                interpreter.inkey_func = terminal.inkey;
                interpreter.run();
                # SOUND is non-blocking while BASIC executes, but a one-shot CLI
                # process must stay alive long enough for its queued final notes.
                interpreter.tone_player.wait_for_background();
            return 0;
    if args.plain: return _plain_repl(interpreter);
    return int(SumBasicConsoleApp(interpreter=interpreter).run() or 0);
