# Changelog

## 0.1.0a11

- Fixed command-line `INKEY$` for `sumbasic --run`: interactive terminal programs now receive keys immediately without requiring Enter.
- Added a terminal input adapter that keeps POSIX terminals in cbreak mode while a BASIC program runs and restores the original terminal attributes on exit.
- A BASIC `INPUT` statement temporarily restores normal cooked/echo terminal mode so line input remains editable, then resumes immediate `INKEY$` mode.
- Added Windows non-blocking console-key support through `msvcrt`.
- Escape remains `CHR$(27)`; ANSI cursor/function-key sequences are read as a sequence rather than misreported as a bare Escape whenever the remaining bytes arrive together.
- Updated `examples/retro_clock.bas` documentation: Escape/Q/q now works in both the F5 IDE run and direct `--run` console execution.
- Added pseudo-terminal regression tests proving a key can be read without a newline and distinguishing bare Escape from an ANSI arrow sequence.
- No ASC indices changed in this release; this is terminal frontend behavior.

## 0.1.0a10

- Added free-form named labels using `:Name`; `GOTO Name` and `GOSUB Name` are case-insensitive and coexist with classic numeric line targets.
- Added `RESTORE Name`, targeting the first `DATA` at or after a named label, so data blocks can be named without requiring classic line numbers.
- Kept colon as a statement separator, so forms such as `BEEP .1, 0: PAUSE 45` execute left-to-right on one source line.
- Updated `examples/retro_clock.bas` to run continuously until Escape, `Q`, or `q`, using `:LOOP`, `INKEY$`, and `GOTO LOOP` instead of a fixed `FOR` count.
- The retro clock now emits `BEEP .1, 0` once per update. Because BEEP blocks for 0.1 s and Spectrum `PAUSE` uses 50 Hz ticks, the example uses `PAUSE 45` (0.9 s) for an approximately one-second cadence.
- The source IDE now routes printable keys and Escape to the running BASIC program's non-blocking `INKEY$` queue instead of inserting those keys into the editor while F5 execution is active. F6 remains the explicit emergency stop.
- Added regression coverage for named labels, named RESTORE, colon-separated BEEP/PAUSE timing, the clock-style INKEY$ exit loop, and IDE Q/Escape routing.
- No ASC indices changed in this release; named labels and IDE key routing are syntax/frontend behavior rather than new BASIC vocabulary tokens.

## 0.1.0a9

- Fixed hybrid free-form/classic line-number execution. A numeric line such as `10 PRINT ...` inside otherwise unnumbered source is now kept at its physical position and acts as a classic `GOTO`/`GOSUB` target instead of causing all unnumbered statements to be moved after it.
- `GOTO 10` in a modern source buffer now jumps to the explicit `10` label and continues from there exactly once unless the program itself jumps back.
- Added an explicit hybrid program representation to `BasicProgram`; pure classic programs still execute in numeric line-number order, while pure free-form and hybrid programs execute in physical source order.
- `RENUM` now preserves hybrid physical order while renumbering explicit labels and rewriting `GOTO`, `GOSUB`, inline `THEN`/`ELSE`, and `RESTORE` targets.
- `RESTORE <line>` in hybrid source now targets explicit BASIC line labels rather than accidental physical editor line numbers.
- Added regression tests using the reported `sound.bas` pattern (`GOTO 10` before a later `10 PRINT ...`) to ensure the skipped BEEP block stays skipped and the SOUND heading is printed only once.
- No ASC entries changed in this release.

## 0.1.0a8

- Fixed the IDE `F5` freeze: BASIC execution now runs on a worker thread while the sumTUI event loop remains responsive.
- IDE program output is streamed while the program is running instead of appearing only after `RUN` returns.
- Added a small ANSI-aware run screen so `CLS`, `LOCATE` and terminal-style text programs such as `examples/retro_clock.bas` render coherently inside the IDE output pane.
- Added `F6` Stop and cooperative interpreter cancellation; infinite `DO/LOOP`, `WHILE/WEND`, `FOR/NEXT` and `PAUSE 0` programs can be stopped without killing the IDE.
- Pressing `F5` while a program is already running no longer starts a second interpreter run.
- Expanded the IDE run pane to 12 rows so the 7-row retro font plus clock/status output fits comfortably on ordinary terminals.
- Added regression tests for asynchronous F5 execution, F6 cancellation and the ANSI run-screen buffer.
- No ASC entries changed in this release; F5/F6 are IDE controls rather than BASIC tokens.


## 0.1.0a7

- Fixed distorted/overlapping `SOUND` playback on POSIX systems by replacing one-thread-per-note playback with a single monophonic tone queue.
- `SOUND frequency, ticks` now converts Hertz to the equivalent fractional Spectrum semitone and feeds the same tone generator used by `BEEP`, while preserving GW-BASIC parameter order and tick timing.
- `BEEP` remains blocking; `SOUND` remains non-blocking, but queued SOUND notes now play sequentially instead of simultaneously.
- Added `spectrum_frequency_pitch()` as the inverse of `spectrum_pitch_frequency()` and regression coverage for exact round-trip tuning.
- Added backend regression coverage proving multiple background SOUND requests are serialized on one channel.
- One-shot `--run` execution now lets queued final SOUND notes finish before the host process exits; SOUND remains non-blocking during BASIC execution.
- No new ASC entries are required in this release.


## 0.1.0a6

- Added a sumBASIC-aware source IDE based on sumTUI edit; `F5` runs the current editor buffer without forcing a save first and shows program output in an IDE output pane.
- Implemented ZX Spectrum-style `BEEP duration, pitch`: seconds first, semitone offset from Middle C second, blocking execution.
- Implemented GW-BASIC-style `SOUND frequency, duration`: Hertz first, duration in 18.2 Hz PC timer ticks, non-blocking/background execution, historical `37..32767` Hz range.
- Added a pluggable tone backend with Windows/native and common POSIX best-effort playback plus a terminal-bell fallback.
- Added `docs/AUDIO.md`, `examples/sound.bas`, and regression tests for BEEP/SOUND timing, pitch/frequency conversion, range checking, background semantics, and F5 unsaved-buffer execution.
- No new ASC token numbers were required: `BEEP` and `SOUND` already occupy their historical shared-table positions, while F5 is an IDE key binding rather than a BASIC token.

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
