import re
import unicodedata
from functools import wraps
import asyncio

SUPERSCRIPT_REGEX = re.compile(r"\^([+|-]?\d+)")


def slugify(txt):

    """
    Slugify a unicode string.

    >>> slugify("Héllo Wörld-LCID#2")
    'hello_world_lcid2'
    >>> slugify("mystran-test-cases.BAR.no_offset.test_bar_06.ini")
    'bar_no_offset_test_bar_06_ini'
    """
    txt = unicodedata.normalize("NFKD", txt)
    txt = txt.replace("mystran-test-cases.", "")
    txt = txt.replace(".", "_")
    txt = re.sub(r"[^\w\s-]", "", txt).strip().lower()
    return re.sub(r"[-\s]+", "_", txt)


if __name__ == "__main__":
    import doctest

    doctest.testmod(optionflags=doctest.ELLIPSIS | doctest.NORMALIZE_WHITESPACE)
