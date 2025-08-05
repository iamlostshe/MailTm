"""The main module for interacting with EMail."""

import random
import string

import requests

from .consts import BASE_URL
from .message import Listen


def username_gen(
    length: int = 24,
    chars: str = string.ascii_letters + string.digits,
) -> str:
    """Username generation."""
    return "".join(random.choice(chars) for _ in range(length))  # noqa: S311


def password_gen(
    length: int = 8,
    chars: str = string.ascii_letters + string.digits + string.punctuation,
) -> str:
    """Password generation."""
    return "".join(random.choice(chars) for _ in range(length))  # noqa: S311


class Email(Listen):
    """The class module for interacting with EMail."""

    def __init__(self) -> None:
        self.domains()
        self.session = requests.Session(headers={"Content-Type": "application/json"})

    def domains(self) -> None:
        url = f"{BASE_URL}domains"
        response = self.session.get(url)
        response.raise_for_status()

        data = response.json()
        for domain in data["hydra:member"]:
            if domain["isActive"]:
                self.domain = domain["domain"]

    def register(
        self,
        username: str | None = username_gen(),
        password: str | None = password_gen(),
        domain: str | None = None,
    ) -> None:
        if domain:
            self.domain = domain

        url = f"{BASE_URL}accounts"
        self.address = f"{username}@{self.domain}"
        payload = {
            "address": self.address,
            "password": password,
        }
        response = self.session.post(url, json=payload)
        response.raise_for_status()

        self.get_token(password)

    def get_token(self, password):
        url = f"{BASE_URL}token"
        payload = {
            "address": self.address,
            "password": password,
        }
        response = self.session.post(url, json=payload)
        response.raise_for_status()

        self.token = response.json()["token"]
