#!/usr/bin/python3

# FurBot by BugadinhoGamers (https://github.com/BugadinhoGamers/FurBot)
# Licensed under GPLv3.0

import argparse
import io
import aiohttp
import os
import sys
import platform
import discord
import asyncio
import subprocess
from discord.ext import commands, tasks
from discord.utils import get
from discord import Game
import discord_argparse.errors as da_errors
import json
import requests
from datetime import datetime
from datetime import date
from datetime import timezone
import psutil
import random
import logging
import py621
import json

import mysql.connector

logger = logging.getLogger()
logger.setLevel(logging.CRITICAL)

parser = argparse.ArgumentParser(description='A glorified e621 Discord browser!')
parser.add_argument('--bot', type=str,
                   default="FurBot", help='Specify token for out-of-loop execution')
args = parser.parse_args()

bot = commands.Bot(command_prefix = 'f-')
bot.remove_command('help')

bot.json = []

with open('../' + args.bot + ".json") as json_file:
    bot.json = json.load(json_file)

bot.CringeList = ["fortnite", "undertale"]

bot.helpCommand = []

loadedCogs = []

IsAlive = True

async def status_task():
    while IsAlive:
        await bot.change_presence(status=discord.Status.online, activity=discord.Game(name="f-help | Currently on " + str(len(bot.guilds)) + " servers!"))
        await asyncio.sleep(60)

@bot.event
async def on_ready():
    print('Logged in as {0.user}'.format(bot))
    bot.loop.create_task(status_task())
    
    for guild in bot.guilds:
        try:
            if (guild.voice_client.is_playing()):
                pass
            else:
                await guild.voice_client.disconnect()
        except:
            pass

@bot.event
async def on_command_error(ctx, error):
    if hasattr(ctx.command, 'on_error'):
        return
    
    ignored = (commands.CommandNotFound, commands.UserInputError)

    if isinstance(error, commands.CommandNotFound):
        embed=discord.Embed(title="Invalid command!", description="Command does not exist!" , color=0xff0000)
        return await ctx.message.channel.send(embed=embed)
    
    embed=discord.Embed(title="Error!", description="Something went wrong when calling the command!", color=0xff0000)
    embed.set_footer(text=error)
    return await ctx.message.channel.send(embed=embed)

@bot.command()
async def help(ctx):
    embed=discord.Embed(title=":book: Help", description="These are the commands and how to use them, please keep in mind that the list is very big!", color=0xe5ff24)
    
    for Command in bot.helpCommand:
        embed.add_field(name=Command[0], value=Command[1], inline=Command[2])
    
    await ctx.message.channel.send(embed=embed)

@bot.command()
async def info(ctx):
    embed=discord.Embed(title="FurBot", url="https://github.com/BugadinhoGamers/FurBot", description="The glorified e621 browser!", color=0x80ecff)
    
    embed.set_thumbnail(url="https://cdn.discordapp.com/attachments/747843765057880208/768545986074378291/IconTransparent.png")
    
    embed.add_field(name="Latency", value=str(int(bot.latency * 1000)) + "ms", inline=True)
    embed.add_field(name="CPU Usage", value=str(psutil.cpu_percent()) + "%", inline=True)
    embed.add_field(name="RAM Usage", value=str(psutil.virtual_memory().percent) + "%", inline=True)

    embed.add_field(name="Servers", value=str(len(bot.guilds)), inline=True)

    embed.add_field(name="Platform", value=str(platform.platform()), inline=False)
    #embed.add_field(name="Version", value=str(Version), inline=False)
    #embed.add_field(name="Lead Programmer", value="*Bugadinho#5769*", inline=False)

    #result = subprocess.run(['git', 'rev-parse HEAD'], stdout=subprocess.PIPE)

    #embed.add_field(name="Commit ID", value=result.stdout.decode('utf-8'), inline=False)
    
    await ctx.message.channel.send(embed=embed)

@bot.event
async def on_message(message):
    await bot.process_commands(message)

@bot.command()
async def disconnect(ctx):
    if (ctx.message.channel.type is discord.ChannelType.private):
        embed=discord.Embed(title="Error!", description="This command only works on servers!", color=0xff0000)
        return await ctx.message.channel.send(embed=embed)
    
    guild = ctx.message.guild

    try:
        if (guild.voice_client.is_playing()):
            await guild.voice_client.stop()
            await guild.voice_client.disconnect()
        else:
            await guild.voice_client.disconnect()
    except:
        pass

@bot.command()
async def update(ctx):
    if (ctx.message.author.id not in bot.json["maintainers"]):
        embed=discord.Embed(title="Error!", description="This is a maintainer only command", color=0xff0000)
        return await ctx.message.channel.send(embed=embed)
    
    await ctx.message.channel.send("Updating and restarting bot!")

    IsAlive = False

    await bot.change_presence(status=discord.Status.dnd, activity=discord.Game(name="Updating..."))

    await bot.close()
    os.system("git pull")
    os.execv(__file__, sys.argv)

@bot.command()
async def restart(ctx):
    if (ctx.message.author.id not in bot.json["maintainers"]):
        embed=discord.Embed(title="Error!", description="This is a maintainer only command", color=0xff0000)
        return await ctx.message.channel.send(embed=embed)
    
    await ctx.message.channel.send("Restarting bot!")

    IsAlive = False

    await bot.change_presence(status=discord.Status.dnd, activity=discord.Game(name="Restarting..."))

    await bot.close()
    os.execv(__file__, sys.argv)

if __name__ == "__main__": 
    potentialCogs = os.listdir("cogs/")

    for cog in potentialCogs:
        cogDiferential = cog.split(".")
        if len(cogDiferential) > 1:
            if cogDiferential[0] in bot.json["blacklistedCogs"]:
                print("Blacklisted cog [" + cogDiferential[0] + "]!")
            elif cogDiferential[1] == "py":
                try:
                    bot.load_extension("cogs." + cogDiferential[0])
                    print("Loaded cog [" + cogDiferential[0] + "]!")
                except Exception as e:
                    print("Cog [" + cogDiferential[0] + "] failed to load! " + str(e))

    bot.run(bot.json["token"])