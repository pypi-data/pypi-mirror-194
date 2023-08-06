"""Print to stdout with colour."""
from __future__ import annotations

from typing import List
from typing import Optional
from typing import Union

from colourout.process_styles import process_styles
from colourout.styles import Styles


def printc(
    *__values: object,
    sep: str = " ",
    end: str = "\n",
    styles: Optional[List[Union[Styles, str]]] = None,
) -> None:
    r"""
    Print with colour.

    Prints text to stdout with provided formatting.
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

    >>> printc("Hello, world!", styles=["BLUE", "ITALIC"])
    \033[94m\033[3mHello, world!\033[0m
    """
    styles = styles or [Styles.END]
    processed_styles = process_styles(styles)

    print(*processed_styles, sep="", end="")
    print(*__values, sep=sep, end=end)
    print(Styles.END.value, end="")
