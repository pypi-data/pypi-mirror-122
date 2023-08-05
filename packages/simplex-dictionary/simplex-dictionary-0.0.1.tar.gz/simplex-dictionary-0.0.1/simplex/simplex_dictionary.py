# -*- encoding: utf-8 -*-

import typing
from abc import ABC, abstractmethod
from fractions import Fraction

from .magic_dictionary import magic_dictionary


class Comparable(ABC):
    @abstractmethod
    def __lt__(self, other: typing.Any) -> bool:
        ...


# Type that can be converted by convert_value:
convertable_type = typing.Union[str, int, Fraction]


def convert_value(value: convertable_type) -> Fraction:
    if type(value) is float:
        # For float value, we don't handle float:
        raise TypeError("Cannot set value as float, use fractions.Fraction instead.")
    return Fraction(value)


# Type of variables in a simplex_dictionary:
V = typing.TypeVar("V", bound=Comparable)


class simplex_dictionary(typing.Generic[V]):

    """
    Class representing a dictionary for the simplex algorithm. The class contains
    multiple members representing the elements of a dictionary.

    Members:
      - B The list of basic variables (immutable).
      - N The list of non-basic variables (immutable).
      - b The current value of the basic variables.
      - a The current coefficients of the non-basic variables in the expression
        of the basic variables.
      - c The current coefficients of the non-basic variables in the objective.
      - z The current value of the objective.

    The magic member ".variables" can also be used to access the list of all
    variables.

    The various arrays of coefficients or values (b, a, c) are indexed by their
    respective variables, which must be in B or N.

    All values are converted to fractions.Fraction object in order to maintain
    consistency in the dictionary.

    Examples:
    ```
    # Create a simplex dictionary with two basic and two non-basic variables:
    >>> sdict = simplex_dictionary(B=['x_1', 'x_2'], N=['x_3', 'x_4'])

    # Set the value of x_1:
    >>> sdict.b['x_1'] = 4

    # Set the coefficient of x_3 in x_1:
    >>> sdict.a['x_1']['x_3'] = 12
    ```
    """

    _a: magic_dictionary[V, magic_dictionary[V, Fraction]]
    _b: magic_dictionary[V, Fraction]
    _c: magic_dictionary[V, Fraction]
    _z: Fraction

    def __init__(self, B: typing.Iterable[V], N: typing.Iterable[V]):
        """
        Args:
            B The list of basic variables.
            N The list of non-basic variables.
        """
        self.__B = list(B)
        self.__N = list(N)
        self.b = {}  # type: ignore
        self.a = {}  # type: ignore
        self.c = {}  # type: ignore
        self.z = Fraction(0)

    def _check_basic(self, key: V) -> typing.Optional[str]:
        """
        Check if the given key is a basic variable, returning None if it is,
        and a custom exception string if not. Suitable for magic_dictionary use.
        """
        if key not in self.B:
            return "{} is not a basic variable.".format(key)
        return None

    def _check_non_basic(self, key: V) -> typing.Optional[str]:
        """
        Check if the given key is a non-basic variable, returning None if it is,
        and a custom exception string if not. Suitable for magic_dictionary use.
        """
        if key not in self.N:
            return "{} is not a non-basic variable.".format(key)
        return None

    @property
    def variables(self) -> typing.List[V]:
        """
        Returns:
            The list of variables in this dictionary.
        """
        return sorted(self.B + self.N)

    @property
    def B(self) -> typing.List[V]:
        """
        Returns: The list of basic variables for this dictionary.
        """
        return self.__B

    @property
    def N(self) -> typing.List[V]:
        """
        Returns:
            The list of non-basic variables for this dictionary.
        """
        return self.__N

    @property
    def a(self) -> magic_dictionary[V, magic_dictionary[V, Fraction]]:
        """
        Returns:
            The a matrix of this dictionary.
        """
        return self._a

    @a.setter
    def a(
        self,
        value: typing.Union[
            typing.Mapping[V, typing.Mapping[V, convertable_type]],
            typing.Iterable[typing.Tuple[V, typing.Mapping[V, convertable_type]]],
        ],
    ):
        self._a = magic_dictionary(
            value,
            key_predicate=self._check_basic,
            value_converter=lambda value: magic_dictionary(
                value,
                key_predicate=self._check_non_basic,
                value_converter=convert_value,
            ),
            default_factory=lambda: magic_dictionary(
                key_predicate=self._check_non_basic, value_converter=convert_value
            ),
        )

    @property
    def b(self) -> magic_dictionary[V, Fraction]:
        return self._b

    @b.setter
    def b(
        self,
        value: typing.Union[
            typing.Mapping[V, convertable_type],
            typing.Iterable[typing.Tuple[V, convertable_type]],
        ],
    ):
        self._b = magic_dictionary(
            value, key_predicate=self._check_basic, value_converter=convert_value
        )

    @property
    def c(self) -> magic_dictionary[V, Fraction]:
        return self._c

    @c.setter
    def c(
        self,
        value: typing.Union[
            typing.Mapping[V, convertable_type],
            typing.Iterable[typing.Tuple[V, convertable_type]],
        ],
    ):
        self._c = magic_dictionary(
            value, key_predicate=self._check_non_basic, value_converter=convert_value
        )

    @property
    def z(self) -> Fraction:
        return self._z

    @z.setter
    def z(self, value: convertable_type):
        self._z = convert_value(value)

    def name_latex(self, name: typing.Any) -> str:
        """
        Convert the given variable name to a clean latex name.

        Args:
            name: The name of the variable to convert.

        Returns:
            A latex version of the given name.
        """

        sname = str(name)

        s = sname.split("_")

        # We only handle special case:
        if len(s) == 1 or len(s) > 2:
            return sname

        return s[0] + "_{" + s[1] + "}"

    def value_latex(self, value: Fraction) -> str:
        """
        Convert the given fraction to a latex fraction.

        Args:
            value: The fraction to convert.

        Returns:
            A valid latex code that is either a number (if the fraction has a
            denominator of 1), or a latex fraction.
        """
        if value.denominator == 1:
            return str(value)
        return r"{}\frac{{{}}}{{{}}}".format(
            "-" if value.numerator < 0 else "", abs(value.numerator), value.denominator
        )

    def display(self, name: str = None):
        """
        Display this simplex dictionary on the standard Jupyter output.

        Args:
            name: Name of the dictionary.
        """
        from IPython.display import Math, display

        d = (
            r"\begin{{array}}{{r||{}}}".format("r|" * (1 + len(self.B)))
            + r" & b & "
            + " & ".join(self.name_latex(v) for v in self.N)
            + r"\\\hline "
            + r"\\".join(
                "{} & {} &".format(self.name_latex(b), self.value_latex(self.b[b]))
                + " & ".join(self.value_latex(-self.a[b][n]) for n in self.N)
                for i, b in enumerate(self.B)
            )
            + r"\\\hline\hline "
            + r"&".join(
                ["z", self.value_latex(self.z)]
                + [self.value_latex(self.c[n]) for n in self.N]
            )
            + r"\\\hline\end{array}"
        )

        if name is not None:
            d = r"{} = \left.{}\right.".format(name, d)

        display(Math(d))

    def __str__(self) -> str:
        # Length for the variables:
        vnames = [str(x) for x in self.variables]
        vlength = max(len(n) for n in vnames)

        # Length for the b column:
        z = str(self.z)
        b = [str(self.b[x]) for x in self.B]
        blength = max(len(z), max(len(n) for n in b))

        # Length for the other columns:
        a = [[str(self.a[xb][xn]) for xn in self.N] for xb in self.B]
        c = [str(self.c[xn]) for xn in self.N]
        alength = max(
            vlength, max(len(n) for r in a for n in r), max(len(n) for n in c)
        )

        # Create the string:
        row_format_s = " {:>{vwidth}} | {:>{bwidth}} | "
        row_format_s += " | ".join("{:>{awidth}}" for _ in self.N)
        row_format_s += " |"

        def format(*args):
            return row_format_s.format(
                *map(str, args), vwidth=vlength, bwidth=blength, awidth=alength
            )

        s = []

        # First row:
        s.append(format("", "b", *self.N))

        # Length of a row:
        lr = len(s[0])

        # Separator:
        s.append("-" * lr)

        for xb in self.B:
            s.append(format(xb, self.b[xb], *[self.a[xb][xn] for xn in self.N]))

        s.append("-" * lr)
        s.append(format("z", self.z, *[self.c[xn] for xn in self.N]))
        s.append("-" * lr)

        return "\n".join(s)
