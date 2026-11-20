import pytest

from app.core.hypixel_client import _tier_from_colored_name


@pytest.mark.parametrize("name, expected", [
    ("§6Hyperion",                          "LEGENDARY"),
    ("§5Enderman",                          "EPIC"),
    ("§aEnderman",                          "UNCOMMON"),
    ("[§7Lvl 100§8] §5Enderman",            "EPIC"),
    ("§fCommon Item",                       "COMMON"),
    ("§eUltimate Wise",                     "ULTIMATE"),
    ("Hyperion",                            None),   # без цветов — None
    ("",                                    None),
    (None,                                  None),
])
def test_tier_from_colored_name(name, expected):
    assert _tier_from_colored_name(name) == expected