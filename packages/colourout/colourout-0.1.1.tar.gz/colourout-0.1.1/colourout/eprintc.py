"""Print to stderr with colour."""
from __future__ import annotations

import sys
from typing import List
from typing import Optional
from typing import Union

from colourout.printc import printc
from colourout.styles import Styles


def eprintc(
    *__values: object,
    sep: str = " ",
    end: str = "\n",
    styles: Optional[List[Union[Styles, str]]] = None,
) -> None:
    r"""
    Print to stderr with colour.

    Prints text to stderr with provided formatting.
    Always ends with a reset.

    Params
    ------
    __values: :class:`object`
        The values to print.

    sep: :class:`str`
        The separator to use between values.

    end: :class:`str`
        The string to print at the end.

    styles: :class:`List[Union[Styles, str]]`
        The styles to apply to the output.

    >>> eprintc("Hello, world!", styles=["BLUE", "ITALIC"])
    \033[94m\033[3mHello, world!\033[0m
    """
    printc(*__values, sep=sep, end=end, styles=styles, file=sys.stderr)
