# STOP preserves runtime state; CONTINUE resumes at the next statement.
# IDE: F5 runs; when STOP suspends the program, F5 continues it. F6 changes window.
# Console: after STOP, use CONTINUE (or CONT) to resume.
A! = 1
PRINT "Before STOP:"; A!
STOP
A! = A! + 1
PRINT "After CONTINUE:"; A!
END
