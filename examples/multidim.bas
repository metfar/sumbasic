# Four-dimensional classic BASIC array.
# With OPTION BASE 0, DIM A$(5,7,3,8) has bounds 0..5, 0..7, 0..3, 0..8.
DIM A$(5, 7, 3, 8)
A$(2, 4, 1, 6) = "X"
PRINT A$(2, 4, 1, 6)
PRINT LBOUND(A$, 1); ":"; UBOUND(A$, 1)
