"""Process styles from strings to Enum values."""
from __future__ import annotations

from typing import List
from typing import Union

from colourout.styles import Styles


def process_styles(styles: List[Union[Styles, str]]) -> List[str]:
    """Convert strings to Enum values."""
    processed = []

    for style in styles:
        if not isinstance(style, Styles):
            style = Styles[style]

        processed.append(style.value)

    return processed
