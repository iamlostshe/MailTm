"""Manage messages module."""

import asyncio

from .consts import BASE_URL


class Listen:
    """Listener class."""

    def __init__(self) -> None:
        """Init class."""
        self.message_ids = []

    async def message_list(self) -> list:
        """Get a list of messages."""
        url = f"{BASE_URL}messages"

        async with self.session.get(url) as response:
            data = await response.json()

        return [
            msg
            for i, msg in enumerate(data["hydra:member"])
            if data["hydra:member"][i]["id"] not in self.message_ids
        ]

    async def message(self, idx: str) -> dict:
        """Get the text of the message."""
        url = f"{BASE_URL}messages/{idx}"
        async with self.session.get(url) as response:
            return await response.json()

    async def run(self, listener: any) -> None:
        """Run a message check."""
        for message in await self.message_list():
            self.message_ids.append(message["id"])
            listener(await self.message(message["id"]))

    async def start(self, listener: any, interval: int = 3) -> None:
        """Run a message check cycle."""
        while True:
            try:
                await self.run(listener)
                await asyncio.sleep(interval)
            except KeyboardInterrupt:
                print("Stop working")  # noqa: T201
                await self.session.close()
                break
