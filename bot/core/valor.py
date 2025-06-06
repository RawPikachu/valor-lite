import logging
from typing import TYPE_CHECKING

import discord
from discord.ext.commands import Bot

if TYPE_CHECKING:
    from core import ValorSQL, WynnRequest

logger = logging.getLogger(__name__)


class Valor(Bot):
    def __init__(
        self,
        *args,
        testing_guild: str | None = None,
        **kwargs,
    ):
        super().__init__(*args, **kwargs)
        self.testing_guild = testing_guild

        self.request: "WynnRequest"
        self.db: "ValorSQL"

    async def on_ready(self) -> None:
        logger.info(f"Logged in as {self.user} | {self.user.id}")

    async def setup_hook(self) -> None:
        if self.testing_guild:
            guild_object = discord.Object(int(self.testing_guild))
            self.tree.copy_global_to(guild=guild_object)
            await self.tree.sync(guild=guild_object)
        else:
            await self.tree.sync()
