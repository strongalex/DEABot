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
        print("Oh god please make it stop")

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.name != "MatthewBot":
            chance = random.randint(1, 100)
            print(f"{message.author.name}, #{message.channel.name}: {message.content}(Chance: {chance})")

            if chance > 95:
                responses = ['Interesting', 'Sure', 'The effect resolves', 'Shutdown prodcedure: Lights off']
                await message.channel.send(random.choice(responses))

            imList = ["im", "i'm", "i am", "sono", "soy", "je suis", "ich bin", "i’m", "わたしわ", "tôi là", "je'susi", "eu sou", "אני"]
            for x in imList:
                if message.content.lower().startswith(f"{x} ") or message.content.lower().startswith(f"­{x} "):
                    temp = message.content[len(x) + 1:]
                    await message.reply(f"Hi {temp}, I am Matthew, pleasure to meet you")

            if "crazy" in message.content.lower():
                await message.reply("Crazy! I was cra... wait no no no")
    
    

async def setup(bot):
    await bot.add_cog(Setup(bot))