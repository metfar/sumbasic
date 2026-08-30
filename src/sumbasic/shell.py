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
import os;
import shutil;
import subprocess;
import sys;


class ShellExecutionError(RuntimeError):
    pass;


def preferred_shell():
    if os.name == "nt":
        return os.environ.get("COMSPEC") or "cmd.exe";
    configured = os.environ.get("SHELL");
    if configured:
        return configured;
    discovered = shutil.which("sh");
    if discovered:
        return discovered;
    if os.path.exists("/system/bin/sh"):
        return "/system/bin/sh";
    return "/bin/sh";


def command_argv(command, shell=None):
    executable = str(shell or preferred_shell());
    if os.name == "nt":
        return [executable, "/c", str(command)];
    return [executable, "-lc", str(command)];


def run_shell_command(command, stop_event=None, shell=None):
    """Run one command through the user's shell and capture combined output.""";
    try:
        process = subprocess.Popen(
            command_argv(command, shell=shell),
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            errors="replace",
        );
    except OSError as exc:
        raise ShellExecutionError("cannot start shell: {}".format(exc)) from exc;
    while True:
        try:
            output, _unused = process.communicate(timeout=0.05);
            return int(process.returncode or 0), output or "";
        except subprocess.TimeoutExpired:
            if stop_event is None or not stop_event.is_set():
                continue;
            process.terminate();
            try:
                output, _unused = process.communicate(timeout=1.0);
            except subprocess.TimeoutExpired:
                process.kill();
                output, _unused = process.communicate();
            return int(process.returncode or 1), output or "";


def run_interactive_shell(shell=None):
    """Give the current controlling terminal to an interactive system shell.""";
    if not bool(getattr(sys.stdin, "isatty", lambda: False)()) or not bool(getattr(sys.stdout, "isatty", lambda: False)()):
        raise ShellExecutionError("interactive SHELL requires a terminal");
    executable = str(shell or preferred_shell());
    try:
        return int(subprocess.call([executable]));
    except OSError as exc:
        raise ShellExecutionError("cannot start shell: {}".format(exc)) from exc;
