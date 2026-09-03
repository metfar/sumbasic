# sumBASIC music demo: Spectrum 128 PLAY plus GW-BASIC MML.
# PLAY is an alias of ZXPLAY.

PRINT "ZX Spectrum 128 PLAY - melody"
PLAY "T180O5N3cdefgabC"

PRINT "ZXPLAY - two simultaneous voices"
Melody$ = "T180O5N3cdefgabC"
Bass$ = "O4N5c&c&g&g&"
ZXPLAY Melody$, Bass$

PRINT "Background music with independent BEEP and SOUND"
PLAY BACKGROUND "T200O5N3cdefgC"
BEEP .08, 12
SOUND 660, 3
PRINT "BASIC keeps running while PLAY and SOUND continue"
PAUSE .7
PLAY OFF

PRINT "GW-BASIC Music Macro Language"
GWPLAY "MF T180 O4 L8 C D E F G A B > C"

PRINT "GWPLAY background"
GWPLAY "MB T200 O4 L8 C E G > C"
PRINT "queued"
PAUSE .6
GWPLAY OFF

END
