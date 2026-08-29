# Sound in sumBASIC

sumBASIC intentionally keeps two historically different tone commands instead of making them aliases.

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

Examples:

```basic
BEEP 1, 0
BEEP .5, 12
BEEP .5, -12
```

## GW-BASIC `SOUND`

```basic
SOUND frequency, duration
```

- `frequency` is in Hertz, with the historical range `37..32767` Hz.
- `duration` is in PC timer ticks at approximately `18.2` ticks per second.
- execution is non-blocking/background: the BASIC program continues while the tone plays.

Examples:

```basic
SOUND 262, 18.2
SOUND 440, 9.1
```

The first example is approximately the same note and duration as `BEEP 1, 0`, but uses the GW-BASIC physical-frequency model and does not block program execution.

The default Python backend uses the native Windows beep API when available, then common POSIX audio tools when installed, with a terminal-bell fallback. Frontends/tests may inject their own tone backend without changing BASIC semantics.
