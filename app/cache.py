from cachetools import TTLCache

# Sample in-memory cache with a 5-minute TTL
cache = TTLCache(maxsize=1000, ttl=300)