import asyncio
import pytest


@pytest.fixture
def no_sleep(monkeypatch):

    calls: list[float] = []

    async def _fake_sleep(seconds):
        calls.append(seconds)

    monkeypatch.setattr(asyncio, "sleep", _fake_sleep)
    return calls