# Retro digital clock for sumBASIC.
# TIME$ supplies HH:MM:SS. TIMER is seconds since local midnight.
# The bitmap font is loaded once from DATA into DIM SHARED arrays.
# The clock runs until Escape, Q or q is pressed in the IDE.

DIM SHARED Font$(9, 6), Colon$(6)

FOR Digit! = 0 TO 9
    FOR Row! = 0 TO 6
        READ Font$(Digit!, Row!)
    NEXT Row!
NEXT Digit!

FOR Row! = 0 TO 6
    READ Colon$(Row!)
NEXT Row!

:LOOP
T$ = TIME$
CLS

FOR Row! = 0 TO 6
    Line$ = ""
    FOR Pos! = 1 TO 8
        C$ = MID$(T$, Pos!, 1)
        IF C$ = ":" THEN
            Line$ = Line$ + Colon$(Row!) + " "
        ELSE
            Digit! = VAL(C$)
            Line$ = Line$ + Font$(Digit!, Row!) + " "
        END IF
    NEXT Pos!
    LOCATE Row! + 4, 20
    PRINT Line$
NEXT Row!

LOCATE 13, 20
PRINT "TIME$ = "; T$; "   TIMER = "; INT(TIMER)

# BEEP blocks for .1 s. PAUSE uses Spectrum 50 Hz ticks, so 45 ticks
# contribute another .9 s: approximately one update/beep per second.
BEEP .1, 0: PAUSE 45
A$ = INKEY$: IF A$ = CHR$(27) OR A$ = "Q" OR A$ = "q" THEN END
GOTO LOOP

# 0
DATA " ███ ", "█   █", "█  ██", "█ █ █", "██  █", "█   █", " ███ "
# 1
DATA "  █  ", " ██  ", "  █  ", "  █  ", "  █  ", "  █  ", "█████"
# 2
DATA " ███ ", "█   █", "    █", "   █ ", "  █  ", " █   ", "█████"
# 3
DATA "████ ", "    █", "    █", " ███ ", "    █", "    █", "████ "
# 4
DATA "█  █ ", "█  █ ", "█  █ ", "█████", "   █ ", "   █ ", "   █ "
# 5
DATA "█████", "█    ", "█    ", "████ ", "    █", "    █", "████ "
# 6
DATA " ███ ", "█    ", "█    ", "████ ", "█   █", "█   █", " ███ "
# 7
DATA "█████", "    █", "   █ ", "  █  ", " █   ", " █   ", " █   "
# 8
DATA " ███ ", "█   █", "█   █", " ███ ", "█   █", "█   █", " ███ "
# 9
DATA " ███ ", "█   █", "█   █", " ████", "    █", "    █", " ███ "
# colon
DATA "  ", "██", "██", "  ", "██", "██", "  "
