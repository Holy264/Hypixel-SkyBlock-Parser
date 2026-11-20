import httpx
import pytest

from app.core.hypixel_client import HypixelClient


@pytest.fixture
def make_client():
    """HypixelClient, у которого httpx-клиент заменён на MockTransport."""
    def _make(handler, api_key=""):
        c = HypixelClient(api_key=api_key)
        c._client = httpx.AsyncClient(
            base_url="https://api.hypixel.net/v2",
            transport=httpx.MockTransport(handler),
        )
        return c
    return _make


async def test_returns_on_first_success(make_client, no_sleep):
    client = make_client(lambda r: httpx.Response(200, json={"ok": True}))
    try:
        assert await client.get_bazaar() == {"ok": True}
    finally:
        await client.close()
    assert no_sleep == []


async def test_retries_on_429_with_backoff(make_client, no_sleep):
    calls = []

    def handler(req):
        calls.append(req.url.path)
        if len(calls) < 3:
            return httpx.Response(429, json={"error": "rate limited"})
        return httpx.Response(200, json={"ok": True})

    client = make_client(handler)
    try:
        assert await client.get_bazaar() == {"ok": True}
    finally:
        await client.close()

    assert len(calls) == 3
    # 15 * 1, 15 * 2 — и никакого сна перед последней (успешной) попыткой
    assert no_sleep == [15, 30]


async def test_does_not_retry_on_401(make_client, no_sleep):
    calls = []
    def handler(req):
        calls.append(req.url.path)
        return httpx.Response(401, json={"error": "bad key"})

    client = make_client(handler)
    try:
        with pytest.raises(httpx.HTTPStatusError):
            await client.get_bazaar()
    finally:
        await client.close()

    assert len(calls) == 1
    assert no_sleep == []


async def test_gives_up_after_max_retries_without_last_sleep(make_client, no_sleep):
    calls = []
    def handler(req):
        calls.append(req.url.path)
        return httpx.Response(429, json={"error": "rate limited"})

    client = make_client(handler)
    try:
        with pytest.raises(httpx.HTTPStatusError):
            await client.get_bazaar()
    finally:
        await client.close()

    assert len(calls) == 3
    # 2 sleep'а (после 1-й и 2-й попытки), на последней — сразу raise
    assert no_sleep == [15, 30]


async def test_retries_on_network_error(make_client, no_sleep):
    calls = []
    def handler(req):
        calls.append(req.url.path)
        if len(calls) < 2:
            raise httpx.ConnectError("boom")
        return httpx.Response(200, json={"ok": True})

    client = make_client(handler)
    try:
        assert await client.get_bazaar() == {"ok": True}
    finally:
        await client.close()

    assert no_sleep == [1]  # 2**0