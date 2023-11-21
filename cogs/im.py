import discord
from discord.ext import commands, tasks
from discord import app_commands
from discord.ext.commands import bot
import asyncio
import gspread
from google.oauth2.service_account import Credentials
import asyncio
import random
from random import choice

responded_messages = []

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

imList = ["im", "i'm", "i am", "sono", "soy", "je suis", "ich bin", "i’m", "わたしわ", "tôi là", "je'susi", "eu sou", "אני", 'estoy']

class Im(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.check_reactions.start()


    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.bot:
            return
        # Select the specific worksheet (tab) within the Google Sheet
        worksheet_name = 'Bot'
        worksheet = sheet.worksheet(worksheet_name)

        # Get all values from the worksheet
        data = worksheet.get('A2:E')
            
        for x in imList:
            if message.content.lower().startswith(f"{x} "):
                temp = message.content[len(x) + 1:]
                response_message = await message.reply(f"Hi {temp}, I am Matthew")
                await response_message.add_reaction("🤝")
                responded_messages.append((response_message.id, 0, message.author.name, message.id, message.channel.id, message.author.id))

            if message.content.lower().startswith(f"­{x} ") or message.content.lower().startswith(f"⃤{x} "):
                user_in_sheet = False
                for x in range(len(data)):
                    if data[x][0] == message.author.name:
                        user_in_sheet = True
                        worksheet.update_cell(x+2, 3, 1 + int(data[x][2]))

                if not user_in_sheet:
                    try:
                        # Add the user to the sheet
                        new_row = [message.author.name, 0, 1]  
                        worksheet.insert_rows([new_row], 2)  # Add a new row to the end of the worksheet
                    except Exception as e:
                        print(f"Error adding user to the sheet: {str(e)}")

                await message.reply(f"Well well well, what do we have here? A little rascal trying to cheat the system? -1 point!")

    @tasks.loop(seconds=1)
    async def check_reactions(self):
        
        # Create a copy of the list to avoid modifying it while iterating
        messages_to_remove = []

        for i, x in enumerate(responded_messages):
            reacted = False
            if x[1] < 5:
                # Create a new tuple with the updated value
                responded_messages[i] = (x[0], x[1] + 1, x[2], x[3], x[4], x[5])
            else:
                # Get the channel using get_channel
                channel = self.bot.get_channel(x[4])

                if channel:
                    # Get the message using fetch_message
                    message = await channel.fetch_message(x[3])
                    response_message = await channel.fetch_message(x[0])
                    # Do something with the message

                    for reaction in response_message.reactions:
                        if str(reaction.emoji) == "🤝":
                            async for user in reaction.users():
                                if user.id == x[5]:
                                    await message.reply("Pleasure to meet you!")
                                    reacted = True
                    if not reacted: 
                        # Select the specific worksheet (tab) within the Google Sheet
                        worksheet_name = 'Bot'
                        worksheet = sheet.worksheet(worksheet_name)

                        # Get all values from the worksheet
                        data = worksheet.get('A2:E')
                        user_in_sheet = False
                        for x in range(len(data)):
                            if data[x][0] == message.author.name:
                                user_in_sheet = True
                                worksheet.update_cell(x+2, 4, 1 + int(data[x][3]))

                        if not user_in_sheet:
                            try:
                                # Add the user to the sheet
                                new_row = [message.author.name, 0, 0, 1]  
                                worksheet.insert_rows([new_row], 2)  # Add a new row to the end of the worksheet
                            except Exception as e:
                                print(f"Error adding user to the sheet: {str(e)}")
                        await message.reply("Failure to follow handshake protocol")

                else:
                    print("Channel not found")

                messages_to_remove.append(i)

        # Remove the messages that reached 10 reactions
        for index in reversed(messages_to_remove):
            responded_messages.pop(index)


async def setup(bot):
    await bot.add_cog(Im(bot))