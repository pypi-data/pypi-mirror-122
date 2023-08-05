import threading
from abc import abstractmethod
from typing import Dict, Optional, Tuple

from limits.storage import StorageRegistry


class AsyncStorage(object, metaclass=StorageRegistry):
    """
    Base class to extend when implementing an asyncio storage backend. Storage backends
    are automatically registered with the limits `StorageRegistry`.
    """

    def __init__(self, uri: Optional[str] = None, **options: Dict) -> None:
        self.lock = threading.RLock()

    @abstractmethod
    async def incr(self, key: str, expiry: int, elastic_expiry: bool = False) -> int:
        """
        Increments the counter for a given rate limit key.

        - key: the key to increment
        - expiry: amount in seconds for the key to expire in
        - elastic_expiry: whether to keep extending the rate limit window every hit.
        """
        raise NotImplementedError

    @abstractmethod
    async def get(self, key: str) -> int:
        """Returns the counter value for the given key."""
        raise NotImplementedError

    @abstractmethod
    async def get_expiry(self, key: str) -> int:
        """Returns the expiry time for the given key."""
        raise NotImplementedError

    @abstractmethod
    async def check(self) -> bool:
        """Check if storage is healthy."""
        raise NotImplementedError

    @abstractmethod
    async def reset(self):
        """Reset storage to clear limits."""
        raise NotImplementedError

    @abstractmethod
    async def clear(self, key: str):
        """Resets the rate limit key."""
        raise NotImplementedError

    @abstractmethod
    async def acquire_entry(
        self, key: str, limit: int, expiry: int, no_add: bool = False
    ) -> bool:
        """
        Aquires an entry within the rate limit attached to the given key, returning if
        successful.

        - key: rate limit key to acquire an entry in
        - limit: amount of entries allowed
        - expiry: expiry of the entry
        - no_add: if an entry is not actually acquired but instead serves as a 'check'
        """
        raise NotImplementedError

    @abstractmethod
    async def get_moving_window(
        self, key: str, limit: int, expiry: int
    ) -> Tuple[int, int]:
        """
        Returns the starting point and the number of entries in the moving window.
        """
        raise NotImplementedError
