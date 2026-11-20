import pytest

from app.core.utils.category_utils import slugify


@pytest.mark.parametrize("raw, expected", [
    ("Carrot",                        "CARROT"),
    ("Carrot Item",                   "CARROT_ITEM"),
    ("Enchanted Carrot on a Stick",   "ENCHANTED_CARROT_ON_A_STICK"),
    ("L.A.S.R.'s Eye",                "L_A_S_R_S_EYE"),
    ("  hello  world  ",              "HELLO_WORLD"),
    ("",                              ""),
])
def test_slugify(raw, expected):
    assert slugify(raw) == expected