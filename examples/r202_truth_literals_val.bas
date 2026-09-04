# r20.2 demo: BASIC truth values, modern literals, base strings and VAL.
PRINT "TRUE="; TRUE; " FALSE="; FALSE
PRINT "Move left delta="; ("izquierda" = "izquierda") - ("izquierda" = "derecha")
PRINT "AND mask: "; 0x55 AND TRUE
PRINT "hex: "; &H1FF; " = "; 0x1FF
PRINT "bin: "; %11101; " = "; 0b11101; " = "; BIN 11101
PRINT "oct: "; &O777; " = "; 0o777
PRINT "HEX$="; HEX$(255,4); " OCT$="; OCT$(255,4); " BIN$="; BIN$(5,8)
PRINT "VAL U="; VAL("   U -1.5p6")
PRINT "VAL LUN="; VAL("   LUN 1.5-6")
PRINT "VAL accounting="; VAL("USD 10-")
PRINT "VAL first sign="; VAL("+10-")
PRINT "VAL exponent="; VAL("45.3e-6")
PRINT "EVAL 2+2="; EVAL("2+2"); " ; VAL 2+2="; VAL("2+2")
