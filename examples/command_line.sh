#!/usr/bin/env bash
# sumBASIC can execute source from a Unix pipeline or directly with -c/--command.

echo 'PRINT "casa!"' | sumbasic
sumbasic -c 'PRINT "la casa roja"'
sumbasic --command 'BEEP 1, 1'
sumbasic -c 'PLAY "T200O5N3cdefgabC"'
