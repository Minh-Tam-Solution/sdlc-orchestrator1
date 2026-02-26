"""
Unit tests for OTT Identity Resolver — Sprint 209 (E7, E8, E9, E10, E13).

Covers the resolution chain defined in D-068-01:
    1. oauth_accounts lookup (E7)
    2. OTT_GATEWAY_USER_ID env var fallback (E8)
    3. None / anonymous (E9)
    4. UUID passthrough for web/CLI users (E10)
    5. Group chat permission isolation (E13)
"""

from __future__ import annotations

import uuid
from unittest.mock import AsyncMock, MagicMock, patch

import pytest

from app.services.agent_bridge.ott_identity_resolver import (
    _CACHE_TTL,
    resolve_ott_user_id,
)


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------

@pytest.fixture
def redis_mock() -> AsyncMock:
    """AsyncMock Redis client with get/setex methods."""
    mock = AsyncMock()
    mock.get = AsyncMock(return_value=None)
    mock.setex = AsyncMock(return_value=True)
    return mock


@pytest.fixture
def db_mock() -> AsyncMock:
    """AsyncMock async DB session with execute chain."""
    mock = AsyncMock()
    result = MagicMock()
    result.scalar_one_or_none = MagicMock(return_value=None)
    mock.execute = AsyncMock(return_value=result)
    return mock


# ---------------------------------------------------------------------------
# E7: Resolve with oauth_accounts match → returns User UUID
# ---------------------------------------------------------------------------

@pytest.mark.asyncio
async def test_e7_resolve_via_oauth_accounts(redis_mock: AsyncMock, db_mock: AsyncMock) -> None:
    """E7: When oauth_accounts has a matching row for (channel, sender_id),
    the resolver returns the linked User UUID and caches the result."""
    expected_user_id = uuid.uuid4()
    channel = "telegram"
    sender_id = "123456789"

    # Arrange: DB returns a matching user_id
    db_result = MagicMock()
    db_result.scalar_one_or_none = MagicMock(return_value=expected_user_id)
    db_mock.execute = AsyncMock(return_value=db_result)

    # Act
    result = await resolve_ott_user_id(channel, sender_id, redis_mock, db=db_mock)

    # Assert: returns the user UUID as string
    assert result == str(expected_user_id)

    # Assert: DB was queried
    db_mock.execute.assert_awaited_once()

    # Assert: result was cached with correct key and TTL
    cache_key = f"ott:identity:{channel}:{sender_id}"
    redis_mock.setex.assert_awaited_once_with(cache_key, _CACHE_TTL, str(expected_user_id))


@pytest.mark.asyncio
async def test_e7_cached_result_returns_without_db_lookup(redis_mock: AsyncMock, db_mock: AsyncMock) -> None:
    """E7 supplement: When the Redis cache already holds the mapping,
    the resolver returns it directly without querying the DB."""
    cached_user_id = str(uuid.uuid4())
    channel = "telegram"
    sender_id = "123456789"

    # Arrange: Redis cache hit
    redis_mock.get = AsyncMock(return_value=cached_user_id)

    # Act
    result = await resolve_ott_user_id(channel, sender_id, redis_mock, db=db_mock)

    # Assert: returns cached value
    assert result == cached_user_id

    # Assert: DB was NOT queried (cache hit)
    db_mock.execute.assert_not_awaited()


# ---------------------------------------------------------------------------
# E8: Resolve with OTT_GATEWAY_USER_ID env var fallback
# ---------------------------------------------------------------------------

@pytest.mark.asyncio
async def test_e8_resolve_via_env_var_fallback(redis_mock: AsyncMock, db_mock: AsyncMock) -> None:
    """E8: When oauth_accounts has no match but OTT_GATEWAY_USER_ID is set,
    the resolver falls back to the env var UUID."""
    gateway_user_id = str(uuid.uuid4())
    channel = "telegram"
    sender_id = "999888777"

    # Arrange: DB returns no match
    db_result = MagicMock()
    db_result.scalar_one_or_none = MagicMock(return_value=None)
    db_mock.execute = AsyncMock(return_value=db_result)

    # Arrange: env var set
    with patch.dict("os.environ", {"OTT_GATEWAY_USER_ID": gateway_user_id}):
        # Act
        result = await resolve_ott_user_id(channel, sender_id, redis_mock, db=db_mock)

    # Assert: returns the env var UUID
    assert result == gateway_user_id

    # Assert: result was cached
    cache_key = f"ott:identity:{channel}:{sender_id}"
    redis_mock.setex.assert_awaited_with(cache_key, _CACHE_TTL, gateway_user_id)


@pytest.mark.asyncio
async def test_e8_env_var_non_uuid_ignored(redis_mock: AsyncMock, db_mock: AsyncMock) -> None:
    """E8 supplement: If OTT_GATEWAY_USER_ID is set but not UUID-like,
    the resolver skips it and returns None."""
    channel = "telegram"
    sender_id = "999888777"

    # Arrange: DB returns no match
    db_result = MagicMock()
    db_result.scalar_one_or_none = MagicMock(return_value=None)
    db_mock.execute = AsyncMock(return_value=db_result)

    # Arrange: env var set to non-UUID value
    with patch.dict("os.environ", {"OTT_GATEWAY_USER_ID": "not-a-valid-uuid"}):
        result = await resolve_ott_user_id(channel, sender_id, redis_mock, db=db_mock)

    # Assert: returns None (env var is not UUID-like)
    assert result is None


# ---------------------------------------------------------------------------
# E9: Resolve with no mapping → returns None
# ---------------------------------------------------------------------------

@pytest.mark.asyncio
async def test_e9_no_mapping_returns_none(redis_mock: AsyncMock, db_mock: AsyncMock) -> None:
    """E9: When no oauth_accounts match and no OTT_GATEWAY_USER_ID env var,
    the resolver returns None and caches the negative result."""
    channel = "telegram"
    sender_id = "000111222"

    # Arrange: DB returns no match
    db_result = MagicMock()
    db_result.scalar_one_or_none = MagicMock(return_value=None)
    db_mock.execute = AsyncMock(return_value=db_result)

    # Arrange: no env var
    with patch.dict("os.environ", {}, clear=True):
        result = await resolve_ott_user_id(channel, sender_id, redis_mock, db=db_mock)

    # Assert: returns None
    assert result is None

    # Assert: negative result cached as "__none__"
    cache_key = f"ott:identity:{channel}:{sender_id}"
    redis_mock.setex.assert_awaited_with(cache_key, _CACHE_TTL, "__none__")


@pytest.mark.asyncio
async def test_e9_cached_negative_returns_none(redis_mock: AsyncMock) -> None:
    """E9 supplement: When Redis cache holds '__none__' sentinel,
    the resolver returns None without DB lookup."""
    channel = "telegram"
    sender_id = "000111222"

    # Arrange: Redis returns negative sentinel
    redis_mock.get = AsyncMock(return_value="__none__")

    # Act
    result = await resolve_ott_user_id(channel, sender_id, redis_mock, db=None)

    # Assert: returns None (cached negative)
    assert result is None


@pytest.mark.asyncio
async def test_e9_empty_sender_id_returns_none(redis_mock: AsyncMock) -> None:
    """E9 edge case: Empty sender_id returns None immediately."""
    result = await resolve_ott_user_id("telegram", "", redis_mock, db=None)
    assert result is None

    # Assert: no Redis or DB calls made
    redis_mock.get.assert_not_awaited()


@pytest.mark.asyncio
async def test_e9_no_db_session_no_env_returns_none(redis_mock: AsyncMock) -> None:
    """E9 edge case: When db=None and no env var, returns None."""
    channel = "zalo"
    sender_id = "5551234"

    with patch.dict("os.environ", {}, clear=True):
        result = await resolve_ott_user_id(channel, sender_id, redis_mock, db=None)

    assert result is None


# ---------------------------------------------------------------------------
# E10: Resolve with UUID sender_id (web/CLI user) → passthrough
# ---------------------------------------------------------------------------

@pytest.mark.asyncio
async def test_e10_uuid_sender_id_passthrough(redis_mock: AsyncMock, db_mock: AsyncMock) -> None:
    """E10: When sender_id is already a valid UUID (web/CLI user),
    the resolver returns it directly without any DB or cache lookup."""
    web_user_uuid = str(uuid.uuid4())
    channel = "web"

    # Act
    result = await resolve_ott_user_id(channel, web_user_uuid, redis_mock, db=db_mock)

    # Assert: passthrough — same UUID returned
    assert result == web_user_uuid

    # Assert: no Redis get or DB lookup (fast path)
    redis_mock.get.assert_not_awaited()
    db_mock.execute.assert_not_awaited()
    redis_mock.setex.assert_not_awaited()


@pytest.mark.asyncio
async def test_e10_uuid_passthrough_cli_channel(redis_mock: AsyncMock) -> None:
    """E10 supplement: UUID passthrough works regardless of channel name."""
    cli_user_uuid = str(uuid.uuid4())

    result = await resolve_ott_user_id("cli", cli_user_uuid, redis_mock, db=None)

    assert result == cli_user_uuid
    redis_mock.get.assert_not_awaited()


# ---------------------------------------------------------------------------
# E13: Group chat permission isolation
# ---------------------------------------------------------------------------

@pytest.mark.asyncio
async def test_e13_group_chat_different_senders_different_users(
    redis_mock: AsyncMock,
) -> None:
    """E13: In a group chat, different sender_ids resolve to different users.
    Each sender gets an independent identity lookup and cache entry."""
    channel = "telegram"
    sender_a = "111222333"
    sender_b = "444555666"
    user_a_id = uuid.uuid4()
    user_b_id = uuid.uuid4()

    # Use sequential side_effect: first call returns user_a, second returns user_b
    result_a_mock = MagicMock()
    result_a_mock.scalar_one_or_none = MagicMock(return_value=user_a_id)
    result_b_mock = MagicMock()
    result_b_mock.scalar_one_or_none = MagicMock(return_value=user_b_id)

    db_mock = AsyncMock()
    db_mock.execute = AsyncMock(side_effect=[result_a_mock, result_b_mock])

    # Act: resolve sender A
    result_a = await resolve_ott_user_id(channel, sender_a, redis_mock, db=db_mock)

    # Act: resolve sender B
    result_b = await resolve_ott_user_id(channel, sender_b, redis_mock, db=db_mock)

    # Assert: different senders → different resolved users
    assert result_a == str(user_a_id)
    assert result_b == str(user_b_id)
    assert result_a != result_b

    # Assert: DB was called twice (once per sender)
    assert db_mock.execute.await_count == 2

    # Assert: each sender got its own cache key
    setex_calls = redis_mock.setex.await_args_list
    cache_keys_set = {call.args[0] for call in setex_calls}
    assert f"ott:identity:{channel}:{sender_a}" in cache_keys_set
    assert f"ott:identity:{channel}:{sender_b}" in cache_keys_set


@pytest.mark.asyncio
async def test_e13_same_sender_different_channels_isolated(
    redis_mock: AsyncMock,
) -> None:
    """E13 supplement: Same sender_id on different channels resolves independently.
    A Telegram user '12345' and a Zalo user '12345' are distinct identities."""
    sender_id = "12345"
    telegram_user = uuid.uuid4()
    zalo_user = uuid.uuid4()

    # Sequential side_effect: first call (telegram) → telegram_user, second (zalo) → zalo_user
    result_tg_mock = MagicMock()
    result_tg_mock.scalar_one_or_none = MagicMock(return_value=telegram_user)
    result_zalo_mock = MagicMock()
    result_zalo_mock.scalar_one_or_none = MagicMock(return_value=zalo_user)

    db_mock = AsyncMock()
    db_mock.execute = AsyncMock(side_effect=[result_tg_mock, result_zalo_mock])

    result_tg = await resolve_ott_user_id("telegram", sender_id, redis_mock, db=db_mock)
    result_zalo = await resolve_ott_user_id("zalo", sender_id, redis_mock, db=db_mock)

    # Assert: same sender_id, different channels → different users
    assert result_tg == str(telegram_user)
    assert result_zalo == str(zalo_user)
    assert result_tg != result_zalo

    # Assert: different cache keys per channel
    setex_calls = redis_mock.setex.await_args_list
    cache_keys_set = {call.args[0] for call in setex_calls}
    assert f"ott:identity:telegram:{sender_id}" in cache_keys_set
    assert f"ott:identity:zalo:{sender_id}" in cache_keys_set


# ---------------------------------------------------------------------------
# Error resilience
# ---------------------------------------------------------------------------

@pytest.mark.asyncio
async def test_redis_get_error_falls_through_to_db(redis_mock: AsyncMock, db_mock: AsyncMock) -> None:
    """When Redis.get raises an exception, the resolver ignores the cache error
    and proceeds to the DB lookup."""
    expected_user_id = uuid.uuid4()
    channel = "telegram"
    sender_id = "777888999"

    # Arrange: Redis get raises
    redis_mock.get = AsyncMock(side_effect=ConnectionError("Redis down"))

    # Arrange: DB returns a match
    db_result = MagicMock()
    db_result.scalar_one_or_none = MagicMock(return_value=expected_user_id)
    db_mock.execute = AsyncMock(return_value=db_result)

    # Act
    result = await resolve_ott_user_id(channel, sender_id, redis_mock, db=db_mock)

    # Assert: still resolves via DB
    assert result == str(expected_user_id)
    db_mock.execute.assert_awaited_once()


@pytest.mark.asyncio
async def test_db_error_falls_through_to_env_var(redis_mock: AsyncMock, db_mock: AsyncMock) -> None:
    """When DB execute raises an exception, the resolver falls through to
    the OTT_GATEWAY_USER_ID env var."""
    gateway_user_id = str(uuid.uuid4())
    channel = "telegram"
    sender_id = "111000111"

    # Arrange: DB raises
    db_mock.execute = AsyncMock(side_effect=Exception("DB connection lost"))

    with patch.dict("os.environ", {"OTT_GATEWAY_USER_ID": gateway_user_id}):
        result = await resolve_ott_user_id(channel, sender_id, redis_mock, db=db_mock)

    assert result == gateway_user_id


@pytest.mark.asyncio
async def test_cache_setex_error_ignored(redis_mock: AsyncMock, db_mock: AsyncMock) -> None:
    """When Redis.setex raises during caching, the resolver still returns
    the resolved user_id without propagating the error."""
    expected_user_id = uuid.uuid4()
    channel = "telegram"
    sender_id = "333444555"

    # Arrange: DB returns a match
    db_result = MagicMock()
    db_result.scalar_one_or_none = MagicMock(return_value=expected_user_id)
    db_mock.execute = AsyncMock(return_value=db_result)

    # Arrange: Redis setex raises
    redis_mock.setex = AsyncMock(side_effect=ConnectionError("Redis write failed"))

    # Act — should not raise
    result = await resolve_ott_user_id(channel, sender_id, redis_mock, db=db_mock)

    # Assert: still returns the resolved user
    assert result == str(expected_user_id)
