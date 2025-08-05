# mail-tm API wrapper

> Fork of [MainSilent/MailTm](https://github.com/MainSilent/MailTm).

> There are plans to write a custom server for deploying personal temporary email on your server.

Mail-tm is a free temporary mail service, This library is useful for automation tasks such as making accounts that needs email verification.

## Installation

```bash
pip install git+https://github.com/iamlostshe/mail-tm
```

## Example

```python
import asyncio

from mailtm import Email


async def main() -> None:
    """Start msg cycle."""
    def listener(message: dict) -> None:
        print("\nSubject: " + message["subject"])
        print("Content: " + message["text"] if message["text"] else message["html"])

    # Get Domains
    test = Email()
    await test.init()
    print("\nDomain: " + test.domain)

    # Make new email address
    await test.register()
    print("\nEmail Adress: " + str(test.address))

    # Start listening
    await test.start(listener)
    print("\nWaiting for new emails...")


if __name__ == "__main__":
    asyncio.run(main())

```

# Documentation

API: [api.mail.tm](https://api.mail.tm/)

- `register(username: str | None = username_gen(), password: str | None = password_gen(), domain: str | None = None)`:

Make an email account with random credentials, You can also pass a username, password and domain to use the same account.

- `start(listener: any, interval: int = 3) -> None`:

Start listening for new emails, Interval means how many seconds takes to sync, And you also need to pass a function for `listener`, This function gets called when new email arrive.
