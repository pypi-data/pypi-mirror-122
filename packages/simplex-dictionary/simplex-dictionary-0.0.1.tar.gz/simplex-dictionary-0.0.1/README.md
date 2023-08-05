# Simplex dictionary

[![Python Versions](https://img.shields.io/badge/python-3.6%20|%203.7-blue.svg)](https://img.shields.io/badge/python-3.6%20|%203.7%20|%203.8%20|%203.9-blue.svg)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](https://img.shields.io/badge/license-MIT-green.svg)
[![Build Status](https://drone.typename.fr/api/badges/mikael.capelle/simplex/status.svg)](https://drone.typename.fr/mikael.capelle/simplex)

`simplex` is a small python module that implements a `simplex_dictionary` structure
representing a dictionary for the
[Simplex algorithm](https://en.wikipedia.org/wiki/Simplex_algorithm).
The package is intended for educational purpose, e.g., to have students implement the
Simplex algorithm based on the structure.

## Basic usage

The following code creates a simplex dictionary with 5 variables:

```python
from simplex import simplex_dictionary

# The list of variables (can be anything):
x1, x2, x3, x4, x5 = ('x_{}'.format(i + 1) for i in range(5))
variables = [x1, x2, x3, x4, x5]

# The simplex dictionary with B = (x3, x4, x5):
sdict = simplex_dictionary(B=[x3, x4, x5], N=[x1, x2])

# Set the values of the basic variables:
sdict.b = {x3: 18, x4: 42, x5: 24}

# Coefficients of the non-basic variables in the dictionary (we represent
# the positive coefficients):
sdict.a = {
    x3: {x1: 2, x2: 1},
    x4: {x1: 2, x2: 3},
    x5: {x1: 3, x2: 1}
}

# Current value of the objective:
sdict.z = 0

# Coefficients of the non-basic variables in the objective function:
sdict.c[x1] = 3
sdict.c[x2] = 2

# Trying to set the coefficients for a basic variables that should be 0 raise an
# exception:
sdict.c[x3] = 4  # raises "x_3 is not a non-basic variable."
sdict.b[x1] = 1  # raises "x_1 is not a basic variable."
```

When using the `simplex` module within a jupyter notebook, the `display()` method
outputs a latex version of the dictionary:

```python
sdict.display(name='S_0')
```

<a href="https://www.codecogs.com/eqnedit.php?latex=\displaystyle&space;S_0&space;=&space;\left.\begin{array}{r||r|r|r|r|}&space;&&space;b&space;&&space;x_{1}&space;&&space;x_{2}\\\hline&space;x_{3}&space;&&space;18&space;&-2&space;&&space;-1\\x_{4}&space;&&space;42&space;&-2&space;&&space;-3\\x_{5}&space;&&space;24&space;&-3&space;&&space;-1\\\hline\hline&space;z&0&3&2\\\hline\end{array}\right." target="_blank"><img src="https://latex.codecogs.com/gif.latex?\displaystyle&space;S_0&space;=&space;\left.\begin{array}{r||r|r|r|r|}&space;&&space;b&space;&&space;x_{1}&space;&&space;x_{2}\\\hline&space;x_{3}&space;&&space;18&space;&-2&space;&&space;-1\\x_{4}&space;&&space;42&space;&-2&space;&&space;-3\\x_{5}&space;&&space;24&space;&-3&space;&&space;-1\\\hline\hline&space;z&0&3&2\\\hline\end{array}\right." title="\displaystyle S_0 = \left.\begin{array}{r||r|r|r|r|} & b & x_{1} & x_{2}\\\hline x_{3} & 18 &-2 & -1\\x_{4} & 42 &-2 & -3\\x_{5} & 24 &-3 & -1\\\hline\hline z&0&3&2\\\hline\end{array}\right." /></a>
