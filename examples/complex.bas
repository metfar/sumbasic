# Complex-number arithmetic in sumBASIC.
DIM Z AS COMPLEX
DIM W AS COMPLEX

Z = COMPLEX(3, 4)
W = COMPLEX(1, -2)

PRINT "Z = "; Z
PRINT "W = "; W
PRINT "Z + W = "; Z + W
PRINT "Z * W = "; Z * W
PRINT "Z / W = "; Z / W
PRINT "ABS(Z) = "; ABS(Z)
PRINT "REAL(Z) = "; REAL(Z)
PRINT "IMAG(Z) = "; IMAG(Z)
PRINT "CONJ(Z) = "; CONJ(Z)
PRINT "PHASE(Z) = "; PHASE(Z)
PRINT "SQR(COMPLEX(-1,0)) = "; SQR(COMPLEX(-1, 0))
PRINT "EXP(COMPLEX(0,PI)) = "; EXP(COMPLEX(0, PI))
