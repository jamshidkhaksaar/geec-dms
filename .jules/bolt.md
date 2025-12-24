## 2024-05-23 - [Cached Hot-Path Database Query]
**Learning:** `functools.lru_cache` is a zero-dependency way to optimize read-heavy database queries in Flask context processors, as long as cache invalidation is handled in update routes.
**Action:** Always look for context processors executing DB queries on every request.
