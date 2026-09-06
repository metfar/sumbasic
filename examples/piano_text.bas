# sumBASIC clickable text piano.
# Two chromatic octaves plus C..E; uses the existing PLAY engine.
# GPL-2.0-or-later

DIM Key$(28), Note$(28), Name$(28), Kind$(28), WhiteIndex!(28)

FOR I! = 0 TO 28
    READ Key$(I!), Note$(I!), Name$(I!), Kind$(I!), WhiteIndex!(I!)
NEXT I!

BaseVolume! = 150
VOLUME PLAY BaseVolume!
KEYREPEAT OFF
PollPause! = .04
InitialGracePolls! = 15
ReleaseMissLimit! = 3
MissedPolls! = 0
GracePolls! = 0
RepeatSeen! = 0
CLS
CURSOR OFF

Left! = 2
Top! = 3
WhiteWidth! = 4
VisibleWhites! = MIN(17, MAX(1, INT((COLS - Left!) / WhiteWidth!)))

PRINT "sumBASIC piano: hold keyboard/mouse | SPACE=stop | ESC=exit"
PRINT "Click a key or press: zsxdcvgbhnjm q2w3er5t6y7u i9o0p"

# Draw the white keys first.
FOR W! = 0 TO VisibleWhites! - 1
    X! = Left! + W! * WhiteWidth!
    FOR R! = 0 TO 3
        LOCATE Top! + R!, X!: PRINT "|   ";
    NEXT R!
    LOCATE Top! + 4, X!: PRINT "+---";
NEXT W!
LOCATE Top! + 4, Left! + VisibleWhites! * WhiteWidth!: PRINT "+";

# Put the computer-key label near the foot of each white key.
FOR I! = 0 TO 28
    IF Kind$(I!) = "W" AND WhiteIndex!(I!) < VisibleWhites! THEN
        X! = Left! + WhiteIndex!(I!) * WhiteWidth!
        LOCATE Top! + 3, X! + 2: PRINT Key$(I!);
    END IF
NEXT I!

# Black keys overlay the upper part of the white-key drawing.
FOR I! = 0 TO 28
    IF Kind$(I!) = "B" AND WhiteIndex!(I!) < VisibleWhites! - 1 THEN
        X! = Left! + (WhiteIndex!(I!) + 1) * WhiteWidth! - 1
        LOCATE Top!,     X!: PRINT "+-+";
        LOCATE Top! + 1, X!: PRINT "|"; Key$(I!); "|";
        LOCATE Top! + 2, X!: PRINT "+-+";
    END IF
NEXT I!

DO
    K$ = LCASE$(INKEY$)
    Released$ = LCASE$(KEYUP$)
    Selected! = -1

    # Physical keyboard lookup.
    IF K$ <> "" THEN
        FOR I! = 0 TO 28
            IF K$ = Key$(I!) THEN Selected! = I!
        NEXT I!
    END IF

    # Text-cell mouse lookup. Black keys win in their overlapping area.
    Button! = MOUSEBUTTON()
    IF Button! = 1 THEN
        MX! = MOUSEX()
        MY! = MOUSEY()

        IF MY! >= Top! AND MY! <= Top! + 2 THEN
            FOR I! = 0 TO 28
                IF Kind$(I!) = "B" AND WhiteIndex!(I!) < VisibleWhites! - 1 THEN
                    X! = Left! + (WhiteIndex!(I!) + 1) * WhiteWidth! - 1
                    IF MX! >= X! AND MX! <= X! + 2 THEN Selected! = I!
                END IF
            NEXT I!
        END IF

        IF Selected! < 0 AND MY! >= Top! AND MY! <= Top! + 3 THEN
            W! = INT((MX! - Left!) / WhiteWidth!)
            IF W! >= 0 AND W! < VisibleWhites! THEN
                FOR I! = 0 TO 28
                    IF Kind$(I!) = "W" AND WhiteIndex!(I!) = W! THEN Selected! = I!
                NEXT I!
            END IF
        END IF
    END IF

    IF Selected! >= 0 THEN
        NewHeld$ = Key$(Selected!)

        # sumpiano deliberately drives the PLAY bus above unity.  sumCore uses
        # software gain and saturates only if a sample would exceed signed PCM.
        VOLUME PLAY BaseVolume!

        # Hold indefinitely.  GUI/Kitty backends stop on exact KEYUP$.  A legacy
        # TTY cannot report release, so typematic repeats act as a heartbeat.
        PLAY HOLD 0, "T240V15" + Note$(Selected!)
        IF Held$ = NewHeld$ AND HeldSource$ = "keyboard" THEN
            RepeatSeen! = 1
            MissedPolls! = 0
        END IF
        IF Held$ <> NewHeld$ THEN
            Held$ = NewHeld$
            IF Button! = 1 THEN HeldSource$ = "mouse" ELSE HeldSource$ = "keyboard"
            MissedPolls! = 0
            GracePolls! = 0
            RepeatSeen! = 0
            LOCATE 2, 1
            PRINT SPACE$(COLS);
            LOCATE 2, 1
            PRINT "Playing "; Name$(Selected!); " with ["; Key$(Selected!); "]";
        END IF
    END IF

    # Graphical/extended terminals supply exact KEYUP; legacy TTYs use the timeout.
    IF Released$ <> "" AND Released$ = Held$ AND HeldSource$ = "keyboard" THEN
        PLAY STOP
        Held$ = ""
        HeldSource$ = ""
    END IF

    # Legacy terminal fallback: give the OS typematic delay time to start.
    # Once repeats have been observed, three keyboard polls without seeing the
    # same held key are considered a release.
    IF HeldSource$ = "keyboard" AND Released$ = "" THEN
        IF K$ = Held$ AND K$ <> "" THEN
            MissedPolls! = 0
            IF GracePolls! > 0 THEN RepeatSeen! = 1
        ELSE
            GracePolls! = GracePolls! + 1
            IF RepeatSeen! = 1 THEN MissedPolls! = MissedPolls! + 1
            IF RepeatSeen! = 0 AND GracePolls! > InitialGracePolls! THEN MissedPolls! = MissedPolls! + 1
        END IF
        IF MissedPolls! >= ReleaseMissLimit! THEN
            PLAY STOP
            Held$ = ""
            HeldSource$ = ""
            MissedPolls! = 0
            GracePolls! = 0
            RepeatSeen! = 0
        END IF
    END IF

    # Mouse/touch supplies an exact release in both GUI and SGR terminals.
    IF MouseWasDown! = 1 AND Button! = 0 AND HeldSource$ = "mouse" THEN
        PLAY STOP
        Held$ = ""
        HeldSource$ = ""
    END IF
    MouseWasDown! = Button!

    IF K$ = " " THEN
        PLAY STOP
        Held$ = ""
        HeldSource$ = ""
        LOCATE 2, 1: PRINT SPACE$(COLS);
        LOCATE 2, 1: PRINT "Stopped.";
    END IF

    IF K$ = CHR$(27) THEN
        PLAY STOP
        CURSOR ON
        LOCATE Top! + 6, 1
        PRINT "Bye."
        END
    END IF

    PAUSE PollPause!
LOOP

# key, ZXPLAY note, display name, white/black, preceding white-key index
DATA "z", "O4c",  "C3",  "W", 0
DATA "s", "O4#c", "C#3", "B", 0
DATA "x", "O4d",  "D3",  "W", 1
DATA "d", "O4#d", "D#3", "B", 1
DATA "c", "O4e",  "E3",  "W", 2
DATA "v", "O4f",  "F3",  "W", 3
DATA "g", "O4#f", "F#3", "B", 3
DATA "b", "O4g",  "G3",  "W", 4
DATA "h", "O4#g", "G#3", "B", 4
DATA "n", "O4a",  "A3",  "W", 5
DATA "j", "O4#a", "A#3", "B", 5
DATA "m", "O4b",  "B3",  "W", 6
DATA "q", "O5c",  "C4",  "W", 7
DATA "2", "O5#c", "C#4", "B", 7
DATA "w", "O5d",  "D4",  "W", 8
DATA "3", "O5#d", "D#4", "B", 8
DATA "e", "O5e",  "E4",  "W", 9
DATA "r", "O5f",  "F4",  "W", 10
DATA "5", "O5#f", "F#4", "B", 10
DATA "t", "O5g",  "G4",  "W", 11
DATA "6", "O5#g", "G#4", "B", 11
DATA "y", "O5a",  "A4",  "W", 12
DATA "7", "O5#a", "A#4", "B", 12
DATA "u", "O5b",  "B4",  "W", 13
DATA "i", "O6c",  "C5",  "W", 14
DATA "9", "O6#c", "C#5", "B", 14
DATA "o", "O6d",  "D5",  "W", 15
DATA "0", "O6#d", "D#5", "B", 15
DATA "p", "O6e",  "E5",  "W", 16
