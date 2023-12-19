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
        embed = discord.Embed(title="**Matthew Help**", color=0xff5733)
        embed.add_field(name="**-test**", value="Checks if the bot is responding", inline=False)
        embed.add_field(name="**-points {username}**", value="Returns the amount of points for a given discord username", inline=False)
        embed.add_field(name="**-pointsfromname {name}**", value="Returns the amount of points for a given name", inline=False)
        embed.add_field(name="**-leaderboard**", value="Reutrns the top 10 amount of points", inline=False)
        embed.add_field(name="**-sin {name}**", value="Returns a random negative comment when given a name", inline=False)
        embed.add_field(name="**-profile ({name})**", value="Returns either a specified name or the users points and comments", inline=False)
        embed.add_field(name="**-plot {name}**", value="Returns a plot of the specified name", inline=False)
        embed.add_field(name="**-plotAll (legend)**", value="Returns a plot of everyones points, add 'legend' to the command to display a legend for the graph, add a name after to exlucde that person from the graph", inline=False)
        #embed.add_field(name="**-mostpoints**", value="Returns the person with the most amount of points", inline=False)

        await ctx.send(embed=embed)


async def setup(bot):
    await bot.add_cog(Help(bot))