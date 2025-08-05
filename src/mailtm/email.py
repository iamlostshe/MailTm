"""The main module for interacting with EMail."""

import random

from aiohttp import ClientSession

from .consts import BASE_URL, PASSWORD_ALPHABET, USERNAME_ALPHABET
from .message import Listen


def username_gen(
    length: int = 24,
    chars: str = USERNAME_ALPHABET,
) -> str:
    """Username generation."""
    return "".join(random.choice(chars) for _ in range(length))  # noqa: S311


def password_gen(
    length: int = 8,
    chars: str = PASSWORD_ALPHABET,
) -> str:
    """Password generation."""
    return "".join(random.choice(chars) for _ in range(length))  # noqa: S311


class Email(Listen):
    """The class module for interacting with EMail."""

    async def init(self) -> None:
        """Init temporary Email class."""
        self.session = ClientSession(headers={"Content-Type": "application/json"})
        await self.domains()

    async def domains(self) -> None:
        """Init Email domains."""
        url = f"{BASE_URL}domains"

        async with self.session.get(url) as response:
            data = await response.json()

        for domain in data["hydra:member"]:
            if domain["isActive"]:
                self.domain = domain["domain"]

    async def register(
        self,
        username: str | None = username_gen(),
        password: str | None = password_gen(),
        domain: str | None = None,
    ) -> None:
        """Mail registration."""
        if domain:
            self.domain = domain

        self.address = f"{username}@{self.domain}"

        url = f"{BASE_URL}accounts"
        payload = {
            "address": self.address,
            "password": password,
        }

        await self.session.post(url, json=payload)
        await self.get_token(password)

    async def get_token(self, password: str) -> None:
        """Get token."""
        url = f"{BASE_URL}token"
        payload = {
            "address": self.address,
            "password": password,
        }

        async with self.session.post(url, json=payload) as response:
            token = (await response.json())["token"]

        self.session.headers.update({"Authorization": f"Bearer {token}"})
