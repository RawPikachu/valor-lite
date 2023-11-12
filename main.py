from dotenv import load_dotenv
from logging import handlers
from discord.ext import commands
from valor import Valor
import discord
import logging
import asyncio
import aiomysql
import os

load_dotenv()

TEST_GUILD = discord.Object(os.getenv("TESTGUILD"))
BOT_TOKEN = os.getenv("BOTTOKEN")

conn_args = {
    "host": os.getenv("DBHOST"),
    "user": os.getenv("DBUSER"),
    "password": os.getenv("DBPASS"),
    "db": os.getenv("DBNAME")
}

async def main():
    logger = logging.getLogger('discord')
    logger.setLevel(logging.INFO)

    formatter = logging.Formatter("[{asctime}] [{levelname:<8}] {name}: {message}", "%Y-%m-%d %H:%M:%S", style="{")

    handler = logging.StreamHandler()
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    
    file_handler = handlers.RotatingFileHandler(
        filename='discord.log',
        maxBytes=32 * 1024 * 1024,
        backupCount=5
    )
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)

    logger.info("Starting bot")

    async with aiomysql.create_pool(**conn_args) as pool:
        extensions = os.getenv("EXTENSIONS").split(",")
        
        intents = discord.Intents.default()
        async with Valor(
            commands.when_mentioned,
            extensions = extensions,
            db_pool = pool,
            testing_guild = TEST_GUILD,
            intents = intents
        ) as valor:
            await valor.start(BOT_TOKEN)

asyncio.run(main())