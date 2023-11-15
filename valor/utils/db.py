from aiomysql import Pool


async def execute_query(pool: Pool, query: str) -> list[tuple]:
    async with pool.acquire() as conn:
        async with conn.cursor() as cur:
            await cur.execute(query)
            return await cur.fetchall()
