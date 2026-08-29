# STOP preserves runtime state; CONTINUE resumes at the next statement.
A! = 1
PRINT "Before STOP:"; A!
STOP
A! = A! + 1
PRINT "After CONTINUE:"; A!
END
