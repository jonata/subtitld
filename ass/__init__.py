from . import document, line, section
from .document import *  # noqa: F40
from .line import *  # noqa: F40
from .section import *  # noqa: F40

__all__ = [
    *document.__all__,
    *line.__all__,
    *section.__all__,
    "parse",
]

parse = document.Document.parse_file
