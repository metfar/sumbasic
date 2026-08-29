# sumBASIC and the Sum super-extended ASC table

The supplied `asc_h.py` is not an ordinary ASCII table. It is a Sum-wide symbol space containing classic characters, Unicode symbols, Greek letters, BASIC tokens, input events, mathematical symbols, and other project-specific symbols.

The historical BASIC token block is preserved at its existing indexes. In particular:

- `512` = `RND`
- `513` = `INKEY$`
- `514` = `PI`
- `578` = `READ`
- `579` = `DATA`
- `580` = `RESTORE`
- `584` = `DIM`
- `596` = `PRINT`
- `651` = `TOUCH`
- `652..655` = the existing screen-buffer commands

sumBASIC does **not** insert new tokens into that historical block because doing so would shift every later ASC code. The companion file in `extras/asc_h-sumbasic-0.1.0a7.py` therefore appends the modern sumBASIC vocabulary after the existing table, beginning at index `2990` in the supplied version.

The appended block includes `SUB`, `FUNCTION`, `CALL`, `WITH`, `SHARED`, `REDIM`, `PRESERVE`, `OPTION`, `BASE`, named scalar/container types, structured loops, file-channel additions, `SCREEN`, `LBOUND`, `UBOUND`, and related modern vocabulary. Version 0.1.0a4 continued append-only from code `3045` through `3114` with the expanded real/integer mathematical and utility vocabulary. Version 0.1.0a5 continues at `3115..3130` with complex-number, clock and corrected logarithm vocabulary. Existing positions `0..3114` remain unchanged.

The authoritative language parser remains independent of numeric ASC positions. ASC codes are a shared Sum symbol catalogue, not parser opcodes.

<p align=center><b>- oOo -<b></p>

Version 0.1.0a7 adds no new language-token positions. `BEEP` and `SOUND` already have historical positions in the shared table; this release only changes their audio backend behavior.
