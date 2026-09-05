# Text-cell mouse input

`MOUSEX()` and `MOUSEY()` expose the last pointer position as one-based text
cells, using the same coordinate convention as `LOCATE row,column`.
`MOUSEBUTTON()` returns `1` once for a pending left click and consumes that
click. A later call returns `0` until another press arrives.

```basic
DO
    IF MOUSEBUTTON() = 1 THEN
        PRINT "Clicked column "; MOUSEX(); " row "; MOUSEY()
    END IF
    PAUSE .01
LOOP
```

The sumIDE terminal and graphical frontends translate their pointer events to
the common text grid. Interactive POSIX `sumbasic --run` uses SGR mouse input
when the terminal implements it. Keyboard operation remains available when
mouse reporting is unsupported.

The feature does not create or replace an audio backend. Programs such as
`examples/piano_text.bas` continue to use the normal sumBASIC PLAY engine.

GPL-2.0-or-later.

<p align=center><b>- oOo -</b></p>
