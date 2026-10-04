DECLARE FUNCTION repeat$ (char AS STRING, n)
CLS
length = 9
a$ = repeat$(CHR$(219), length)

FOR m = 0 TO 7
    FOR n = 0 TO 11
        LOCATE 1 + n, 1 + m * length
        COLOR m, 5
        PRINT a$
        LOCATE 12 + n, 1 + m * length
        COLOR m + 8, 5
        PRINT a$

    NEXT n
NEXT m
SOUND 220, 2

FUNCTION repeat$ (char AS STRING, n)
out$ = ""
FOR f = 1 TO n
        out$ = out$ + char
NEXT f
repeat$ = out$

END FUNCTION

