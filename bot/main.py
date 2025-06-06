import asyncio
import logging
import os
from logging import handlers

import discord
from core import Valor
from discord.ext import commands
from discord.ext.commands.errors import ExtensionError
from dotenv import load_dotenv

load_dotenv()

TEST_GUILD = os.getenv("TEST_GUILD")
BOT_TOKEN = os.getenv("BOT_TOKEN")

EXTENSION_PATHS = ["core", "commands"]
IGNORED_FILES = ["__init__.py", "valor.py"]
DISABLED_EXTS = os.getenv("DISABLED_EXTS", "").split(",")


async def load_extensions(valor: Valor, logger: logging.Logger):
    for path in EXTENSION_PATHS:
        for python_file in [name for name in os.listdir(path) if name.endswith(".py") and name not in IGNORED_FILES]:
            extension = f"{path}.{python_file.removesuffix(".py")}"

            if extension in DISABLED_EXTS:
                logger.info(f"Skipping disabled extension: {extension}")
                continue

            try:
                await valor.load_extension(extension)
            except ExtensionError as e:
                if path == "core":
                    logger.fatal(f"Critical extension did not load: {e}")
                else:
                    logger.error(e)
                raise e


async def main():
    discord_logger = logging.getLogger("discord")
    discord_logger.setLevel(logging.INFO)

    logger = logging.getLogger()
    logger.setLevel(logging.INFO)

    formatter = logging.Formatter("[{asctime}] [{levelname:<8}] {name}: {message}", "%Y-%m-%d %H:%M:%S", style="{")

    handler = logging.StreamHandler()
    handler.setFormatter(formatter)
    logger.addHandler(handler)

    file_handler = handlers.RotatingFileHandler(filename="valor.log", maxBytes=32 * 1024 * 1024, backupCount=5)
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)

    logger.info("Starting bot")

    intents = discord.Intents.default()

    async with Valor(
        commands.when_mentioned,
        testing_guild=TEST_GUILD,
        intents=intents,
    ) as valor:
        await load_extensions(valor, logger)
        await valor.start(BOT_TOKEN)


asyncio.run(main())
