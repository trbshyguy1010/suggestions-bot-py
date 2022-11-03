import os
import discord
from discord.ext import commands
from datetime import datetime
import time

client = discord.Client()

class Suggest(commands.Cog, name="Suggestion Command"):
    def __init__(self, bot):
        self.bot = bot
    
    
    def get_channel_from_txt(self, guild):
        chread = open(f'{guild}\'s channel.txt', 'r')
        ch = chread.readline()
        return ch
    
    @commands.command(name="suggest_rules", alias="sr", brief="Rules for suggestions", description="DMs you the rules necessary to follow in order to not get banned ;)")
    async def suggest_rules(self, ctx):
        embed = discord.Embed(title="Rules", description="General Rules you should follow before using the `suggest` command :", color=0xdac2f0)
        embed.add_field(name="Rule #1 :", value="No other reactions from the typical :x: or :white_check_mark: allowed")
        embed.add_field(name="Rule #2 :", value="No duplicate :x: or :white_check_mark: reactions allowed")
        embed.set_footer(text='Made with <3 by trbshyguy1100')
        await ctx.author.send(embed=embed)
        await ctx.reply(":mailbox_with_no_mail: | Check your DMs ;)")
        time.sleep(1)
        await ctx.channel.purge(limit=2)

    @commands.command(name="suggest", brief="Command used to send suggestions", description="Use this command to send out suggestions to help improve the bot, cuz every suggestion is important y'know <3")
    async def suggest(self, ctx, *msg):
        response = ""
        for a in msg:
            response = response + " " + a  
        if os.path.exists(f'{ctx.guild}\'s channel.txt') != True:
            cdef = open(f'{ctx.guild}\'s channel.txt', 'w')
        chread = open(f'{ctx.guild}\'s channel.txt', 'r')
        ch = chread.readline()
        print(ch)
        if ch == "":
            channel = discord.utils.get(ctx.guild.channels, name="suggestions")
            print("checking presence of a default \"suggestions\" channel")
            if channel == None:
                print("creating a default channel named \"suggestions\"")
                guild = ctx.guild
                channel = await guild.create_text_channel("suggestions")
                # await channel.set_permissions(ctx.guild.default_role, send_messages=False)# local variable bound to change :)
            chwr = open(f'{ctx.guild}\'s channel.txt', 'w')
            chwr.write("suggestions")
        else:
            print("checking presence of set channel")
            channel = discord.utils.get(ctx.guild.channels, name=ch)
            if channel == None:
                guild = ctx.guild
                channel = await guild.create_text_channel(ch)
                # await channel.set_permissions(ctx.guild.default_role, send_messages=False)

        # note to self : this is garbage ;)

        # Channel permissions check :)
        overwrite = channel.overwrites_for(ctx.guild.default_role)
        if overwrite.send_messages == False:
            print("Channel permissions already set!")
        else:
            await channel.set_permissions(ctx.guild.default_role, send_messages=False)
            print("Setting up permissions")

        if response != "":
            print(f'{ctx.author}:     {response}')
            await ctx.channel.purge(limit=1)
            await ctx.send(f'{ctx.author.mention} your message has been sent fel 7efth wal amen ;)')
            d = open(f'{ctx.author}.txt', "a")
            today = datetime.now()
            de = today.strftime("%d/%m/%y at %H:%M:%S")
            txt_file = f'{de} | {ctx.author} : {response}'
            d.write(txt_file+"\n")
            d.close()
            embed=discord.Embed(title=f'Suggestion #{len(open(str(ctx.author)+".txt").readlines())}', color=0xd0ff45)
            embed.set_author(name=f'{ctx.author}', icon_url=ctx.message.author.avatar_url)
            embed.add_field(name=f'{ctx.author} says :', value=response, inline=False)
            embed.set_footer(text=f'{de} Made with <3 by trbshyguy1100')
            accept_decline = await channel.send(embed=embed)
            await accept_decline.add_reaction('✅')
            await accept_decline.add_reaction('❌')
            time.sleep(1)
            await ctx.channel.purge(limit=1)
            # await channel.send(f'{ctx.author}: {response}')
        else:
            await ctx.send(f'{ctx.author.mention} Please input a message')
    
    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload):
        channel = discord.utils.get(self.bot.get_all_channels(), id=payload.channel_id)
        temp_msg = await channel.fetch_message(payload.message_id)
        print(self.get_channel_from_txt(str(self.bot.get_guild(temp_msg.guild.id))))
        if str(channel) == self.get_channel_from_txt(str(self.bot.get_guild(temp_msg.guild.id))):
            message = await channel.fetch_message(payload.message_id)
            # magiccccc codeeeeee, woah super magical :ooooooooooooo
            for reaction in message.reactions:
                if (not payload.member.bot and payload.member in await reaction.users().flatten()):
                    if str(reaction) != '❌' and str(reaction) != '✅':
                        print("Reaction Error No.1")
                        await message.remove_reaction(reaction.emoji, payload.member)
                        embed=discord.Embed(title="**WARNING**", description="Other reactions aren\'t allowed from the typical yes/no reaction, your previous reaction has been deleted", color=0xff0000)
                        embed.set_footer(text='Made with <3 by trbshyguy1100')
                        await payload.member.send(embed=embed)
                    if reaction.emoji != payload.emoji.name:
                        print("Reaction Error No.2")
                        await message.remove_reaction(reaction.emoji, payload.member)
                        embed=discord.Embed(title="**WARNING**", description="You are not allowed to enter duplicate votes, your previous reaction has been deleted", color=0xff0000)
                        embed.set_footer(text='Made with <3 by trbshyguy1100')
                        await payload.member.send(embed=embed) 
