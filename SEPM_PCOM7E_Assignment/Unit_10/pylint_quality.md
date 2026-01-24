## Pylint

```bash
python -m pylint .\code_with_lint.py
```
```
************* Module code_with_lint
code_with_lint.py:27:0: W0301: Unnecessary semicolon (unnecessary-semicolon)
code_with_lint.py:31:0: C0325: Unnecessary parens after 'return' keyword (superfluous-parens)
code_with_lint.py:33:0: C0325: Unnecessary parens after 'return' keyword (superfluous-parens)
code_with_lint.py:44:0: C0304: Final newline missing (missing-final-newline)
code_with_lint.py:1:0: C0114: Missing module docstring (missing-module-docstring)
code_with_lint.py:2:0: W0622: Redefining built-in 'pow' (redefined-builtin)
code_with_lint.py:2:0: W0401: Wildcard import math (wildcard-import)
code_with_lint.py:7:0: C0103: Constant name "some_global_var" doesn't conform to UPPER_CASE naming style (invalid-name)
code_with_lint.py:13:4: W0621: Redefining name 'some_global_var' from outer scope (line 7) (redefined-outer-name)
code_with_lint.py:16:4: W0101: Unreachable code (unreachable)
code_with_lint.py:13:4: W0612: Unused variable 'some_global_var' (unused-variable)
code_with_lint.py:25:7: C0121: Comparison 'x != None' should be 'x is not None' (singleton-comparison)
code_with_lint.py:28:12: R1705: Unnecessary "else" after "return", remove the "else" and de-indent the code inside it (no-else-return)
code_with_lint.py:19:0: R1710: Either all return statements in a function should return an expression, or none of them should. (inconsistent-return-statements)
code_with_lint.py:35:0: C0115: Missing class docstring (missing-class-docstring)
code_with_lint.py:41:8: W0621: Redefining name 'time' from outer scope (line 5) (redefined-outer-name)
code_with_lint.py:41:15: E0601: Using variable 'time' before assignment (used-before-assignment)
code_with_lint.py:42:8: C0415: Import outside toplevel (datetime.datetime) (import-outside-toplevel)
code_with_lint.py:37:4: R1711: Useless return at end of function or method (useless-return)
code_with_lint.py:37:50: W0613: Unused argument 'verbose' (unused-argument)
code_with_lint.py:40:8: W0612: Unused variable 'list_comprehension' (unused-variable)
code_with_lint.py:43:8: W0612: Unused variable 'date_and_time' (unused-variable)
code_with_lint.py:35:0: R0903: Too few public methods (0/2) (too-few-public-methods)
code_with_lint.py:1:0: W0611: Unused import io (unused-import)
code_with_lint.py:5:0: W0611: Unused time imported from time (unused-import)
code_with_lint.py:2:0: W0614: Unused import(s) acos, acosh, asin, asinh, atan, atan2, atanh, cbrt, ceil, comb, copysign, cos, cosh, degrees, dist, e, erf, erfc, exp, exp2, expm1, fabs, factorial, floor, fmod, frexp, fsum, 
gamma, gcd, hypot, inf, isclose, isfinite, isinf, isnan, isqrt, lcm, ldexp, lgamma, log, log10, log1p, log2, modf, nan, nextafter, perm, pow, prod, radians, remainder, sin, sinh, sqrt, sumprod, tan, tanh, tau, trunc and ulp from wildcard import of math (unused-wildcard-import)

-----------------------------------
Your code has been rated at 0.00/10
```

## Pyflakes

```bash
python -m pyflakes .\code_with_lint.py
```
```
.\code_with_lint.py:1:1: 'io' imported but unused
.\code_with_lint.py:2:1: 'from math import *' used; unable to detect undefined names
.\code_with_lint.py:13:5: local variable 'some_global_var' is assigned to but never used
.\code_with_lint.py:40:44: 'pi' may be undefined, or defined from star imports: math
.\code_with_lint.py:40:9: local variable 'list_comprehension' is assigned to but never used
.\code_with_lint.py:41:16: local variable 'time' defined in enclosing scope on line 5 referenced before assignment
.\code_with_lint.py:41:9: local variable 'time' is assigned to but never used
.\code_with_lint.py:43:9: local variable 'date_and_time' is assigned to but never used
```

## Pycodestyle

```bash
python -m pycodestyle .\code_with_lint.py
```
```
.\code_with_lint.py:9:1: E302 expected 2 blank lines, found 1
.\code_with_lint.py:14:15: E225 missing whitespace around operator
.\code_with_lint.py:19:1: E302 expected 2 blank lines, found 1
.\code_with_lint.py:20:80: E501 line too long (80 > 79 characters)
.\code_with_lint.py:25:10: E711 comparison to None should be 'if cond is not None:'
.\code_with_lint.py:27:25: E703 statement ends with a semicolon
.\code_with_lint.py:31:23: E275 missing whitespace after keyword
.\code_with_lint.py:31:24: E201 whitespace after '('
.\code_with_lint.py:35:1: E302 expected 2 blank lines, found 1
.\code_with_lint.py:37:58: E251 unexpected spaces around keyword / parameter equals
.\code_with_lint.py:37:60: E251 unexpected spaces around keyword / parameter equals
.\code_with_lint.py:38:28: E221 multiple spaces before operator
.\code_with_lint.py:38:31: E222 multiple spaces after operator
.\code_with_lint.py:39:22: E221 multiple spaces before operator
.\code_with_lint.py:39:31: E222 multiple spaces after operator
.\code_with_lint.py:40:80: E501 line too long (83 > 79 characters)
.\code_with_lint.py:44:15: W292 no newline at end of file
```

## Pydocstyle
```bash
python -m pydocstyle .\code_with_lint.py 
```
```
.\code_with_lint.py:1 at module level:
        D100: Missing docstring in public module
.\code_with_lint.py:10 in public function `multiply`:
        D200: One-line docstring should fit on one line with quotes (found 3)
.\code_with_lint.py:10 in public function `multiply`:
        D400: First line should end with a period (not 's')
.\code_with_lint.py:10 in public function `multiply`:
        D401: First line should be in imperative mood; try rephrasing (found 'This')
.\code_with_lint.py:20 in public function `is_sum_lucky`:
        D205: 1 blank line required between summary line and description (found 0)
.\code_with_lint.py:20 in public function `is_sum_lucky`:
        D400: First line should end with a period (not 'y')
.\code_with_lint.py:20 in public function `is_sum_lucky`:
        D401: First line should be in imperative mood; try rephrasing (found 'This')
.\code_with_lint.py:35 in public class `SomeClass`:
        D101: Missing docstring in public class
.\code_with_lint.py:37 in public method `__init__`:
        D107: Missing docstring in __init__
```

