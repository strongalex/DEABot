import discord
from discord.ext import commands
from discord import app_commands
from discord.ext.commands import bot
import asyncio
import random
from random import choice

class Setup(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print("DEABot online")

    @commands.Cog.listener()
    async def on_message(self, message):
        chance = random.randint(1, 100)
        print(f"{message.author.name}, #{message.channel.name}: {message.content}(Chance: {chance})")

async def setup(bot):
    await bot.add_cog(Setup(bot))