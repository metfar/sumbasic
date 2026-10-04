# Streaming audio in sumBASIC

`PLAY STREAM url`, `STREAM PLAY url`, `STREAMPLAY url` are aliases. Their default is **blocking**. Add `, ASYNC` for nonblocking playback. `ISSTREAMING()` returns 1 while the FFplay process exists and is playing; 0 otherwise. `STREAMSTOP` disconnects, `STREAMCONT` reconnects to the current broadcast (not cached position); `STREAMSTART` aliases CONT; `STREAMCLOSE` and `STREAMEND` release session state. Requires `ffplay` installed and available on PATH. `END` and `SYSTEM` close the connection. No browser or IDE is required.

This is a provisional external-player backend; integration with the in-process sumcore audio mixer, sumTUI, sumGUI, and extended error reporting is not yet complete.
