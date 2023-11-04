import discord
from discord.ext import commands
from discord import app_commands
from discord.ext.commands import bot
import asyncio

class Help(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.command()
    async def help(self, ctx):
        embed = discord.Embed(title="**DEABot Help**", color=0xe5e5e5)
        embed.add_field(name="**-test**", value="Checks if the bot is responding", inline=False)
        embed.add_field(name="**-points**", value="Returns the amount of points for a given discord username", inline=False)
        embed.add_field(name="**-pointsfromname**", value="Returns the amount of points for a given name", inline=False)
        #embed.add_field(name="**-mostpoints**", value="Returns the person with the most amount of points", inline=False)

        await ctx.send(embed=embed)


async def setup(bot):
    await bot.add_cog(Help(bot))