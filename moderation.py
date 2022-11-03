import os
from os.path import exists
import discord
from discord.ext import commands

class Moderation(commands.Cog, name="Moderation Tools"):
    def __init__(self, bot):
        self.bot = bot

    def get_channel_from_txt(self, guild):
        chread = open(f'{guild}\'s channel.txt', 'r')
        ch = chread.readline()
        return ch

    @commands.has_permissions(administrator=True)
    @commands.command(name="purge", brief="Deletes n amount of channels", description="Deletes n amount of channels")
    async def purge(self, ctx, no_channel: int):
        await ctx.channel.purge(limit=no_channel)

    @purge.error
    async def clear_error(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            await ctx.send(f'{ctx.author.mention} Missing Permissions : `Manage Messages`')




