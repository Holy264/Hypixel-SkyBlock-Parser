"""
Маппинг display_name → real product_id (Hypixel Bazaar API).
"""

import re
from models.product_id_manual import MANUAL_CATEGORIES 
from core.utils.category_utils import expand_book_range, flatten_categories, slugify
from models.seed_data import BAZAAR_CATEGORIES


# ═══════════════════════════════════════════════════════════════════
# ЯВНЫЕ: display_name → product_id
# ═══════════════════════════════════════════════════════════════════
PRODUCT_ID_OVERRIDES: dict[str, str] = {
    # Farming
    "Carrot":                           "CARROT_ITEM",
    "Potato":                           "POTATO_ITEM",
    "Cocoa Beans":                      "INK_SACK:3",
    "Nether Wart":                      "NETHER_STALK",
    "Raw Porkchop":                     "PORK",
    "Raw Mutton":                       "MUTTON",
    "Raw Rabbit":                       "RABBIT",
    "Raw Beef":                         "RAW_BEEF",
    "Raw Chicken":                      "RAW_CHICKEN",
    "Rabbit's Foot":                    "RABBIT_FOOT",
    "Enchanted Carrot on a Stick":      "ENCHANTED_CARROT_STICK",
    "Melon Slice":                      "MELON",
    "Enchanted Melon Slice":            "ENCHANTED_MELON",
    "Enchanted Glistering Melon Slice": "ENCHANTED_GLISTERING_MELON",
    "Melon":                            "MELON_BLOCK",
    "Enchanted Melon":                  "ENCHANTED_MELON_BLOCK",
    "Enchanted Cocoa Beans":            "ENCHANTED_COCOA",
    "Enchanted Raw Porkchop":           "ENCHANTED_PORK",
    "Enchanted Cooked Porkchop":        "ENCHANTED_GRILLED_PORK",
    "Enchanted Raw Mutton":             "ENCHANTED_MUTTON",
    "Enchanted Nether Wart":            "ENCHANTED_NETHER_STALK",
    "Mutant Nether Wart":               "MUTANT_NETHER_STALK",
    # Mining
    "Lapis Lazuli":                     "INK_SACK:4",
    "Redstone Dust":                    "REDSTONE",
    "Enchanted Redstone Dust":          "ENCHANTED_REDSTONE",
    # Combat
    "Arachne's Calling":                "ARACHNE_CALLING",
    "Arachne's Fang":                   "ARACHNE_FANG",
    "L.A.S.R.'s Eye":                   "LASR_EYE",
    # Woods & Fishes
    "Oak Log":                          "LOG",
    "Spruce Log":                       "LOG:1",
    "Birch Log":                        "LOG:2",
    "Jungle Log":                       "LOG:3",
    "Acacia Log":                       "LOG:4",
    "Dark Oak Log":                     "LOG:5",
    "Raw Cod":                          "RAW_FISH",
    "Raw Salmon":                       "RAW_FISH:1",
    "Tropical Fish":                    "RAW_FISH:2",
    "Pufferfish":                       "RAW_FISH:3",
    "Ink Sac":                          "INK_SACK",
    "Emperor's Skull":                  "EMPEROR_SKULL",
}


# ═══════════════════════════════════════════════════════════════════
# ПАТТЕРН: ГЕМСТОУНЫ
# ═══════════════════════════════════════════════════════════════════
_GEM_QUALITIES = ["Rough", "Flawed", "Fine", "Flawless", "Perfect"]
_GEM_TYPES = [
    "Jade", "Amber", "Topaz", "Sapphire", "Amethyst", "Jasper",
    "Ruby", "Opal", "Onyx", "Aquamarine", "Citrine", "Peridot",
]


def _build_gemstone_overrides() -> dict[str, str]:
    return {
        f"{q} {t} Gemstone": f"{q.upper()}_{t.upper()}_GEM"
        for q in _GEM_QUALITIES
        for t in _GEM_TYPES
    }


# ═══════════════════════════════════════════════════════════════════
# ПАТТЕРН: ENCHANTED BOOKS
# ═══════════════════════════════════════════════════════════════════
_ROMAN = {
    "I": 1, "II": 2, "III": 3, "IV": 4, "V": 5,
    "VI": 6, "VII": 7, "VIII": 8, "IX": 9, "X": 10,
}
_BOOK_RE = re.compile(r"^Enchanted Book \((.+?)\s+([IVX]+)\)$")


def _enchanted_book_id(display: str) -> str | None:
    m = _BOOK_RE.match(display)
    if not m:
        return None
    name, roman = m.groups()
    level = _ROMAN.get(roman)
    if level is None:
        return None
    return f"ENCHANTMENT_{slugify(name)}_{level}"


def _build_enchantment_overrides() -> dict[str, str]:
    result: dict[str, str] = {}
    for _path, display in flatten_categories(BAZAAR_CATEGORIES):
        if not display.startswith("Enchanted Book ("):
            continue
        for single in expand_book_range(display):
            pid = _enchanted_book_id(single)
            if pid:
                result[single] = pid
    return result


# ═══════════════════════════════════════════════════════════════════
# СБОРКА PRODUCT_TO_CATEGORY
# ═══════════════════════════════════════════════════════════════════
def _merge_overrides() -> dict[str, str]:
    merged = dict(PRODUCT_ID_OVERRIDES)
    merged.update(_build_gemstone_overrides())
    merged.update(_build_enchantment_overrides())
    return merged


def _build_product_to_category() -> dict[str, tuple[str, str]]:
    overrides = _merge_overrides()
    result: dict[str, tuple[str, str]] = {}
    for path, display in flatten_categories(BAZAAR_CATEGORIES):
        main, sub = path[0], path[-1]
        for single in expand_book_range(display):
            product_id = overrides.get(single) or slugify(single)
            result[product_id] = (main, sub)
    return result


PRODUCT_TO_CATEGORY: dict[str, tuple[str, str]] = _build_product_to_category()


def _build_product_id_to_display() -> dict[str, str]:
    overrides = _merge_overrides()
    result: dict[str, str] = {}
    for _path, display in flatten_categories(BAZAAR_CATEGORIES):
        for single in expand_book_range(display):
            product_id = overrides.get(single) or slugify(single)
            result[product_id] = single
    return result

# Исаользуется для автокомита поиска 
PRODUCT_ID_TO_DISPLAY: dict[str, str] = _build_product_id_to_display()

# ═══════════════════════════════════════════════════════════════════
# ПРАВИЛА ПО ПРЕФИКСУ / СУФФИКСУ / ПОДСТРОКЕ
# ═══════════════════════════════════════════════════════════════════
PREFIX_RULES: list[tuple[str, tuple[str, str]]] = [
    # порядок важен
    ("ENCHANTMENT_ULTIMATE_",     ("Oddities", "Ultimate Enchantments")),
    ("ENCHANTMENT_",              ("Oddities", "Normal Enchantments")),
    ("SHARD_",                    ("Oddities", "Shards")),
    ("FACTION_RABBIT_",           ("Farming", "Rabbit")),
    ("ESSENCE_",                  ("Oddities", "Essence")),
    ("JERRY_BOX_",                ("Oddities", "Jerry Boxes")),
    ("GENERATOR_UPGRADE_STONE_",  ("Oddities", "Minion Upgrades")),
    ("PET_ITEM_",                 ("Oddities", "Pet Upgrades")),
    ("GRIFFIN_UPGRADE_STONE_",    ("Oddities", "Mythological")),
    ("MAGMA_FISH",                ("Woods & Fishes", "Magmafish")),
    ("GOBLIN_EGG_",               ("Mining", "Goblin Eggs")),
    ("DWARVEN_OS_",               ("Oddities", "Consumables")),
    ("LOG_",                      ("Woods & Fishes", "Oak")),
    ("SAND:",                     ("Mining", "Sand")),
]

SUFFIX_RULES: list[tuple[str, tuple[str, str]]] = [
    ("_GARDEN_CHIP",              ("Farming", "Garden")),
    ("_FROG_TREAT",               ("Farming", "Garden")),
    ("_WITCH_CAULDRON",           ("Farming", "Garden")),
    ("_SEAL_PLUSHIE",             ("Farming", "Garden")),
    ("_PIG_EAR",                  ("Farming", "Garden")),
    ("_SLOTH_CLAW",               ("Farming", "Garden")),
    ("_HONEY_DIPPER",             ("Farming", "Garden")),
    ("_SHARD",                    ("Oddities", "Shards")),
    ("_FOSSIL",                   ("Oddities", "Reforge Stones")),
    ("_DISTILLATE",               ("Combat", "Inferno Demonlord")),
    ("_PORTABLE_WASHER",          ("Oddities", "Item Upgrades")),
]

CONTAINS_RULES: list[tuple[str, tuple[str, str]]] = [
    ("_BOOSTER_",                 ("Oddities", "Boosters")),
    ("_POT_OF_HONEYCOMB",         ("Farming", "Garden")),
    ("_ENCHANTED_CHEST",          ("Oddities", "Minion Upgrades")),
    ("_HONEYCOMB_BLOCK",          ("Farming", "Garden")),
]


def classify_by_pattern(product_id: str) -> tuple[str, str] | None:
    for prefix, cat in PREFIX_RULES:
        if product_id.startswith(prefix):
            return cat
    for suffix, cat in SUFFIX_RULES:
        if product_id.endswith(suffix):
            return cat
    for needle, cat in CONTAINS_RULES:
        if needle in product_id:
            return cat
    return None


def resolve_category(product_id: str) -> tuple[str, str] | None:
    cat = PRODUCT_TO_CATEGORY.get(product_id)
    if cat:
        return cat
    cat = MANUAL_CATEGORIES.get(product_id)
    if cat:
        return cat
    return classify_by_pattern(product_id)