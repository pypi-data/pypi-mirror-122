"""
asyncio-compatible rate limiting strategies
"""

from abc import ABC, abstractmethod
from typing import Tuple

from limits import RateLimitItem

from .storage import AsyncStorage


class AsyncRateLimiter(ABC):
    """The base async limiter for all strategies and rate limits."""

    def __init__(self, storage: AsyncStorage):
        self.storage = storage

    @abstractmethod
    async def hit(self, item: RateLimitItem, *identifiers) -> bool:
        """
        Creates a hit on the rate limit with the given unique identifiers. Returns if
        successful.
        """
        raise NotImplementedError

    @abstractmethod
    async def test(self, item: RateLimitItem, *identifiers) -> bool:
        """
        Checks the rate limit by identifiers and returns `True` if it is not currently
        exceeded.
        """
        raise NotImplementedError

    @abstractmethod
    async def get_window_stats(
        self, item: RateLimitItem, *identifiers
    ) -> Tuple[int, int]:
        """
        Returns the number of requests remaining within this limit as a tuple of reset
        time and remianing requests.
        """
        raise NotImplementedError

    async def clear(self, item: RateLimitItem, *identifiers):
        """Clears the rate limit for the given item."""
        return await self.storage.clear(item.key_for(*identifiers))


class AsyncMovingWindowRateLimiter(AsyncRateLimiter):
    """A superclass of `AsyncRateLimiter` for moving window limits."""

    def __init__(self, storage: AsyncStorage):
        super().__init__(storage)

    async def hit(self, item: RateLimitItem, *identifiers) -> bool:
        return await self.storage.acquire_entry(
            item.key_for(*identifiers), item.amount, item.get_expiry()
        )

    async def test(self, item: RateLimitItem, *identifiers) -> bool:
        res = await self.storage.get_moving_window(
            item.key_for(*identifiers),
            item.amount,
            item.get_expiry(),
        )
        amount = res[1]
        return amount < int(item.amount)

    async def get_window_stats(
        self, item: RateLimitItem, *identifiers
    ) -> Tuple[int, int]:
        window_start, window_items = await self.storage.get_moving_window(
            item.key_for(*identifiers), item.amount, item.get_expiry()
        )
        reset = window_start + item.get_expiry()
        return (reset, item.amount - window_items)


class AsyncFixedWindowRateLimiter(AsyncRateLimiter):
    """A superclass of `AsyncRateLimiter` for fixed window limits."""

    async def hit(self, item: RateLimitItem, *identifiers) -> bool:
        return await self.storage.incr(
            item.key_for(*identifiers), item.get_expiry()
        ) <= int(item.amount)

    async def test(self, item, *identifiers):
        return await self.storage.get(item.key_for(*identifiers)) < item.amount

    async def get_window_stats(self, item, *identifiers) -> Tuple[int, int]:
        remaining = max(
            0,
            item.amount - await self.storage.get(item.key_for(*identifiers)),
        )
        reset = await self.storage.get_expiry(item.key_for(*identifiers))
        return (reset, remaining)


class AsyncFixedWindowElasticRateLimiter(AsyncFixedWindowRateLimiter):
    """
    A superclass of `AsyncRateLimiter` for fixed window limits with elastic expiry.
    """

    async def hit(self, item: RateLimitItem, *identifiers) -> bool:
        amount = await self.storage.incr(
            item.key_for(*identifiers), item.get_expiry(), True
        )
        return amount <= int(item.amount)


STRATEGIES = {
    "fixed-window": AsyncFixedWindowRateLimiter,
    "fixed-window-elastic-expiry": AsyncFixedWindowElasticRateLimiter,
    "moving-window": AsyncMovingWindowRateLimiter,
}
