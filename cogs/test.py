import discord
from discord.ext import commands
from discord import app_commands
from discord.ext.commands import bot
import asyncio

class Test(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.command()
    async def test(self, ctx):
        await ctx.send("Please Stop")

async def setup(bot):
    await bot.add_cog(Test(bot))