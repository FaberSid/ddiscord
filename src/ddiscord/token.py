import os
import platform
import sys
from pathlib import Path


def get_token() -> str:
    """Resolve Discord token from argv, file, or environment, then prompt.

    Priority:
    1. Command line: first arg or '-' to read from stdin
    2. File: './token'
    3. Environment: DISCORD_TOKEN
    4. Prompt user
    """
    token: str | None = None
    token_path = Path("./token")
    token_env = os.environ.get("DISCORD_TOKEN")

    if len(sys.argv) > 1:
        if sys.argv[1] == "-":
            token = input()
        else:
            token = sys.argv[1]
    elif token_path.exists():
        token = token_path.read_text().rstrip()
    elif token_env:
        token = token_env

    print(" - Debugger for discord.py - ")
    print(f"Running on Python {platform.python_version()}. ", end="")
    if os.name == "posix":
        print("Send EOF (Ctrl-D) to exit.")
    elif os.name == "nt":
        print("Send EOF (Ctrl-Z) to exit.")
    else:
        print("Send EOF to exit.")

    if not token:
        token = input("Input your token: ")

    return token


