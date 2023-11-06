# Dependancies

```pip install discord.py```
```pip install gspread```

# DEABot

In order to start DEABot, run the python file `DEABot.py`

# Adding Commands

In order to add commands, add a new file to the cogs folder directory. The file should be formatted `file-name.py`

Here is a template for a command cog, just replace "Test" with the command cog's name:

```
import discord
from discord.ext import commands
from discord import app_commands
from discord.ext.commands import bot
import asyncio

class Test(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    *** Listeners go here ***

async def setup(bot):
    await bot.add_cog(Test(bot))
```

# Listeners

Here are some differnent listener events, they each trigger under different scenarios.

Command Listener - Triggers when someone types -function_name

```
@commands.command()
    async def function_name(self, ctx):
        ***function body***
```

On-ready Listener - Triggers when the bot initally boots up

```
@commands.Cog.listener()
    async def on_ready(self):
        ***function body***
```

On-message Listener - Triggers whenever a user sends a message

```
@commands.Cog.listener()
    async def on_message(self, message):
      ***function body***
```

