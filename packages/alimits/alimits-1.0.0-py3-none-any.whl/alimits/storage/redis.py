import time

from limits.errors import ConfigurationError
from limits.util import get_dependency

from .base import AsyncStorage


class AsyncRedisStorage(AsyncStorage):
    """
    Rate limit storage with redis as backend. Depends on the
    [aredis](https://aredis.readthedocs.io/en/latest/) library.
    """

    STORAGE_SCHEME = ["aredis", "aredis+unix"]
    SCRIPT_MOVING_WINDOW = """
        local items = redis.call('lrange', KEYS[1], 0, tonumber(ARGV[2]))
        local expiry = tonumber(ARGV[1])
        local a = 0
        local oldest = nil
        for idx=1,#items do
            if tonumber(items[idx]) >= expiry then
                a = a + 1
                if oldest == nil then
                    oldest = tonumber(items[idx])
                end
            else
                break
            end
        end
        return {oldest, a}
    """
    SCRIPT_ACQUIRE_MOVING_WINDOW = """
        local entry = redis.call('lindex', KEYS[1], tonumber(ARGV[2]) - 1)
        local timestamp = tonumber(ARGV[1])
        local expiry = tonumber(ARGV[3])
        if entry and tonumber(entry) >= timestamp - expiry then
            return false
        end
        local limit = tonumber(ARGV[2])
        local no_add = tonumber(ARGV[4])
        if 0 == no_add then
            redis.call('lpush', KEYS[1], timestamp)
            redis.call('ltrim', KEYS[1], 0, limit - 1)
            redis.call('expire', KEYS[1], expiry)
        end
        return true
    """
    SCRIPT_CLEAR_KEYS = """
        local keys = redis.call('keys', KEYS[1])
        local res = 0
        for i=1,#keys,5000 do
            res = res + redis.call(
                'del', unpack(keys, i, math.min(i+4999, #keys))
            )
        end
        return res
    """
    SCRIPT_INCR_EXPIRE = """
        local current
        current = redis.call("incr",KEYS[1])
        if tonumber(current) == 1 then
            redis.call("expire",KEYS[1],ARGV[1])
        end
        return current
    """

    def __init__(self, uri: str, **options) -> None:
        """
        - URI of the form `aredis://[:password]@host:port/db`,
        `aredis+unix:///path/to/sock` etc. This uri is passed directly to
        `aredis.StrictRedis.from_url` with the initial "a" removed, except for the case
        of `redis+unix` where it is replaced with `unix`.
        - options: all remaining keyword arguments are passed directly to the
        constructor of `aredis.StrictRedis`
        """
        if not get_dependency("aredis"):
            raise ConfigurationError(
                "aredis prerequisite not available"
            )  # pragma: no cover

        uri = uri.replace("aredis", "redis", 1)
        uri = uri.replace("redis+unix", "unix")
        self.storage = get_dependency("aredis").StrictRedis.from_url(uri, **options)

        # all these methods are coroutines, so must be called with await
        self.lua_moving_window = self.storage.register_script(self.SCRIPT_MOVING_WINDOW)
        self.lua_acquire_window = self.storage.register_script(
            self.SCRIPT_ACQUIRE_MOVING_WINDOW
        )
        self.lua_clear_keys = self.storage.register_script(self.SCRIPT_CLEAR_KEYS)
        self.lua_incr_expire = self.storage.register_script(self.SCRIPT_INCR_EXPIRE)

        super().__init__()

    async def incr(self, key: str, expiry: int, elastic_expiry: bool = False) -> int:
        if elastic_expiry:
            value: int = await self.storage.incr(key)
            if elastic_expiry or value == 1:
                await self.storage.expire(key, expiry)

            return value

        val: int = await self.lua_incr_expire.execute([key], [expiry])
        return val

    async def get(self, key: str) -> int:
        return int(await self.storage.get(key) or 0)

    async def clear(self, key: str):
        await self.storage.delete(key)

    async def acquire_entry(self, key, limit, expiry, no_add=False) -> bool:
        timestamp = time.time()
        acquired = await self.lua_acquire_window.execute(
            [key], [timestamp, limit, expiry, int(no_add)]
        )
        return bool(acquired)

    async def get_expiry(self, key: str) -> int:
        return int(max(await self.storage.ttl(key), 0) + time.time())

    async def check(self) -> bool:
        try:
            b: bool = self.storage.ping()
            return b
        except Exception:
            return False

    async def get_moving_window(self, key, limit, expiry):
        timestamp = time.time()
        window = await self.lua_moving_window.execute(
            [key], [int(timestamp - expiry), limit]
        )
        return window or (timestamp, 0)

    async def reset(self) -> int:
        """
        This function calls a Lua Script to delete keys prefixed with 'LIMITER' in
        block of 5000.

        WARNING: This operation was designed to be fast, but was not tested on a large
        production based system. Be careful with its usage as it could be slow on very
        large data sets.
        """
        cleared: int = await self.lua_clear_keys.execute(["LIMITER*"])
        return cleared
