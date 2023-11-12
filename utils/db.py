async def execute(pool, query):
    async with pool.acquire() as conn:
        async with conn.cursor() as cur:
            await cur.execute(query)
            return await cur.fetchall()