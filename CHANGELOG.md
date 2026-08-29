# Changelog

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
