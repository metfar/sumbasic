# Changelog

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
