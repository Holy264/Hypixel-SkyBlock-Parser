import pytest

from services.bazaar_service import BazaarService


class FakeClient:
    def __init__(self, products):
        self._products = products

    async def get_bazaar(self):
        return {"products": self._products}


class FakeRepo:
    def __init__(self):
        self.saved: list[dict] = []

    async def save_prices(self, prices):
        self.saved.extend(prices)
        return len(prices)


@pytest.fixture
def category_cache():
    """Изолируем глобальный SUB_CATEGORY_CACHE между тестами."""
    from core import category_cache as cc
    cc.SUB_CATEGORY_CACHE.clear()
    cc.SUB_CATEGORY_CACHE[("Farming", "Carrot")] = 1
    cc.SUB_CATEGORY_CACHE[("Unknown", "Uncategorized")] = 999
    yield cc
    cc.SUB_CATEGORY_CACHE.clear()


async def test_fetch_and_save_assigns_categories(category_cache):
    products = {
        "CARROT_ITEM": {
            "quick_status": {
                "buyPrice": 10.5, "sellPrice": 9.5,
                "buyVolume": 100, "sellVolume": 200,
            },
        },
        "TOTALLY_FAKE_PRODUCT_XYZ": {
            "quick_status": {
                "buyPrice": 1.0, "sellPrice": 0.5,
                "buyVolume": 10, "sellVolume": 20,
            },
        },
    }
    repo = FakeRepo()
    service = BazaarService(FakeClient(products), repo)

    count = await service.fetch_and_save()

    assert count == 2
    by_id = {p["product_id"]: p for p in repo.saved}
    # известный продукт — в реальную категорию
    assert by_id["CARROT_ITEM"]["sub_category_id"] == 1
    # неизвестный — в fallback
    assert by_id["TOTALLY_FAKE_PRODUCT_XYZ"]["sub_category_id"] == 999


async def test_fetch_and_save_logs_uncategorized(category_cache, caplog):
    products = {
        "TOTALLY_FAKE_PRODUCT_XYZ": {
            "quick_status": {
                "buyPrice": 1, "sellPrice": 1,
                "buyVolume": 0, "sellVolume": 0,
            },
        },
    }
    service = BazaarService(FakeClient(products), FakeRepo())

    with caplog.at_level("WARNING"):
        await service.fetch_and_save()

    assert any("без категории" in r.message for r in caplog.records)