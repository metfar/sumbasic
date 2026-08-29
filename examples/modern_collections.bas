DIM SHARED Font AS DICT
DIM Rows AS LIST

Rows = [4, 10, 17, 17, 31, 17, 17]
Font["A"] = Rows

PRINT "Rows in A: "; LEN(Font["A"])
FOR EACH Row! IN Font["A"]
PRINT Row!;
NEXT Row!
PRINT
