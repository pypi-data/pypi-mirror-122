from __future__ import annotations

from collections.abc import Iterator

from .exceptions import EmptyString


class nonemptystr(str):
    def __new__(cls, obj: object) -> nonemptystr:
        s = str(obj)
        if not s:
            raise EmptyString("string is empty")
        return str.__new__(nonemptystr, s)

    @classmethod
    def __get_validators__(cls) -> Iterator[type[nonemptystr]]:
        yield cls
