import discord
from discord.ext import commands, tasks
from discord.ext.commands import bot
from discord import app_commands
import asyncio
from random import choice
import os
from itertools import cycle
import numpy as np
import json

#MatthewBot
f = open('token.json')
data = json.load(f)
TOKEN = data[0]["token"]
f.close()

bot = commands.Bot(command_prefix = ["-"], case_insensitive=True, intents=discord.Intents.all())
bot.remove_command("help")

@bot.event
async def on_ready():
    await bot.change_presence(activity=discord.Activity(type = discord.ActivityType.watching, name = "shenanigans unfold"))

@bot.command(pass_context=True)
@commands.has_permissions(administrator=True)
async def load(ctx, extension):
    await bot.load_extension(f'cogs.{extension}')

@bot.command(pass_context=True)
@commands.has_permissions(administrator=True)
async def unload(ctx, extension):
    await bot.unload_extension(f'cogs.{extension}')

@bot.command(pass_context=True)
@commands.has_permissions(administrator=True)
async def reload(ctx, extension):
    await bot.load_extension(f'cogs.{extension}')
    await asyncio.sleep(1)
    await bot.unload_extension(f'cogs.{extension}')
    await asyncio.sleep(1)
    await bot.load_extension(f'cogs.{extension}')

async def preload():
    for filename in os.listdir('./cogs'):
        if filename.endswith('.py'):
            await bot.load_extension(f'cogs.{filename[:-3]}')

async def main():
    await preload()
    await bot.start(TOKEN)

asyncio.run(main())