import asyncio
import discord

from .debugger import run_debugger


class DebugClient(discord.Client):
    async def setup_hook(self) -> None:  # type: ignore[override]
        # Run debugger without blocking ready
        asyncio.create_task(run_debugger(self))


