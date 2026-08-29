# sumBASIC 0.1.0a1

sumBASIC is an educational BASIC frontend for the Sum ecosystem. This first alpha intentionally focuses on text-mode programs: the graphical `SCREEN`/drawing family is planned for the shared Sum Machine video subsystem rather than implemented separately here.

The initial compatibility scope is based on the supplied QBasic 1.1 command inventory: control flow, text I/O, variables/data, file-oriented foundations, and mathematical/string functions are the first targets; graphics and direct hardware access are explicitly deferred.

## First alpha

Implemented now:

- classic numbered program entry and unnumbered structured source;
- immediate mode with `RUN`, `LIST`, `NEW`, `LOAD`, `SAVE`, `DELETE`, `RENUM`;
- `PRINT` / `?`, `INPUT`, `LINE INPUT`, `CLS`, `LOCATE`;
- assignments and BASIC suffixes `$`, `%`, `&`, `!`, `#`;
- `IF ... THEN ... ELSE`, block `IF ... END IF`;
- `FOR ... TO ... STEP ... NEXT`, `WHILE/WEND`, `DO/LOOP`;
- `GOTO`, `GOSUB`, `RETURN`, `END`, `STOP`;
- `DATA`, `READ`, `RESTORE`, `SWAP`, initial `DIM`;
- common numeric and string functions such as `ABS`, `INT`, `RND`, `LEN`, `LEFT$`, `MID$`, `RIGHT$`, `UCASE$`, `LCASE$`, `CHR$`, `ASC`, `STR$`, `VAL`, `HEX$`, `OCT$`;
- sumTUI command-window frontend and `sumedit` integration.

Not yet implemented in this alpha: `SUB/FUNCTION`, `SELECT CASE`, complete arrays, file channels, events/errors, SumIR emission, Python/native compilation, graphics, virtual `PEEK/POKE` and port I/O.

## Usage

Interactive sumTUI command window:

```bash
sumbasic
```

Plain classic command prompt:

```bash
sumbasic --plain
```

Open a BASIC file in sumedit:

```bash
sumbasic program.bas
```

Run directly:

```bash
sumbasic --run program.bas
```

Check source loading:

```bash
sumbasic --check program.bas
```

Classic immediate mode accepts numbered lines:

```text
> 10 PRINT "HELLO"
> 20 FOR I%=1 TO 3
> 30 PRINT I%
> 40 NEXT I%
> 50 END
> LIST
> RUN
```

The runtime currently uses Python values compatible with the value model already used by sumX. A shared SumIR/Sum Machine runtime is the planned convergence point rather than coupling the languages directly.

## License

GPL-2.0-or-later.

<p align=center><b>- oOo -</b></p>
