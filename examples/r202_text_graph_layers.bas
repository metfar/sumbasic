# r20.2 demo: independent text grid and graphics plane plus z-order layers.
DISPLAY (640, 480, 16, AUTO)
PAPER 0
BORDER 1
CLS
PRINT "Text grid: "; COLS; "x"; ROWS
PRINT "Graphics: "; GWIDTH; "x"; GHEIGHT; " colors="; GCOLORS
GPRINT 40, 60, "GPRINT uses graphics coordinates", 15, 18
GPRINTF 40, 90, "GWIDTH=%d GHEIGHT=%d", GWIDTH, GHEIGHT
SORT LAYERS GRAPHICS, TEXT
PAUSE .5
SORT LAYERS GRAPHICS, BORDER, TEXT
PAUSE .5
CLEAR GRAPHLAYER
GPRINT 40, 120, "GRAPHICS layer cleared independently", 10, 16
PAUSE .5
CLEAR TEXTLAYER
PRINT "Text layer was cleared; graphics remains."
PAUSE 1
