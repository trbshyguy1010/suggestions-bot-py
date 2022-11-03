import os
from os.path import exists
import discord
from discord.ext import commands
from discord.utils import get
from datetime import datetime 
import time

class Channel_Configuration(commands.Cog, name="Channel Configurations"):
    def __init__(self, bot):
        self.bot = bot
        
    def get_channel_from_txt(self, guild):
        chread = open(f'{guild}\'s channel.txt', 'r')
        ch = chread.readline()
        return ch

    @commands.command(name="get_channel", brief="Shows the current suggestions channel", description="Retreives the suggestions channel set using the \"set_channel\" command")
    async def get_channel(self, ctx):
        ch = self.get_channel_from_txt(ctx.guild)
        if ch == "":
            await ctx.send(f'{ctx.author.mention} Please specify a suggestions channel name')
        else:
            await ctx.send(f'{ctx.author.mention} \"{ch}\" is currently set as the suggestions channel')

    @commands.has_permissions(administrator=True)
    @commands.command(name="set_channel", brief="changes/sets the channel for suggestions", description="Specifies the channel used to display suggestions from other users, \"\" typing this restores it to default (please use double quotes if your channel name has spaces in them)")
    async def set_channel(self, ctx, channel_name):
        await ctx.send(f'{ctx.author.mention} \"{channel_name}\" is now set as the suggestions channel')
        chconfig = open(f'{ctx.guild}\'s channel.txt', 'w')
        chconfig.write(channel_name)

    @set_channel.error
    async def clear_error(ctx, error):
        if isinstance(error, commands.MissingPermissions):
            await ctx.send(f'{ctx.author.mention} Missing Permissions : `Administrator`')


