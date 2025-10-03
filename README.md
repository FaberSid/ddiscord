ddiscord: debugger for discord.py v2
=====

[![License](https://img.shields.io/badge/license-MIT-informational.svg)](./LICENSE)
[![Python](https://img.shields.io/badge/python-3.13-blue.svg)](#)
[![Fork](https://img.shields.io/badge/Fork-FaberSid%2Fddiscord-informational.svg)](https://github.com/FaberSid/ddiscord)

Powered by [discord.py](https://github.com/Rapptz/discord.py). Tested on discord.py v2.6+.

## Usage (with uv)

Run without installing (via uvx):

    # From this fork (example; no install)
    uvx --from git+https://github.com/FaberSid/ddiscord ddiscord

From local source (inside the project directory):

    # Uses project's interpreter and dependencies
    uv run ddiscord

Example session:

    $ uvx --from git+https://github.com/FaberSid/ddiscord ddiscord
     - Debugger for discord.py -
    Running on Python 3.13.6. Send EOF (Ctrl-Z) to exit.
    Logged in as YourBot#0000 (012345678901234567)
    You can refer to your Client instance as `client` variable. i.e. client.guilds
    
    >>> len(client.guilds)
    1
    >>> client.user.bot
    True
    >>> await client.guilds[0].create_text_channel('test')
    <TextChannel id=012345678901234567 name='test' position=1>
    >>> for channel in client.get_all_channels():
    ...     if channel.name == 'test':
    ...         await channel.send('announcement test!')
    ... 
    >>>

## Installation
    # Run without installing globally (recommended)
    uvx --from ddiscord ddiscord

    # Or install into the current uv-managed environment
    uv add ddiscord

    # Install as a uv tool from a Git repo (alternative)
    # Template
    uv tool install git+https://github.com/user/repo
    # Example (this fork)
    uv tool install git+https://github.com/FaberSid/ddiscord

After installing as a uv tool, invoke it directly:

    ddiscord

## Logging On
There are multiple ways to log into your bot in ddiscord. They are listed below in look up order.

1. Passing your token as an argument.
2. Passing your token via standard input. `-` is needed as a first argument.
3. Storing your token in a file named `token` in the current directory.
4. Passing your token via environment variable `DISCORD_TOKEN`.
5. Run ddiscord first, then ddiscord will ask you the token.

Examples:

    # With uvx (no install)
    uvx --from ddiscord ddiscord 'YOUR TOKEN HERE'
    echo 'YOUR TOKEN HERE' | uvx --from ddiscord ddiscord -
    echo 'YOUR TOKEN HERE' > token
    uvx --from ddiscord ddiscord

    # From local source
    uv run ddiscord 'YOUR TOKEN HERE'
    echo 'YOUR TOKEN HERE' | uv run ddiscord -
    echo 'YOUR TOKEN HERE' > token
    uv run ddiscord

PowerShell (Windows) environment variable example:

    $env:DISCORD_TOKEN = "YOUR TOKEN HERE"
    uv run ddiscord

Note: Privileged intents are disabled by default. Enable them in the Developer Portal if needed or adjust the intents in code.

