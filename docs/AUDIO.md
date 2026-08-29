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

Both commands share one monophonic tone generator. `BEEP` supplies a Spectrum pitch directly. `SOUND` converts its Hertz value to the equivalent fractional semitone relative to Middle C and then uses that same generator. This conversion does not quantize to integer semitones, so frequencies such as 440 Hz remain 440 Hz within floating-point precision.

Background `SOUND` requests are queued on one audio channel and played sequentially. This matters on POSIX systems: launching one independent audio process/thread per SOUND statement causes overlapping tones and audible distortion in loops. `SOUND` still returns immediately to the BASIC program; only the audio channel is serialized.
When `sumbasic --run` reaches the end of the program, the launcher waits for already queued notes to finish so a final SOUND is not cut off merely because the host Python process exits.

The default Python backend uses the native Windows beep API when available, then common POSIX audio tools when installed, with a terminal-bell fallback. Frontends/tests may inject their own tone backend without changing BASIC semantics.
