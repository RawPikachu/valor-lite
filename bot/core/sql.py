import logging
import os
from typing import TYPE_CHECKING

import aiomysql

if TYPE_CHECKING:
    from core import Valor

logger = logging.getLogger(__name__)

CONN_ARGS = {
    "host": os.getenv("DBHOST"),
    "user": os.getenv("DBUSER"),
    "password": os.getenv("DBPASS"),
    "db": os.getenv("DBNAME"),
}


class ValorSQL:
    def __init__(self, conn_args: dict[str, str]) -> None:
        self.pool = None
        self.conn_args = conn_args

    async def setup(self):
        self.pool = await aiomysql.create_pool(**self.conn_args)

    async def unload(self):
        self.pool.close()
        await self.pool.wait_closed()

    async def execute(self, query: str, *args, **kwargs) -> list[tuple]:
        async with self.pool.acquire() as conn:
            async with conn.cursor() as cur:
                await cur.execute(query, *args, **kwargs)
                return await cur.fetchall()


async def setup(valor: "Valor"):
    logger.info("Loading ValorSQL...")
    valor.db = ValorSQL(CONN_ARGS)
    await valor.db.setup()


async def teardown(valor: "Valor"):
    logger.info("Unloading ValorSQL...")
    await valor.db.unload()
