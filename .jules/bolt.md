## 2024-05-23 - Database Connection Bottleneck in Settings Retrieval
**Learning:** The application was creating a new database connection every time `get_setting` was called. Since settings (like `ceo_email`, `company_name`) are accessed frequently (e.g., during email notifications), this caused significant overhead and latency.
**Action:** Implemented `lru_cache` for `get_setting` to cache the results in memory. Also ensured that `update_settings` clears this cache. In the future, always look for frequently accessed read-only data that triggers database connections and consider caching it.
