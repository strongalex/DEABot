import discord
from discord.ext import commands
from discord import app_commands
from discord.ext.commands import bot
import gspread
from google.oauth2.service_account import Credentials
import asyncio
import random
from random import choice

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





class Badwords(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.bot or message.channel.id == 1152247303017615501:
            return
        # Select the specific worksheet (tab) within the Google Sheet
        worksheet_name = 'Bot'
        worksheet = sheet.worksheet(worksheet_name)

        # Get all values from the worksheet
        data = worksheet.get('A2:D')

        badwordList = ['fuck', 'shit', 'ass', 'cunt', 'bitch', 'crap', 'dick', 'asshole', 'fuc', '<:F_:1190878783125848125> uck', '<:F_:1190878783125848125>uck']
        matthewisms = ['*gasp*,', 'Wowzers!', 'Geeze louise,', 'Oh my!', 'Oh geez,']
        badwords = 0
        for x in range(len(badwordList)):
            badwords += (" "+message.content.lower()+" ").count(" "+badwordList[x]+" ")

        replacement = "fubble duckles"
        if "crap" in message.content.lower():
            replacement = "carp"

        if badwords > 0:
            user_in_sheet = False
            for x in range(len(data)):
                if data[x][0] == message.author.name:
                    user_in_sheet = True
                    worksheet.update_cell(x+2, 2, badwords + int(data[x][1]))

            if not user_in_sheet:
                try:
                    # Add the user to the sheet
                    new_row = [message.author.name, badwords]  
                    worksheet.insert_rows([new_row], 2)  # Add a new row to the end of the worksheet
                except Exception as e:
                    print(f"Error adding user to the sheet: {str(e)}")

            await message.reply(f"{random.choice(matthewisms)} I think you mean {replacement}, -{badwords * 2} points")

  
async def setup(bot):
    await bot.add_cog(Badwords(bot))