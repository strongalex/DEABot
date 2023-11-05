import discord
from discord.ext import commands
from discord import app_commands
from discord.ext.commands import bot
import gspread
from google.oauth2.service_account import Credentials
import asyncio

# Define the scope and load the credentials from the JSON key file
scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
credentials = Credentials.from_service_account_file('key.json', scopes=scope)

# Create a gspread client using the loaded credentials
gc = gspread.Client(auth=credentials)

# Authenticate with the client
gc.login()

# Open the Google Sheet by title
spreadsheet_name = 'The Point System (Responses)'
sheet = gc.open(spreadsheet_name)

# Select the specific worksheet (tab) within the Google Sheet
worksheet_name = 'Leaderboard'
worksheet = sheet.worksheet(worksheet_name)



class Points(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    

    @commands.command()
    async def points(self, ctx, username: discord.Member):
        # Get all values from the worksheet
        data = worksheet.get('B2:E')
        points = "Error, this user does not yet have any points"
        for x in range(len(data)):
            if data[x][1] == username.name:
                points = (f'{username.mention} currently has {data[x][3]} points!')
                break

        await ctx.send(points)

    @commands.command()
    async def pointsfromname(self, ctx, *, arg):
        # Get all values from the worksheet
        data = worksheet.get('B2:E')
        points = "Error, this user does not yet have any points"
        for x in range(len(data)):
            if data[x][0] == arg:
                points = (f'{data[x][0]} currently has {data[x][3]} points!')
                break

        await ctx.send(points)

    @commands.command()
    async def leaderboard(self, ctx):
        leaderboard_range = 10

        data = worksheet.get(f'B2:E{leaderboard_range}')
        trimmed_data = []
        for x in range(len(data)):
            if data[x][0] != "":
                trimmed_data.append([data[x][0], data[x][1], data[x][2], int(data[x][3])])
        sorted_data = sorted(trimmed_data, key=lambda x: x[3], reverse=True)
        board = "**Current Leaderboard!**\n"

        for x in range(len(sorted_data)):
            if sorted_data[x][2] == "":
                board += f'{x}. {sorted_data[x][0]} with {sorted_data[x][3]} points!\n'
            else:
                board += f'{x}. <@{sorted_data[x][2]}> with {sorted_data[x][3]} points!\n'

        
        await ctx.send(board)

        

        

async def setup(bot):
    await bot.add_cog(Points(bot))