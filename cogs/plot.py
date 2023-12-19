import discord
from discord.ext import commands
from discord import app_commands
from discord.ext.commands import bot
import gspread
from google.oauth2.service_account import Credentials
import asyncio
import random
from random import choice
import matplotlib.pyplot as plt
import os

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


def makeData(input, name):
        #print("making data")
        data = [{"time": float(input[0][5].replace(",", "")) - 0.005, "points": 0, "label":input[0][0][:input[0][0].index(" ")]}]
        i = 0

        for x in range(len(input)):
            #print(input[x][2])
            if input[x][2].lower() == name.lower():
                
                data.append({"time":float(input[x][5].replace(",", "")), "points":data[i]['points'] + int(input[x][3]), "label":input[x][0][:input[x][0].index(" ")]})
                i += 1
            #print(data)
        return data


class plot(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.command()
    async def plot(self, ctx, *, arg):
        # Select the specific worksheet (tab) within the Google Sheet
        worksheet_name = 'Responses'
        worksheet = sheet.worksheet(worksheet_name)
        # Get all values from the worksheet
        rawdata = worksheet.get('A2:F')

        print("hello")

        data = makeData(rawdata, arg)

        print(data)

        xData = []
        yData = []
        xLabel = []

        for x in data:
            xData.append(x['time'])
            yData.append(x['points'])
            xLabel.append(x['label'])

        print(xLabel)
        # Create a new figure and axes for each graph
        fig, ax = plt.subplots()

        ax.plot(xData, yData)
        ax.set_xlabel('Time')
        ax.set_ylabel('Points')
        ax.axhline(0, color='black', linestyle='--')
        ax.set_xticks(xData)
        ax.set_xticklabels(xLabel, rotation=45, ha='right')
        ax.set_title(f"{arg}'s Graph")

        plt.tight_layout()

        # Save the graph to a file
        file_name = f"{arg.replace(' ', '')}graph.png"
        fig.savefig(file_name)

        # Send the image in a Discord message
        with open(file_name, 'rb') as file:
            await ctx.send(file=discord.File(file, file_name))

        # Close the figure to release resources
        plt.close(fig)

        # Delete the image file
        os.remove(file_name)

    @commands.command()
    async def plotAll(self, ctx, *, legend=''):
        # Select the specific worksheet (tab) within the Google Sheet
        worksheet_name = 'Responses'
        worksheet = sheet.worksheet(worksheet_name)
        # Get all values from the worksheet
        rawdata = worksheet.get('A2:F')

        valid = []

        for x in rawdata:
            if x[2] not in valid and x[2] not in legend:
                valid.append(x[2])

        # Create a new figure and axes for each graph
        fig, ax = plt.subplots(figsize=(10, 6))

        for name in valid:
            data = makeData(rawdata, name)

            xData = []
            yData = []
            xLabel = []

            for x in data:
                xData.append(x['time'])
                yData.append(x['points'])
                xLabel.append(x['label'])

            ax.plot(xData, yData, label=name)


        ax.set_xlabel('Time')
        ax.set_ylabel('Points')
        ax.axhline(0, color='black', linestyle='--')
        ax.set_title(f"Everyones's Graph")
        if "legend" in legend.lower():
            ax.legend(loc='upper right')

        # Save the graph to a file
        file_name = f"Everyonegraph.png"
        fig.savefig(file_name)

        # Send the image in a Discord message
        with open(file_name, 'rb') as file:
            await ctx.send(file=discord.File(file, file_name))

        # Close the figure to release resources
        plt.close(fig)

        # Delete the image file
        os.remove(file_name)
        


  
async def setup(bot):
    await bot.add_cog(plot(bot))