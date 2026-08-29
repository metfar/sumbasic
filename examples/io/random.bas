OPEN "people.dat" FOR RANDOM AS #1 LEN=40
FIELD #1, 24 AS name$, 8 AS born$, 8 AS height$
name$="John O'Connor": born$="19850228": height$="1.82"
PUT #1, 1
name$="": born$="": height$=""
GET #1, 1
PRINT name$; " "; born$; " "; height$
CLOSE #1
