import aiomysql
from typing import Self


class ValorSQL:
    def __init__(self, minsize=1, maxsize=10, echo=False, pool_recycle=-1, loop=None, **kwargs) -> None:
        self.pool = None
        self.minsize = minsize
        self.maxsize = maxsize
        self.echo = echo
        self.pool_recycle = pool_recycle
        self.loop = loop
        self.kwargs = kwargs

    async def __aenter__(self) -> Self:
        self.pool = await aiomysql.create_pool(
            minsize=self.minsize,
            maxsize=self.maxsize,
            echo=self.echo,
            pool_recycle=self.pool_recycle,
            loop=self.loop,
            **self.kwargs
        )
        return self

    async def __aexit__(self) -> None:
        self.pool.close()
        await self.pool.wait_closed()

    async def execute(self, query: str, *args, **kwargs) -> list[tuple]:
        async with self.pool.acquire() as conn:
            async with conn.cursor() as cur:
                await cur.execute(query, *args, **kwargs)
                return await cur.fetchall()
