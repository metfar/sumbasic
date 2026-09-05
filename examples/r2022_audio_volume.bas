# r20.2.2 demo: independent host-output volume for BEEP, SOUND and PLAY.
# Levels are percentages; PLAY volume multiplies the V0..V15 music dynamics.

PRINT "BEEP at 20%"
VOLUME BEEP 20
BEEP .15, 0

PRINT "SOUND at 35%"
VOLUME SOUND 35
SOUND 440, 4
PAUSE .3

PRINT "PLAY at 50%"
VOLUME PLAY 50
PLAY "T240V15O5cde"

PRINT "All buses at 10%"
VOLUME 10
BEEP .1, 7
SOUND 660, 2
PLAY "T240V15O5g"
