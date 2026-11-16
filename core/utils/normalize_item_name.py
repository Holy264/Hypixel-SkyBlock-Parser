
import re

MC_FORMAT_PATTERN = re.compile(r"§[0-9A-Fa-fk-orx]")


LEVEL_PREFIX_PATTERN = re.compile(r"^\[Lvl \d+\]\s*")


#    апостроф, точку, дефис. Остальное (✪, ◆, эмодзи, скобки и т.п.) — режем.
CLEAN_SYMBOLS_PATTERN = re.compile(r"[^\w\s\-'.]", flags=re.UNICODE)

MULTIPLE_SPACES_PATTERN = re.compile(r"\s+")


def normalize_item_name(raw: str) -> str:
    if not isinstance(raw, str):
        return ""
    # порядок ВАЖЕН:
    s = MC_FORMAT_PATTERN.sub("", raw)          # §7 §6 §a … → ''
    s = LEVEL_PREFIX_PATTERN.sub("", s).strip() #  '[Lvl 100] …' 
    s = CLEAN_SYMBOLS_PATTERN.sub("", s)        # ✪ ◆ и т.п.
    s = MULTIPLE_SPACES_PATTERN.sub(" ", s).strip()
    return s