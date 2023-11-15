import os
from discord.ext.commands import Bot
from typing import Optional
from logging import Logger
import aiomysql
import discord


class Valor(Bot):
    def __init__(
        self,
        *args,
        extensions: list[str],
        db_pool: aiomysql.Pool,
        testing_guild: Optional[discord.Object] = None,
        logger: Logger = None,
        **kwargs
    ):
        super().__init__(*args, **kwargs)
        self.db_pool = db_pool
        self.testing_guild = testing_guild
        self.all_extensions = extensions
        self.logger = logger

    async def setup_hook(self) -> None:
        for extension in self.all_extensions:
            await self.load_extension(extension)

        if self.testing_guild:
            self.tree.copy_global_to(guild=self.testing_guild)
            await self.tree.sync(guild=self.testing_guild)
        else:
            await self.tree.sync()
