
import re
from typing import Iterator

_SLUG_RE = re.compile(r"[^A-Z0-9]+")
_BOOK_RANGE_RE = re.compile(r"^Enchanted Book \((.+?)\s+([IVX]+)-([IVX]+)\)$")
_ROMAN_ORDER = ["I", "II", "III", "IV", "V", "VI", "VII", "VIII", "IX", "X"]


def slugify(name: str) -> str:
    s = name.upper()
    s = _SLUG_RE.sub("_", s)
    return s.strip("_")



def flatten_categories(
    tree: dict, path: tuple[str, ...] = (),
) -> Iterator[tuple[tuple[str, ...], str]]:
    """
    Обходит дерево и выдаёт пары (путь_категорий, display_name).
    """
    for key, value in tree.items():
        new_path = path + (key,)
        if isinstance(value, dict):
            yield from flatten_categories(value, new_path)
        elif isinstance(value, list):
            if not value:
                yield new_path, ""
            else:
                for item in value:
                    yield new_path, item


def expand_book_range(display: str) -> list[str]:
    m = _BOOK_RANGE_RE.match(display)
    if not m:
        return [display]
    name, lo, hi = m.groups()
    try:
        i, j = _ROMAN_ORDER.index(lo), _ROMAN_ORDER.index(hi)
    except ValueError:
        return [display]
    if i > j:
        i, j = j, i
    return [f"Enchanted Book ({name} {_ROMAN_ORDER[k]})" for k in range(i, j + 1)]
