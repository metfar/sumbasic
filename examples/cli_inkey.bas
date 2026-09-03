# INKEY$ works immediately in --run console mode; no Enter is required.
PRINT "Press Q to quit"
:LOOP
A$ = INKEY$
IF A$ = "Q" OR A$ = "q" OR A$ = CHR$(27) THEN END
PAUSE .02
GOTO LOOP
