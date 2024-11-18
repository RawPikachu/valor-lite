import logging

import discord
from discord.ext.commands import Bot
from utils import ValorRequest

logger = logging.getLogger(__name__)


class Valor(Bot):
    def __init__(
        self,
        *args,
        extensions: list[str],
        request: ValorRequest,
        testing_guild: str | None = None,
        **kwargs,
    ):
        super().__init__(*args, **kwargs)
        self.request = request
        self.testing_guild = testing_guild
        self.init_extensions = extensions

    async def on_ready(self) -> None:
        logger.info(f"Logged in as {self.user} | {self.user.id}")

    async def setup_hook(self) -> None:
        for extension in self.init_extensions:
            await self.load_extension(extension)

        if self.testing_guild:
            guild_object = discord.Object(int(self.testing_guild))
            self.tree.copy_global_to(guild=guild_object)
            await self.tree.sync(guild=guild_object)
        else:
            await self.tree.sync()
