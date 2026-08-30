# SHELL in sumBASIC

`SHELL` bridges a BASIC program to the host operating-system command interpreter.
It deliberately has two forms.

```basic
SHELL "ls -la"
```

The argument is a normal sumBASIC string expression. The command is executed by
the user's host shell and its combined standard output/error is returned through
the BASIC output frontend. In the source IDE that means the **Output** window;
from `sumbasic --run` or `-c` it means the invoking terminal/stdout.

Variables may build commands without introducing a second BASIC-specific command
syntax:

```basic
Directory$ = "/tmp"
Command$ = "ls -la " + Directory$
SHELL Command$
```

Bare `SHELL` means an interactive subshell:

```basic
PRINT "Type exit to return to BASIC"
SHELL
PRINT "Returned from the shell"
```

On sumTUI frontends the application temporarily gives up its alternate screen and
keyboard mode while the shell owns the controlling terminal. When the shell
exits, sumTUI restores the IDE/console and BASIC continues with the next
statement. `sumbasic --run` similarly leaves the cbreak mode used by `INKEY$`
and restores it after the shell exits.

Shell selection is platform aware:

- POSIX/Linux/Termux: `$SHELL`, then `sh` found on `PATH`, then Android
  `/system/bin/sh`, then `/bin/sh`.
- Windows: `%COMSPEC%` (normally `cmd.exe`).

`SHELL "command"` captures output instead of embedding a full terminal emulator.
That makes ordinary commands, scripts and pipelines reliable now. Full-screen
interactive programs are intended to be run through bare `SHELL`, where they
receive the real terminal directly.

Examples:

```basic
SHELL "pwd"
SHELL "ls -lh"
SHELL "python --version"
SHELL "printf 'one\\ntwo\\n'"
```

From Unix command-line mode the same feature composes with sumBASIC itself:

```bash
sumbasic -c 'SHELL "uname -a"'
printf 'SHELL "pwd"\n' | sumbasic
```

A bare `SHELL` requires a controlling terminal. It intentionally fails when the
program is being executed only from a non-interactive pipeline.

<p align=center><b>- oOo -<b></p>
