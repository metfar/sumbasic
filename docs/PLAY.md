# PLAY music language

sumBASIC exposes two deliberately separate historical string-music dialects over one audio engine:

```basic
PLAY "T120O5cdefgabC"
ZXPLAY "T120O5cdefgabC"
GWPLAY "T120 O4 L8 C D E F G A B > C"
```

`PLAY` is an alias of `ZXPLAY`. `GWPLAY` selects the Microsoft/GW-BASIC Music Macro Language instead of trying to guess the dialect from a string.

## ZX Spectrum 128 PLAY

The syntax follows the ZX Spectrum 128 PLAY model documented in *ZX Spectrum 128 Introducción y Guía de Funcionamiento*, especially the "Música y sonido" section (printed pages 12-16).

One to three strings form simultaneous voices:

```basic
Melody$ = "T180O5N3cdefgabC"
Bass$ = "O4N5c&c&g&g&"
PLAY Melody$, Bass$
```

The current alpha implements the musical core:

- note letters `c d e f g a b` and `C D E F G A B`; upper-case notes are the upper octave of the current two-octave range;
- `#` before a note raises it by a semitone and `$` lowers it by a semitone; repeated accidentals are accepted;
- `O0..O8` chooses the Spectrum octave range; the default is `O5`;
- duration codes `1..9`, plus triplet codes `10..12`;
- `&` is a rest using the current duration;
- `N` is the original numeric separator, useful in strings such as `O5N3cde`;
- `T60..T240` selects tempo in quarter-note beats per minute; default `T120`;
- `V0..V15` controls music volume where the host backend supports amplitude;
- `_` supports the Spectrum tied-duration spelling;
- a parenthesized phrase is repeated once, matching the finite phrase-repeat form from the manual;
- `!comment!` embeds a comment inside the music string;
- `H` stops interpretation of the current musical string.

The AY-specific selectors `M`, `W`, `X`, and `U` are parsed and range-checked so old strings can already be loaded. Exact AY noise/envelope synthesis and the manual's indefinite `))` phrase repetition are reserved for the next audio pass rather than silently emulated incorrectly.

### Foreground and background

The historical Spectrum PLAY is foreground by default:

```basic
PLAY "T180O5N3cdefg"
PRINT "This appears when the phrase finishes"
```

sumBASIC also provides an explicit background extension:

```basic
PLAY BACKGROUND "T180O5N3cdefg"
PRINT "This appears immediately"

# Replace background music without allowing the old queue to continue.
PLAY STOP
PLAY BACKGROUND "T240O5c"
```

The same spelling works with the explicit name:

```basic
ZXPLAY FOREGROUND A$, B$, C$
ZXPLAY BACKGROUND A$, B$, C$
```

`PLAY STOP` and `PLAY OFF` (likewise `ZXPLAY` / `GWPLAY`) cancel the current music session immediately where the host audio backend supports interruption, invalidate queued notes, and allow the next background phrase to start cleanly. `STOP` and `OFF` are aliases.

### Held notes

`PLAY HOLD` sustains exactly one note on the existing PLAY bus:

```basic
PLAY HOLD "T240V15O4c"
PLAY HOLD 3, "T240V15O4c"
PLAY STOP
```

The default safety timeout is three seconds. Repeating the identical command
renews that timeout without restarting the tone, so keyboard auto-repeat can
keep it alive smoothly. A timeout of zero disables the safety limit when the
input backend guarantees a release event. `PLAY STOP` releases it immediately.

## GW-BASIC PLAY

`GWPLAY` implements the classic Microsoft music-macro spelling separately:

```basic
GWPLAY "T120 O4 L8 C D E F G A B > C"
```

The current alpha supports:

- notes `A..G`;
- `#` or `+` for sharp and `-` for flat after a note;
- `O0..O6` and `<` / `>` octave movement;
- `L1..L64` default note length;
- a numeric length directly after a note;
- dotted notes and rests;
- `T32..T255` tempo;
- `P` rests;
- `N0..N84` numeric notes;
- `MN`, `ML`, `MS` for normal, legato, and staccato articulation;
- `MF` foreground and `MB` background.

Therefore both historical and explicit sumBASIC spellings work:

```basic
GWPLAY "MB T180 O4 L8 CDEFG"
GWPLAY BACKGROUND "T180 O4 L8 CDEFG"
```

An explicit `FOREGROUND` or `BACKGROUND` after `GWPLAY` overrides `MF` / `MB` inside the string.

## Independent audio buses

`BEEP`, `SOUND`, and music are intentionally independent:

```basic
PLAY BACKGROUND "T160O5N3cdefgabC"
BEEP .08, 12
SOUND 440, 4
PRINT "music continues"
```

`BEEP` remains blocking with respect to BASIC execution, `SOUND` remains an asynchronous monophonic PC-speaker-style queue, and `PLAY`/`ZXPLAY`/`GWPLAY` use a separate music queue. A ZXPLAY session can run up to three voices concurrently.

`STOP` suspends BASIC without discarding background music. An IDE user-abort requests audio cancellation; a normal command-line run waits for queued background sound/music before the short-lived `sumbasic` process exits.

<p align=center><b>- oOo -</b></p>
