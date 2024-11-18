import asyncio
import logging
import os
from logging import handlers

import discord
from core import Valor
from discord.ext import commands
from dotenv import load_dotenv
from utils import ValorRequest

load_dotenv()

TEST_GUILD = os.getenv("TEST_GUILD")
BOT_TOKEN = os.getenv("BOT_TOKEN")

EXTENSIONS = {
    "commands.test_embed",
}

conn_args = {
    "host": os.getenv("DBHOST"),
    "user": os.getenv("DBUSER"),
    "password": os.getenv("DBPASS"),
    "db": os.getenv("DBNAME"),
}


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

    async with ValorRequest() as request:

        intents = discord.Intents.default()
        async with Valor(
            commands.when_mentioned,
            extensions=EXTENSIONS,
            request=request,
            testing_guild=TEST_GUILD,
            intents=intents,
        ) as valor:
            await valor.start(BOT_TOKEN)


asyncio.run(main())
