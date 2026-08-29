REM Requires an existing table in the sumX database connection used by the program.
DB.SELECT A
PRINT "WORK AREA:"; 1
PRINT "RECORD:"; DB.RECNO(); "/"; DB.RECCOUNT()
