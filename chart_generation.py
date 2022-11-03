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

class Chart_Generator(commands.Cog, name="Database"):
    def __init__(self, bot):
        self.bot = bot

    def get_channel_from_txt(self, guild):
        chread = open(f'{guild}\'s channel.txt', 'r')
        ch = chread.readline()
        return ch

    @commands.has_permissions(administrator=True)
    @commands.command(name="get_chart", brief="Command used to transform yes/no votes into a pie chart", description="Use this command to transfer the amount of yes/no reactions into a .png file of a pie chart")
    async def get_chart(self, ctx, msg_id: int):
        print("getting message")
        channel = discord.utils.get(ctx.guild.channels, name=self.get_channel_from_txt(ctx.guild))
        message = await channel.fetch_message(msg_id)
        eFm = message.embeds
        msg_g = ""
        for embed in eFm:
            u_dit = embed.to_dict()
            print(u_dit)
            for i in u_dit['fields']:
                msg_g = i['value']
        print(message, "gotten")
        yes, no = [], []
        for r in message.reactions:
            print(f'{r.count}')
            if str(r) == '✅':
                users = await r.users().flatten()
                yes.extend(users)
                print(yes[1:])

            elif str(r) == '❌':
                users = await r.users().flatten()
                no.extend(users)
                print(no[1:])
        if len(yes[1:]) == 0 and len(no[1:]) == 0:
            await ctx.send(f'{ctx.author.mention} No reactions/votes have been added')
        else:
            async with ctx.typing():
                matplotlib.use('Agg')
                y = np.array([len(yes[1:]), len(no[1:])])
                if os.path.exists(f"{str(msg_id)}.png"):
                    os.remove(f"{str(msg_id)}.png")
                rLabels = ["Yes", "No"]
                rColors = ["#8df2a6", "#f29e8d"]
                cha.pie(y, labels = rLabels, colors = rColors, autopct='%1.1f%%')
                cha.title(msg_g)
                cha.legend()
                cha.savefig(str(msg_id)+".png", dpi=300) 
            await ctx.send(f'{ctx.author.mention}',file=discord.File(f"{str(msg_id)}.png"))
            cha.close('all')

    @get_chart.error
    async def clear_error(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            await ctx.send(f'{ctx.author.mention} Missing Permissions : `Administrator`')
