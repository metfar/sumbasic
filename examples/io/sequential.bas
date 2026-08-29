OPEN "people.txt" FOR OUTPUT AS #1
WRITE #1, "Ada", 37
CLOSE #1
OPEN "people.txt" FOR INPUT AS #A
INPUT #A, name$, age!
CLOSE #A
PRINT name$; " "; age!
