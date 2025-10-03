import discord

from .client import DebugClient
from .token import get_token


def main() -> None:
    token = get_token()
    intents = discord.Intents.default()
    client = DebugClient(intents=intents)
    client.run(token)


if __name__ == "__main__":
    main()


