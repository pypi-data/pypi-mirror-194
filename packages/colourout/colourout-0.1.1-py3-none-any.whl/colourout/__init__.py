r"""
Colourout - A Python package for printing coloured text to the terminal.

Exports
-------
:meth:`printc`
    Print coloured text to stdout.

:meth:`eprintc`
    Print coloured text to stderr.

:class:`Styles`
    Enum of valid terminal styles, foreground colours, and background colours.
    Background colours are prefixed with `BG_`.
    Light colours are prefixed with `LIGHT_`.
    Light colours may not be supported by all terminals.

Examples
--------
>>> from colourout import printc
>>> printc("Hello, world!", styles=["BLUE", "ITALIC"])
\033[94m\033[3mHello, world!\033[0m
>>> from colourout import eprintc
>>> eprintc("Hello, world!", styles=["BLUE", "ITALIC"])
\033[94m\033[3mHello, world!\033[0m
>>> from colourout import Styles
>>> printc("Hello, world!", styles=[Styles.BLUE, Styles.ITALIC])
\033[94m\033[3mHello, world!\033[0m
>>> printc("Hello, world!", styles=[Styles.BLUE, "ITALIC"])
\033[94m\033[3mHello, world!\033[0m
"""
from __future__ import annotations

__all__ = ("eprintc", "printc", "Styles")
__version__ = "0.1.1"

from colourout.eprintc import eprintc
from colourout.printc import printc
from colourout.styles import Styles
