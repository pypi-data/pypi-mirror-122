# -*- encoding: utf-8 -*-

import typing

V = typing.TypeVar("V")
T = typing.TypeVar("T")


class magic_dictionary(typing.Dict[V, T]):

    """
    A magic dictionary is a dictionary that:
      - May contain a default value, much like collections.defaultdict.
      - Raise custom errors when the given key does not match a given
        predicate.
      - Can convert values using a specific functor.

    Magic dictionary can be constructed the same way standard python dictionary
    are, except that the constructor takes three extra named parameters.
    """

    key_predicate: typing.Optional[typing.Callable[[V], typing.Optional[str]]] = None
    value_converter: typing.Optional[typing.Callable[[typing.Any], T]] = None
    default_factory: typing.Optional[typing.Callable[[], T]] = None

    def __init__(
        self,
        *args,
        key_predicate: typing.Callable[[V], typing.Optional[str]] = None,
        value_converter: typing.Callable[[typing.Any], T] = None,
        default_factory: typing.Callable[[], T] = None,
        **kwargs
    ):
        """
        Args:
            key_predicate: Predicate to apply on new key, which should return None if
                the key is valid, or a message indicating why the key is invalid
                otherwize. The predicates is not applied on the initial keys of the
                dictionary (from args or kwargs). Can be None.
            value_converter:  Functor to apply to values in this dictionary, when set
                by the index operator. This functor is also applied to all initial
                values of the dictionary. Can be None.
            default_facotry:  Default factory to use to create object when the key is
                not set. Can be None.
        """
        super().__init__(*args, **kwargs)

        self.key_predicate = key_predicate
        self.value_converter = value_converter
        self.default_factory = default_factory

        # Copy construction:
        if len(args) >= 1 and isinstance(args[0], magic_dictionary):
            if key_predicate is None:
                self.key_predicate = args[0].key_predicate
            if value_converter is None:
                self.value_converter = args[0].value_converter
            if default_factory is None:
                self.default_factory = args[0].default_factory

        # Check the value:
        if self.key_predicate is not None:
            for k in self:
                check = self.key_predicate(k)
                if check is not None:
                    raise IndexError(check)

        # Convert the value:
        if self.value_converter is not None:
            for k in self:
                super().__setitem__(k, self.value_converter(self[k]))

    def __getitem__(self, key: V) -> T:

        # If the key does not exists:
        if key not in self:
            # We try to set it to a new object:
            if self.default_factory is not None:
                self.__setitem__(key, self.default_factory())

        # Return the key:
        return super().__getitem__(key)

    def __setitem__(self, key: V, value: typing.Any):
        # If the key predicate is not empty, we check the key:
        if self.key_predicate is not None:
            check = self.key_predicate(key)
            if check is not None:
                raise KeyError(check)

        # Convert the value:
        if self.value_converter is not None:
            value = self.value_converter(value)

        super().__setitem__(key, value)

    def update(self, *args, **kargs):
        super().update(
            magic_dictionary(
                *args,
                **kargs,
                value_converter=self.value_converter,
                key_predicate=self.key_predicate,
                default_factory=self.default_factory
            )
        )
