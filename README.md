# sumBASIC 0.1.0a17

sumBASIC is an educational BASIC frontend for the Sum ecosystem. It keeps classic BASIC ideas available while deliberately modernizing the language so it can also be used to learn contemporary programming concepts.

This alpha makes the language model substantially more explicit: Spectrum-compatible `PI`, literal `DATA`, line-aware `RESTORE`, multidimensional arrays, modern type declarations and containers, `DIM SHARED`, `FOR EACH`, a substantially expanded mathematical core, and a reserved graphics vocabulary whose backend is still pending.

## Installation note for 0.1.0a17

Version 0.1.0a17 adds executable `SHELL` support on top of the movable-window IDE: quoted shell commands are captured into BASIC output, while bare `SHELL` can temporarily hand the real terminal to the user's interactive shell and restore the IDE afterward.

Quick verification:

```bash
sumbasic --version
sumbasic --check examples/music.bas
sumbasic -c 'PLAY "T240O5N10c"'
```

## Language identity

sumBASIC is BASIC, but it is not intended to be a byte-for-byte clone of GW-BASIC, QuickBASIC or Sinclair BASIC. Compatibility is preserved where it remains useful; deliberate differences are documented.

### Classic line numbers inside modern source

sumBASIC deliberately permits classic numeric jump targets inside otherwise free-form source:

```basic
PRINT "before"
GOTO 100
PRINT "skipped"
100 PRINT "target"
PRINT "after"
```

This prints `before`, `target`, and `after`. In a **hybrid** source file the numeric line is a jump label at that physical position; it does not reorder the surrounding unnumbered source. Fully numbered classic programs continue to execute in numeric line-number order. This lets teaching examples mix structured/free-form BASIC with `GOTO`, `GOSUB`, and line-aware `RESTORE` when demonstrating historical control flow.

Free-form code can also use case-insensitive named labels without consuming a line number:

```basic
:LOOP
A$ = INKEY$
IF A$ = CHR$(27) OR A$ = "Q" OR A$ = "q" THEN END
GOTO LOOP
```

A named label may also identify a DATA block for `RESTORE FontData`. A leading `:Name` defines a label; ordinary colons elsewhere remain statement separators, so `BEEP .1, 0: PAUSE 45` is valid.

Comments have three forms:

```basic
# modern Sum comment
' classic BASIC comment
REM classic BASIC comment
```

`#` is therefore **not** a numeric type suffix. File-channel forms such as `OPEN ... AS #1`, `PRINT #1` and `CLOSE #1` remain valid because the lexer recognizes channel `#` in those contexts.

### Type suffixes

sumBASIC uses:

```text
$   STRING
!   INTEGER
&   LONG
%   DOUBLE
```

The named form is the recommended educational spelling:

```basic
DIM Name AS STRING
DIM Count AS INTEGER
DIM Population AS LONG
DIM Ratio AS DOUBLE
```

The suffix form remains concise and unmistakably BASIC:

```basic
Name$ = "Ada"
Count! = 3
Population& = 8000000000
Ratio% = 1.5
```

## PI

`PI` is a built-in immutable language constant. Its value intentionally follows the ZX Spectrum value:

```basic
PRINT PI
```

prints:

```text
3.1415927
```

`PI = 3` is an error.

## Mathematical core

sumBASIC deliberately provides a broader mathematical toolbox than traditional xBase-style languages. Classic BASIC/Spectrum spellings remain available, while modern aliases and additional functions make the same interpreter useful for teaching numerical programming.

Arithmetic operators:

```basic
PRINT 2 + 3 * 4
PRINT 7 / 2
PRINT 7 \ 2
PRINT 7 DIV 2
PRINT 7 MOD 3
PRINT 2 ^ 8
PRINT 1 << 5
PRINT 32 >> 3
PRINT 5 XOR 3
```

Numeric literals include decimal, scientific notation, hexadecimal `&H`, octal `&O`, and binary `&B` forms. Relational/logical operations include `=`, `<>`, `<`, `<=`, `>=`, `>`, `NOT`, `AND`, `OR`, and `XOR`.

The Spectrum family is supported directly: `SIN`, `COS`, `TAN`, `ASN`, `ACS`, `ATN`, `LN`, `EXP`, `INT`, `SQR`, `SGN`, and `ABS`. `LOG(x)` is the common/base-10 logarithm, while `LN(x)` is the natural/Napierian logarithm. The extended family adds roots/powers, hyperbolic functions, arbitrary-base logarithms through `LOGB`/`LOGBASE`, rounding, angle conversion, number theory, combinatorics, special functions, complex numbers, and explicit bitwise functions. Examples:

```basic
PRINT ROOT(27, 3)
PRINT LOG(1000)
PRINT LN(EXP(1))
PRINT LOGB(81, 3)
PRINT ROUND(2.5)
PRINT GCD(18, 24)
PRINT COMB(6, 2)
PRINT BAND(7, 3)
PRINT DEG(ATN(1))
```

`ROUND` uses half-away-from-zero semantics, so `ROUND(2.5)` is `3` and `ROUND(-2.5)` is `-3`. `INT` floors toward negative infinity, while `FIX`/`TRUNC` truncate toward zero. Mixed `DECIMAL` arithmetic promotes ordinary numeric operands to `DECIMAL` rather than silently falling back to binary floating point.

See `docs/MATH.md` for the complete alpha mathematical surface and its semantics.

## Complex numbers

Complex values are first-class numbers rather than a library-side workaround:

```basic
DIM Z AS COMPLEX
Z = COMPLEX(3, 4)
PRINT Z                # 3+4i
PRINT ABS(Z)           # 5
PRINT REAL(Z); IMAG(Z)
PRINT CONJ(Z)
PRINT SQR(COMPLEX(-1, 0))
```

Arithmetic `+`, `-`, `*`, `/` and `^` works directly. `SIN`, `COS`, `TAN`, inverse/hyperbolic functions, `LN`, `LOG`, `LOG2`, `LOGB`, `EXP`, `SQR` and `SQRT` accept complex operands. See `examples/complex.bas` and `docs/MATH.md`.

## Clock functions and retro clock demo

`TIME$` returns the local wall-clock time as `HH:MM:SS`. `TIMER` returns seconds since local midnight, including a fractional part when the host clock provides it. `PAUSE n` uses the Spectrum convention of 50 frames per second, so `PAUSE 50` waits approximately one second.

`examples/retro_clock.bas` loads a 5x7 digit font once from `DATA` into `DIM SHARED` multidimensional arrays, then renders `TIME$` in large block characters with `LOCATE`/`PRINT`. It runs continuously and exits when Escape, `Q`, or `q` is pressed. Each update plays `BEEP .1, 0`; because `BEEP` is blocking and Spectrum `PAUSE` is measured at 50 ticks per second, `PAUSE 45` contributes 0.9 seconds for an approximately one-second clock cadence. The same immediate `INKEY$` exit works both inside the IDE and with `sumbasic --run examples/retro_clock.bas`; on an interactive terminal no Enter key is required.

## IDE execution

Opening a BASIC source file uses the sumBASIC-aware sumTUI IDE. Its workspace contains three independent default windows: **Code**, **Output**, and **Command**. They can overlap like a classic FoxPro-style desktop: drag a title border to move a window, use `Alt+Arrow` for keyboard movement, F11 to maximize/restore, Ctrl+F4 to close the active window, and the **Window** menu to activate or reopen any default window. `F6` cycles Code → Output → Command.

`F5` is a **Run/Stop toggle** for the current editor buffer, including unsaved edits, without silently saving or modifying the source file. Execution is asynchronous with respect to the IDE: the editor/event loop remains responsive while BASIC runs, and output is streamed into Output. `CLS` and `LOCATE` are interpreted by the IDE run screen, so terminal-style programs such as the retro clock can update in place rather than dumping raw ANSI escape sequences. While an F5 program is running, printable keys and Escape are delivered to its `INKEY$` queue instead of editing the source.

The floating **Command** window executes BASIC directly in the same interpreter state. Assignments persist between commands, so `A! = 10` followed by `PRINT A!` prints `10`; sound/music commands can be tried interactively, and `CONTINUE`/`CONT` resumes a program suspended by BASIC `STOP`. Direct commands do not require changing or saving the source buffer.

```text
F2        Save
F5        Run / Stop current BASIC buffer
F6        Next Window (Code / Output / Command)
F11       Maximize / Restore active window
Ctrl+F4   Close active window
F9        Menu
F10       Exit
```

If execution reaches the BASIC statement `STOP`, it is **suspended**, not aborted. The next F5 continues from the statement after `STOP`. Pressing F5 while a program is actively running is a user abort and intentionally does not create a `CONTINUE` point.

For direct command-line execution, `--run` places an interactive POSIX terminal in cbreak mode while BASIC is running so `INKEY$` receives keystrokes immediately rather than waiting for a newline. The original terminal settings are restored on normal exit and exceptions. If a BASIC `INPUT` statement is encountered, sumBASIC temporarily restores ordinary cooked/echo mode for line editing and then returns to immediate-key mode. Windows uses the corresponding non-blocking console-key API.

Programs that require interactive `INPUT` should currently be run from the sumBASIC console; source-IDE modal input is a separate frontend milestone.

## Command-line source and Unix pipelines

sumBASIC can be used as a normal Unix-language interpreter as well as through the IDE and interactive console:

```bash
echo 'PRINT "casa!"' | sumbasic
sumbasic -c 'PRINT "la casa roja"'
sumbasic --command 'BEEP 1, 1'
```

With no filename, a non-interactive standard input is treated as BASIC source and executed. `-c` and `--command` execute the supplied source directly without opening the IDE. Multi-statement BASIC source may use colons or an embedded newline in the command string.

## SHELL

`SHELL` uses the host command interpreter without turning sumBASIC into a shell parser. A string expression runs one command and captures both standard output and standard error:

```basic
SHELL "ls -la"
Cmd$ = "pwd"
SHELL Cmd$
```

From the source IDE the captured text is routed to the **Output** window even when `SHELL` was entered from the floating **Command** window. In console/`--run` mode it is written to the current terminal output. The command is executed through the user's configured shell (`$SHELL` on POSIX/Termux, `%COMSPEC%` on Windows); POSIX fallback discovery also covers `sh` and Android's `/system/bin/sh`.

Bare `SHELL` starts an interactive subshell:

```basic
PRINT "Entering the system shell"
SHELL
PRINT "Back in BASIC"
```

In the IDE and other sumTUI frontends, sumTUI temporarily leaves its alternate screen and restores normal terminal input before launching the shell. Type `exit` (or the shell's normal EOF command) to return to the same BASIC session and redraw the IDE. In `sumbasic --run`, the cbreak mode used by `INKEY$` is likewise suspended while the shell owns the terminal and restored afterward. A bare `SHELL` from a non-interactive pipe has no controlling terminal and reports an error instead.

`SHELL "command"` is stoppable with the IDE's F5 Run/Stop mechanism when it belongs to a running BASIC program; direct-mode shell commands also honor the same stop request. See `docs/SHELL.md` and `examples/shell.bas`.

See `examples/command_line.sh`.

## BEEP, SOUND and PLAY

sumBASIC deliberately keeps the ZX Spectrum and GW-BASIC sound models distinct:

```basic
BEEP 1, 0
SOUND 262, 18.2
```

`BEEP duration, pitch` takes seconds followed by semitones relative to Middle C (`0` ≈ `261.625565 Hz`) and blocks until the tone ends. `SOUND frequency, duration` takes Hertz followed by approximately 18.2 PC timer ticks per second, accepts the historical `37..32767` Hz range, and plays in the background while BASIC execution continues. SOUND still uses the same frequency synthesis as BEEP, but from 0.1.0a15 BEEP and SOUND have independent buses so one need not serialize the other.

Music is available through both historical string languages without ambiguous dialect guessing:

```basic
PLAY "T180O5N3cdefgabC"          # alias of ZXPLAY
ZXPLAY A$, B$, C$                 # up to three Spectrum-style voices
PLAY BACKGROUND "T180O5N3cdefg"
GWPLAY "MB T180 O4 L8 CDEFG"     # Microsoft/GW-BASIC MML
```

`PLAY` is deliberately an alias of `ZXPLAY`; `GWPLAY` names the Microsoft dialect explicitly. Foreground/background music uses a separate music bus, so background PLAY can coexist with BEEP and SOUND. See `docs/AUDIO.md`, `docs/PLAY.md`, `examples/sound.bas`, and `examples/music.bas`.

## DATA, READ and RESTORE

`DATA` contains literal program data; it is not evaluated as a deferred expression.

```basic
10 DATA "first", 10
20 DATA "second", 20
30 READ A$, A!
40 RESTORE 20
50 READ B$, B!
```

`RESTORE` without an argument returns to the beginning. `RESTORE n` moves to the first `DATA` statement at or after program line `n`.

This is intended to support classic embedded data such as lookup tables, sprites and retro bitmap fonts. A program can load those values once at startup into a `DIM SHARED` array or dictionary and then reuse the in-memory structure throughout execution.

## Classic multidimensional arrays

Classic arrays now support multiple dimensions:

```basic
DIM A$(5, 7, 3, 8)
A$(2, 4, 1, 6) = "X"
PRINT A$(2, 4, 1, 6)
```

Classic bounds are retained. With the default:

```basic
OPTION BASE 0
```

`DIM A(5)` means bounds `0 TO 5`. For an exact five-element one-based dimension, write either:

```basic
OPTION BASE 1
DIM A(5)
```

or make the bounds explicit:

```basic
DIM A(1 TO 5)
```

Explicit bounds work per dimension:

```basic
DIM Page$(1 TO 5, 1 TO 7, 1 TO 3, 1 TO 8)
```

Bounds can be inspected with:

```basic
PRINT LBOUND(Page$, 1)
PRINT UBOUND(Page$, 4)
```

`REDIM` and initial `REDIM PRESERVE` are also available.

## DIM SHARED and modern containers

`SHARED` marks global program state intended to remain visible to future structured `SUB`/`FUNCTION` scopes:

```basic
DIM SHARED Font AS DICT
```

Modern containers are first-class language types:

```basic
DIM Names AS LIST
DIM Font AS DICT
DIM Seen AS SET
DIM Point AS TUPLE
```

Literals and indexing are supported:

```basic
Names = ["Ada", "Linus", "Grace"]
Font = {"A": [4, 10, 17, 17, 31, 17, 17]}
Point = (10, 20)

PRINT Names[0]
PRINT Font["A"][4]
```

Common collection methods are available:

```basic
Names.APPEND("Ken")
Seen.ADD("Ada")
PRINT Font.HASKEY("A")
```

and collections can be iterated without exposing indexes unnecessarily:

```basic
FOR EACH Name$ IN Names
PRINT Name$
NEXT Name$
```

The type vocabulary currently includes `BOOLEAN`, `INTEGER`, `LONG`, `SINGLE`, `DOUBLE`, `DECIMAL`, `COMPLEX`, `STRING`, `BYTES`, `ANY`, `LIST`, `DICT`, `SET` and `TUPLE`. Typed generic forms such as `LIST[STRING]` are reserved by the type parser; deeper element-type enforcement will evolve in later alphas.

## Interactive INPUT prompts

The separator after an `INPUT` prompt is meaningful:

```basic
INPUT "texto"; Value$
```

shows `texto? ` followed by the live input cursor, while:

```basic
INPUT "texto", Value$
```

shows `texto` directly followed by the input cursor. With no explicit prompt:

```basic
INPUT Value$
```

shows `? ` followed by the cursor. The cursor itself belongs to the active frontend and is not a literal underscore emitted by the language.

## Graphics vocabulary

The Spectrum-inspired graphics vocabulary is now reserved even though the shared Sum Machine graphics backend is not ready yet. Statements such as:

```basic
SCREEN 1
CIRCLE 100, 100, 40
RECTANGLE 20, 20, 180, 120
PLOT 10, 10
```

are recognized and currently print, for example:

```text
CIRCLE: NOT IMPLEMENTED YET
```

rather than being rejected as unknown syntax.

The reserved family includes `SCREEN`, `PLOT`, `DRAW`, `LINE`, `CIRCLE`, `INK`, `PAPER`, `FLASH`, `BRIGHT`, `INVERSE`, `OVER`, `BORDER`, `UDG`, `DISPLAY`, `SHOW`, `RECTANGLE`, `POLYGON`, `ELLIPSE` and the existing screen-buffer commands. `POINT`, `SCREEN$` and `ATTR` are registered as graphical function stubs.

## File channels

Classic sequential access remains available:

```basic
OPEN "people.txt" FOR OUTPUT AS #1
WRITE #1, "Ada", 37
CLOSE #1

OPEN "people.txt" FOR INPUT AS #A
INPUT #A, name$, age!
CLOSE #A
PRINT name$; " "; age!
```

`A..J` are aliases for channels `1..10`, matching the work-area numbering convention used by xBase `SELECT`.

The fopen-like form is also accepted:

```basic
OPEN "notes.txt" MODE "r" AS #1
OPEN "output.txt" MODE "w" AS #2
OPEN "events.log" MODE "a" AS #3
OPEN "data.bin" MODE "r+b" AS #4
```

Random fixed-record access, `FIELD`, `GET`, `PUT`, standard streams, pipelines and the initial sumX database bridge from 0.1.0a2 remain available.

## Super-extended ASC table

The supplied `asc_h.py` is treated as a shared Sum symbol catalogue. Its existing BASIC block begins at `ASC[512]` with `RND`, `INKEY$`, `PI`, etc. Existing positions are not renumbered.

The companion `extras/asc_h-sumbasic-0.1.0a17.py` appends the newer sumBASIC vocabulary starting at index `2990`, after the existing 2990 entries. This preserves every historical code while still giving `SUB`, `FUNCTION`, `CALL`, `SHARED`, the modern types, structured-loop words and newer runtime vocabulary stable ASC positions.

The parser does not depend on those numeric positions; they remain a cross-project symbol space rather than parser opcodes.

## Still pending

Structured `SUB`/`FUNCTION` execution and `CALL ... WITH ...` are reserved design work for the next procedure-scope milestone. The current `DIM SHARED` implementation establishes the global-state semantics those procedures will use.

Also pending: full graphics rendering, virtual `PEEK`/`POKE` and port I/O, exact AY noise/envelope synthesis and indefinite Spectrum PLAY phrase repetition, events/errors beyond current control flow, SumIR emission, and Python/native compilation.

## Usage

```bash
sumbasic
sumbasic --plain
sumbasic program.bas
sumbasic --run program.bas
sumbasic --check program.bas
```

## Tests

The alpha includes 84 regression tests. The mathematical suite covers arithmetic and integer division, powers/modulo, shifts and bitwise operations, comparisons/logical operations, Spectrum transcendental functions, extended logarithms and roots, rounding, number theory, combinatorics, special functions, decimal promotion, and the `INPUT` prompt-separator rules.


### STOP and CONTINUE

`STOP` is deliberately different from `END`. It returns control to the environment but keeps the current BASIC runtime resumable. `CONTINUE` resumes at the statement immediately following the `STOP`:

```basic
A! = 1
PRINT A!
STOP
A! = A! + 1
PRINT A!
END
```

After `STOP`, variables, arrays, loop/GOSUB state, and the DATA pointer remain intact. In the command console type `CONTINUE`; in the source IDE F5 continues when the previous run is suspended by a BASIC `STOP`. `END`, `SYSTEM`, or an IDE F5 user-stop terminate the run and do not leave a continuation point.

## License

GPL-2.0-or-later.

<p align=center><b>- oOo -<b></p>
