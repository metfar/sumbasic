#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
#  asc_h.py
#  
#  Copyright 2020 William Martinez Bas <metfar@gmail.com>
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
#  
import platform;

WINDOWS="nt";
LINUX="x";
ASC_H=True;

if ("win" in platform.system().lower()):
	def O_S():
		global WIN,LIN;
		WIN=True;
		LIN=False;
		return(WINDOWS);
else:
	def O_S():
		global WIN,LIN;
		WIN=False;
		LIN=True;
		return(LINUX);
OS=O_S();

if (LIN):
	LEFT_ARR,RIGHT_ARR,UP_ARR,DOWN_ARR=68,67,65,66;
else:
	LEFT_ARR,RIGHT_ARR,UP_ARR,DOWN_ARR=75,77,72,80;



#   JUST TO REMEMBER "NUL","SOH","STX","ETX","EOT","ENQ","ACK","BEL","BS","HT","LF","VT","FF","CR","SO","SI","DLE","DC1","DC2","DC3","DC4","NAK","SYN","ETB","CAN","EOM","SUB","ESC","FS","GS","RS","US"

ASC=[   #0      1       2       3       4       5       6       7 
		"ø",    "☺",    "☻",    "♥",    "♦",    "♣",    "♠",    "●", 
		#8      9       10      11      12      13      14      15
		"◘",    "◦",    "◙",    "♂",    "♀",    "♪",    "♫",    "✶",
		#16     17      18      19      20      21      22      23
		"►",    "◄",    "↕",    "‼",    "¶",    "§",    "‗",    "↨",
		#24     25      26      27      28      29      30      31
		"↑",    "↓",    "→",    "←",    "∟",    "↔",    "▲",    "▼",
		#32     33      34      35      36      37      38      39
		" ",    "!",    '"',    "#",    "$",    "%",    "&",    "'",
		#40     41      42      43      44      45      46      47
		"(",    ")",    "*",    "+",    ",",    "-",    ".",    "/",
		#48     49      50      51      52      53      54      55
		"0",    "1",    "2",    "3",    "4",    "5",    "6",    "7",
		#56     57      58      59      60      61      62      63
		"8",    "9",    ":",    ";",    "<",    "=",    ">",    "?",
		#64     65      66      67      68      69      70      71
		"@",    "A",    "B",    "C",    "D",    "E",    "F",    "G",
		#72     73      74      75      76      77      78      79
		"H",    "I",    "J",    "K",    "L",    "M",    "N",    "O",
		#80     81      82      83      84      85      86      87
		"P",    "Q",    "R",    "S",    "T",    "U",    "V",    "W",
		#88     89      90      91      92      93      94      95
		"X",    "Y",    "Z",    "[",    "\\",   "]",    "^",    "_",
		#96     97      98      99      100     101     102     103
		"`",    "a",    "b",    "c",    "d",    "e",    "f",    "g",
		#104    105     106     107     108     109     110     111
		"h",    "i",    "j",    "k",    "l",    "m",    "n",    "o",
		#112    113     114     115     116     117     118     119
		"p",    "q",    "r",    "s",    "t",    "u",    "v",    "w",
		#120    121     122     123     124     125     126     127
		"x",    "y",    "z",    "{",    "|",    "}",    "~",    "⌂",
		#128    129     130     131     132     133     134     135
		"Ç",    "ü",    "é",    "â",    "ä",    "à",    "å",    "ç",
		#136    137     138     139     140     141     142     143
		"ê",    "ë",    "è",    "ï",    "î",    "ì",    "Ä",    "Å",
		#144    145     146     147     148     149     150     151
		"É",    "æ",    "Æ",    "ô",    "ö",    "ò",    "û",    "ù",
		#152    153     154     155     156     157     158     159
		"ÿ",    "Ö",    "Ü",    "¢",    "£",    "¥",    "₧",    "ƒ",
		#160    161     162     163     164     165     166     167
		"á",    "í",    "ó",    "ú",    "ñ",    "Ñ",    "ª",    "º",
		#168    169     170     171     172     173     174     175
		"¿",    "⌐",    "¬",    "½",    "¼",    "¡",    "«",    "»",
		#176    177     178     179     180     181     182     183
		"░",    "▒",    "▓",    "│",    "┤",    "┥",    "┨",    "┒",
		#184    185     186     187     188     189     190     191
		"┑",    "┫",    "┃",    "┓",    "┛",    "┚",    "┙",    "┐",
		#192    193     194     195     196     197     198     199
		"└",    "┴",    "┬",    "├",    "─",    "┼",    "┝",    "┠",
		#200    201     202     203     204     205     206     207
		"┗",    "┏",    "┻",    "┳",    "┣",    "━",    "╋",    "┷",
		#208    209     210     211     212     213     214     215
		"┸",    "┯",    "┰",    "┖",    "┕",    "┍",    "┎",    "╂",
		#216    217     218     219     220     221     222     223
		"┿",    "┘",    "┌",    "█",    "▄",    "▌",    "▐",    "▀",
		#224    225     226     227     228     229     230     231
		"α",    "ß",    "Γ",    "π",    "Σ",    "σ",    "μ",    "τ",
		#232    233     234     235     236     237     238     239
		"Φ",    "Θ",    "Ω",    "δ",    "∞",    "ø",    "ε",    "∩",
		#240    241     242     243     244     245     246     247
		"≡",    "±",    "≥",    "≤",    "⌠",    "⌡",    "÷",    "≈",
		#248    249     250     251     252     253     254     255
		"°",    "·",    "∙",    "√",    "ⁿ",    "²",    "■",    "◌",
		#256    257     258     259     260     261     262     263
		'¤',    '¦',    '¨',    '©',    '®',    '¯',    '³',    '´',
		#264    265     266     267     268     269     270     271
		'µ',    '¸',    '¹',    '¾',    'À',    'Á',    'Â',    'Ã',
		#272    273     274     275     276     277     278     279
		'È',    'Ê',    'Ë',    'Ì',    'Í',    'Î',    'Ï',    'Ð'
		#280    281     282     283     284     285     286     287,
		'Ò',    'Ó',    'Ô',    'Õ',    '×',    'Ø',    'Ù',    'Ú',
		#288    289     290     291     292     293     294     295
		'Û',    'Ý',    'Þ',    'ã',    'ð',    'õ',    'ý',    'þ',
		#296    297     298     299     300     301     302     303
		'ã',    'ð',    'õ',    'ý',    'þ',    'Ā',    'ā',    'Ă',
		#304    305     306     307     308     309     310     311
		'ă',    'Ą',    'ą',    'Ć',    'ć',    'Ĉ',    'ĉ',    'Ċ',
		#312    313     314     315     316     317     318     319
		'ċ',    'Č',    'č',    'Ď',    'ď',    'Đ',    'đ',    'Ē',
		#320    321     322     323     324     325     326     327
		'ē',    'Ĕ',    'ĕ',    'Ė',    'ė',    'Ę',    'ę',    'Ě',
		#328
		'ě',    'Ĝ',    'ĝ',    'Ğ',    'ğ',    'Ġ',    'ġ',    'Ģ',
		#336
		'ģ',    'Ĥ',    'ĥ',    'Ħ',    'ħ',    'Ĩ',    'ĩ',    'Ī',
		#344
		'ī',    'Ĭ',    'ĭ',    'Į',    'į',    'İ',    'ı',    'Ĳ',
		#352
		'ĳ',    'Ĵ',    'ĵ',    'Ķ',    'ķ',    'ĸ',    'Ĺ',    'ĺ',
		#360
		'Ļ',    'ļ',    'Ľ',    'ľ',    'Ŀ',    'ŀ',    'Ł',    'ł',
		#368
		'Ń',    'ń',    'Ņ',    'ņ',    'Ň',    'ň',    'ŉ',    'Ŋ',
		#376
		'ŋ',    'Ō',    'ō',    'Ŏ',    'ŏ',    'Ő',    'ő',    'Œ',
		#384
		'œ',    'Ŕ',    'ŕ',    'Ŗ',    'ŗ',    'Ř',    'ř',    'Ś',
		#392
		'ś',    'Ŝ',    'ŝ',    'Ş',    'ş',    'Š',    'š',    'Ţ',
		#400
		'ţ',    'Ť',    'ť',    'Ŧ',    'ŧ',    'Ũ',    'ũ',    'Ū',
		#408
		'ū',    'Ŭ',    'ŭ',    'Ů',    'ů',    'Ű',    'ű',    'Ų',
		#416
		'ų',    'Ŵ',    'ŵ',    'Ŷ',    'ŷ',    'Ÿ',    'Ź',    'ź',
		#424
		'Ż',    'ż',    'Ž',    'ž',    '⏩',    '⏪',    '⏫',    '⏬',
		#432
		'⏭',    '⏮',    '⏯',    '▇',    '▉',    '▊',    '▖',    '▗',
		#440
		'▘',    '▙',    '▚',    '▛',    '▜',    '▝',    '▞',    '▟',
		#448
		'⏸',    '⮠',    '⮡',    '⮢',    '⮣',    '⮤',    '⮥',    '⮦',
		#456
		'⮧',    '⯅',    '⯆',    '⯇',    '⯈',     'ⴸ',    'ⴹ',    'ⴺ',
		#464    465
		"Α",    "α",        #alpha
		#466    467
		"Β",    "β",        #beta
		#468    469
		"Γ",    "γ",        #gamma
		#470    471
		"Δ",    "δ",        #delta
		#472    473
		"Ε",    "ε",        #epsilon
		#474    475
		"Ζ",    "ζ",        #zêta
		#476    477
		"Η",    "η",        #êta
		#478    479
		"Θ",    "θ",        #thêta
		#480    481
		"Ι",    "ι",            #iota
		#482    483
		"Κ",    "κ",        #kappa
		#484    485
		"Λ",    "λ",        #lambda
		#486    487
		"Μ",    "μ",        #mu
		#488    489
		"Ν",    "ν",        #nu
		#490    491
		"Ξ",    "ξ",        #xi
		#492    493
		"Ο",    "ο",        #omikron
		#494    495
		"Π",    "π",        #pi
		#496    497
		"Ρ",    "ρ",        #rho
		#498    499
		"Σ",    "σ","ς",    #sigma
		#500    501 502
		"Τ",    "τ",        #tau
		#503    504
		"Υ",    "υ",        #upsilon
		#505    506
		"Φ",    "φ",        #phi
		#507    508
		"Χ",    "χ",        #chi
		#509    510
		"Ψ",    "ψ",        #psi
		#511    512
		"Ω",    "ω",        #omega
		#513    514
		"RND ",     "INKEY$ ",      "PI ",      "FN ",
		#515            516                 517         518
		"POINT ","SCREEN$ ",    "ATTR ",    "AT ",
		#519            520                     521         522
		"TAB ",     "VAL$ ",            "CODE " ,   "VAL ",
		#523            524                 525         526
		"LEN ",     "SIN ",             "COS ",     "TAN ",
		#527            528                 529         530
		"ASN ",     "ACS ",             "ATN ",     "LN ",
		#531            532                 533         534
		"EXP ",     "INT ",             "SQR ",     "SGN ",
		#535            536                 537         538
		"ABS ",     "PEEK ",            "IN ",      "USR ",
		#539            540                     541         542
		"STR$ ",    "CHR$ ",            "NOT ",     "BIN ",
		#543            544                 545         546
		"OR ",      "AND ",             "<< ",          "< ",
		#547            548                 549         550
		"<= ",      ">= ",      ">> ",      "> ",
		#551            552         553             554
		"<> ",      "LINE ",    "THEN ",    "TO ",
		#555            556         557             558
		"STEP ",    "DEF FN ",  "CAT ",     "FORMAT ",
		#559            560             561         562
		"MOVE ",    "ERASE ",   "OPEN #",   "CLOSE #",
		#563            564         565         566
		"MERGE ",   "VERIFY ",  "BEEP ",    "CIRCLE ",
		#567            568             569         570
		"INK ",     "PAPER ",   "FLASH ",   "BRIGHT ",
		#571            572         573         574
		"INVERSE ", "OVER ",    "OUT ",     "LPRINT ",
		#575            576         577         578
		"LLIST ",   "STOP ",    "READ ",    "DATA ",
		#579            580         581         582
		"RESTORE ", "NEW ",     "BORDER ",  "CONTINUE ",
		#583            584         585         586 
		"DIM ",     "REM ",     "FOR ",     "GOTO ",
		#587            588         589         589
		"GOSUB ",   "INPUT ",   "LOAD ",    "LIST ",
		#590            591         592         593
		"LET ",     "PAUSE ",   "NEXT ",    "POKE ",
		#594            595         596         597
		"PRINT ",   "PLOT ",    "RUN ",     "SAVE ",
		#598            599         600         601
		"RANDOMIZE ","IF ",     "CLS ",     "DRAW ",
		#602            603         604         605
		"CLEAR ",   "RETURN ",  "COPY ",    "EDIT ",
		#606            607         608         609
		"RENUM ",   "DELETE ",  "WIDTH ",   "UDG ",
		#610            611         612         613
		"FREE ",    "ON ERROR", "RESET ",   "SOUND ",
		#614            615         616         617
		"PLAY ",    "HELP ",    "TRY "  ,   "CATCH ",
		#618            619         620         621
		"EXCEPT ",  "ELSE ",    "END  IF  ",
		#622            623         624         625
		"LISTEN ",  "ACT ", "SHOW ",    "LINE  ",
		#626            627         628         629
		"RECTANGLE  ",      "POLYGON ", "ELLIPSE    ",
		#630            631                     632         633 
		"SPACE$ ",  "LEFT$ ",   "RIGHT$  ", "MID$ ",
		#634                    635                     636         637     
		"MEMORY  ", "DISPLAY  ",    "RESERVE ", "ALIAS  ",
		#638                    639                 640         641
		"POINTER  ",    "BLOAD ",   "BSAVE ",   "ASC ",
		#642                643             644             645
		"SHELL ", "SYSTEM ", "SHELL ", "DIR ",
		#646            647             648             649
		"TREE ","MKDIR ","CHDIR  ","RMDIR ",
		#650                651
		"RMFILE ","TOUCH ",
		"CREATE-SCR ",      #652 CREATE SCREEN BUFFER
		"SELECT-SCR ",      #653 SELECT VARIABLE AS SCREEN
		"WRITE-SCR ",           #654 WRITE ON SCREEN
		"REPRESENT-SCR ",#655 PRINT SCREN TO DISPLAY
		#656    657     658     659 
		"¬",    "¢",    "£",    "¥",
		#660    661     662     663
		"”",    "¦",        "§",        "‰",
		#664    665     667     668
		"«",    "»",    "↔",    "ð",
		#669    670     671     672
		"Ð",    "ƒ",        "ø",    "Ø",
		#673    674     675     676
		"œ",    "Œ",    "š",        "Š",
		#677    678     679     680
		"ß",    "™",    "º",        "ª",
		#681    682     683     684
		"°",        "∂",        "¤",        "∞",
		#685    686     687     688
		"½",    "↉",    "⅓",    "⅔",    
		#689    690
		"¼",    "¾",
		#691    692     693     694
		"⅕",    "⅖",    "⅗",    "⅘",
		#695    696
		"⅙",    "⅚",    
		#697
		"⅐",    
		#698    699     670     671
		"⅛" ,   "⅜",    "⅝",    "⅞",
		#672    673
		"⅑",    "⅒",    
		#674    675     676     677
		"⁰",        "¹",        "²",        "³",
		#678    679     680     681
		"⁴",        "⁵",        "⁶",        "⁷",
		#682    683     684     685
		"⁸",        "⁹",        "⁺",        "⁻",
		#686    687     688     689
		"⁼",        "⁽",        "⁾",        "ⁱ",
		#690
		"ⁿ",
		#691    692     693     694
		"₀",        "₁",        "₂",        "₃",
		#695    696     697     698
		"₄",        "₅",        "₆",        "₇",
		#699    700     701     702
		"₈",        "₉",        "₊",        "₋",
		#703    704     705     706
		"₌",        "₍",        "₎",        "ₐ",
		#707    708     709     710
		"ₑ",        "ₒ",        "ₓ",        "ₔ",
		#711    712     713     714
		"ₕ",        "ₖ",        "ₗ",        "ₘ",
		#715    716     717     718
		"ₙ",        "ₚ",        "ₛ",        "ₜ",
		
		#MATH
		"≌",    #719 ALL EQUAL TO
		"≊",    #720 ALMOST EQUAL OR EQUAL TO
		"≈",    #721 ALMOST EQUAL TO
		"∠",    #722 ANGLE
		"∳",        #723 ANTICLOCKWISE CONTOUR INTEGRAL
		"≐",    #724 APPROACHES THE LIMIT
		"≆",    #725 APPROXIMATELY BUT NOT ACTUALLY EQUAL TO
		"≅",    #726 APPROXIMATELY EQUAL TO
		"≒",    #727 APPROXIMATELY EQUAL TO OR THE IMAGE OF
		"⊦",        #728 ASSERTION
		"∗",    #729 ASTERISK OPERATOR
		"≃",    #730 ASYMPTOTICALLY EQUAL TO
		"∵",    #731 BECAUSE
		"≬",        #732 BETWEEN
		"⋈",    #733 BOWTIE
		"∙",        #734 BULLET OPERATOR
		"⊛",    #735 CIRCLED ASTERISK OPERATOR
		"⊝",    #736 CIRCLED DASH
		"⊘",    #737 CIRCLED DIVISION SLASH
		"⊙",    #738 CIRCLED DOT OPERATOR
		"⊜",    #738 CIRCLED EQUALS
		"⊖",    #740 CIRCLED MINUS
		"⊕",    #741 CIRCLED PLUS
		"⊚",    #742 CIRCLED RING OPERATOR
		"⊗",    #743 CIRCLED TIMES
		"∲",        #744 CLOCKWISE CONTOUR INTEGRAL
		"∱",        #745 CLOCKWISE INTEGRAL
		"≔",    #746 COLON EQUALS
		"∁",    #747 COMPLEMENT
		"∋",    #748 CONTAINS AS MEMBER
		"⊳",    #749 CONTAINS AS NORMAL SUBGROUP
		"⊵",    #750 CONTAINS AS NORMAL SUBGROUP OR EQUAL TO
		"⋺",    #751 CONTAINS WITH LONG HORIZONTAL STROKE
		"⋽",    #752 CONTAINS WITH OVERBAR
		"⋻",    #753 CONTAINS WITH VERTICAL BAR AT END OF HORIZONTAL STROKE
		"∮",        #754 CONTOUR INTEGRAL
		"≘",    #755 CORRESPONDS TO
		"∛",    #756 CUBE ROOT
		"⋏",    #757 CURLY LOGICAL AND
		"⋎",    #758 CURLY LOGICAL OR
		"≜",    #759 DELTA EQUAL TO
		"⋄",        #760 DIAMOND OPERATOR
		"≏",    #761 DIFFERENCE BETWEEN
		"∣",        #762 DIVIDES
		"∕",        #763 DIVISION SLASH
		"⋇",    #764 DIVISION TIMES
		"∌",    #765 DOES NOT CONTAIN AS MEMBER
		"⋫",    #766 DOES NOT CONTAIN AS NORMAL SUBGROUP
		"⋭",    #767 DOES NOT CONTAIN AS NORMAL SUBGROUP OR EQUAL
		"∤",        #768 DOES NOT DIVIDE
		"⊮",    #769 DOES NOT FORCE
		"⊀",    #770 DOES NOT PRECEDE
		"⋠",    #771 DOES NOT PRECEDE OR EQUAL
		"⊬",    #772 DOES NOT PROVE
		"⊁",    #773 DOES NOT SUCCEED
		"⋡",    #774 DOES NOT SUCCEED OR EQUAL
		"∸",    #775 DOT MINUS
		"⋅",        #776 DOT OPERATOR
		"∔",    #777 DOT PLUS
		"∬",    #778 DOUBLE INTEGRAL
		"⋒",    #779 DOUBLE INTERSECTION
		"⋐",    #780 DOUBLE SUBSET
		"⋑",    #781 DOUBLE SUPERSET
		"⋓",    #782 DOUBLE UNION
		"⊫",    #783 DOUBLE VERTICAL BAR DOUBLE RIGHT TURNSTILE
		"⋱",    #784 DOWN RIGHT DIAGONAL ELLIPSIS
		"⊤",    #785 DOWN TACK
		"∈",    #786 ELEMENT OF
		"⋵",    #787 ELEMENT OF WITH DOT ABOVE
		"⋲",    #788 ELEMENT OF WITH LONG HORIZONTAL STROKE
		"⋶",    #789 ELEMENT OF WITH OVERBAR
		"⋹",    #790 ELEMENT OF WITH TWO HORIZONTAL STROKES
		"⋸",    #791 ELEMENT OF WITH UNDERBAR
		"⋳",    #792 ELEMENT OF WITH VERTICAL BAR AT END OF HORIZONTAL STROKE
		"∅",    #793 EMPTY SET
		"∎",    #794 END OF PROOF
		"⋕",    #795 EQUAL AND PARALLEL TO
		"≝",    #796 EQUAL TO BY DEFINITION
		"⋝",    #797 EQUAL TO OR GREATER-THAN
		"⋜",    #798 EQUAL TO OR LESS-THAN
		"⋞",    #799 EQUAL TO OR PRECEDES
		"⋟",    #800 EQUAL TO OR SUCCEEDS
		"≕",    #801 EQUALS COLON
		"≚",    #802 EQUIANGULAR TO
		"≍",    #803 EQUIVALENT TO
		"≙",    #804 ESTIMATES
		"∹",    #805 EXCESS
		"∀",    #806 FOR ALL
		"⊩",    #807 FORCES
		"∜",    #808 FOURTH ROOT
		"∺",    #809 GEOMETRIC PROPORTION
		"≑",    #810 GEOMETRICALLY EQUAL TO
		"≎",    #811 GEOMETRICALLY EQUIVALENT TO
		"≩",    #812 GREATER-THAN BUT NOT EQUAL TO
		"⋧",    #813 GREATER-THAN BUT NOT EQUIVALENT TO
		"⋛",    #814 GREATER-THAN EQUAL TO OR LESS-THAN
		"≥",    #815 GREATER-THAN OR EQUAL TO
		"≳",    #816 GREATER-THAN OR EQUIVALENT TO
		"≷",    #817 GREATER-THAN OR LESS-THAN
		"≧",    #818 GREATER-THAN OVER EQUAL TO
		"⋗",    #819 GREATER-THAN WITH DOT
		"⊹",    #820 HERMITIAN CONJUGATE MATRIX
		"∻",    #821 HOMOTHETIC
		"≡",    #822 IDENTICAL TO
		"⊷",    #823 IMAGE OF
		"≓",    #824 IMAGE OF OR APPROXIMATELY EQUAL TO
		"∆",    #825 INCREMENT
		"∞",    #826 INFINITY
		"∫",        #827 INTEGRAL
		"⊺",        #828 INTERCALATE
		"∩",    #829 INTERSECTION
		"∾",    #830 INVERTED LAZY S
		"⋉",    #831 LEFT NORMAL FACTOR SEMIDIRECT PRODUCT
		"⋋",    #832 LEFT SEMIDIRECT PRODUCT
		"⊣",    #833 LEFT TACK
		"≨",    #834 LESS-THAN BUT NOT EQUAL TO
		"⋦",    #835 LESS-THAN BUT NOT EQUIVALENT TO
		"⋚",    #836 LESS-THAN EQUAL TO OR GREATER-THAN
		"≤",    #837 LESS-THAN OR EQUAL TO
		"≲",    #838 LESS-THAN OR EQUIVALENT TO
		"≶",    #839 LESS-THAN OR GREATER-THAN
		"≦",    #840 LESS-THAN OVER EQUAL TO
		"⋖",    #841 LESS-THAN WITH DOT
		"∧",    #842 LOGICAL AND
		"∨",    #843 LOGICAL OR
		"∡",    #844 MEASURED ANGLE
		"≞",    #845 MEASURED BY
		"⋯",    #846 MIDLINE HORIZONTAL ELLIPSIS
		"−",    #847 MINUS SIGN
		"≂",    #848 MINUS TILDE
		"∓",    #849 MINUS-OR-PLUS SIGN
		"⊧",        #850 MODELS
		"≫",    #851 MUCH GREATER-THAN
		"≪",    #852 MUCH LESS-THAN
		"⊸",    #853 MULTIMAP
		"⊌",    #854 MULTISET
		"⊍",    #855 MULTISET MULTIPLICATION
		"⊎",    #856 MULTISET UNION
		"∇",    #857 NABLA
		"⊼",    #858 NAND
		"∐",    #859 N-ARY COPRODUCT
		"⋂",    #860 N-ARY INTERSECTION
		"⋀",    #861 N-ARY LOGICAL AND
		"⋁",    #862 N-ARY LOGICAL OR
		"∏",    #863 N-ARY PRODUCT
		"∑",    #864 N-ARY SUMMATION
		"⋃",    #865 N-ARY UNION
		"⊯",    #866 NEGATED DOUBLE VERTICAL BAR DOUBLE RIGHT TURNSTILE
		"⊈",    #867 NEITHER A SUBSET OF NOR EQUAL TO
		"⊉",    #868 NEITHER A SUPERSET OF NOR EQUAL TO
		"≇",    #869 NEITHER APPROXIMATELY NOR ACTUALLY EQUAL TO
		"≱",    #870 NEITHER GREATER-THAN NOR EQUAL TO
		"≵",    #871 NEITHER GREATER-THAN NOR EQUIVALENT TO
		"≹",    #872 NEITHER GREATER-THAN NOR LESS-THAN
		"≰",    #873 NEITHER LESS-THAN NOR EQUAL TO
		"≴",    #874 NEITHER LESS-THAN NOR EQUIVALENT TO
		"≸",    #875 NEITHER LESS-THAN NOR GREATER-THAN
		"⊽",    #876 NOR
		"⊲",    #877 NORMAL SUBGROUP OF
		"⊴",    #878 NORMAL SUBGROUP OF OR EQUAL TO
		"⊄",    #879 NOT A SUBSET OF
		"⊅",    #880 NOT A SUPERSET OF
		"≉",    #881 NOT ALMOST EQUAL TO
		"∉",    #882 NOT AN ELEMENT OF
		"≄",    #883 NOT ASYMPTOTICALLY EQUAL TO
		"≠",    #884 NOT EQUAL TO
		"≭",    #885 NOT EQUIVALENT TO
		"≯",    #886 NOT GREATER-THAN
		"≢",    #887 NOT IDENTICAL TO
		"≮",    #888 NOT LESS-THAN
		"⋪",    #889 NOT NORMAL SUBGROUP OF
		"⋬",    #890 NOT NORMAL SUBGROUP OF OR EQUAL TO
		"∦",        #891 NOT PARALLEL TO
		"⋢",    #892 NOT SQUARE IMAGE OF OR EQUAL TO
		"⋣",    #893 NOT SQUARE ORIGINAL OF OR EQUAL TO
		"≁",    #894 NOT TILDE
		"⊭",    #895 NOT TRUE
		"⊶",    #896 ORIGINAL OF
		"∥",        #897 PARALLEL TO
		"∂",        #898 PARTIAL DIFFERENTIAL
		"⋔",    #899 PITCHFORK
		"≺",    #900 PRECEDES
		"⋨",    #901 PRECEDES BUT NOT EQUIVALENT TO
		"≼",    #902 PRECEDES OR EQUAL TO
		"≾",    #903 PRECEDES OR EQUIVALENT TO
		"⊰",    #904 PRECEDES UNDER RELATION
		"∷",    #905 PROPORTION
		"∝",    #906 PROPORTIONAL TO
		"≟",    #907 QUESTIONED EQUAL TO
		"∶",        #908 RATIO
		"∽",    #909 REVERSED TILDE
		"⋍",    #910 REVERSED TILDE EQUALS
		"∟",    #911 RIGHT ANGLE
		"⊾",    #912 RIGHT ANGLE WITH ARC
		"⋊",    #913 RIGHT NORMAL FACTOR SEMIDIRECT PRODUCT
		"⋌",    #914 RIGHT SEMIDIRECT PRODUCT
		"⊢",    #915 RIGHT TACK
		"⊿",    #916 RIGHT TRIANGLE
		"≗",    #917 RING EQUAL TO
		"≖",    #918 RING IN EQUAL TO
		"∘",        #919 RING OPERATOR
		"∖",    #920 SET MINUS
		"∿",    #921 SINE WAVE
		"∍",    #922 SMALL CONTAINS AS MEMBER
		"⋾",    #923 SMALL CONTAINS WITH OVERBAR
		"⋼",    #924 SMALL CONTAINS WITH VERTICAL BAR AT END OF HORIZONTAL STROKE
		"∊",    #925 SMALL ELEMENT OF
		"⋷",    #926 SMALL ELEMENT OF WITH OVERBAR
		"⋴",    #927 SMALL ELEMENT OF WITH VERTICAL BAR AT END OF HORIZONTAL STROKE
		"∢",    #928 SPHERICAL ANGLE
		"⊓",    #929 SQUARE CAP
		"⊔",    #930 SQUARE CUP
		"⊏",    #931 SQUARE IMAGE OF
		"⊑",    #932 SQUARE IMAGE OF OR EQUAL TO
		"⋤",    #933 SQUARE IMAGE OF OR NOT EQUAL TO
		"⊐",    #934 SQUARE ORIGINAL OF
		"⊒",    #935 SQUARE ORIGINAL OF OR EQUAL TO
		"⋥",    #936 SQUARE ORIGINAL OF OR NOT EQUAL TO
		"√",    #937 SQUARE ROOT
		"⊡",    #938 SQUARED DOT OPERATOR
		"⊟",    #939 SQUARED MINUS
		"⊞",    #940 SQUARED PLUS
		"⊠",    #941 SQUARED TIMES
		"≛",    #942 STAR EQUALS
		"⋆",        #943 STAR OPERATOR
		"≣",    #944 STRICTLY EQUIVALENT TO
		"⊂",    #945 SUBSET OF
		"⊆",    #946 SUBSET OF OR EQUAL TO
		"⊊",    #947 SUBSET OF WITH NOT EQUAL TO
		"≻",    #948 SUCCEEDS
		"⋩",    #949 SUCCEEDS BUT NOT EQUIVALENT TO
		"≽",    #950 SUCCEEDS OR EQUAL TO
		"≿",    #951 SUCCEEDS OR EQUIVALENT TO
		"⊱",    #952 SUCCEEDS UNDER RELATION
		"⊃",    #953 SUPERSET OF
		"⊇",    #954 SUPERSET OF OR EQUAL TO
		"⊋",    #955 SUPERSET OF WITH NOT EQUAL TO
		"∯",    #956 SURFACE INTEGRAL
		"∄",    #957 THERE DOES NOT EXIST
		"∃",    #958 THERE EXISTS
		"∴",    #959 THEREFORE
		"∼",    #960 TILDE OPERATOR
		"∭",    #961 TRIPLE INTEGRAL
		"≋",    #962 TRIPLE TILDE
		"⊪",    #963 TRIPLE VERTICAL BAR RIGHT TURNSTILE
		"⊨",    #964 TRUE
		"∪",    #965 UNION
		"⋰",    #966 UP RIGHT DIAGONAL ELLIPSIS
		"⊥",    #967 UP TACK
		"⋮",    #968 VERTICAL ELLIPSIS
		"⋙",    #969 VERY MUCH GREATER-THAN
		"⋘",    #970 VERY MUCH LESS-THAN
		"∰",    #971 VOLUME INTEGRAL
		"≀",        #972 WREATH PRODUCT
		"⊻",    #973 XOR
		"⋿",    #974 Z NOTATION BAG MEMBERSHIP

		"ESCAPE ",              #975
		"LEFT-ARROW ",  #976
		"RIGHT-ARROW ", #977
		"UP-ARROW ",            #978
		"DOWN-ARROW ",  #979
		"ENTER ",                   #980
		"BACKSPACE ",       #981
		"DELETE ",              #982
		"INSERT ",              #983
		"HOME ",                    #984
		"END ",                     #985
		"CTRL ",                    #986
		"ALT ",                     #987
		"ALT-GR ",              #988
		"LEFT-SHIFT ",  #989
		"RIGHT-SHIFT ", #990
		"LEFT-TAB ",            #991
		"RIGHT-TAB ",       #992
		"CAPS-LOCK ",       #993
		"SCROLL-LOCK ", #994
		"NUM-LOCK ",            #995
		"PAGE-UP ",         #996
		"PAGE-DOWN ",       #997
		"PRINT-SCR ",       #998
		"STARTUP ",         #999
		"MENU ",                    #1000
		"LEFT-CLICK ",  #1001
		"RIGHT-CLICK ", #1002
		"DOUBLE-CLICK ",#1003
		"MIDDLE-CLICK ",#1004
		"SCROLL-UP ",       #1005
		"SCROLL-DOWN ", #1006
		"MUTE ",#k160               1007
		"VOLUME-UP ",#k176  1008
		"VOLUME-DOWN ",#k174    1009
		"MEDIA-PLAY ",#k162 1010
		"MEDIA-STOP ",#k164 1011
		"MEDIA-PREV ",#k144 1012
		"MEDIA-NEXT ",# k145    1013
		"HOME-PAGE ",#k237      1014
		"INTERNET ",#k238           1015
		"SEARCH ",#k239             1016
		"E-MAIL ",#k240             1017
		"MEDIA-OPEN ",#k241     1018
		"ℕ",    #1019
		"ℤ",    #1020
		"ℚ",    #1021
		"ℝ",    #1022
		"ℂ",    #1023
		"𝒫",    #1024
		"ℵ",    #1025
		"·",        #1026
		"•",        #1027
		"∘",        #1028
		"°",        #1029
		"º",        #1030
		"∝",    #1031 PROPORTIONAL
		"±",    #1032 PLUSMINUS
		"ᗣ",    #1033 TTO
		"ᗤ",    #1034 TTE
		"ᗧ",    #1035 TTA
		"🚀",    #1036 LAUNCH
		"💡",    #1037 IDEA
		"👻",    #1038 GHOST
		"SOFT-ESCAPE ", #1039 SOFT-ESCAPE (FIRST ESCAPE)
		"⚙",#1040 GEAR♡ 
		"🍓",#1041 
		"🍒",#1042
		"🍑",#1043
		"🍊",#1044
		"🍎",#1045
		"💣",#1046
		"☔",#1047
		"🎁",#1048
		"⚡",#1049
		"🚨",#1050
		"✈",#1051
		"💎",#1052
		"💧",#1053
		"💦",#1054
		"❄",#1055
		#1056 &h420+
		#420    1       2       3       4       5       6       7
		"𓀀",    "𓀁",    "𓀂",    "𓀃",    "𓀄",    "𓀅",    "𓀆",    "𓀇",
		#428    9       A       B       C       D       E       F
		"𓀈",    "𓀉",    "𓀊",    "𓀋",    "𓀌",    "𓀍",    "𓀎",    "𓀏",
		#430    1       2       3       4       5       6       7
		"𓀐",    "𓀑",    "𓀒",    "𓀓",    "𓀔",    "𓀕",    "𓀖",    "𓀗",
		#438    9       A       B       C       D       E       F
		"𓀘",    "𓀙",    "𓀚",    "𓀛",    "𓀜",    "𓀝",    "𓀞",    "𓀟",
		#440    1       2       3       4       5       6       7
		"𓀠",    "𓀡",    "𓀢",    "𓀣",    "𓀤",    "𓀥",    "𓀦",    "𓀧",
		#448    9       A       B       C       D       E       F
		"𓀨",    "𓀩",    "𓀪",    "𓀫",    "𓀬",    "𓀭",    "𓀮",    "𓀯",
		#450    1       2       3       4       5       6       7
		"𓀰",    "𓀱",    "𓀲",    "𓀳",    "𓀴",    "𓀵",    "𓀶",    "𓀷",
		#458    9       A       B       C       D       E       F
		"𓀸",    "𓀹",    "𓀺",    "𓀻",    "𓀼",    "𓀽",    "𓀾",    "𓀿",
		#460    1       2       3       4       5       6       7
		"𓁀",    "𓁁",    "𓁂",    "𓁃",    "𓁄",    "𓁅",    "𓁆",    "𓁇",
		#468    9       A       B       C       D       E       F
		"𓁈",    "𓁉",    "𓁊",    "𓁋",    "𓁌",    "𓁍",    "𓁎",    "𓁏",
		#470    1       2       3       4       5       6       7
		"𓁐",    "𓁑",    "𓁒",    "𓁓",    "𓁔",    "𓁕",    "𓁖",    "𓁗",
		#478    9       A       B       C       D       E       F
		"𓁘",    "𓁙",    "𓁚",    "𓁛",    "𓁜",    "𓁝",    "𓁞",    "𓁟",
		#480    1       2       3       4       5       6       7
		"𓁠",    "𓁡",    "𓁢",    "𓁣",    "𓁤",    "𓁥",    "𓁦",    "𓁧",
		#488    9       A       B       C       D       E       F
		"𓁨",    "𓁩",    "𓁪",    "𓁫",    "𓁬",    "𓁭",    "𓁮",    "𓁯",
		#490    1       2       3       4       5       6       7
		"𓁰",    "𓁱",    "𓁲",    "𓁳",    "𓁴",    "𓁵",    "𓁶",    "𓁷",
		#498    9       A       B       C       D       E       F
		"𓁸",    "𓁹",    "𓁺",    "𓁻",    "𓁼",    "𓁽",    "𓁾",    "𓁿",
		#500    1       2       3       4       5       6       7
		"𓂀",    "𓂁",    "𓂂",    "𓂃",    "𓂄",    "𓂅",    "𓂆",    "𓂇",
		#508    9       A       B       C       D       E       F
		"𓂈",    "𓂉",    "𓂊",    "𓂋",    "𓂌",    "𓂍",    "𓂎",    "𓂏",
		#510    1       2       3       4       5       6       7
		"𓂐",    "𓂑",    "𓂒",    "𓂓",    "𓂔",    "𓂕",    "𓂖",    "𓂗",
		#518    9       A       B       C       D       E       F
		"𓂘",    "𓂙",    "𓂚",    "𓂛",    "𓂜","𓂝","𓂞",    "𓂟",
		#520    1       2       3       4       5       6       7
		"𓂠","𓂡","𓂢","𓂣","𓂤","𓂥","𓂦",    "𓂧",
		#528    9       A       B       C       D       E       F
		"𓂨","𓂩","𓂪","𓂫","𓂬","𓂭",    "𓂮",    "𓂯",
		#530    1       2       3       4       5       6       7
		"𓂰",    "𓂱",    "𓂲",    "𓂳",    "𓂴",    "𓂵",    "𓂶","𓂷",
		#538    9       A       B       C       D       E       F
		"𓂸","𓂹",    "𓂺","𓂻",    "𓂼",    "𓂽",    "𓂾",    "𓂿",
		#540    1       2       3       4       5       6       7
		"𓃀",    "𓃁","𓃂",    "𓃃","𓃄","𓃅","𓃆","𓃇",
		#548    9       A       B       C       D       E       F
		"𓃈","𓃉",    "𓃊",    "𓃋",    "𓃌",    "𓃍",    "𓃎",    "𓃏",
		#550    1       2       3       4       5       6       7
		"𓃐","𓃑","𓃒",    "𓃓",    "𓃔",    "𓃕",    "𓃖",    "𓃗",
		#558    9       A       B       C       D       E       F
		"𓃘",    "𓃙",    "𓃚",    "𓃛",    "𓃜",    "𓃝","𓃞",    "𓃟",
		#560    1       2       3       4       5       6       7
		"𓃠",    "𓃡",    "𓃢",    "𓃣",    "𓃤",    "𓃥",    "𓃦",    "𓃧",
		#568    9       A       B       C       D       E       F
		"𓃨",    "𓃩",    "𓃪",    "𓃫",    "𓃬",    "𓃭",    "𓃮",    "𓃯",
		#570    1       2       3       4       5       6       7
		"𓃰","𓃱",    "𓃲",    "𓃳",    "𓃴",    "𓃵",    "𓃶",    "𓃷",
		#578    9       A       B       C       D       E       F
		"𓃸",    "𓃹","𓃺",    "𓃻",    "𓃼",    "𓃽",    "𓃾",    "𓃿",
		#580    1       2       3       4       5       6       7
		"𓄀",    "𓄁",    "𓄂",    "𓄃",    "𓄄",    "𓄅","𓄆","𓄇",
		#588    9       A       B       C       D       E       F
		"𓄈",    "𓄉",    "𓄊",    "𓄋",    "𓄌",    "𓄍",    "𓄎",    "𓄏",
		#590    1       2       3       4       5       6       7
		"𓄐",    "𓄑",    "𓄒",    "𓄓",    "𓄔",    "𓄕",    "𓄖",    "𓄗",
		#598    9       A       B       C       D       E       F
		"𓄘",    "𓄙",    "𓄚",    "𓄛",    "𓄜",    "𓄝",    "𓄞",    "𓄟",
		#5A0    1       2       3       4       5       6       7
		"𓄠",    "𓄡",    "𓄢",    "𓄣",    "𓄤",    "𓄥",    "𓄦",    "𓄧",
		#5A8    9       A       B       C       D       E       F
		"𓄨",    "𓄩",    "𓄪",    "𓄫",    "𓄬",    "𓄭",    "𓄮",    "𓄯",
		#5B0    1       2       3       4       5       6       7
		"𓄰",    "𓄱",    "𓄲",    "𓄳",    "𓄴",    "𓄵",    "𓄶",    "𓄷",
		#5B8    9       A       B       C       D       E       F
		"𓄸",    "𓄹",    "𓄺",    "𓄻",    "𓄼",    "𓄽",    "𓄾",    "𓄿",
		#5C0    1       2       3       4       5       6       7
		"𓅀",    "𓅁",    "𓅂",    "𓅃",    "𓅄",    "𓅅",    "𓅆",    "𓅇",
		#5C8    9       A       B       C       D       E       F
		"𓅈",    "𓅉",    "𓅊",    "𓅋",    "𓅌",    "𓅍",    "𓅎",    "𓅏",
		#5D0    1       2       3       4       5       6       7
		"𓅐",    "𓅑",    "𓅒","𓅓",    "𓅔",    "𓅕",    "𓅖",    "𓅗",
		#5D8    9       A       B       C       D       E       F
		"𓅘",    "𓅙",    "𓅚",    "𓅛",    "𓅜",    "𓅝",    "𓅞",    "𓅟",
		#5E0    1       2       3       4       5       6       7
		"𓅠",    "𓅡",    "𓅢","𓅣",    "𓅤",    "𓅥",    "𓅦",    "𓅧",
		#5E8    9       A       B       C       D       E       F
		"𓅨",    "𓅩",    "𓅪",    "𓅫",    "𓅬",    "𓅭",    "𓅮",    "𓅯",
		#5F0    1       2       3       4       5       6       7
		"𓅰",    "𓅱",    "𓅲",    "𓅳",    "𓅴",    "𓅵",    "𓅶",    "𓅷",
		#5F8    9       A       B       C       D       E       F
		"𓅸",    "𓅹",    "𓅺","𓅻",    "𓅼","𓅽",    "𓅾","𓅿",
		#600    1       2       3       4       5       6       7
		"𓆀",    "𓆁",    "𓆂",    "𓆃","𓆄",    "𓆅",    "𓆆","𓆇",
		#608    9       A       B       C       D       E       F
		"𓆈","𓆉","𓆊","𓆋",    "𓆌",    "𓆍","𓆎",    "𓆏",
		#610    1       2       3       4       5       6       7
		"𓆐",    "𓆑","𓆒",    "𓆓",    "𓆔",    "𓆕",    "𓆖",    "𓆗",
		#618    9       A       B       C       D       E       F
		"𓆘",    "𓆙",    "𓆚",    "𓆛",    "𓆜",    "𓆝",    "𓆞",    "𓆟",
		#620    1       2       3       4       5       6       7
		"𓆠",    "𓆡",    "𓆢",    "𓆣",    "𓆤",    "𓆥",    "𓆦",    "𓆧",
		#628    9       A       B       C       D       E       F
		"𓆨",    "𓆩",    "𓆪",    "𓆫",    "𓆬",    "𓆭",    "𓆮",    "𓆯",
		#630    1       2       3       4       5       6       7
		"𓆰",    "𓆱",    "𓆲",    "𓆳",    "𓆴",    "𓆵",    "𓆶",    "𓆷",
		#638    9       A       B       C       D       E       F
		"𓆸",    "𓆹",    "𓆺",    "𓆻",    "𓆼",    "𓆽",    "𓆾",    "𓆿",
		#640    1       2       3       4       5       6       7
		"𓇀",    "𓇁",    "𓇂",    "𓇃",    "𓇄",    "𓇅",    "𓇆",    "𓇇",
		#648    9       A       B       C       D       E       F
		"𓇈",    "𓇉",    "𓇊",    "𓇋",    "𓇌",    "𓇍",    "𓇎",    "𓇏",
		#650    1       2       3       4       5       6       7
		"𓇐",    "𓇑",    "𓇒",    "𓇓",    "𓇔",    "𓇕",    "𓇖",    "𓇗",
		#658    9       A       B       C       D       E       F
		"𓇘",    "𓇙",    "𓇚",    "𓇛",    "𓇜",    "𓇝",    "𓇞",    "𓇟",
		#660    1       2       3       4       5       6       7
		"𓇠",    "𓇡",    "𓇢",    "𓇣",    "𓇤",    "𓇥",    "𓇦",    "𓇧",
		#668    9       A       B       C       D       E       F
		"𓇨",    "𓇩",    "𓇪",    "𓇫",    "𓇬",    "𓇭",    "𓇮",    "𓇯",
		#670    1       2       3       4       5       6       7
		"𓇰",    "𓇱",    "𓇲",    "𓇳",    "𓇴",    "𓇵",    "𓇶",    "𓇷",
		#678    9       A       B       C       D       E       F
		"𓇸",    "𓇹",    "𓇺",    "𓇻",    "𓇼",    "𓇽",    "𓇾",    "𓇿",
		#680    1       2       3       4       5       6       7
		"𓈀",    "𓈁",    "𓈂",    "𓈃",    "𓈄","𓈅",    "𓈆","𓈇",
		#688    9       A       B       C       D       E       F
		"𓈈",    "𓈉","𓈊",    "𓈋",    "𓈌",    "𓈍",    "𓈎",    "𓈏",
		#690    1       2       3       4       5       6       7
		"𓈐",    "𓈑",    "𓈒",    "𓈓",    "𓈔",    "𓈕",    "𓈖",    "𓈗",
		#698    9       A       B       C       D       E       F
		"𓈘",    "𓈙",    "𓈚",    "𓈛",    "𓈜",    "𓈝",    "𓈞",    "𓈟",
		#6A0    1       2       3       4       5       6       7
		"𓈠",    "𓈡",    "𓈢",    "𓈣",    "𓈤",    "𓈥",    "𓈦",    "𓈧",
		#6A8    9       A       B       C       D       E       F
		"𓈨",    "𓈩",    "𓈪",    "𓈫",    "𓈬",    "𓈭",    "𓈮",    "𓈯",
		#6B0    1       2       3       4       5       6       7
		"𓈰",    "𓈱",    "𓈲",    "𓈳",    "𓈴",    "𓈵",    "𓈶",    "𓈷",
		#6B8    9       A       B       C       D       E       F
		"𓈸",    "𓈹",    "𓈺",    "𓈻",    "𓈼",    "𓈽",    "𓈾",    "𓈿",
		#6C0    1       2       3       4       5       6       7
		"𓉀",    "𓉁",    "𓉂",    "𓉃",    "𓉄",    "𓉅",    "𓉆",    "𓉇",
		#6C8    9       A       B       C       D       E       F
		"𓉈",    "𓉉",    "𓉊",    "𓉋",    "𓉌",    "𓉍",    "𓉎",    "𓉏",
		#6D0    1       2       3       4       5       6       7
		"𓉐",    "𓉑",    "𓉒",    "𓉓",    "𓉔",    "𓉕",    "𓉖",    "𓉗",
		#6D8    9       A       B       C       D       E       F
		"𓉘",    "𓉙",    "𓉚",    "𓉛",    "𓉜",    "𓉝",    "𓉞",    "𓉟",
		#6E0    1       2       3       4       5       6       7
		"𓉠",    "𓉡",    "𓉢",    "𓉣",    "𓉤",    "𓉥",    "𓉦",    "𓉧",
		#6E8    9       A       B       C       D       E       F
		"𓉨",    "𓉩",    "𓉪","𓉫",    "𓉬",    "𓉭","𓉮",    "𓉯",
		#6F0    1       2       3       4       5       6       7
		"𓉰",    "𓉱",    "𓉲",    "𓉳","𓉴",    "𓉵",    "𓉶",    "𓉷",
		#6F8    9       A       B       C       D       E       F
		"𓉸",    "𓉹",    "𓉺",    "𓉻",    "𓉼",    "𓉽",    "𓉾","𓉿",
		#700    1       2       3       4       5       6       7
		"𓊀",    "𓊁",    "𓊂",    "𓊃",    "𓊄",    "𓊅",    "𓊆",    "𓊇",
		#708    9       A       B       C       D       E       F
		"𓊈",    "𓊉",    "𓊊",    "𓊋",    "𓊌",    "𓊍",    "𓊎",    "𓊏",
		#710    1       2       3       4       5       6       7
		"𓊐",    "𓊑",    "𓊒",    "𓊓",    "𓊔",    "𓊕",    "𓊖",    "𓊗",
		#718    9       A       B       C       D       E       F
		"𓊘",    "𓊙",    "𓊚",    "𓊛",    "𓊜",    "𓊝",    "𓊞",    "𓊟",
		#720    1       2       3       4       5       6       7
		"𓊠",    "𓊡",    "𓊢",    "𓊣",    "𓊤",    "𓊥",    "𓊦",    "𓊧",
		#728    9       A       B       C       D       E       F
		"𓊨",    "𓊩",    "𓊪",    "𓊫",    "𓊬",    "𓊭",    "𓊮",    "𓊯",
		#730    1       2       3       4       5       6       7
		"𓊰",    "𓊱",    "𓊲",    "𓊳",    "𓊴",    "𓊵",    "𓊶",    "𓊷",
		#738    9       A       B       C       D       E       F
		"𓊸",    "𓊹",    "𓊺",    "𓊻",    "𓊼",    "𓊽",    "𓊾",    "𓊿",
		#740    1       2       3       4       5       6       7
		"𓋀",    "𓋁",    "𓋂",    "𓋃",    "𓋄",    "𓋅",    "𓋆",    "𓋇",
		#748    9       A       B       C       D       E       F
		"𓋈",    "𓋉",    "𓋊",    "𓋋",    "𓋌",    "𓋍",    "𓋎",    "𓋏",
		#750    1       2       3       4       5       6       7
		"𓋐",    "𓋑",    "𓋒",    "𓋓",    "𓋔",    "𓋕",    "𓋖",    "𓋗",
		#758    9       A       B       C       D       E       F
		"𓋘",    "𓋙",    "𓋚",    "𓋛",    "𓋜",    "𓋝",    "𓋞",    "𓋟",
		#760    1       2       3       4       5       6       7
		"𓋠",    "𓋡",    "𓋢",    "𓋣",    "𓋤",    "𓋥",    "𓋦",    "𓋧",
		#768    9       A       B       C       D       E       F
		"𓋨",    "𓋩",    "𓋪",    "𓋫",    "𓋬",    "𓋭",    "𓋮",    "𓋯",
		#770    1       2       3       4       5       6       7
		"𓋰",    "𓋱",    "𓋲",    "𓋳",    "𓋴",    "𓋵",    "𓋶",    "𓋷",
		#778    9       A       B       C       D       E       F
		"𓋸",    "𓋹",    "𓋺",    "𓋻",    "𓋼",    "𓋽",    "𓋾",    "𓋿",
		#780    1       2       3       4       5       6       7
		"𓌀",    "𓌁",    "𓌂",    "𓌃",    "𓌄",    "𓌅",    "𓌆",    "𓌇",
		#788    9       A       B       C       D       E       F
		"𓌈",    "𓌉",    "𓌊",    "𓌋",    "𓌌",    "𓌍",    "𓌎",    "𓌏",
		#790    1       2       3       4       5       6       7
		"𓌐",    "𓌑",    "𓌒",    "𓌓",    "𓌔",    "𓌕",    "𓌖",    "𓌗",
		#798    9       A       B       C       D       E       F
		"𓌘",    "𓌙",    "𓌚",    "𓌛",    "𓌜",    "𓌝",    "𓌞",    "𓌟",
		#7A0    1       2       3       4       5       6       7
		"𓌠",    "𓌡",    "𓌢",    "𓌣",    "𓌤",    "𓌥",    "𓌦",    "𓌧",
		#7A8    9       A       B       C       D       E       F
		"𓌨",    "𓌩",    "𓌪",    "𓌫",    "𓌬",    "𓌭",    "𓌮",    "𓌯",
		#7B0    1       2       3       4       5       6       7
		"𓌰",    "𓌱",    "𓌲",    "𓌳",    "𓌴",    "𓌵",    "𓌶",    "𓌷",    
		#7B8    9       A       B       C       D       E       F
		"𓌸",    "𓌹",    "𓌺",    "𓌻",    "𓌼",    "𓌽",    "𓌾",    "𓌿",
		#7C0    1       2       3       4       5       6       7
		"𓍀",    "𓍁",    "𓍂",    "𓍃",    "𓍄","𓍅",    "𓍆",    "𓍇",
		#7C8    9       A       B       C       D       E       F
		"𓍈",    "𓍉",    "𓍊",    "𓍋",    "𓍌",    "𓍍",    "𓍎",    "𓍏",
		#7D0    1       2       3       4       5       6       7
		"𓍐",    "𓍑",    "𓍒",    "𓍓",    "𓍔",    "𓍕",    "𓍖",    "𓍗",
		#7D8    9       A       B       C       D       E       F
		"𓍘",    "𓍙",    "𓍚",    "𓍛",    "𓍜",    "𓍝",    "𓍞",    "𓍟",
		#7E0    1       2       3       4       5       6       7
		"𓍠",    "𓍡",    "𓍢",    "𓍣",    "𓍤",    "𓍥","𓍦",    "𓍧",
		#7E8    9       A       B       C       D       E       F
		"𓍨",    "𓍩",    "𓍪","𓍫","𓍬",    "𓍭",    "𓍮",    "𓍯",
		#7F0    1       2       3       4       5       6       7
		"𓍰",    "𓍱",    "𓍲",    "𓍳",    "𓍴",    "𓍵",    "𓍶",    "𓍷",
		#7F8    9       A       B       C       D       E       F
		"𓍸",    "𓍹",    "𓍺",    "𓍻",    "𓍼",    "𓍽",    "𓍾",    "𓍿",
		#800    1       2       3       4       5       6       7
		"𓎀",    "𓎁",    "𓎂",    "𓎃",    "𓎄",    "𓎅",    "𓎆",    "𓎇",
		#808    9       A       B       C       D       E       F
		"𓎈",    "𓎉",    "𓎊",    "𓎋",    "𓎌",    "𓎍",    "𓎎",    "𓎏",
		#810    1       2       3       4       5       6       7
		"𓎐",    "𓎑",    "𓎒","𓎓",    "𓎔",    "𓎕",    "𓎖",    "𓎗",
		#818    9       A       B       C       D       E       F
		"𓎘",    "𓎙",    "𓎚",    "𓎛",    "𓎜",    "𓎝",    "𓎞",    "𓎟",
		#820    1       2       3       4       5       6       7
		"𓎠",    "𓎡",    "𓎢",    "𓎣",    "𓎤",    "𓎥",    "𓎦",    "𓎧",
		#828    9       A       B       C       D       E       F
		"𓎨",    "𓎩",    "𓎪",    "𓎫",    "𓎬",    "𓎭",    "𓎮",    "𓎯",
		#830    1       2       3       4       5       6       7
		"𓎰",    "𓎱",    "𓎲",    "𓎳",    "𓎴",    "𓎵",    "𓎶",    "𓎷",
		#838    9       A       B       C       D       E       F
		"𓎸",    "𓎹",    "𓎺",    "𓎻",    "𓎼",    "𓎽",    "𓎾",    "𓎿",
		#840    1       2       3       4       5       6       7
		"𓏀",    "𓏁",    "𓏂",    "𓏃",    "𓏄",    "𓏅",    "𓏆",    "𓏇",
		#848    9       A       B       C       D       E       F
		"𓏈",    "𓏉",    "𓏊",    "𓏋",    "𓏌",    "𓏍",    "𓏎",    "𓏏",
		#850    1       2       3       4       5       6       7
		"𓏐",    "𓏑",    "𓏒",    "𓏓",    "𓏔",    "𓏕",    "𓏖",    "𓏗",
		#858    9       A       B       C       D       E       F
		"𓏘",    "𓏙",    "𓏚",    "𓏛",    "𓏜",    "𓏝",    "𓏞",    "𓏟",
		#860    1       2       3       4       5       6       7
		"𓏠",    "𓏡",    "𓏢",    "𓏣",    "𓏤",    "𓏥",    "𓏦",    "𓏧",
		#868    9       A       B       C       D       E       F
		"𓏨",    "𓏩",    "𓏪",    "𓏫",    "𓏬",    "𓏭",    "𓏮",    "𓏯",
		#870    1       2       3       4       5       6       7
		"𓏰",    "𓏱",    "𓏲",    "𓏳",    "𓏴",    "𓏵",    "𓏶",    "𓏷",
		#878    9       A       B       C       D       E       F
		"𓏸",    "𓏹",    "𓏺",    "𓏻",    "𓏼",    "𓏽",    "𓏾",    "𓏿",
		#880    1       2       3       4       5       6       7
		"𓐀",    "𓐁",    "𓐂",    "𓐃",    "𓐄",    "𓐅",    "𓐆",    "𓐇",
		#888    9       A       B       C       D       E       F
		"𓐈",    "𓐉",    "𓐊",    "𓐋",    "𓐌","𓐍",    "𓐎",    "𓐏",
		#890    1       2       3       4       5       6       7
		"𓐐",    "𓐑",    "𓐒",    "𓐓",    "𓐔",    "𓐕",    "𓐖",    "𓐗",
		#898    9       A       B       C       D       E       F
		"𓐘","𓐙",    "𓐚",    "𓐛",    "𓐜",    "𓐝",    "𓐞",    "𓐟",
		#8A0    1       2       3       4       5       6       7
		"𓐠",    "𓐡",    "𓐢",    "𓐣",    "𓐤",    "𓐥",    "𓐦","𓐧",
		#8A8    9       A       B       C       D       E       F 2223
		"𓐨",    "𓐩",    "𓐪",    "𓐫",    "𓐬",    "𓐭",    "𓐮",    "❑",
		#8B0    1       2       3       4       5       6       7
		'♥️',       '❣️',   '❤️',   '💌',    '💓',    '💔',    '💕',    '💖', 
		#8B8    9       A       B       C       D       E       F
		'💗',        '💘',    '💙',    '💚',    '💛',    '💜',    '💝',    '💞', 
		#8C0    1       2       3       4       5       6       7
		'💟',        '🧡',    "🦋",    "🌹",    "🌸",    "🍀",    "🌷",    "🌿",
		#8C8    9       A       B       C       D       E       F
		"💐",        "🌺",    "🌻",    "🌼",    "🌴",    "🥀",    "🌱",    "🏆",
		#8D0    1       2       3       4       5       6       7
		"☕",        "☀️",   "☀",    "🌙",    "🌚",    "🌞",    "🚩",    "☎",
		#8D8    9       A       B       C       D       E       F
		"📸",        "📱",    "🥂",    "💯",    "👅",    "💋",    "👀",    "💢", 
		#8E0    1       2       3       4       5       6       7
		"✔",        "❌",    "✅",    "⭐",    "🌟",    "⚠",    "🎀",    "🌈",
		#8E8    9       A       B       C       D       E       F
		"🤯",    "🎼",    "🎤",    "🎵",    "🎶",    "🔥",    "🎂",    "🎈",
		#8F0    1       2       3       4       5       6       7
		"📌",        "🎉",    "✨",    "💥",    '☝',    '✊',    '✋',    '✌️', 
		#8F8    9       A       B       C       D       E       F
		'✍️',       '👆',    '👊',    '👋',    '👌',    '👍',    '👎',    '👏', 
		#900    1       2       3       4       5       6       7
		'👐',        '💪',    '🖕',    '🙈',    '🙋',    '🙌',    '🙏',    '🤘', 
		#908    9       A       B       C       D       E       F
		'🤙',        '🤝',    '🤞',    '🤟',    '🤦',    '🤲',    '🤷',    "⚽",
		#910    1       2       3       4       5       6       7
		"🗣",        "🙇",    "🙊",    "🙅",    "🙆",    "👶",    "💆",    "🐶",
		#918    9       A       B       C       D       E       F
		"🐷",        '☹',    '☺️',   '💀',    '🔴',    '🔵',    '😀',    '😁',
		#920    1       2       3       4       5       6       7
		'😂',        '😃',    '😄',    '😅',    '😆',    '😇',    '😈',    '😉', 
		#928    9       A       B       C       D       E       F
		'😊',        '😋',    '😌',    '😍',    '😎',    '😏',    '😐',    '😑', 
		#930    1       2       3       4       5       6       7
		'😒',        '😓',    '😔',    '😕',    '😖',    '😗',    '😘',    '😙', 
		#938    9       A       B       C       D       E       F
		'😚',        '😛',    '😜',    '😝',    '😞',    '😟',    '😠',    '😡', 
		#940    1       2       3       4       5       6       7
		'😢',        '😣',    '😤',    '😥',    '😨',    '😩',    '😪',    '😫', 
		#948    9       A       B       C       D       E       F
		'😬',        '😭',    '😮',    '😯',    '😰',    '😱',    '😲',    '😳', 
		#950    1       2       3       4       5       6       7
		'😴',        '😵',    '😶',    '😷',    '😹',    '😻',    '🙁',    '🙂', 
		#958    9       A       B       C       D       E       F
		'🙃',        '🙄',    '🤐',    '🤑',    '🤓',    '🤔',    '🤗',    '🤠', 
		#960    1       2       3       4       5       6       7
		'🤢',        '🤣',    '🤤',    '🤧',    '🤨',    '🤩',    '🤪',    '🤫', 
		#968    9       A       B       C       D       E       F
		'🤬',        '🤭',    '🤮',    '🧐',    "☹",    "☺",    "☻",    
		#970    1       2       3       4       5       6       7
		"⚽",    "⚾",    "🎱",    "🎳",    "🎷",    "🎹",    "🎸",
		#978    9       A       B       C       D       E       F
		"☀",    "☁",    "☂",    "☃",    "☄",    "★",    "☆",    "☇",
		#980    1       2       3       4       5       6       7
		"☈",    "☉",    "☊",    "☋",    "☌  ",  "☍",    "☎","☏",    
		#988    9       A       B       C       D       E       F
		"☐",    "☑",    "☒",    "☓",    "☖",    "☗",    "☘",    "☙",
		#990    1       2       3       4       5       6       7
		"☚",    "☛",    "☜",    "☝",    "☞",    "☟",    "☠",    "☡",    
		#998    9       A       B       C       D       E       F
		"☢",    "☣",    "☤",    "☥",    "☦",    "☧",    "☨",    "☩",
		#9A0    1       2       3       4       5       6       7
		"☪",    "☫",    "☬",    "☭",    "☮",    "☯",    "☸",    "☼",
		#9A8    9       A       B       C       D       E       F
		"☽",    "☾",    "☿",    "♀",    "♁",    "♂",    "♃",    "♄",
		#9B0    1       2       3       4       5       6       7
		"♅",    "♆",    "♇",    "♈",    "♉",    "♊",    "♋",    "♌",
		#9B8    9       A       B       C       D       E       F
		"♍",    "♎",    "♏",    "♐",    "♑",    "♒",    "♓",    "♔",
		#9C0    1       2       3       4       5       6       7
		"♕",    "♖",    "♗",    "♘",    "♙",    "♚",    "♛",    "♜",
		#9C8    9       A       B       C       D       E       F
		"♝",    "♞",    "♟",    "♠",    "♡",    "♢",    "♣",    "♤",
		#9D0    1       2       3       4       5       6       7
		"♥",    "♦",    "♧",    "♨",    "♩",    "♪",    "♫",    "♬",
		#9D8    9       A       B       C       D       E       F
		"♭",    "♮",    "♯",    "♰",    "♱",    "♲",    "♺",    "♻",
		#9E0    1       2       3       4       5       6       7
		"♼",    "♽",    "♾",    "♿",    "⚀",    "⚁",    "⚂",    "⚃",
		#9E8    9       A       B       C       D       E       F
		"⚄",    "⚅",    "⚆",    "⚇",    "⚈",    "⚉",    "⚐",    "⚑",
		#9F0    1       2       3       4       5       6       7
		"⚒",    "⚓",    "⚔",    "⚕",    "⚖",    "⚗",    "⚘",    "⚙",
		#9F8    9       A       B       C       D       E       F
		"⚚",    "⚛",    "⚜",    "⚝",    "⚞",    "⚟",    "⚠",    "⚡",
		#A00    1       2       3       4       5       6       7
		"⚢",    "⚣",    "⚤",    "⚥",    "⚦",    "⚧",    "⚨",    "⚩",
		#A08    9       A       B       C       D       E       F
		"⚪",    "⚫",    "⚬",    "⚭",    "⚮",    "⚯",    "⚰",    "⚱",    
		#A10    1       2       3       4       5       6       7
		"⚲",    "⚳",    "⚴",    "⚵",    "⚶",    "⚷",    "⚸",    "⚹",    
		#A18    9       A       B       C       D       E       F
		"⚺",    "⚻",    "⚼",    "⚿",    "⛀",    "⛁",    "⛂",    "⛃",    
		#A20    1       2       3       4       5       6       7
		"⛄",    "⛅",    "⛆",    "⛇",    "⛈",    "⛉",    "⛊",    "⛋",    
		#A28    9       A       B       C       D       E       F
		"⛌",    "⛍",    "⛎",    "⛏",    "⛐",    "⛑",    "⛒",    "⛓",    
		#A30    1       2       3       4       5       6       7
		"⛔",    "⛕",    "⛖",    "⛗",    "⛘",    "⛙",    "⛚",    "⛛",    
		#A38    9       A       B       C       D       E       F
		"⛜",    "⛝",    "⛞",    "⛟","⛠",    "⛡",    "⛢",    "⛣",    
		#A40    1       2       3       4       5       6       7
		"⛤",    "⛥",    "⛦",    "⛧",    "⛨",    "⛩",    "⛪",    "⛫",    
		#A48    9       A       B       C       D       E       F
		"⛬",    "⛭",    "⛮",    "⛯",    "⛰",    "⛱",    "⛲",    "⛳",    
		#A50    1       2       3       4       5       6       7
		"⛴",    "⛵",    "⛶",    "⛷",    "⛸",    "⛹",    "⛺",    "⛻",    
		#A58    9       A       B       C       D       E       F
		"⛼",    "⛽",    "⛾",    "⛿",    "■",    "□",    "▢",    "▣",
		#A60    1       2       3       4       5       6       7
		"▤",    "▥",    "▦",    "▧",    "▨",    "▩",    "₠",    "₡",
		#A68    9       A       B       C       D       E       F
		"₢",    "₣",    "₤",    "₥",    "₦",    "₧","₨",    "₩",
		#A70    1       2       3       4       5       6       7
		"₪",    "₫",    "€",    "₭",    "₮",    "₯","₰",    "₱",
		#A78    9       A       B       C       D       E       F
		"₲",    "₳",    "₴",    "₵",    "₶",    "₷",    "₸",    "₹",
		#A80    1       2       3       4       5       6       7
		"₺",    "₻",    "₼",    "₽",    "₾",    "₿",    "※",    "‽",
		#A88    9       A       B       C       D       E       F
		"⁂",    "⁅",    "⁆",    "⁊",    "⁋",    "⁎",    "⁕", "⁓",
		#A90    1       2       3       4       5       6       7
		 "․",   "‥",    "…",    "‧",    "⁚",    "⁖",    "⁘",    "⁛", 
		#A98    9       A       B       C       D       E       F
		 "⁜","⁝",   "⁞",    "℀",    "℁",    "ℂ",    "℃",    "℄",
		#AA0    1       2       3       4       5       6       7
		 "℅","℆",   "ℇ",    "℈",    "℉",    "ℊ",    "ℋ",    "ℌ",
		#AA8    9       A       B       C       D       E       F
		 "ℍ","ℎ",   "ℏ",    "ℐ",    "ℑ",    "ℒ",    "ℓ",    "℔",
		#AB0    1       2       3       4       5       6       7
		 "ℕ",   "№",    "℗",    "℘",    "ℙ",    "ℚ",    "ℛ",    "ℜ",
		#AB8    9       A       B       C       D       E       F
		 "ℝ",   "℞",    "℟",    "℠",    "℡",    "™",    "℣",    "ℤ",
		#AC0    1       2       3       4       5       6       7
		 "℥",   "Ω",    "℧",    "ℨ",    "℩",    "K",    "Å",    "ℬ",
		#AC8    9       A       B       C       D       E       F
		 "ℭ",   "℮",    "ℯ",    "ℰ",    "ℱ",    "Ⅎ",    "ℳ",    "ℴ",
		#AD0    1       2       3       4       5       6       7
		 "ℵ",   "ℶ",    "ℷ",    "ℸ",    "ℹ",    "℺",    "℻",    "ℼ",
		#AD8    9       A       B       C       D       E       F
		 "ℽ",   "ℾ",    "ℿ",    "⅀",    "⅁",    "⅂",    "⅃",    "⅄",
		#AE0    1       2       3       4       5       6       7
		 "ⅅ",   "ⅆ",    "ⅇ",    "ⅈ",    "ⅉ",    "⅊",    "⅋",    "⅌",
		#AE8    9       A       B       C       D       E       F
		 "⅍","ⅎ",   "⅏",    "➡",    "⬆",    "⬅",    "⬇",    "🌀",
		#AF0    1       2       3       4       5       6       7
		 "🌐","🌑",   "🌒",    "🌓",    "🌔",    "🌕",    "🌖",    "🌗",
		#AF8    9       A       B       C       D       E       F   2815
		 "🌘","🌙",   "🌛",    "🌜",    "🌝",    "😬",    "😰",    "🤭",
		#B00    1       2       3       4       5       6       7 
		 "a",       "ä",    "ɑ",    "ɒ",    "æ",    "b",    "ḇ",    "β",
		#B08    9       A       B       C       D       E       F   
		"c",        "č",    "ɔ",    "ɕ",    "ç",    "d",    "ḏ",    "ḍ",
		#B10    1       2       3       4       5       6       7 
		"ð",    "e",    "ə",    "ɚ",    "ɛ",    "ɝ",    "f",    "g",
		#B18    9       A       B       C       D       E       F   
		"ḡ",    "h",    "ʰ",    "ḥ",    "ḫ",    "ẖ",    "i",    "ɪ",
		#B20    1       2       3       4       5       6       7 
		"ỉ",    "ɨ",    "j",    "ʲ",    "ǰ",    "k",    "ḳ",    "ḵ",
		#B28    9       A       B       C       D       E       F   
		"l",    "ḷ",    "ɬ",    "ɫ",    "m",    "n",    "ŋ",    "ṇ",
		#B30    1       2       3       4       5       6       7 
		"ɲ",    "ɴ",    "o",    "ŏ",    "ɸ",    "θ",    "p",    "p̅",
		#B38    9       A       B       C       D       E       F   
		"þ",    "q",    "r",    "ɹ",    "ɾ",    "ʀ",    "ʁ",    "ṛ",
		#B40    1       2       3       4       5       6       7 
		"s",    "š",    "ś",    "ṣ",    "ʃ",    "t",    "ṭ",    "ṯ",
		#B48    9       A       B       C       D       E       F   
		"ʨ",    "tʂu","ʊ","ŭ",  "ü",    "v",    "ʌ",    "ɣ",
		#B50    1       2       3       4       5       6       7 
		"w",    "ʍ",    "x",    "χ",    "y",    "ʸ",    "ʎ",    "z",
		#B58    9       A       B       C       D       E       F   
		"ẓ",    "ž",    "ʒ",    "’",    "‘",    "ʔ",    "ʕ",    "ā",
		#B60    1       2       3       4       5       6       7 
		"ē",    "ī",    "ō",    "ū",    "ǖ",    "á",    "é",    "í",
		#B68    9       A       B       C       D       E       F   
		"ó",    "ú",    "ǘ",    "ǎ",    "ě",    "ǐ",    "ǒ",    "ǔ",
		#B70    1       2       3       4       5       6       7 
		"ǚ",    "à",    "è",    "ì",    "ò",    "ù",    "ǜ",    "â",
		#B78    9       A       B       C       D       E       F   
		"ê",    "î",    "ô",    "û",    "ʦ",    "ʧ",    "ɖ",    "ˁ",
		#B80    1       2       3       4       5       6       7 
		"ər",   "ɣ",    "ħ",    "ỉ",    "ʤ",    "ɭ",    "ŋg","ɳ",
		#B88    9       A       B       C       D       E       F   
		"ñ",    "ɸ",    "θ",    "ᴅ",    "ɽ",    "ʃ",    "ɕ",    "ʂ",
		#B90    1       2       3       4       5       6       7 
		"ʈ",    "ɨ",    "ü",    "ʲ",    "ʐ",    "→",    "‖",    "ᵗ",
		#B98    9       A       B       C       D       E       F   
		" ̃",   " ̩",   "–",    "—",    "’",    "“",    "”",    "ˈ",
		#BA0    1       2       3       4       5       6       7 
		"ˌ",
		"∃",        #	there exists
		"∄",        #		there does not exists
		"∈",	    #	belongs to
		"∉",        #	does not belong to
		"⇒","→",    #	implies, then
		"⇔","↔",    #		if and only if, double implication
		"∴",	    #	therefore
		"∵",        #		because, since
		"∀",        #		for all
		":","|","ꟻ",#	such that
		"↦",        #   corresponds to
		"✓",        # verification ok
		"✗",        #verification wrong
		"𝔸","𝔹","ℂ","𝔻","𝔼","𝔽","𝔾","ℍ","𝕀","𝕁",
		"𝕂","𝕃","𝕄","ℕ","ℕ̃","𝕆","ℙ","ℚ","ℝ","𝕊",
		"𝕋","𝕌","𝕍","𝕎","𝕏","𝕐","ℤ",
		"𝕒","𝕓","𝕔","𝕕","𝕖","𝕗","𝕘","𝕙","𝕚","𝕛",
		"𝕜","𝕝","𝕞","𝕟","𝕟̃","𝕠","𝕡","𝕢","𝕣","𝕤",
		"𝕥","𝕦","𝕧","𝕨","𝕩","𝕪","𝕫",
		"𝟘","𝟙","𝟚","𝟛","𝟜","𝟝","𝟞","𝟟","𝟠","𝟡",
		'⯑', #void

		# sumBASIC modern language additions; appended so existing ASC indexes remain stable.
		#2990    2991    2992    2993
		'SUB ', 'END SUB ', 'FUNCTION ', 'END FUNCTION ',
		#2994    2995    2996    2997
		'CALL ', 'WITH ', 'SHARED ', 'REDIM ',
		#2998    2999    3000    3001
		'PRESERVE ', 'OPTION ', 'BASE ', 'AS ',
		#3002    3003    3004    3005
		'BOOLEAN ', 'INTEGER ', 'LONG ', 'SINGLE ',
		#3006    3007    3008    3009
		'DOUBLE ', 'DECIMAL ', 'BYTES ', 'ANY ',
		#3010    3011    3012    3013
		'ARRAY ', 'DICT ', 'SET ', 'TUPLE ',
		#3014    3015    3016    3017
		'EACH ', 'WHILE ', 'WEND ', 'DO ',
		#3018    3019    3020    3021
		'LOOP ', 'UNTIL ', 'SWAP ', 'LOCATE ',
		#3022    3023    3024    3025
		'FIELD ', 'GET ', 'PUT ', 'WRITE ',
		#3026    3027    3028    3029
		'FREEFILE ', 'EOF ', 'LOF ', 'LOC ',
		#3030    3031    3032    3033
		'STDIN ', 'STDOUT ', 'STDERR ', 'CHANNEL ',
		#3034    3035    3036    3037
		'SELECT CASE ', 'CASE ', 'END SELECT ', 'MOD ',
		#3038    3039    3040    3041
		'XOR ', 'TRUE ', 'FALSE ', 'SCREEN ',
		#3042    3043    3044
		'LBOUND ', 'UBOUND ', 'END ',
		# sumBASIC 0.1.0a4 mathematical and utility additions; append-only.
		#3045    3046    3047    3048
		'DIV ', 'FIX ', 'LOG ', 'SQRT ',
		#3049    3050    3051    3052
		'CBRT ', 'ROOT ', 'POW ', 'SQUARE ',
		#3053    3054    3055    3056
		'CUBE ', 'COT ', 'SEC ', 'CSC ',
		#3057    3058    3059    3060
		'ASIN ', 'ACOS ', 'ATAN ', 'ATN2 ',
		#3061    3062    3063    3064
		'ATAN2 ', 'SINH ', 'COSH ', 'TANH ',
		#3065    3066    3067    3068
		'ASNH ', 'ACSH ', 'ATNH ', 'ASINH ',
		#3069    3070    3071    3072
		'ACOSH ', 'ATANH ', 'LOG10 ', 'LOG2 ',
		#3073    3074    3075    3076
		'TRUNC ', 'FLOOR ', 'CEIL ', 'ROUND ',
		#3077    3078    3079    3080
		'FRAC ', 'MIN ', 'MAX ', 'CLAMP ',
		#3081    3082    3083    3084
		'HYPOT ', 'RAD ', 'RADIANS ', 'DEG ',
		#3085    3086    3087    3088
		'DEGREES ', 'GCD ', 'LCM ', 'FACT ',
		#3089    3090    3091    3092
		'FACTORIAL ', 'COMB ', 'PERM ', 'GAMMA ',
		#3093    3094    3095    3096
		'LGAMMA ', 'ERF ', 'ERFC ', 'ISFINITE ',
		#3097    3098    3099    3100
		'ISINF ', 'ISNAN ', 'BAND ', 'BOR ',
		#3101    3102    3103    3104
		'BXOR ', 'BNOT ', 'SHL ', 'SHR ',
		#3105    3106    3107    3108
		'IDIV ', 'SIGN ', 'HEX$ ', 'OCT$ ',
		#3109    3110    3111    3112
		'INSTR ', 'STRING$ ', 'LCASE$ ', 'UCASE$ ',
		#3113    3114
		'LTRIM$ ', 'RTRIM$ ',
		# sumBASIC 0.1.0a5 complex-number, clock and logarithm additions; append-only.
		# sumBASIC 0.1.0a7 adds no new tokens: BEEP/SOUND already have historical positions.
		#3115    3116    3117    3118
		'COMPLEX ', 'CMPLX ', 'REAL ', 'IMAG ',
		#3119    3120    3121    3122
		'CONJ ', 'CONJUGATE ', 'PHASE ', 'ARG ',
		#3123    3124    3125    3126
		'MAG ', 'NORM ', 'POLAR ', 'ISCOMPLEX ',
		#3127    3128    3129    3130
		'TIME$ ', 'TIMER ', 'LOGB ', 'LOGBASE ',
		# sumBASIC 0.1.0a16 (unchanged indices; a14 music-language additions); append-only.
		#3131    3132    3133    3134
		'ZXPLAY ', 'GWPLAY ', 'FOREGROUND ', 'BACKGROUND ',
		];
"""
SP U+0020
✁ U+2701
✂ U+2702
✃ U+2703
✄ U+2704
☎ U+260E
✆ U+2706
✇ U+2707
✈ U+2708
✉ U+2709
☛ U+261B
☞ U+261E
✌ U+270C
✍ U+270D
✎ U+270E
✏ U+270F
✐ U+2710
✑ U+2711
✒ U+2712
✓ U+2713
✔ U+2714
✕ U+2715
✖ U+2716
✗ U+2717
✘ U+2718
✙ U+2719
✚ U+271A
✛ U+271B
✜ U+271C
✝ U+271D
✞ U+271E
✟ U+271F
✠ U+2720
✡ U+2721
✢ U+2722
✣ U+2723
✤ U+2724
✥ U+2725
✦ U+2726
✧ U+2727
★ U+2605
✩ U+2729
✪ U+272A
✫ U+272B
✬ U+272C
✭ U+272D
✮ U+272E
✯ U+272F
✰ U+2730
✱ U+2731
✲ U+2732
✳ U+2733
✴ U+2734
✵ U+2735
✶ U+2736
✷ U+2737
✸ U+2738
✹ U+2739
✺ U+273A
✻ U+273B
✼ U+273C
✽ U+273D
✾ U+273E
✿ U+273F
❀ U+2740
❁ U+2741
❂ U+2742
❃ U+2743
❄ U+2744
❅ U+2745
❆ U+2746
❇ U+2747
❈ U+2748
❉ U+2749
❊ U+274A
❋ U+274B
● U+25CF
❍ U+274D
■ U+25A0
❏ U+274F
❐ U+2750
❑ U+2751
❒ U+2752
▲ U+25B2
▼ U+25BC
◆ U+25C6
❖ U+2756
◗ U+25D7
❘ U+2758
❙ U+2759
❚ U+275A
❛ U+275B
❜ U+275C
❝ U+275D
❞ U+275E
"""
#719-974
MATH_CHARS=[
		"ALL EQUAL TO ",
		"ALMOST EQUAL OR EQUAL TO ",
		"ALMOST EQUAL TO ",
		"ANGLE ",
		"ANTICLOCKWISE CONTOUR INTEGRAL ",
		"APPROACHES THE LIMIT ",
		"APPROXIMATELY BUT NOT ACTUALLY EQUAL TO ",
		"APPROXIMATELY EQUAL TO ",
		"APPROXIMATELY EQUAL TO OR THE IMAGE OF ",
		"ASSERTION ",
		"ASTERISK OPERATOR ",
		"ASYMPTOTICALLY EQUAL TO ",
		"BECAUSE ",
		"BETWEEN ",
		"BOWTIE ",
		"BULLET OPERATOR ",
		"CIRCLED ASTERISK OPERATOR ",
		"CIRCLED DASH ",
		"CIRCLED DIVISION SLASH ",
		"CIRCLED DOT OPERATOR ",
		"CIRCLED EQUALS ",
		"CIRCLED MINUS ",
		"CIRCLED PLUS ",
		"CIRCLED RING OPERATOR ",
		"CIRCLED TIMES ",
		"CLOCKWISE CONTOUR INTEGRAL ",
		"CLOCKWISE INTEGRAL ",
		"COLON EQUALS ",
		"COMPLEMENT ",
		"CONTAINS AS MEMBER ",
		"CONTAINS AS NORMAL SUBGROUP ",
		"CONTAINS AS NORMAL SUBGROUP OR EQUAL TO ",
		"CONTAINS WITH LONG HORIZONTAL STROKE ",
		"CONTAINS WITH OVERBAR ",
		"CONTAINS WITH VERTICAL BAR AT END OF HORIZONTAL STROKE ",
		"CONTOUR INTEGRAL ",
		"CORRESPONDS TO ",
		"CUBE ROOT ",
		"CURLY LOGICAL AND ",
		"CURLY LOGICAL OR ",
		"DELTA EQUAL TO ",
		"DIAMOND OPERATOR ",
		"DIFFERENCE BETWEEN ",
		"DIVIDES ",
		"DIVISION SLASH ",
		"DIVISION TIMES ",
		"DOES NOT CONTAIN AS MEMBER ",
		"DOES NOT CONTAIN AS NORMAL SUBGROUP ",
		"DOES NOT CONTAIN AS NORMAL SUBGROUP OR EQUAL ",
		"DOES NOT DIVIDE ",
		"DOES NOT FORCE ",
		"DOES NOT PRECEDE ",
		"DOES NOT PRECEDE OR EQUAL ",
		"DOES NOT PROVE ",
		"DOES NOT SUCCEED ",
		"DOES NOT SUCCEED OR EQUAL ",
		"DOT MINUS ",
		"DOT OPERATOR ",
		"DOT PLUS ",
		"DOUBLE INTEGRAL ",
		"DOUBLE INTERSECTION ",
		"DOUBLE SUBSET ",
		"DOUBLE SUPERSET ",
		"DOUBLE UNION ",
		"DOUBLE VERTICAL BAR DOUBLE RIGHT TURNSTILE ",
		"DOWN RIGHT DIAGONAL ELLIPSIS ",
		"DOWN TACK ",
		"ELEMENT OF ",
		"ELEMENT OF WITH DOT ABOVE ",
		"ELEMENT OF WITH LONG HORIZONTAL STROKE ",
		"ELEMENT OF WITH OVERBAR ",
		"ELEMENT OF WITH TWO HORIZONTAL STROKES ",
		"ELEMENT OF WITH UNDERBAR ",
		"ELEMENT OF WITH VERTICAL BAR AT END OF HORIZONTAL STROKE ",
		"EMPTY SET ",
		"END OF PROOF ",
		"EQUAL AND PARALLEL TO ",
		"EQUAL TO BY DEFINITION ",
		"EQUAL TO OR GREATER-THAN ",
		"EQUAL TO OR LESS-THAN ",
		"EQUAL TO OR PRECEDES ",
		"EQUAL TO OR SUCCEEDS ",
		"EQUALS COLON ",
		"EQUIANGULAR TO ",
		"EQUIVALENT TO ",
		"ESTIMATES ",
		"EXCESS ",
		"FOR ALL ",
		"FORCES ",
		"FOURTH ROOT ",
		"GEOMETRIC PROPORTION ",
		"GEOMETRICALLY EQUAL TO ",
		"GEOMETRICALLY EQUIVALENT TO ",
		"GREATER-THAN BUT NOT EQUAL TO ",
		"GREATER-THAN BUT NOT EQUIVALENT TO ",
		"GREATER-THAN EQUAL TO OR LESS-THAN ",
		"GREATER-THAN OR EQUAL TO ",
		"GREATER-THAN OR EQUIVALENT TO ",
		"GREATER-THAN OR LESS-THAN ",
		"GREATER-THAN OVER EQUAL TO ",
		"GREATER-THAN WITH DOT ",
		"HERMITIAN CONJUGATE MATRIX ",
		"HOMOTHETIC ",
		"IDENTICAL TO ",
		"IMAGE OF ",
		"IMAGE OF OR APPROXIMATELY EQUAL TO ",
		"INCREMENT ",
		"INFINITY ",
		"INTEGRAL ",
		"INTERCALATE ",
		"INTERSECTION ",
		"INVERTED LAZY S ",
		"LEFT NORMAL FACTOR SEMIDIRECT PRODUCT ",
		"LEFT SEMIDIRECT PRODUCT ",
		"LEFT TACK ",
		"LESS-THAN BUT NOT EQUAL TO ",
		"LESS-THAN BUT NOT EQUIVALENT TO ",
		"LESS-THAN EQUAL TO OR GREATER-THAN ",
		"LESS-THAN OR EQUAL TO ",
		"LESS-THAN OR EQUIVALENT TO ",
		"LESS-THAN OR GREATER-THAN ",
		"LESS-THAN OVER EQUAL TO ",
		"LESS-THAN WITH DOT ",
		"LOGICAL AND ",
		"LOGICAL OR ",
		"MEASURED ANGLE ",
		"MEASURED BY ",
		"MIDLINE HORIZONTAL ELLIPSIS ",
		"MINUS SIGN ",
		"MINUS TILDE ",
		"MINUS-OR-PLUS SIGN ",
		"MODELS ",
		"MUCH GREATER-THAN ",
		"MUCH LESS-THAN ",
		"MULTIMAP ",
		"MULTISET ",
		"MULTISET MULTIPLICATION ",
		"MULTISET UNION ",
		"NABLA ",
		"NAND ",
		"N-ARY COPRODUCT ",
		"N-ARY INTERSECTION ",
		"N-ARY LOGICAL AND ",
		"N-ARY LOGICAL OR ",
		"N-ARY PRODUCT ",
		"N-ARY SUMMATION ",
		"N-ARY UNION ",
		"NEGATED DOUBLE VERTICAL BAR DOUBLE RIGHT TURNSTILE ",
		"NEITHER A SUBSET OF NOR EQUAL TO ",
		"NEITHER A SUPERSET OF NOR EQUAL TO ",
		"NEITHER APPROXIMATELY NOR ACTUALLY EQUAL TO ",
		"NEITHER GREATER-THAN NOR EQUAL TO ",
		"NEITHER GREATER-THAN NOR EQUIVALENT TO ",
		"NEITHER GREATER-THAN NOR LESS-THAN ",
		"NEITHER LESS-THAN NOR EQUAL TO ",
		"NEITHER LESS-THAN NOR EQUIVALENT TO ",
		"NEITHER LESS-THAN NOR GREATER-THAN ",
		"NOR ",
		"NORMAL SUBGROUP OF ",
		"NORMAL SUBGROUP OF OR EQUAL TO ",
		"NOT A SUBSET OF ",
		"NOT A SUPERSET OF ",
		"NOT ALMOST EQUAL TO ",
		"NOT AN ELEMENT OF ",
		"NOT ASYMPTOTICALLY EQUAL TO ",
		"NOT EQUAL TO ",
		"NOT EQUIVALENT TO ",
		"NOT GREATER-THAN ",
		"NOT IDENTICAL TO ",
		"NOT LESS-THAN ",
		"NOT NORMAL SUBGROUP OF ",
		"NOT NORMAL SUBGROUP OF OR EQUAL TO ",
		"NOT PARALLEL TO ",
		"NOT SQUARE IMAGE OF OR EQUAL TO ",
		"NOT SQUARE ORIGINAL OF OR EQUAL TO ",
		"NOT TILDE ",
		"NOT TRUE ",
		"ORIGINAL OF ",
		"PARALLEL TO ",
		"PARTIAL DIFFERENTIAL ",
		"PITCHFORK ",
		"PRECEDES ",
		"PRECEDES BUT NOT EQUIVALENT TO ",
		"PRECEDES OR EQUAL TO ",
		"PRECEDES OR EQUIVALENT TO ",
		"PRECEDES UNDER RELATION ",
		"PROPORTION ",
		"PROPORTIONAL TO ",
		"QUESTIONED EQUAL TO ",
		"RATIO ",
		"REVERSED TILDE ",
		"REVERSED TILDE EQUALS ",
		"RIGHT ANGLE ",
		"RIGHT ANGLE WITH ARC ",
		"RIGHT NORMAL FACTOR SEMIDIRECT PRODUCT ",
		"RIGHT SEMIDIRECT PRODUCT ",
		"RIGHT TACK ",
		"RIGHT TRIANGLE ",
		"RING EQUAL TO ",
		"RING IN EQUAL TO ",
		"RING OPERATOR ",
		"SET MINUS ",
		"SINE WAVE ",
		"SMALL CONTAINS AS MEMBER ",
		"SMALL CONTAINS WITH OVERBAR ",
		"SMALL CONTAINS WITH VERTICAL BAR AT END OF HORIZONTAL STROKE ",
		"SMALL ELEMENT OF ",
		"SMALL ELEMENT OF WITH OVERBAR ",
		"SMALL ELEMENT OF WITH VERTICAL BAR AT END OF HORIZONTAL STROKE ",
		"SPHERICAL ANGLE ",
		"SQUARE CAP ",
		"SQUARE CUP ",
		"SQUARE IMAGE OF ",
		"SQUARE IMAGE OF OR EQUAL TO ",
		"SQUARE IMAGE OF OR NOT EQUAL TO ",
		"SQUARE ORIGINAL OF ",
		"SQUARE ORIGINAL OF OR EQUAL TO ",
		"SQUARE ORIGINAL OF OR NOT EQUAL TO ",
		"SQUARE ROOT ",
		"SQUARED DOT OPERATOR ",
		"SQUARED MINUS ",
		"SQUARED PLUS ",
		"SQUARED TIMES ",
		"STAR EQUALS ",
		"STAR OPERATOR ",
		"STRICTLY EQUIVALENT TO ",
		"SUBSET OF ",
		"SUBSET OF OR EQUAL TO ",
		"SUBSET OF WITH NOT EQUAL TO ",
		"SUCCEEDS ",
		"SUCCEEDS BUT NOT EQUIVALENT TO ",
		"SUCCEEDS OR EQUAL TO ",
		"SUCCEEDS OR EQUIVALENT TO ",
		"SUCCEEDS UNDER RELATION ",
		"SUPERSET OF ",
		"SUPERSET OF OR EQUAL TO ",
		"SUPERSET OF WITH NOT EQUAL TO ",
		"SURFACE INTEGRAL ",
		"THERE DOES NOT EXIST ",
		"THERE EXISTS ",
		"THEREFORE ",
		"TILDE OPERATOR ",
		"TRIPLE INTEGRAL ",
		"TRIPLE TILDE ",
		"TRIPLE VERTICAL BAR RIGHT TURNSTILE ",
		"TRUE ",
		"UNION ",
		"UP RIGHT DIAGONAL ELLIPSIS ",
		"UP TACK ",
		"VERTICAL ELLIPSIS ",
		"VERY MUCH GREATER-THAN ",
		"VERY MUCH LESS-THAN ",
		"VOLUME INTEGRAL ",
		"WREATH PRODUCT ",
		"XOR ",
		"Z NOTATION BAG MEMBERSHIP "
		];
OTHERKEYS={
		"ESCAPE":975,
		"LEFT-ARROW":976,
		"RIGHT-ARROW":977,
		"UP-ARROW":978,
		"DOWN-ARROW":979,
		"ENTER":980,
		"BACKSPACE":981,
		"DELETE":982,
		"INSERT":983,
		"HOME":984,
		"END":985,
		"CTRL":986,
		"ALT":987,
		"ALT-GR":988,
		"LEFT-SHIFT":989,
		"RIGHT-SHIFT":990,
		"LEFT-TAB":991,
		"RIGHT-TAB":992,
		"CAPS-LOCK":993,
		"SCROLL-LOCK":  994,
		"NUM-LOCK":995,
		"PAGE-UP":996,
		"PAGE-DOWN":997,
		"PRINT-SCR":998,
		"STARTUP":999,
		"MENU":1000,
		"LEFT-CLICK":1001,
		"RIGHT-CLICK":  1002,
		"DOUBLE-CLICK":1003,
		"MIDDLE-CLICK":1004,
		"SCROLL-UP":1005,
		"SCROLL-DOWN":1006,
		"MUTE":1007,
		"VOLUME-UP":1008,
		"VOLUME-DOWN":1009,
		"MEDIA-PLAY":1010,
		"MEDIA-STOP":1011,
		"MEDIA-PREV":1012,
		"MEDIA-NEXT":1013,
		"HOME-PAGE":1014,
		"INTERNET":1015,
		"SEARCH":1016,
		"E-MAIL":1017,
		"MEDIA-OPEN":1018
		};

MEDIA_PREV ='MEDIA-PREV ';
ALT ='ALT ';
ALT_GR ='ALT-GR ';
BACKSPACE ='BACKSPACE ';
CAPS_LOCK ='CAPS-LOCK ';
CTRL ='CTRL ';
DELETE ='DELETE ';
DOUBLE_CLICK ='DOUBLE-CLICK ';
DOWN_ARROW ='DOWN-ARROW ';
E_MAIL ='E-MAIL ';
K_END ='END ';#End key is K_END because END is keyword in ruby
ENTER ='ENTER ';
SPACE =" ";
ESCAPE ='ESCAPE ';
HOME ='HOME ';
HOME_PAGE ='HOME-PAGE ';
INSERT ='INSERT ';
INTERNET ='INTERNET ';
LEFT_ARROW ='LEFT-ARROW ';
LEFT_CLICK ='LEFT-CLICK ';
LEFT_SHIFT ='LEFT-SHIFT ';
LEFT_TAB ='LEFT-TAB ';
MEDIA_NEXT ='MEDIA-NEXT ';
MEDIA_OPEN ='MEDIA-OPEN ';
MEDIA_PLAY ='MEDIA-PLAY ';
MEDIA_STOP ='MEDIA-STOP ';
MENU ='MENU ';
MIDDLE_CLICK ='MIDDLE-CLICK ';
MUTE ='MUTE ';
NUM_LOCK ='NUM-LOCK ';
PAGE_DOWN ='PAGE-DOWN ';
PAGE_UP ='PAGE-UP ';
PRINT_SCR ='PRINT-SCR ';
RIGHT_ARROW ='RIGHT-ARROW ';
RIGHT_CLICK ='RIGHT-CLICK ';
RIGHT_SHIFT ='RIGHT-SHIFT ';
RIGHT_TAB ='RIGHT-TAB ';
SCROLL_DOWN ='SCROLL-DOWN ';
SCROLL_LOCK ='SCROLL-LOCK ';
SCROLL_UP ='SCROLL-UP ';
SEARCH ='SEARCH ';
SOFT_ESCAPE='SOFT-ESCAPE ';
STARTUP ='STARTUP ';
UP_ARROW ='UP-ARROW ';
VOLUME_DOWN ='VOLUME-DOWN ';
VOLUME_UP ='VOLUME-UP ';



def asc(cha=""):
	if(len(cha)>1):
		cha=cha[0];
	return(ASC.index(cha) if(cha in ASC) else 0);

def chr(number):
	try:
		return(ASC[int(number)% len(ASC)]);
	except:
		return(ASC[0]);

def toList(inp):
	out=[];
	for f in inp:
		out.append(f);
	return(out);


def ascToIntl(inString=""):
	substi='¡¿~_¬\ÀÈÌÒÙẀỲǸÂÊÎÔÛŴŶÁÉÍÓÚẂÝŃÄËÏÖÜẄŸÑÇàèìòùẁỳǹâêîôûŵŷáéíóúẃýńäëïöüẅÿñç';
	substo='!?---/AEIOUWYNAEIOUWYAEIOUWYNAEIOUWYNCaeiouwynaeiouwyaeiouwynaeiouwync';
	out="";
	for f in toList(inString):
		cha=f;
		if f in substi:
			try:
				cha=substo[substi.index(cha)];
			except:
				pass;
		try:
			out+=str(cha);
		except:
			pass;
	return(out);

def aGrossoModo(x,force=False):
	""" aGrossoModo
	
			Filters codes and spaces of strings to make a rough comparison.
			"""
	out=str(ascToIntl(x)).replace("\\\\","\\").replace("\t","").replace("\r","").replace("\n","").replace('"',"").replace("'","").replace(" ","").replace('\\n',"").replace("/n","");
	if(force):
		out=out.replace('[',"").replace('{',"").replace(']',"").replace('}',"").replace('(',"").replace(')',"").replace(':',"").replace('.',"").replace(',',"");
	return(out);

def main(*argv):
	print(chr(164));
	print(asc("ñ"));
	print(toList("La casa roja"));
	print(toList({"la":2,"casa":1}));
	print (ascToIntl("¿Comió maní?"));
	
	
if __name__ == '__main__':
    import sys;
    sys.exit(main(sys.argv));
