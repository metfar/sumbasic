# sumBASIC r21.1 command-tail demo.
# Run: sumbasic --run examples/r211_command_args.bas --octava 5 "two words"

PRINT "COMMAND$ = ["; COMMAND$; "]"
PRINT "ARGS$    = ["; ARGS$; "]"
PRINT "ARGC     = "; ARGC
IF ARGC > 0 THEN
    FOR I! = 0 TO ARGC - 1
        PRINT "ARGV$("; I!; ") = ["; ARGV$(I!); "]"
    NEXT I!
END IF
