from app.core.utils.category_utils import expand_book_range, flatten_categories


def test_expand_book_range():
    assert expand_book_range("Enchanted Book (Growth V-VII)") == [
        "Enchanted Book (Growth V)",
        "Enchanted Book (Growth VI)",
        "Enchanted Book (Growth VII)",
    ]
    # одиночный уровень — возвращается как есть
    assert expand_book_range("Enchanted Book (Chimera I)") == [
        "Enchanted Book (Chimera I)",
    ]
    # не книга — как есть
    assert expand_book_range("Hyperion") == ["Hyperion"]


def test_flatten_categories_yields_paths():
    tree = {
        "Farming": {
            "Carrot": ["Carrot", "Enchanted Carrot"],
            "Empty": [],
        },
        "Mining": {
            "Diamond": ["Diamond"],
        },
    }
    result = list(flatten_categories(tree))
    assert (("Farming", "Carrot"), "Carrot") in result
    assert (("Farming", "Carrot"), "Enchanted Carrot") in result
    assert (("Farming", "Empty"), "") in result           # пустая подкатегория
    assert (("Mining", "Diamond"), "Diamond") in result