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
        data = worksheet.get('B2:E10')
        points = "Error, this user does not yet have any points"
        for x in range(len(data)):
            if data[x][1] == username.name:
                points = (f'{username.mention} currently has {data[x][2]} points!')
                break

        await ctx.send(points)

    @commands.command()
    async def pointsfromname(self, ctx, *, arg):
        # Get all values from the worksheet
        data = worksheet.get('B2:E10')
        points = "Error, this user does not yet have any points"
        for x in range(len(data)):
            if data[x][0] == arg:
                points = (f'{data[x][0]} currently has {data[x][2]} points!')
                break

        await ctx.send(points)
        

async def setup(bot):
    await bot.add_cog(Points(bot))