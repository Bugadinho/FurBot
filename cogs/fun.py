# FurBot by BugadinhoGamers (https://github.com/BugadinhoGamers/FurBot)
# Licensed under GPLv3.0

import discord
import random
from datetime import datetime
from datetime import date
from datetime import timezone
from discord.ext import commands

class Fun(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self._last_member = None
    
    AnimalList = ["wolf", "dog", "cat", "goat", "eagle", "fox", "lion", "protogen", "cow", "horse"]

    @commands.command()
    async def whichanimal(self, ctx):
        random.seed(ctx.message.author.id * 2)
        await ctx.message.channel.send("You are a " + self.AnimalList[random.randint(0,len(self.AnimalList) - 1)])
    
    @commands.command()
    async def pounce(self, ctx, *, pounced):
        embed=discord.Embed(color=0x8000ff)
        embed.set_image(url="https://static1.e926.net/data/06/65/066570f0b541f23c8d03d1956a590167.gif")
        await ctx.message.channel.send(content=ctx.message.author.mention + " pounced on " + pounced,embed=embed)
    
    @commands.command()
    async def yiff(self, ctx, *, yiffed):
        gif = "https://static1.e926.net/data/07/a9/07a9e5aa8770e86c1b58e117e6deee4a.png"

        embed=discord.Embed(color=0x8000ff)
        embed.set_image(url=gif)
        await ctx.message.channel.send(content=ctx.message.author.mention + " yiffed " + yiffed,embed=embed)

    @commands.command()
    async def measuredick(self, ctx):
        random.seed(ctx.message.author.id * 2)

        embed=discord.Embed(title="Cock Measurer 3000", description="Your cock is about " + str(random.randint(0,200) / 10) + "cm", color=0x8000ff)
        await ctx.message.channel.send(embed=embed)
    
    @commands.command()
    async def cumlord(self, ctx):
        if (ctx.message.channel.type is discord.ChannelType.private):
            embed=discord.Embed(title="Error!", description="This command only works on servers!", color=0xff0000)
            return await ctx.message.channel.send(embed=embed)
    
        random.seed(datetime.combine(date.today(), datetime.min.time()).replace(tzinfo=timezone.utc).timestamp())
        serverUsers = ctx.message.guild.members

        embed=discord.Embed(title="Daily cumlord", description="The daily cumlord is " + serverUsers[random.randint(0,len(serverUsers)-1)].mention, color=0x8000ff)
        await ctx.message.channel.send(embed=embed)
    
    @commands.command()
    async def howmuch(self, ctx, stuff):
        bobao = stuff

        random.seed(ctx.message.author.id * int(bobao, 36) * 2)
        bobin = random.randint(0,100)

        embed=discord.Embed(title="How much?", description=ctx.message.author.mention + " is " + str(bobin) + "% " + bobao, color=0x8000ff)
        await ctx.message.channel.send(embed=embed)

        if (bobin == 100):
            await ctx.invoke(bot.get_command('request'), type='sfw', tags=bobao)


def setup(bot):
    bot.add_cog(Fun(bot))