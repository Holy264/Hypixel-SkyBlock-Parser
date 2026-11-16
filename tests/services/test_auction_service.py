import pytest

from services import auction_service as svc_mod
from services.auction_service import AuctionService


class FakeClient:
    def __init__(self, ended):
        self._ended = ended

    async def get_auctions_ended(self):
        return self._ended


class FakeRepo:
    def __init__(self):
        self.saved: list[dict] = []

    async def save_sales(self, sales):
        self.saved.extend(sales)
        return len(sales)


async def test_fetch_and_save_sales_filters_invalid(monkeypatch):
    # подменяем извлечение NBT — нам нужен только happy-path фильтра
    def fake_extract(item_bytes):
        if item_bytes == "bad":
            return None
        return item_bytes, "LEGENDARY"

    monkeypatch.setattr(svc_mod, "extract_item_meta", fake_extract)

    ended = {
        "auctions": [
            {"auction_id": "u1", "item_bytes": "§6Hyperion", "price": 1_000, "bin": True},
            {"auction_id": "u2", "item_bytes": "§6Hyperion", "price": 2_000, "bin": True},
            {"auction_id": "u3", "item_bytes": "bad",         "price": 3_000},  # NBT fail
            {"item_bytes": "§6Hyperion", "price": 4_000},                       # нет uuid
            {"auction_id": "u4", "item_bytes": "§6Hyperion"},                   # нет price
        ]
    }
    repo = FakeRepo()
    service = AuctionService(FakeClient(ended), repo)

    saved = await service.fetch_and_save_sales()

    assert saved == 2
    assert all(s["item_name"] == "Hyperion" for s in repo.saved)
    assert all(s["tier"] == "LEGENDARY" for s in repo.saved)


async def test_fetch_and_save_sales_returns_zero_on_client_error():
    class BrokenClient:
        async def get_auctions_ended(self):
            raise RuntimeError("api down")

    service = AuctionService(BrokenClient(), FakeRepo())
    assert await service.fetch_and_save_sales() == 0