import os
from os.path import exists
import discord
from discord.ext import commands
from discord.utils import get
from datetime import datetime 
import matplotlib.pyplot as cha
import matplotlib
import numpy as np
import time
import channel_config
import chart_generation
import moderation
import inbox

token = "your token here"
bot = commands.Bot(command_prefix=commands.when_mentioned_or("m$"),
        description="Made with love by trbshyguy1100 <3")

client = discord.Client()

def get_channel_from_txt(guild):
    chread = open(f'{guild}\'s channel.txt', 'r')
    ch = chread.readline()
    return ch

@bot.event
async def on_ready():
    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name="your suggestions"))
    print("bot has been connected to discord")
    bot.add_cog(channel_config.Channel_Configuration(bot))
    bot.add_cog(chart_generation.Chart_Generator(bot))
    bot.add_cog(moderation.Moderation(bot))
    bot.add_cog(inbox.Suggest(bot))

async def on_message(message):
    if message.author.bot:
        return
    await bot.process_commands(message)

try:
    bot.run(token)
except Exception:
    print('Could not connect to bot: \n', str(Exception))
    
