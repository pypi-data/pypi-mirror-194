import asyncpg


async def get_connection_pool() -> asyncpg.Pool:
    return await asyncpg.create_pool(
        user='ace',
        password='ace',
        database='ace',
        host='db',
    )
