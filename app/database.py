import asyncpg

DB_CONFIG = {
    "user": "stocktrack_user",
    "password": "STpass123",
    "database": "stocktrack_db",
    "host": "postgres",
    "port": 5432
}

_pool = None

async def get_pool():
    global _pool
    if _pool is None:
        _pool = await asyncpg.create_pool(**DB_CONFIG, min_size=1, max_size=4)
    return _pool
