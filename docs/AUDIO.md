# Sound in sumBASIC

sumBASIC keeps historical command semantics visible while using the common `sumCore` audio engine. `sumbasic.audio` remains a compatibility re-export; the implementation, ZX/GW parsers and shell commands live in `sumcore`.

## ZX Spectrum `BEEP`

```basic
BEEP duration, pitch
```

- `duration` is measured in seconds.
- `pitch` is measured in semitones relative to Middle C.
- `0` is Middle C, approximately `261.625565 Hz`.
- `12` is one octave above; `-12` is one octave below.
- execution is blocking: the BASIC program waits until the tone finishes.

The frequency conversion is:

```text
frequency = 261.6255653005986 * 2^(pitch / 12)
```

## GW-BASIC `SOUND`

```basic
SOUND frequency, duration
```

- `frequency` is in Hertz, with the historical range `37..32767` Hz.
- `duration` is in PC timer ticks at approximately `18.2` ticks per second.
- execution is non-blocking/background: BASIC continues while the SOUND queue plays.

```basic
SOUND 262, 18.2
SOUND 440, 9.1
```

SOUND converts Hertz to the equivalent fractional Spectrum semitone and feeds the same sine/tone synthesis algorithm. It is not quantized to integer semitones.

## Music: PLAY, ZXPLAY and GWPLAY

```basic
PLAY "T180O5N3cdefgabC"
ZXPLAY "T180O5N3cdefgabC"
GWPLAY "T180 O4 L8 C D E F G A B"
```

`PLAY` is an alias of `ZXPLAY`. The Spectrum 128 dialect supports up to three simultaneous strings. `GWPLAY` is a separate Microsoft/GW-BASIC MML parser rather than an auto-detected dialect. See `docs/PLAY.md` for the string languages and current compatibility surface.

Quick notation reminder: ZX uses `c..b` / `C..B` for notes, `#c` for a sharp, `$e` for a flat and `&` for a rest. ZX dotted values are encoded by duration codes `2`, `4`, `6`, and `8`; it does not use `.` as a dotted-note suffix. GWPLAY uses `C#` or `C+` for a sharp, `E-` for a flat, `P4` for a rest and `C4.` / `P4.` for dotted notes/rests.

Both music dialects accept the sumBASIC execution-mode extension:

```basic
PLAY FOREGROUND A$
PLAY BACKGROUND A$, B$, C$
GWPLAY FOREGROUND G$
GWPLAY BACKGROUND G$
```

GWPLAY additionally understands its historical `MF` and `MB` macro codes.

## Independent buses

The default engine is arranged as independent logical buses:

```text
AudioEngine
├── BEEP                 blocking Spectrum tone bus
├── SOUND                asynchronous monophonic queue
└── MUSIC                queued PLAY sessions
    ├── ZX voice A
    ├── ZX voice B
    └── ZX voice C
```

A background PLAY therefore continues while BASIC executes a BEEP or queues SOUND. BEEP is still blocking **to the BASIC program**, but it does not pause the music worker. SOUND notes remain serialized with other SOUND notes to avoid the distorted overlapping-process behavior fixed in 0.1.0a7.

A short-lived command-line invocation waits for queued SOUND/music after normal program completion so the final phrase is not truncated. `STOP` suspends BASIC state without discarding background music. A frontend user-abort requests music cancellation.

The default backend uses Windows `winsound` where available, then common POSIX audio tools, with generated WAV/terminal-bell fallback. Music volume is honored by backends that expose amplitude control. BASIC bus
volume accepts `0..300`: `100` is unity gain and values above 100 apply software
gain before output. Synthesized 16-bit PCM is saturated at full scale rather
than wrapping if an amplified waveform exceeds the numeric range.

## Shell commands

The same `AudioEngine` is available directly from Bash:

```bash
sumbeep 0.25 12
sumsound 440 18.2
sumplay 'T180O5cdefgabC'
sumplay 'O4c' 'O3g'
sumplay --gw 'T180 O4 L8 CDEFG'
sumplay --hold --timeout 3 'T240V15O4c'
```

`sumbeep` keeps the BASIC order `duration pitch`; `sumsound` keeps `frequency
ticks`. All three accept `--volume 0..300`; `100` is unity gain. Shell quoting is strongly advised,
especially because `#` in a PLAY string has meaning to both ZX music and the
shell.

`sumplay --hold` uses a three-second safety timeout. Set another duration with
`--timeout`, while `--timeout 0` runs until interrupted. `Ctrl+C`, `TERM`, or
normal process control should be used for Bash background jobs.

```bash
sumplay --hold --timeout 0 'O4c' &
sum_audio_pid=$!
sleep 1
kill "$sum_audio_pid"
wait "$sum_audio_pid" || test $? -eq 130
```

### Android / Termux

On Termux, sumCore first checks for `termux-media-player`. When available it
generates a temporary WAV tone and delegates playback to Android's native
MediaPlayer service. This is the preferred compatibility backend because an
unprivileged Termux process normally does not expose Android audio hardware as
a conventional ALSA device.

For F-Droid/GitHub Termux installations, install the matching Termux:API app and
the `termux-api` package so `termux-media-player` is present. Recent Google Play
Termux builds include this particular API command directly. Check with:

```bash
command -v termux-media-player
```

PulseAudio can still be used by other applications, but its OpenSL ES/AAudio
sink is device/Android-version dependent. If neither native MediaPlayer nor a
usable PCM/Pygame backend is available, Sum can still reach the terminal-bell
fallback. This is a backend limitation, not a change to PLAY, BEEP, SOUND, or
music-string semantics.

<p align=center><b>- oOo -<b></p>

### Stopping/replacing background music

`PLAY STOP` and `PLAY OFF` stop the shared music bus, discard queued notes from the previous session, and are intended to be used before starting a replacement background phrase. The explicit dialect names accept the same forms: `ZXPLAY STOP`, `GWPLAY STOP`, `ZXPLAY OFF`, and `GWPLAY OFF`.

```basic
PLAY BACKGROUND "T120O5cdefgabC"
PAUSE .25
PLAY STOP
PLAY BACKGROUND "T240O4g"
```

<p align=center><b>- oOo -</b></p>
