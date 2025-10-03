import asyncio
import io
import re
import textwrap
import traceback
from code import compile_command
from contextlib import redirect_stdout
from typing import Any, Dict

import discord


class AsyncInteractiveDebugger:
    """Asynchronous REPL-like debugger executed inside a Discord client's loop.

    This class encapsulates the input/execute/print loop to keep responsibilities
    separated from the Discord client and the application entrypoint.
    """

    def __init__(self, client: discord.Client) -> None:
        self.client = client
        # Shared environment for executed code. Exposes the client instance.
        self.execution_globals: Dict[str, Any] = {"client": client}
        # Also allow access to module-level globals if needed by executed code
        self.execution_globals.update(globals())

    async def run(self) -> None:
        """Runs the interactive loop until EOF or KeyboardInterrupt."""
        print("Connecting to discord...")
        await self.client.wait_until_ready()
        user = self.client.user
        if user is None:
            # Defensive check: some discord.py typings mark user as Optional
            # even after ready; avoid attribute access on None.
            print("Logged in, but user information is not available.")
        else:
            print(f"Logged in as {user} ({user.id})")
        print(
            "You can refer to your Client instance as `client` variable. i.e. client.guilds\n"
        )

        while True:
            try:
                try:
                    # Read first line
                    body = await self._run_input(">>> ")
                    # Keep reading continuation lines while it is incomplete
                    while not compile_command(re.sub(r"(\s*)(await|async) *", r"\1", body)):
                        body += "\n" + await self._run_input("... ")
                except (EOFError, KeyboardInterrupt):
                    await self._attempt_logout()
                    break

                if not body:
                    continue

                # Capture locally created variables back into globals for continuity
                body = body + "\nglobal env\nenv.update(locals())"

                # Prepare function wrappers to support expression result printing
                source = f"async def func():\n{textwrap.indent(body, '  ')}"
                source_with_return = (
                    f"async def func():\n{textwrap.indent('return ' + body, '  ')}"
                )

                # Provide `env` in globals for executed code
                self.execution_globals.setdefault("env", {"client": self.client})

                try:
                    exec(source_with_return, self.execution_globals)
                except SyntaxError:
                    exec(source, self.execution_globals)

                func = self.execution_globals["func"]

                stdout_capture = io.StringIO()
                with redirect_stdout(stdout_capture):
                    result = await func()

                captured = stdout_capture.getvalue()
                if captured:
                    print(captured, end="")
                elif result is not None:
                    print(repr(result))

            except Exception:
                traceback.print_exc()
                continue

    async def _run_input(self, prompt: str) -> str:
        """Run blocking input in executor to avoid blocking the event loop."""
        try:
            # noqa: F401 - optional, improves input UX if available
            import readline  # type: ignore
            # Touch an attribute to mark as used for linters
            _ = getattr(readline, "__doc__", None)
        except Exception:
            pass
        loop = asyncio.get_running_loop()
        return await loop.run_in_executor(None, input, prompt)

    async def _attempt_logout(self) -> None:
        try:
            # discord.py v2 removed logout(); close() logs out and closes the connection
            await self.client.close()
        except asyncio.CancelledError:
            # Swallow cancellation to allow graceful shutdown of the loop
            pass


async def run_debugger(client: discord.Client) -> None:
    """Convenience function to run the interactive debugger with a client."""
    debugger = AsyncInteractiveDebugger(client)
    await debugger.run()


