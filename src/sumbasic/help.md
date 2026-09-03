# sumBASIC Help

The BASIC reference is example-driven. Select a topic and copy or run its functional example.

## Console I/O

### PRINT

Writes values to the current output stream.

#### Syntax

```text
PRINT expression
PRINT expression;
? expression
```

#### Notes

- A trailing semicolon suppresses the normal newline where supported.
- ? is the short PRINT form.

#### Functional example

```basic
name$ = "Ada"
PRINT "Hello "; name$
? 2 + 2
```

#### See also

INPUT, LOCATE

#### Aliases

?

### INPUT

Reads a value from the user into a variable.

#### Syntax

```text
INPUT variable
INPUT "Prompt"; variable
INPUT "Prompt", variable
```

#### Notes

- With a semicolon after the prompt, sumBASIC displays the traditional "? " prompt marker.
- With a comma after the prompt, input follows the prompt directly.

#### Functional example

```basic
INPUT "Name"; name$
PRINT "Hello "; name$
```

#### See also

PRINT, INKEY$

## Programming

### IF

Executes code conditionally.

#### Syntax

```text
IF condition THEN statement
IF condition THEN
    statements
ELSE
    statements
END IF
```

#### Functional example

```basic
age = 20
IF age >= 18 THEN
    PRINT "adult"
ELSE
    PRINT "minor"
END IF
```

#### See also

FOR, WHILE, DO

### FOR

Repeats a block while a numeric control variable advances toward a limit.

#### Syntax

```text
FOR variable = first TO last [STEP step]
NEXT [variable]
```

#### Functional example

```basic
FOR i = 1 TO 5
    PRINT i
NEXT i
```

#### See also

WHILE, DO

#### Aliases

NEXT

### WHILE

Repeats a block while its condition remains true.

#### Syntax

```text
WHILE condition
WEND
```

#### Functional example

```basic
i = 1
WHILE i <= 3
    PRINT i
    i = i + 1
WEND
```

#### See also

FOR, DO

#### Aliases

WEND

### DO

Provides DO/LOOP structured repetition, optionally controlled by WHILE or UNTIL.

#### Syntax

```text
DO
LOOP
DO WHILE condition
LOOP UNTIL condition
```

#### Functional example

```basic
i = 0
DO
    i = i + 1
    PRINT i
LOOP UNTIL i >= 3
```

#### See also

WHILE, FOR

#### Aliases

LOOP

### DATA

Stores literal data in the program for sequential READ operations.

#### Syntax

```text
DATA value [, value ...]
READ variable [, variable ...]
RESTORE [line-or-label]
```

#### Notes

- RESTORE without an argument rewinds the DATA pointer.
- Named labels may identify DATA blocks.

#### Functional example

```basic
DATA "red", "green", "blue"
READ a$, b$
PRINT a$; " "; b$
RESTORE
READ c$
PRINT c$
```

#### See also

READ, RESTORE

#### Aliases

READ, RESTORE

## Data

### DIM

Creates arrays using BASIC dimensions.

#### Syntax

```text
DIM name(size)
DIM name(rows, columns)
```

#### Functional example

```basic
DIM table(2, 2)
table(1, 1) = 42
PRINT table(1, 1)
```

#### See also

LBOUND, UBOUND, REDIM

## Audio

### BEEP

Plays a ZX Spectrum-style note using duration then semitone pitch offset from middle C.

#### Syntax

```text
BEEP duration, pitch
```

#### Notes

- 0 is middle C; +12 is one octave above and -12 one octave below.
- BEEP is intentionally blocking.

#### Functional example

```basic
BEEP .15, 0
BEEP .15, 4
BEEP .15, 7
BEEP .3, 12
```

#### See also

SOUND, PLAY

### SOUND

Plays a GW-BASIC-style tone using frequency and duration.

#### Syntax

```text
SOUND frequency, duration
```

#### Notes

- SOUND and BEEP intentionally keep different historical argument semantics.

#### Functional example

```basic
SOUND 440, .25
SOUND 660, .25
```

#### See also

BEEP, PLAY

### PLAY

Plays music using the BASIC music-string facilities.

#### Syntax

```text
PLAY string-expression
ZXPLAY string-expression
GWPLAY string-expression
```

#### Functional example

```basic
PLAY "C D E F G"
```

#### See also

BEEP, SOUND

## Environment

### SHELL

Runs a host shell command or opens an interactive shell when used without a command.

#### Syntax

```text
SHELL
SHELL string-expression
```

#### Notes

- The configured host shell is used; sumBASIC does not implement a second shell parser.

#### Functional example

```basic
SHELL "printf 'hello from the shell\n'"
```

#### See also

SYSTEM

## Programming

### STOP

Suspends a running BASIC program while preserving state for CONTINUE.

#### Syntax

```text
STOP
CONTINUE
CONT
```

#### Notes

- STOP is resumable; END and a user-requested IDE stop are not.
- In the IDE, F5 resumes when the previous run stopped at STOP.

#### Functional example

```basic
PRINT "before"
STOP
PRINT "after"
```

#### See also

CONTINUE, END

#### Aliases

CONT, CONTINUE

## Console I/O

### INKEY$

Returns a pending key immediately, or an empty string when no key is waiting.

#### Syntax

```text
INKEY$
```

#### Notes

- Interactive --run mode places POSIX terminals in cbreak mode so INKEY$ does not wait for Enter.

#### Functional example

```basic
PRINT "Press Q to quit"
DO
    k$ = INKEY$
LOOP UNTIL UCASE$(k$) = "Q"
```

#### See also

INPUT

## Files

### OPEN

Opens BASIC file/channel I/O resources.

#### Syntax

```text
OPEN ...
OPEN # ...
CLOSE #channel
FREEFILE
```

#### Functional example

```basic
OPEN "example.txt" FOR OUTPUT AS #1
WRITE #1, "hello"
CLOSE #1
```

#### See also

GET, PUT, WRITE, EOF, LOF, LOC

## Functions

### MATH

sumBASIC includes classic BASIC/Spectrum functions plus an extended mathematical vocabulary.

#### Syntax

```text
SIN(x)  COS(x)  TAN(x)
SQR(x)  SQRT(x)  ABS(x)
LOG(x)  LOG10(x)  LOG2(x)
GCD(a,b)  LCM(a,b)  FACT(n)
```

#### Notes

- PI follows the Spectrum-inspired BASIC vocabulary.

#### Functional example

```basic
PRINT SIN(PI / 2)
PRINT SQRT(81)
PRINT GCD(84, 30)
```

#### Aliases

SQR, SQRT

### PAUSE

Waits for a number of seconds or until the user provides input. `PAUSE 0` waits indefinitely. In graphical mode, keyboard, mouse and touch presses interrupt the wait while the window continues to process redraw and resize events.

#### Syntax

```text
PAUSE seconds
```

#### Functional example

```basic
PRINT "Press a key/click/touch, or wait one second"
PAUSE 1
PRINT "Continuing"
```

#### See also

INKEY$, DISPLAY

## Graphics and images

### COLOR

Sets the BASIC foreground, background and optional border colors. Numeric colors 0-15 use the GW-BASIC/QBASIC-compatible 16-color palette on arbitrary BASIC graphics modes.

#### Syntax

```text
COLOR foreground [, background [, border]]
```

#### Functional example

```basic
SCREEN 640,480
COLOR 14,0,1
LINE (0,0)-(639,479)
```

#### See also

INK, PAPER, BORDER

### PAINT

Flood-fills an enclosed area. `FILL` is an alias.

#### Syntax

```text
PAINT (x,y) [, color [, border]]
FILL (x,y) [, color [, border]]
```

#### Functional example

```basic
SCREEN 320,240
COLOR 15,0
RECTANGLE 20,20,100,80,14
PAINT (30,30),1,14
```

#### See also

COLOR, RECTANGLE

#### Aliases

FILL

### GET

Captures a graphical region as a portable image value.

#### Syntax

```text
image = GET(x,y,width,height)
GET (x1,y1)-(x2,y2)
```

#### Functional example

```basic
Tile = GET(10,10,64,64)
PUT (100,100), Tile
PUT (50,50), GET(150,150,10,10)
```

#### See also

PUT, BSAVE, BLOAD

### PUT

Draws an image value or a direct `GET(...)` capture at a destination coordinate.

#### Syntax

```text
PUT (x,y), image
PUT (x,y), GET(source_x,source_y,width,height)
```

#### Functional example

```basic
SCREEN 320,240
PUT (50,50), GET(150,150,10,10)
```

#### See also

GET, BSAVE, BLOAD

### BSAVE

Preserves classic memory-range binary saving and also saves portable graphical images. The image format is inferred from the filename extension; PNG is the preferred format.

#### Syntax

```text
BSAVE filename, address, length
BSAVE filename, SCREEN
BSAVE filename, image
BSAVE filename, GET(x,y,width,height)
BSAVE filename, GET (x1,y1)-(x2,y2)
```

#### Functional example

```basic
SCREEN 640,480
LINE (0,0)-(639,479),14
BSAVE "screen.png", SCREEN
BSAVE "part.png", GET(0,0,100,100)
```

#### See also

BLOAD, GET, PUT

### BLOAD

Preserves classic binary loading and can load an image into a variable or directly onto the graphics screen.

#### Syntax

```text
BLOAD filename, address
BLOAD filename, image_variable
BLOAD filename, SCREEN [, x, y]
```

#### Functional example

```basic
BLOAD "sprite.png", sprite
PUT (100,80), sprite
```

#### See also

BSAVE, GET, PUT

### CHART

Draws a chart into the current graphics surface using the backend-neutral Sum chart model. Supported kinds are BAR, HBAR, LINE, SCATTER, PIE and RADAR.

#### Syntax

```text
CHART kind,x,y,width,height,categories,values [,title [,series_name]]
CHART kind TITLE title X categories Y values [AT x,y] [SIZE width,height] [FONT SIZE n] [TITLE FONT SIZE n] [RENDERER native|matplotlib|seaborn]
```

A physical line ending in `\` or `_` continues on the next line. The named form lowers to the same backend-neutral `ChartSpec` used by Python and SumGUI. Matplotlib and Seaborn are optional renderers; the native SumGUI renderer remains the dependency-light default.

#### Functional example

```basic
DISPLAY 640,480,65536,AUTO
CHART BAR \
    TITLE "Users by OS" \
    X "Android","Linux","Windows" \
    Y 500,800,600 \
    FONT SIZE 10 \
    RENDERER "native"
PAUSE 0
```

#### See also

TABLE, BSAVE

### TABLE

Draws a formatted table with optional title into the current graphics surface.

#### Syntax

```text
TABLE x,y,width,height,headers,rows [,title]
```

#### Functional example

```basic
SCREEN 640,480
TABLE 20,20,300,160,["OS","Users"],[["Android",500],["Linux",800]],"Usage"
```

#### See also

CHART, BSAVE


### DISPLAY

Creates a modern arbitrary-resolution graphics display. Unlike historical `SCREEN` modes, `DISPLAY` is not limited to legacy resolutions or palette sizes. `AUTO` presents each drawing command immediately; `MANUAL` keeps drawing off-screen until `DISPLAY UPDATE`.

#### Syntax

```text
DISPLAY width,height,colors_or_bits,AUTO|MANUAL [,pages [,active_page [,visible_page]]]
DISPLAY ACTIVE page
DISPLAY VISIBLE page
DISPLAY UPDATE
```

Use a `BIT` suffix to specify bit depth explicitly, for example `24BIT` or `32BIT`. A numeric value such as `65536` means number of colors.

#### Functional example

```basic
DISPLAY 640,480,65536,MANUAL,2,1,0
LINE (0,0)-(639,479),11
DISPLAY VISIBLE 1
DISPLAY UPDATE
```

#### See also

SCREEN, COPY, FONT

### SCREEN

Selects a historical BASIC graphics profile or text mode. `SCREEN 12` is 640x480 with 16 colors and `SCREEN 13` is 320x200 with 256 colors. Active and visible pages are preserved as separate concepts.

#### Syntax

```text
SCREEN 0
SCREEN 12 [,colorswitch [,active_page [,visible_page]]]
SCREEN 13 [,colorswitch [,active_page [,visible_page]]]
SCREEN "SPECTRUM"
```

#### Functional example

```basic
SCREEN 12,,1,0
LINE (10,10)-(200,100),11
```

#### See also

DISPLAY, COPY

### COPY SCREEN

Copies a complete graphics page to another page.

#### Syntax

```text
COPY SCREEN FROM source_page TO destination_page
COPY SCREEN source_page TO destination_page
```

#### Functional example

```basic
DISPLAY 320,240,256,MANUAL,2,1,0
LINE (0,0)-(319,239),11
COPY SCREEN FROM 1 TO 0
DISPLAY VISIBLE 0
DISPLAY UPDATE
```

#### See also

DISPLAY, SCREEN

### FONT

Sets the default graphical font. Charts, tables and text inherit it unless they provide a more specific font size/family.

#### Syntax

```text
FONT family,size [,bold [,italic [,underline]]]
```

#### Functional example

```basic
DISPLAY 640,480,65536,AUTO
FONT "monospace",12
OUTTEXTXY 20,20,"Sum",15
```

#### See also

OUTTEXTXY, CHART, TABLE

### ARC

Draws a circular arc using BGI-style start/end angles in degrees.

#### Syntax

```text
ARC x,y,start_angle,end_angle,radius [,color]
```

#### Functional example

```basic
DISPLAY 320,240,256,AUTO
ARC 160,120,220,320,60,15
```

#### See also

CIRCLE, ELLIPSE

### ELLIPSE

Draws an ellipse or elliptical arc.

#### Syntax

```text
ELLIPSE x,y,start_angle,end_angle,rx,ry [,color]
```

#### Functional example

```basic
DISPLAY 320,240,256,AUTO
ELLIPSE 160,120,0,360,80,40,11
```

#### See also

ARC, CIRCLE

### OUTTEXTXY

Draws text at pixel coordinates on the graphics surface.

#### Syntax

```text
OUTTEXTXY x,y,text [,color [,size [,font_family]]]
```

#### Functional example

```basic
DISPLAY 640,480,65536,AUTO
OUTTEXTXY 20,20,"Hello from sumBASIC",15,14,"monospace"
```

#### See also

FONT

### GOTOXY

Moves the text cursor using the classic `conio.h` order `X,Y`. Coordinates are one-based. `LOCATE Y,X` reaches the same logical cell. Spectrum-compatible `PRINT AT Y,X; ...` keeps the historical zero-based AT coordinates.

#### Syntax

```text
GOTOXY x,y
LOCATE y,x
PRINT AT y,x; expression
```

#### Functional example

```basic
GOTOXY 10,5
PRINT "GOTOXY"
LOCATE 7,10
PRINT "LOCATE"
PRINT AT 8,9; "PRINT AT"
```

#### See also

LOCATE, PRINT
