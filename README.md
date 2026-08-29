# sumBASIC 0.1.0a13

sumBASIC is an educational BASIC frontend for the Sum ecosystem. It keeps classic BASIC ideas available while deliberately modernizing the language so it can also be used to learn contemporary programming concepts.

This alpha makes the language model substantially more explicit: Spectrum-compatible `PI`, literal `DATA`, line-aware `RESTORE`, multidimensional arrays, modern type declarations and containers, `DIM SHARED`, `FOR EACH`, a substantially expanded mathematical core, and a reserved graphics vocabulary whose backend is still pending.

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

Opening a BASIC source file uses the sumBASIC-aware sumTUI IDE. `F5` is a **Run/Stop toggle** for the current editor buffer, including unsaved edits, without silently saving or modifying the source file. Execution is asynchronous with respect to the IDE: the editor/event loop remains responsive while BASIC runs, and output is streamed into the run pane as it is produced. `CLS` and `LOCATE` are interpreted by the IDE run screen, so terminal-style programs such as the retro clock can update in place rather than dumping raw ANSI escape sequences. While an F5 program is running, printable keys and Escape are delivered to its `INKEY$` queue instead of editing the source. `F6` changes focus between the Editor and Output windows.

```text
F2        Save
F5        Run / Stop current BASIC buffer
F6        Next Window (Editor / Output)
F9        Menu
F10       Exit
```

If execution reaches the BASIC statement `STOP`, it is **suspended**, not aborted. The next F5 continues from the statement after `STOP`. Pressing F5 while a program is actively running is a user abort and intentionally does not create a `CONTINUE` point.

For direct command-line execution, `--run` places an interactive POSIX terminal in cbreak mode while BASIC is running so `INKEY$` receives keystrokes immediately rather than waiting for a newline. The original terminal settings are restored on normal exit and exceptions. If a BASIC `INPUT` statement is encountered, sumBASIC temporarily restores ordinary cooked/echo mode for line editing and then returns to immediate-key mode. Windows uses the corresponding non-blocking console-key API.

Programs that require interactive `INPUT` should currently be run from the sumBASIC console; source-IDE modal input is a separate frontend milestone.

## BEEP and SOUND

sumBASIC deliberately keeps the ZX Spectrum and GW-BASIC tone models distinct:

```basic
BEEP 1, 0
SOUND 262, 18.2
```

`BEEP duration, pitch` takes seconds followed by semitones relative to Middle C (`0` ≈ `261.625565 Hz`) and blocks until the tone ends. `SOUND frequency, duration` takes Hertz followed by approximately 18.2 PC timer ticks per second, accepts the historical `37..32767` Hz range, and plays in the background while BASIC execution continues. See `docs/AUDIO.md` and `examples/sound.bas`. Since 0.1.0a7 both commands use the same monophonic tone generator: SOUND converts Hertz to an equivalent fractional BEEP pitch and queues background notes sequentially, preventing overlapping POSIX audio processes from distorting sweeps and melodies.

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

The companion `extras/asc_h-sumbasic-0.1.0a13.py` appends the newer sumBASIC vocabulary starting at index `2990`, after the existing 2990 entries. This preserves every historical code while still giving `SUB`, `FUNCTION`, `CALL`, `SHARED`, the modern types, structured-loop words and newer runtime vocabulary stable ASC positions.

The parser does not depend on those numeric positions; they remain a cross-project symbol space rather than parser opcodes.

## Still pending

Structured `SUB`/`FUNCTION` execution and `CALL ... WITH ...` are reserved design work for the next procedure-scope milestone. The current `DIM SHARED` implementation establishes the global-state semantics those procedures will use.

Also pending: full graphics rendering, virtual `PEEK`/`POKE` and port I/O, richer music/`PLAY` support, events/errors beyond current control flow, SumIR emission, and Python/native compilation.

## Usage

```bash
sumbasic
sumbasic --plain
sumbasic program.bas
sumbasic --run program.bas
sumbasic --check program.bas
```

## Tests

The alpha includes 65 regression tests. The mathematical suite covers arithmetic and integer division, powers/modulo, shifts and bitwise operations, comparisons/logical operations, Spectrum transcendental functions, extended logarithms and roots, rounding, number theory, combinatorics, special functions, decimal promotion, and the `INPUT` prompt-separator rules.


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
