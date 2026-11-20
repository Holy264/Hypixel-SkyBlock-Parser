import pytest

from app.core.utils.normalize_item_name import normalize_item_name
from app.core.utils.normalize_product_id import normalize_product_id


class TestNormalizeItemName:
    @pytest.mark.parametrize("raw, expected", [
        ("§6Hyperion",                        "Hyperion"),
        ("Hyperion",                          "Hyperion"),
        ("[Lvl 100] Enderman",                "Enderman"),
        ("§7[§7Lvl 100§8] §5Enderman",        "Enderman"),
        ("✪ Hyperion ✪",                      "Hyperion"),
        ("  Hyperion  ",                      "Hyperion"),
        ("Hyperion  Pet",                     "Hyperion Pet"),
        ("L.A.S.R.'s Eye",                    "L.A.S.R.'s Eye"),
    ])
    def test_normalizes(self, raw, expected):
        assert normalize_item_name(raw) == expected

    def test_idempotent(self):
        for s in ("Hyperion", "Hyperion Pet", "L.A.S.R.'s Eye"):
            assert normalize_item_name(normalize_item_name(s)) == s

    def test_non_string(self):
        assert normalize_item_name(None) == ""
        assert normalize_item_name(123) == ""


class TestNormalizeProductId:
    @pytest.mark.parametrize("raw, expected", [
        ("Carrot Item ",        "CARROT_ITEM"),
        ("  carrot_item  ",     "CARROT_ITEM"),
        ("ENCHANTED_CARROT",    "ENCHANTED_CARROT"),
        ("",                    ""),
        (None,                  ""),
    ])
    def test_normalizes(self, raw, expected):
        assert normalize_product_id(raw) == expected