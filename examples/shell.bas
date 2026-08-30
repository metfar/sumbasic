# sumBASIC host-shell bridge.
# SHELL "command" captures stdout/stderr into BASIC output.
# Bare SHELL is interactive; uncomment it to enter your system shell.

PRINT "Current directory from the host shell:"
SHELL "pwd"

PRINT "A short directory listing:"
SHELL "ls"

PRINT "Back in BASIC after captured commands."

# PRINT "Type exit to return to sumBASIC."
# SHELL
# PRINT "Returned from interactive SHELL."

END
