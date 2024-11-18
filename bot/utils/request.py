import asyncio
import logging
from typing import Self

from aiohttp import ClientError, ClientSession

logger = logging.getLogger(__name__)


class ValorRequest:
    def __init__(self, hostname: str = "api.wynncraft.com", ver: str = "v3"):
        self.url = f"https://{hostname}/{ver}"
        self.session: ClientSession | None = None
        self.headers = {
            "User-Agent": "valor-lite/1.0",
        }
        self.ratelimit_remaining = 180
        self.ratelimit_reset = 0

    async def __aenter__(self) -> Self:
        self.session = ClientSession(headers=self.headers)
        return self

    async def __aexit__(self, exc_type, exc_value, traceback) -> None:
        await self.session.close()

    async def get(self, endpoint: str) -> dict:
        await self.ratelimit()

        try:
            response = await self.session.get(f"{self.url}/{endpoint}")
            data = await response.json()
        except ClientError as e:
            logger.error(f"Request failed: {e}")
            raise e

        self.update_ratelimit(response.headers)
        return data

    async def ratelimit(self) -> None:
        if self.ratelimit_remaining <= 1:
            logger.warning(f"Ratelimit reached, waiting for {self.ratelimit_reset} seconds")
            await asyncio.sleep(self.ratelimit_reset)

    def update_ratelimit(self, headers: dict) -> None:
        self.ratelimit_remaining = int(headers.get("ratelimit-remaining", 180))
        self.ratelimit_reset = int(headers.get("ratelimit-reset", 0))
