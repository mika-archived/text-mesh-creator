# -----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
#  Copyright (c) Natsuneko. All rights reserved.
#  Licensed under the License Zero Parity 7.0.0 (see LICENSE-PARITY file) and MIT (contributions, see LICENSE-MIT file) with exception License Zero Patron 1.0.0 (see LICENSE-PATRON file)
# -----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

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
