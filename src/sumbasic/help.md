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
```

#### Functional example

```basic
SCREEN 640,480
C = ["Android","Linux","Windows"]
V = [500,800,600]
CHART "BAR",20,20,280,200,C,V,"Users","Users"
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

