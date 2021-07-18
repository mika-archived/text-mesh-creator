# -------------------------------------------------------------------------------------------
#  Copyright (c) Natsuneko. All rights reserved.
#  Licensed under the MIT License. See LICENSE in the project root for license information.
# -------------------------------------------------------------------------------------------

from __future__ import annotations

import string
import sys


def get_unprintable_ascii_chars() -> list[str]:
    return [chr(c) for c in range(128) if chr(c) not in string.printable]


def get_invalid_filename_chars() -> list[str]:
    if sys.platform == "win32":
        invalid_chars = get_unprintable_ascii_chars()
        return invalid_chars + ["/", ":", "*", "?", "\"", "<", ">", "|", "\t", "\n", "\r", "\x0b", "\x0c"]

    else:
        invalid_chars = get_unprintable_ascii_chars()
        return invalid_chars + ["/"]


def replace_invalid_filename_chars(filename: str) -> str:
    for c in get_invalid_filename_chars():
        filename = filename.replace(c, "_")

    return filename
