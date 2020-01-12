# This program is free software. See file LICENSE for details.

from math import floor

_typical_prefix_map = {
    0   :   "th",
    1   :   "st",
    2   :   "nd",
    3   :   "rd",
    4   :   "th",
    5   :   "th",
    6   :   "th",
    7   :   "th",
    8   :   "th",
    9   :   "th",
}

def ordinal(number: int) -> str:
    if not isinstance(number, int):
        raise TypeError(f"Expected {int} but got {type(number)}")
    
    elif _is_teenthish(abs(number)):
        return f"{number}th"
    else:
        return f"{number}{_typical_prefix_map[abs(number) % 10]}"

def _is_teenthish(number: int) -> bool:
    return (floor(number / 10) % 10) == 1
