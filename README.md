# sumBASIC 0.1.0a3

sumBASIC is an educational BASIC frontend for the Sum ecosystem. It keeps classic BASIC ideas available while deliberately modernizing the language so it can also be used to learn contemporary programming concepts.

This alpha makes the language model substantially more explicit: Spectrum-compatible `PI`, literal `DATA`, line-aware `RESTORE`, multidimensional arrays, modern type declarations and containers, `DIM SHARED`, `FOR EACH`, and a reserved graphics vocabulary whose backend is still pending.

## Language identity

sumBASIC is BASIC, but it is not intended to be a byte-for-byte clone of GW-BASIC, QuickBASIC or Sinclair BASIC. Compatibility is preserved where it remains useful; deliberate differences are documented.

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

The type vocabulary currently includes `BOOLEAN`, `INTEGER`, `LONG`, `SINGLE`, `DOUBLE`, `DECIMAL`, `STRING`, `BYTES`, `ANY`, `LIST`, `DICT`, `SET` and `TUPLE`. Typed generic forms such as `LIST[STRING]` are reserved by the type parser; deeper element-type enforcement will evolve in later alphas.

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

The companion `extras/asc_h-sumbasic-0.1.0a3.py` appends the newer sumBASIC vocabulary starting at index `2990`, after the existing 2990 entries. This preserves every historical code while still giving `SUB`, `FUNCTION`, `CALL`, `SHARED`, the modern types, structured-loop words and newer runtime vocabulary stable ASC positions.

The parser does not depend on those numeric positions; they remain a cross-project symbol space rather than parser opcodes.

## Still pending

Structured `SUB`/`FUNCTION` execution and `CALL ... WITH ...` are reserved design work for the next procedure-scope milestone. The current `DIM SHARED` implementation establishes the global-state semantics those procedures will use.

Also pending: full graphics rendering, virtual `PEEK`/`POKE` and port I/O, sound, events/errors beyond current control flow, SumIR emission, and Python/native compilation.

## Usage

```bash
sumbasic
sumbasic --plain
sumbasic program.bas
sumbasic --run program.bas
sumbasic --check program.bas
```

## Tests

The alpha includes 29 regression tests covering the existing interpreter plus the new PI, comments, suffixes, `RESTORE` targeting, multidimensional arrays, modern containers, `FOR EACH`, graphics stubs and `INKEY$` hook.

## License

GPL-2.0-or-later.

<p align=center><b>- oOo -<b></p>
