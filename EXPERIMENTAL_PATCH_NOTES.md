# Experimental patch from 0.2.32 source

Changed `src/sumbasic/cli.py`: `--run` no longer diverts text-mode programs to sumIDE GUI; it executes using the existing CLI interpreter.

Changed `src/sumbasic/interpreter.py`: initial, deliberately limited support for `DECLARE FUNCTION name(args)`, `FUNCTION name(args)` and `END FUNCTION`; scalar parameters and local scalar assignments (including FOR loop variables) are restored after returning. `DECLARE` before implementation is accepted. Definitions are registered before execution; they do not run as top-level statements.

LIMITATIONS: Not a complete QuickBASIC FUNCTION/SUB implementation; no `DECLARE SUB`, BYREF, recursive locals and advanced type annotations; `--check` currently excludes inspection of function body statements; full program execution requires sum ecosystem dependencies including `sumcore` (unavailable in the validation container), so the patch is **unverified at runtime**. DO NOT replace production checkout without running tests. The signal source example uses `FOR f = 1 TO n`.

Try in a disposable checkout:

    python3 -m compileall -q src/sumbasic
    PYTHONPATH=src python3 -m sumbasic --check examples/compat/function_repeat_test.bas
    PYTHONPATH=src python3 -m sumbasic --run examples/compat/function_repeat_test.bas
    PYTHONPATH=src python3 -m sumbasic --run examples/compat/signal_qbasic.bas
    PYTHONPATH=src python3 -m pytest -q tests

No PCM export has been implemented; the audio engine lives in sumcore.audio, not in this archive.

<p align=center><b>- oOo -</b></p>
