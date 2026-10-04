DECLARE FUNCTION repeat$ (char AS STRING, n)
PRINT repeat$("ab", 3)
END
FUNCTION repeat$ (char AS STRING, n)
    out$ = ""
    FOR f = 1 TO n
        out$ = out$ + char
    NEXT f
    repeat$ = out$
END FUNCTION
