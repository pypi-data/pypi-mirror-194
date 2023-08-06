import typing

# Generated with uglyduck



class ITest(typing.Protocol):
    bool_with_type: bool
    bool_without_type: bool
    int_with_type: int
    int_without_type: int
    str_with_type: str
    str_without_type: str
    # __init__ attributes
    a: int
    b: 'ITest'

    def __init__(self, a: int, b: 'ITest'):
        ...


class ITestInspect(typing.Protocol):

    def test_types(self):
        ...


class ITestParse(typing.Protocol):

    def test_list_literal(self):
        ...

    def test_tuple_literal(self):
        ...
