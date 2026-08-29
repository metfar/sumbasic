# sumBASIC mathematical core

sumBASIC aims to make scalar mathematics a first-class teaching feature rather than inheriting the deliberately small numerical toolbox typical of xBase-family languages.

This document describes the mathematical surface implemented in `0.1.0a6`. It does not claim that every field of mathematics is already built in: matrix algebra, statistics and symbolic algebra are separate future layers. Real, integer, decimal and complex arithmetic below are executable now.

## Constants

`PI` is a built-in immutable constant and intentionally uses the ZX Spectrum value:

```basic
PI = 3.1415927
```

Assignment to `PI` is an error.

## Numeric literals

```basic
42          # decimal integer
3.1415      # floating point
1.25E-3     # scientific notation
&HFF        # hexadecimal
&O377       # octal
&B101010    # binary
```

## Arithmetic operators

| Operation | sumBASIC | Example |
| --- | --- | --- |
| addition | `+` | `A + B` |
| subtraction | `-` | `A - B` |
| multiplication | `*` | `A * B` |
| real division | `/` | `7 / 2` -> `3.5` |
| integer division | `\`, `DIV` | `7 \ 2` -> `3` |
| remainder | `MOD` | `7 MOD 3` -> `1` |
| power | `^` | `2 ^ 8` -> `256` |
| left shift | `<<` | `1 << 5` -> `32` |
| right shift | `>>` | `32 >> 3` -> `4` |
| integer/Boolean XOR | `XOR` | `5 XOR 3` -> `6` |
| unary positive | `+` | `+X` |
| unary negative | `-` | `-X` |

`**` and `//` are accepted by the expression engine as modern aliases, although `^` and `\`/`DIV` are the recommended BASIC spellings.

## Relational and logical operators

`=`, `<>`, `<`, `<=`, `>=`, `>`, `NOT`, `AND`, `OR`, and `XOR` are supported.

`AND` and `OR` are logical operations. Explicit integer bit operations are provided by `BAND`, `BOR`, `BXOR`, and `BNOT`; this avoids making the educational meaning of `AND`/`OR` depend on operand type.

## Spectrum mathematical family

The historical family is available directly:

`SIN`, `COS`, `TAN`, `ASN`, `ACS`, `ATN`, `LN`, `EXP`, `INT`, `SQR`, `SGN`, `ABS`.

`ASN`, `ACS`, and `ATN` also have modern aliases `ASIN`, `ACOS`, and `ATAN`.

Angles are in radians, as in the Spectrum and most programming-language math libraries.

## Powers, roots and geometry

- `SQR(x)`, `SQRT(x)` - square root.
- `CBRT(x)` - real cube root, including negative values.
- `ROOT(x, n)` - real nth root.
- `POW(x, y)` - power function.
- `SQUARE(x)`, `CUBE(x)` - explicit second/third powers.
- `HYPOT(x, ...)` - Euclidean hypotenuse/norm.

## Trigonometry

- `SIN`, `COS`, `TAN`.
- `COT`, `SEC`, `CSC`.
- `ASN`/`ASIN`, `ACS`/`ACOS`, `ATN`/`ATAN`.
- `ATN2(y, x)` / `ATAN2(y, x)`.
- `RAD(x)` / `RADIANS(x)` converts degrees to radians.
- `DEG(x)` / `DEGREES(x)` converts radians to degrees.

## Hyperbolic functions

- `SINH`, `COSH`, `TANH`.
- `ASNH`/`ASINH`.
- `ACSH`/`ACOSH`.
- `ATNH`/`ATANH`.

## Logarithms and exponentials

The BASIC convention is explicit and intentional:

- `LOG(x)` - common logarithm, base 10.
- `LOG10(x)` - explicit alias for base 10.
- `LN(x)` - natural/Napierian logarithm, base `e`.
- `LOG2(x)` - base 2.
- `LOGB(x, base)` / `LOGBASE(x, base)` - arbitrary base.
- `EXP(x)` - `e` raised to `x`.

Examples:

```basic
PRINT LOG(1000)       # 3
PRINT LN(EXP(1))      # 1
PRINT LOGB(81, 3)     # 4
```


## Complex numbers

`COMPLEX` is a first-class numeric type. The canonical constructor is `COMPLEX(real, imag)`; `CMPLX` is a short alias. Ordinary arithmetic operators `+`, `-`, `*`, `/`, and `^` operate directly on complex values.

```basic
DIM Z AS COMPLEX
Z = COMPLEX(3, 4)
PRINT Z                # 3+4i
PRINT ABS(Z)           # 5
PRINT Z ^ 2
```

Complex helpers:

- `REAL(z)` and `IMAG(z)` return the components.
- `CONJ(z)` / `CONJUGATE(z)` returns the complex conjugate.
- `MAG(z)` is the magnitude (and `ABS(z)` is equivalent).
- `NORM(z)` returns the squared magnitude.
- `PHASE(z)` / `ARG(z)` returns the argument in radians.
- `POLAR(radius, angle)` constructs a complex value from polar coordinates.
- `ISCOMPLEX(z)` tests whether the runtime value is complex.

The transcendental functions `SQR`/`SQRT`, `SIN`, `COS`, `TAN`, their inverse/hyperbolic counterparts, `LN`, `LOG`, `LOG2`, `LOGB`, and `EXP` accept complex operands. Real operands retain their real-domain behavior: for example `SQR(-1)` remains a real-domain error, while `SQR(COMPLEX(-1,0))` returns `i`.

## Integer conversion, rounding and fractions

- `INT(x)` floors toward negative infinity.
- `FIX(x)` and `TRUNC(x)` truncate toward zero.
- `FLOOR(x)` and `CEIL(x)` are explicit floor/ceiling operations.
- `ROUND(x [, digits])` uses half-away-from-zero semantics.
- `FRAC(x)` returns the signed fractional part.
- `SGN(x)` / `SIGN(x)` returns `-1`, `0`, or `1`.
- `ABS(x)` returns absolute value.

Examples:

```basic
PRINT INT(-1.2)       # -2
PRINT FIX(-1.8)       # -1
PRINT ROUND(2.5)      # 3
PRINT ROUND(-2.5)     # -3
PRINT FRAC(-2.25)     # -0.25
```

## Range helpers

- `MIN(a, ...)`.
- `MAX(a, ...)`.
- `CLAMP(x, low, high)`.

## Number theory and combinatorics

- `GCD(a, ...)` - greatest common divisor.
- `LCM(a, ...)` - least common multiple.
- `FACT(n)` / `FACTORIAL(n)`.
- `COMB(n, k)` - combinations.
- `PERM(n [, k])` - permutations.

## Special functions

- `GAMMA(x)`.
- `LGAMMA(x)`.
- `ERF(x)`.
- `ERFC(x)`.
- `ISFINITE(x)`.
- `ISINF(x)`.
- `ISNAN(x)`.

## Explicit integer bit operations

- `BAND(a, ...)`.
- `BOR(a, ...)`.
- `BXOR(a, ...)`.
- `BNOT(a)`.
- `SHL(a, n)`.
- `SHR(a, n)`.
- `IDIV(a, b)`.

The operators `<<` and `>>` are aliases for the shift operations.

## Decimal arithmetic

`DECIMAL` is a real language type. The expression evaluator promotes the other operand when a `DECIMAL` participates in ordinary arithmetic, so this is exact decimal arithmetic rather than an accidental conversion back to binary float:

```basic
DIM Price AS DECIMAL
Price = DECIMAL("0.1")
PRINT Price + 0.2
```

produces the exact decimal value `0.3` internally.

## Error domains

Invalid mathematical domains, such as an even real root of a negative number or a logarithm outside its real domain, raise a sumBASIC expression error rather than silently returning a fabricated value.

<p align=center><b>- oOo -<b></p>
