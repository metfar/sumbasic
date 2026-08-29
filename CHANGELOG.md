# Changelog

## 0.1.0a5

- Corrected logarithm semantics: `LOG(x)` is base 10 and `LN(x)` is natural/base `e`; arbitrary-base logarithms are now `LOGB(x, base)` / `LOGBASE(x, base)`.
- Added first-class `COMPLEX` values plus `CMPLX`, `REAL`, `IMAG`, `CONJ`/`CONJUGATE`, `MAG`, `NORM`, `PHASE`/`ARG`, `POLAR` and `ISCOMPLEX`.
- Extended ordinary arithmetic and transcendental functions to complex operands where mathematically meaningful.
- Added `TIME$` (`HH:MM:SS`) and `TIMER` (seconds since local midnight).
- Implemented Spectrum-style `PAUSE n` at 50 frames per second.
- Added `examples/retro_clock.bas`, which loads a large 5x7 digit font once from `DATA` into `DIM SHARED` arrays and renders a live digital clock in the terminal.
- Added `examples/complex.bas` and expanded mathematical documentation/tests.
- Appended the a5 vocabulary to the shared ASC symbol space at codes `3115..3130` without shifting any previous entry.

## 0.1.0a4

- Expanded the mathematical expression core beyond the Spectrum/xBase baseline while retaining the classic Spectrum names.
- Added classic integer division with `\` plus `DIV`, binary literals with `&B`, and fixed `<>` and leading `NOT` expression parsing.
- Added extended roots/powers, trigonometric aliases, reciprocal and hyperbolic functions, arbitrary-base/log2/log10 logarithms, rounding and angle conversion.
- Added number-theory and combinatoric functions (`GCD`, `LCM`, `FACT`, `COMB`, `PERM`) plus selected special functions (`GAMMA`, `LGAMMA`, `ERF`, `ERFC`).
- Added explicit integer bit operations (`BAND`, `BOR`, `BXOR`, `BNOT`, `SHL`, `SHR`, `IDIV`) and numeric predicates (`ISFINITE`, `ISINF`, `ISNAN`).
- Added mixed `DECIMAL` arithmetic promotion so decimal values are not silently converted back to binary floats.
- Added `ROUND` with documented half-away-from-zero behavior; kept the distinction between `INT` (floor) and `FIX`/`TRUNC` (truncate).
- Implemented the requested `INPUT` prompt separator semantics: semicolon adds `? `, comma does not, and bare `INPUT variable` uses `? `.
- Appended new mathematical/utility names to the shared ASC symbol space at codes `3045..3114` without moving previous entries.
- Added `docs/MATH.md`, `examples/math.bas`, and expanded the regression suite from 29 to 38 tests.

## 0.1.0a3

- Reserved `#` for modern comments, alongside apostrophe comments and `REM`, while preserving channel syntax such as `PRINT #1` and `OPEN ... AS #1`.
- Changed sumBASIC suffix semantics deliberately: `$` = `STRING`, `!` = `INTEGER`, `&` = `LONG`, `%` = `DOUBLE`; `#` is no longer a numeric suffix.
- Added immutable built-in `PI` with the ZX Spectrum-compatible value `3.1415927`.
- Reworked `DATA` scanning as literal program data instead of deferred expression evaluation.
- Added `RESTORE <line>`; it resets to the first `DATA` at or after the requested program line.
- Added classic multidimensional arrays, explicit `low TO high` bounds, `OPTION BASE 0/1`, `LBOUND()` and `UBOUND()`.
- Added `DIM SHARED` metadata in preparation for structured procedure scopes.
- Added modern scalar/container declarations including `BOOLEAN`, `INTEGER`, `LONG`, `SINGLE`, `DOUBLE`, `DECIMAL`, `STRING`, `BYTES`, `ANY`, `LIST`, `DICT`, `SET` and `TUPLE`.
- Added list/dict/set/tuple literals, collection indexing, common collection methods and `FOR EACH` iteration.
- Added `REDIM` and initial `REDIM PRESERVE` support across overlapping multidimensional bounds.
- Added bare `RND` and `INKEY$`; `INKEY$` can be supplied by the active frontend through the interpreter input hook.
- Added Spectrum-style numeric functions/aliases including `ASN`, `ACS`, `LN`, `CODE` and `BIN`.
- Reserved the initial graphics vocabulary (`SCREEN`, `PLOT`, `DRAW`, `LINE`, `CIRCLE`, `INK`, `PAPER`, `BORDER`, `RECTANGLE`, `POLYGON`, `ELLIPSE`, etc.); statement forms currently report `NOT IMPLEMENTED YET` instead of failing to parse.
- Added a formal vocabulary module containing the existing `asc_h.py` BASIC positions (`512..655`) and the modern vocabulary append block.
- Added `extras/asc_h-sumbasic-0.1.0a3.py`, appending new sumBASIC vocabulary at index `2990` without shifting any existing ASC index.
- Expanded the regression suite from 19 to 29 tests.

## 0.1.0a2

- Fixed the sumTUI console status update to use `StatusBar.set()`; immediate expressions no longer crash the TUI after execution.
- Added a regression test proving BASIC exponentiation `? 5^3` produces `125`.
- Added channels `1..10` with `A..J` aliases matching the xBase work-area convention.
- Added sequential `OPEN ... FOR INPUT/OUTPUT/APPEND`, binary modes and fopen-style `MODE` strings.
- Added `STDIN`, `STDOUT`, `STDERR` channel endpoints and input/output pipelines.
- Added `INPUT #`, `LINE INPUT #`, `PRINT #`, `WRITE #`, `CLOSE`, `FREEFILE()`, `EOF()`, `LOF()` and `LOC()`.
- Added `RANDOM` fixed-record access with `LEN`, `FIELD`, `GET` and `PUT`.
- Added the initial `BasicDatabase`/`DB` bridge to the xBase-compatible sumX database engine.

## 0.1.0a1

- First executable sumBASIC alpha.
- Added numbered and structured BASIC programs plus immediate mode.
- Added initial text I/O, expressions, control flow, DATA/READ, loops and classic BASIC functions.
- Added sumTUI command window and sumedit integration.
- Graphics, virtual hardware and SumIR intentionally deferred to subsequent milestones.
