# sumBASIC clickable text piano.
# Two chromatic octaves plus C..E; uses the existing PLAY engine.
# GPL-2.0-or-later

DIM Key$(28), Note$(28), Name$(28), Kind$(28), WhiteIndex!(28)

FOR I! = 0 TO 28
    READ Key$(I!), Note$(I!), Name$(I!), Kind$(I!), WhiteIndex!(I!)
NEXT I!

VOLUME PLAY 25
CLS
CURSOR OFF

Left! = 2
Top! = 3
WhiteWidth! = 4
VisibleWhites! = MIN(17, MAX(1, INT((COLS - Left!) / WhiteWidth!)))

PRINT "sumBASIC piano: keyboard/mouse | SPACE=stop | ESC=exit"
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
        PLAY STOP
        PLAY BACKGROUND "T240V15" + Note$(Selected!)
        LOCATE 2, 1
        PRINT SPACE$(COLS);
        LOCATE 2, 1
        PRINT "Playing "; Name$(Selected!); " with ["; Key$(Selected!); "]";
    END IF

    IF K$ = " " THEN
        PLAY STOP
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

    PAUSE .01
LOOP

# key, ZXPLAY note, display name, white/black, preceding white-key index
DATA "z", "O3c",  "C3",  "W", 0
DATA "s", "O3#c", "C#3", "B", 0
DATA "x", "O3d",  "D3",  "W", 1
DATA "d", "O3#d", "D#3", "B", 1
DATA "c", "O3e",  "E3",  "W", 2
DATA "v", "O3f",  "F3",  "W", 3
DATA "g", "O3#f", "F#3", "B", 3
DATA "b", "O3g",  "G3",  "W", 4
DATA "h", "O3#g", "G#3", "B", 4
DATA "n", "O3a",  "A3",  "W", 5
DATA "j", "O3#a", "A#3", "B", 5
DATA "m", "O3b",  "B3",  "W", 6
DATA "q", "O4c",  "C4",  "W", 7
DATA "2", "O4#c", "C#4", "B", 7
DATA "w", "O4d",  "D4",  "W", 8
DATA "3", "O4#d", "D#4", "B", 8
DATA "e", "O4e",  "E4",  "W", 9
DATA "r", "O4f",  "F4",  "W", 10
DATA "5", "O4#f", "F#4", "B", 10
DATA "t", "O4g",  "G4",  "W", 11
DATA "6", "O4#g", "G#4", "B", 11
DATA "y", "O4a",  "A4",  "W", 12
DATA "7", "O4#a", "A#4", "B", 12
DATA "u", "O4b",  "B4",  "W", 13
DATA "i", "O5c",  "C5",  "W", 14
DATA "9", "O5#c", "C#5", "B", 14
DATA "o", "O5d",  "D5",  "W", 15
DATA "0", "O5#d", "D#5", "B", 15
DATA "p", "O5e",  "E5",  "W", 16
