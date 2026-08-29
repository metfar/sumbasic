#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#pylint:disable=W0301
#  
#  Copyright 2018- William Martinez Bas <metfar@gmail.com>
#  
#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 2 of the License, or
#  (at your option) any later version.
#  
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#  
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software
#  Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#  MA 02110-1301, USA.
#  

ZX_SPECTRUM_PI = 3.1415927;

# Stable positions in the supplied asc_h.py super-extended ASC table.
ASC_BASIC_CODES = {
    512: "RND", 513: "INKEY$", 514: "PI", 515: "FN", 516: "POINT", 517: "SCREEN$", 518: "ATTR", 519: "AT",
    520: "TAB", 521: "VAL$", 522: "CODE", 523: "VAL", 524: "LEN", 525: "SIN", 526: "COS", 527: "TAN",
    528: "ASN", 529: "ACS", 530: "ATN", 531: "LN", 532: "EXP", 533: "INT", 534: "SQR", 535: "SGN",
    536: "ABS", 537: "PEEK", 538: "IN", 539: "USR", 540: "STR$", 541: "CHR$", 542: "NOT", 543: "BIN",
    544: "OR", 545: "AND", 546: "<<", 547: "<", 548: "<=", 549: ">=", 550: ">>", 551: ">", 552: "<>",
    553: "LINE", 554: "THEN", 555: "TO", 556: "STEP", 557: "DEF FN", 558: "CAT", 559: "FORMAT", 560: "MOVE",
    561: "ERASE", 562: "OPEN #", 563: "CLOSE #", 564: "MERGE", 565: "VERIFY", 566: "BEEP", 567: "CIRCLE",
    568: "INK", 569: "PAPER", 570: "FLASH", 571: "BRIGHT", 572: "INVERSE", 573: "OVER", 574: "OUT",
    575: "LPRINT", 576: "LLIST", 577: "STOP", 578: "READ", 579: "DATA", 580: "RESTORE", 581: "NEW",
    582: "BORDER", 583: "CONTINUE", 584: "DIM", 585: "REM", 586: "FOR", 587: "GOTO", 588: "GOSUB",
    589: "INPUT", 590: "LOAD", 591: "LIST", 592: "LET", 593: "PAUSE", 594: "NEXT", 595: "POKE",
    596: "PRINT", 597: "PLOT", 598: "RUN", 599: "SAVE", 600: "RANDOMIZE", 601: "IF", 602: "CLS",
    603: "DRAW", 604: "CLEAR", 605: "RETURN", 606: "COPY", 607: "EDIT", 608: "RENUM", 609: "DELETE",
    610: "WIDTH", 611: "UDG", 612: "FREE", 613: "ON ERROR", 614: "RESET", 615: "SOUND", 616: "PLAY",
    617: "HELP", 618: "TRY", 619: "CATCH", 620: "EXCEPT", 621: "ELSE", 622: "END IF", 623: "LISTEN",
    624: "ACT", 625: "SHOW", 626: "LINE", 627: "RECTANGLE", 628: "POLYGON", 629: "ELLIPSE", 630: "SPACE$",
    631: "LEFT$", 632: "RIGHT$", 633: "MID$", 634: "MEMORY", 635: "DISPLAY", 636: "RESERVE", 637: "ALIAS",
    638: "POINTER", 639: "BLOAD", 640: "BSAVE", 641: "ASC", 642: "SHELL", 643: "SYSTEM", 644: "SHELL",
    645: "DIR", 646: "TREE", 647: "MKDIR", 648: "CHDIR", 649: "RMDIR", 650: "RMFILE", 651: "TOUCH",
    652: "CREATE-SCR", 653: "SELECT-SCR", 654: "WRITE-SCR", 655: "REPRESENT-SCR",
};

# Appended to the supplied ASC table in asc_h-sumbasic-0.1.0a5.py so no
# historical index is shifted.  The supplied table contained 2990 entries.
ASC_MODERN_START = 2990;
ASC_MODERN_WORDS = [
    "SUB", "END SUB", "FUNCTION", "END FUNCTION", "CALL", "WITH", "SHARED", "REDIM", "PRESERVE", "OPTION", "BASE", "AS",
    "BOOLEAN", "INTEGER", "LONG", "SINGLE", "DOUBLE", "DECIMAL", "BYTES", "ANY", "ARRAY", "DICT", "SET", "TUPLE", "EACH",
    "WHILE", "WEND", "DO", "LOOP", "UNTIL", "SWAP", "LOCATE", "FIELD", "GET", "PUT", "WRITE", "FREEFILE", "EOF", "LOF",
    "LOC", "STDIN", "STDOUT", "STDERR", "CHANNEL", "SELECT CASE", "CASE", "END SELECT", "MOD", "XOR", "TRUE", "FALSE", "SCREEN",
    "LBOUND", "UBOUND", "END",
    "DIV", "FIX", "LOG", "SQRT", "CBRT", "ROOT", "POW", "SQUARE", "CUBE", "COT", "SEC", "CSC",
    "ASIN", "ACOS", "ATAN", "ATN2", "ATAN2", "SINH", "COSH", "TANH", "ASNH", "ACSH", "ATNH", "ASINH",
    "ACOSH", "ATANH", "LOG10", "LOG2", "TRUNC", "FLOOR", "CEIL", "ROUND", "FRAC", "MIN", "MAX", "CLAMP",
    "HYPOT", "RAD", "RADIANS", "DEG", "DEGREES", "GCD", "LCM", "FACT", "FACTORIAL", "COMB", "PERM", "GAMMA",
    "LGAMMA", "ERF", "ERFC", "ISFINITE", "ISINF", "ISNAN", "BAND", "BOR", "BXOR", "BNOT", "SHL", "SHR",
    "IDIV", "SIGN", "HEX$", "OCT$", "INSTR", "STRING$", "LCASE$", "UCASE$", "LTRIM$", "RTRIM$",
    "COMPLEX", "CMPLX", "REAL", "IMAG", "CONJ", "CONJUGATE", "PHASE", "ARG", "MAG", "NORM", "POLAR", "ISCOMPLEX",
    "TIME$", "TIMER", "LOGB", "LOGBASE",
];
ASC_MODERN_CODES = {ASC_MODERN_START + index: word for index, word in enumerate(ASC_MODERN_WORDS)};

GRAPHICS_STUBS = {
    "SCREEN", "PLOT", "DRAW", "LINE", "CIRCLE", "INK", "PAPER", "FLASH", "BRIGHT", "INVERSE", "OVER", "BORDER", "UDG",
    "DISPLAY", "SHOW", "RECTANGLE", "POLYGON", "ELLIPSE", "CREATE-SCR", "SELECT-SCR", "WRITE-SCR", "REPRESENT-SCR",
};

GRAPHICS_FUNCTION_STUBS = {"POINT", "SCREEN$", "ATTR"};
