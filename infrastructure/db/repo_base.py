# infrastructure/db/repo_base.py
from asyncpg import Pool
from contextvars import ContextVar

_pool_ctx: ContextVar[Pool] = ContextVar("pool")
conn_ctx = ContextVar("connection")

class DBSessionMiddleware:
    """Aiogram middleware: кладём connection в context"""
    def __init__(self, pool: Pool):
        self.pool = pool

    async def __call__(self, handler, event, data):
        async with self.pool.acquire() as conn:
            token = conn_ctx.set(conn)
            try:
                return await handler(event, data)
            finally:
                conn_ctx.reset(token)

def get_conn():
    """Вытащить текущее соединение из контекста"""
    conn = conn_ctx.get(None)
    if conn is None:
        raise RuntimeError("DB connection is not set")
    return conn
