# Text-cell mouse input

`MOUSEX()` and `MOUSEY()` expose the last pointer position as one-based text
cells, using the same coordinate convention as `LOCATE row,column`.
`MOUSEBUTTON()` returns the current primary-button state: `1` while it is held
and `0` after release. This permits controls such as piano keys to remain active
for the complete mouse or touch gesture.

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
