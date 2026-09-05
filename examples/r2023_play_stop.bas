# sumBASIC r20.2.3 - replace background PLAY cleanly.
# PLAY STOP / PLAY OFF cancel the current music bus before a new phrase.

VOLUME PLAY 25
PRINT "Long background phrase starts..."
PLAY BACKGROUND "T120O5cdefgabC"
PAUSE .25

PRINT "Stopping it before replacement..."
PLAY STOP
PLAY BACKGROUND "T240O4g"
PAUSE .30
PLAY STOP

PRINT "Done."
