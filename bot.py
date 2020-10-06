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
from chatterbot import ChatBot
from chatterbot.trainers import ListTrainer
import mysql.connector
import logging
import py621

# logger = logging.getLogger()
# logger.setLevel(logging.DEBUG)

parser = argparse.ArgumentParser(description='A glorified e621 Discord browser!')
parser.add_argument('--token', type=str,
                   help='Specify token for out-of-loop execution')
args = parser.parse_args()

if args.token is not None:
    token = args.token
else:
    with open('../token.txt', 'r') as file:
        token = file.read().replace('\n', '')\

with open('../dbpassword.txt', 'r') as file:
    dbpassword = file.read().replace('\n', '')

chatbot = ChatBot(
    'FurBot',
    trainer='chatterbot.trainers.ChatterBotCorpusTrainer'
)

BlackList = ["bestiality", "pony", "watersports", "gore", "scat", "young", "loli", "my_little_pony", "vore", "friendship_is_magic", "nightmare_fuel"]

CringeList = ["fortnite", "undertale"]
AnimalList = ["wolf", "dog", "cat", "goat", "eagle", "fox", "lion", "protogen", "cow", "horse"]

MoanList = ["media/moan 1.ogg", "media/moan 2.ogg", "media/moan 3.ogg", "media/moan 4.ogg", "media/moan 5.ogg", "media/moan 6.ogg"]
owoList = ["media/OWO_1.ogg", "media/OWO_2.ogg", "media/OWO_3.ogg"]

MantainerList = [306540670724734976, 413108421790007313]
CumList = [338468574970511371, 228659079420182539]

bot = commands.Bot(command_prefix = 'f-')
bot.remove_command('help')

IsAlive = True

#Version = subprocess.run('git rev-parse HEAD', stdout=subprocess.PIPE).stdout.decode("utf-8") 

async def status_task():
    while IsAlive:
        await bot.change_presence(status=discord.Status.online, activity=discord.Game(name="f-help | Currently on " + str(len(bot.guilds)) + " servers!"))
        await asyncio.sleep(60)

async def VoicePlay(ctx, audiopath):
    if (ctx.message.channel.type is discord.ChannelType.private):
        embed=discord.Embed(title="Error!", description="This command only works on servers!", color=0xff0000)
        return await ctx.message.channel.send(embed=embed)

    guild = ctx.guild
    author = ctx.message.author
    voice_channel = author.voice.channel

    try:
        vc = await voice_channel.connect()
    except:
        vc = guild.voice_client
    
    audio_source = discord.FFmpegOpusAudio(audiopath)

    if not vc.is_playing():
        vc.play(audio_source, after=None)
    else:
        embed=discord.Embed(title="Error!", description="Something is already playing, please wait!", color=0xff0000)
        return await ctx.message.channel.send(embed=embed)
    
    while vc.is_playing():
        await asyncio.sleep(1)

    await vc.disconnect()

@bot.event
async def on_ready():
    print('Logged in as {0.user}'.format(bot))
    bot.loop.create_task(status_task())

    print(bot.heartbeat_timeout)
    
    for guild in bot.guilds:
        try:
            if (guild.voice_client.is_playing()):
                pass
            else:
                await guild.voice_client.disconnect()
        except:
            pass

@bot.event
async def on_message_delete(message):
    # TODO: MAKE THIS FEATURE SERVER AGNOSTIC

    if (message.channel.type is discord.ChannelType.private):
        return
    if (message.guild.id != 540651642463453253):
        return
    
    Cl = bot.get_channel(746838742295248958)
    
    embed=discord.Embed(title=str(message.author.name) + "#" + str(message.author.discriminator) + " [" + str(message.author.id) + "]", description=str(message.id), color=0xff0000)
    embed.add_field(name="Files", value=str(len(message.attachments)), inline=False)
    embed.add_field(name="Time", value=datetime.now().strftime("%d/%m/%Y %H:%M:%S"), inline=False)
    embed.set_footer(text=message.content)
    await Cl.send(embed=embed)

@bot.event
async def on_member_join(member):
    # TODO: MAKE THIS FEATURE SERVER AGNOSTIC

    if (member.guild.id != 540651642463453253):
        return
    
    Cc = bot.get_channel(745811042893955082)
    await Cc.send('UwU OwO, um novo aluno chegou, <@' + str(member.id) + '>!')

@bot.event
async def on_member_remove(member):
    # TODO: MAKE THIS FEATURE SERVER AGNOSTIC

    if (member.guild.id != 540651642463453253):
        return
    
    Cc = bot.get_channel(745811042893955082)
    await Cc.send(str(member.name) + '#' + member.discriminator + ' saiu...')

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
    
    embed.add_field(name="\n<:die:747162817714454570>", value="**e621/e926**", inline=False)
    
    embed.add_field(name=":globe_with_meridians: f-request", value="Looks up content on e621 or e926\nUsage: f-request nsfw dick | f-request sfw random", inline=True)
    embed.add_field(name="<:impressive:744230514994708590> f-meme", value="Looks up a meme on e926\nUsage: f-meme", inline=True)
    
    embed.add_field(name="\n:microphone:", value="**Voice Fun**", inline=False)

    embed.add_field(name="<:gooz:747231402285727776> f-moan", value="Moans on your voice channel\nUsage: f-moan", inline=True)
    embed.add_field(name="<:hot:747160250158940180> f-owo", value="OwOs on your voice channel\nUsage: f-owo", inline=True)
    embed.add_field(name="<:legocity:747163763085672518> f-rap", value="Raps on your voice channel\nUsage: f-rap", inline=True)
    embed.add_field(name=":stop_button: f-disconnect", value="Disconnects from voice channel\nUsage: f-disconnect", inline=True)

    embed.add_field(name="\n:bookmark_tabs:", value="**Text Fun**", inline=False)

    embed.add_field(name=":speech_left: f-chat", value="Chats with a very dumb AI\nUsage: f-chat hello, how are you doing?", inline=True)
    embed.add_field(name=":satellite_orbital: f-obliterate", value="Obliterate your target's DM\nUsage: f-obliterate @Bugadinho#5769", inline=True)
    embed.add_field(name=":airplane: f-airstrike", value="Airstrikes your target's DM\nUsage: f-airstrike @Bugadinho#5769", inline=True)
    embed.add_field(name="<:fapgamer:747188878951186433> f-cumlord", value="Tells you who is the daily cumlord\nUsage: f-cumlord", inline=True)
    embed.add_field(name=":gun: f-roulette", value="A innocent russian roulette game\nUsage: f-roulette", inline=True)
    embed.add_field(name=":thinking: f-howmuch", value="Tells how much of a something you are\nUsage: f-howmuch alive", inline=True)
    embed.add_field(name=":dog: f-whichanimal", value="Tells you which animal you are\nUsage: f-whichanimal", inline=True)
    embed.add_field(name="<:subway:744236763735785483> f-yiff", value="Yiffs your target\nUsage: f-yiff @Bugadinho#5769", inline=True)
    embed.add_field(name=":fox: f-pounce", value="Pounces your target\nUsage: f-pounce @Bugadinho#5769", inline=True)

    await ctx.message.channel.send(embed=embed)

@bot.command()
async def info(ctx):
    embed=discord.Embed(title="FurBot", url="https://github.com/BugadinhoGamers/FurBot", description="The glorified e621 browser!", color=0x80ecff)
    
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

@bot.command()
async def balance(ctx):
    botdb = mysql.connector.connect(
        host="192.168.0.169",
        user="root",
        password=dbpassword,
        database="FurBot"
    )
    mycursor = botdb.cursor()

    sql = "SELECT * FROM Members WHERE ID = %s"
    val = (ctx.message.author.id, )

    mycursor.execute(sql, val)

    myresult = mycursor.fetchall()

    if myresult == []:
        await ctx.message.channel.send("Your account is not associated with a balance, creating one...")
        sql = "INSERT INTO Members (ID, Credits, HornyJail, Likeness) VALUES (%s, %s, %s, %s)"
        val = (ctx.message.author.id, 0, 0, 50)
        mycursor.execute(sql, val)
        botdb.commit()
        return await ctx.message.channel.send("Balance created!")

    embed=discord.Embed(title=ctx.message.author.name + "'s balance", description=str(myresult[0][1]) + " credits", color=0x80ecff)
    
    await ctx.message.channel.send(embed=embed)

    

@bot.command()
async def request(ctx, type, *, tags):
    if(ctx.message.author.id in CumList):
        print("Blacklisted user attempted to use bot")
        embed=discord.Embed(title="Error!", description="no <:subway:744236763735785483>", color=0xff0000)
        return await ctx.message.channel.send(embed=embed)
    
    async with ctx.message.channel.typing():
        Safe = True
        Tags = ["order:random"]

        if(type == "sfw"):
            link = "https://e926.net/"
            prefix = ""
            colormaster = 0x00ff88
            Safe = True
        elif(type == "nsfw"):
            if (ctx.message.channel.is_nsfw()):
                link = "https://e621.net/"
                prefix = "SPOILER_"
                colormaster = 0x8000ff
                Safe = False
                Tags.append("rating:explicit")
            elif (ctx.message.channel.type is discord.ChannelType.private):
                link = "https://e621.net/"
                prefix = "SPOILER_"
                colormaster = 0x8000ff
                Safe = False
                Tags.append("rating:explicit")
            else:
                embed=discord.Embed(title="Error!", description="NSFW is disabled on this channel!", color=0xff0000)
                return await ctx.message.channel.send(embed=embed)
        else:
            link = "https://e926.net/"
            colormaster = 0x00ff88
            Safe = True
        
        for Tag in tags.split():
            Tags.append(Tag)
        
        for Tag in BlackList:
            Tags.append("-" + Tag)

        loop = asyncio.get_event_loop()
        asyncRequest = loop.run_in_executor(None, py621.public.getPosts, Safe, Tags, 1, 1, False)

        #Posts = py621.public.getPosts(Safe, Tags, 1, 1, False)
        Posts = await asyncRequest

        if(len(Posts) == 0):
            embed=discord.Embed(title="Error!", description="No post was found!", color=0xff0000)
            return await ctx.message.channel.send(embed=embed)

        Post = Posts[0]

        PostURL = Post["file"]["url"]

        Link = link + (f"posts/{Post['id']}")
        Link = "<" + Link + ">"

        if ("webm" in PostURL):
            await ctx.message.channel.send(Link + "\n" + PostURL)
        elif ("avi" in PostURL):
            await ctx.message.channel.send(Link + "\n" + PostURL)
        elif ("mp4" in PostURL):
            await ctx.message.channel.send(Link + "\n" + PostURL)
        else:
            embed=discord.Embed(title=Link, color=colormaster)
            embed.set_image(url=PostURL)
            await ctx.message.channel.send(embed=embed)

        #await ctx.message.channel.send(Link + "\n" + Post)
        #await ctx.message.channel.send(embed=embed)
        #await ctx.send(Post)
        #await bot.send_file(ctx.message.channel, Post,filename="SPOILER_Hello",content="Message test")
        #async with aiohttp.ClientSession() as session:
        #    async with session.get(Post) as resp:
        #        if resp.status != 200:
        #            return await ctx.message.channel.send('Erro baixando arquivo')
        #        data = io.BytesIO(await resp.read())
        #        await ctx.message.channel.send(content=Link,file=discord.File(data, prefix + 'esix.png'))

@bot.command()
async def meme(ctx):
    await ctx.invoke(bot.get_command('request'), type='sfw', tags="meme")

@bot.command()
async def pounce(ctx, *, pounced):
    embed=discord.Embed(color=0x8000ff)
    embed.set_image(url="https://static1.e926.net/data/06/65/066570f0b541f23c8d03d1956a590167.gif")
    await ctx.message.channel.send(content=ctx.message.author.mention + " pounced on " + pounced,embed=embed)

@bot.command()
async def yiff(ctx, *, yiffed):
    gif = "https://static1.e926.net/data/07/a9/07a9e5aa8770e86c1b58e117e6deee4a.png"

    embed=discord.Embed(color=0x8000ff)
    embed.set_image(url=gif)
    await ctx.message.channel.send(content=ctx.message.author.mention + " yiffed " + yiffed,embed=embed)

@bot.command()
async def measuredick(ctx):
    random.seed(ctx.message.author.id * 2)

    embed=discord.Embed(title="Cock Measurer 3000", description="Your cock is about " + str(random.randint(0,200) / 10) + "cm", color=0x8000ff)
    await ctx.message.channel.send(embed=embed)

    #await ctx.message.channel.send("Your cock is about " + str(random.randint(0,200) / 10) + "cm")

@bot.command()
async def cumlord(ctx):
    if (ctx.message.channel.type is discord.ChannelType.private):
        embed=discord.Embed(title="Error!", description="This command only works on servers!", color=0xff0000)
        return await ctx.message.channel.send(embed=embed)
    
    random.seed(datetime.combine(date.today(), datetime.min.time()).replace(tzinfo=timezone.utc).timestamp())
    serverUsers = ctx.message.guild.members

    embed=discord.Embed(title="Daily cumlord", description="The daily cumlord is " + serverUsers[random.randint(0,len(serverUsers)-1)].mention, color=0x8000ff)
    await ctx.message.channel.send(embed=embed)
    #await ctx.message.channel.send("The daily cumlord is " + serverUsers[random.randint(0,len(serverUsers)-1)].mention)

@bot.command()
async def whichanimal(ctx):
    random.seed(ctx.message.author.id * 2)
    await ctx.message.channel.send("You are a " + AnimalList[random.randint(0,len(AnimalList) - 1)])

@bot.command()
async def roulette(ctx):
    if (ctx.message.channel.type is discord.ChannelType.private):
        embed=discord.Embed(title="Error!", description="This command only works on servers!", color=0xff0000)
        return await ctx.message.channel.send(embed=embed)
    
    botdb = mysql.connector.connect(
        host="192.168.0.169",
        user="root",
        password=dbpassword,
        database="FurBot"
    )

    mycursor = botdb.cursor()

    sql = "SELECT * FROM Members WHERE ID = %s"
    val = (ctx.message.author.id, )

    mycursor.execute(sql, val)

    myresult = mycursor.fetchall()

    curCredits = myresult[0][1]
    
    sql = "UPDATE Members SET Credits = %s WHERE ID = %s"

    bullet = random.randint(1,6)
    if (bullet == 6):
        embed=discord.Embed(title="Russian Roulette", description="You lost!", color=0xff0000)
        val = (max(curCredits - 60, 0) , ctx.message.author.id, )
        mycursor.execute(sql, val)
        botdb.commit()
        return await ctx.message.channel.send(embed=embed)
    else:
        embed=discord.Embed(title="Russian Roulette", description="You won!", color=0x00ff88)
        val = (max(curCredits + 10, 0) , ctx.message.author.id, )
        mycursor.execute(sql, val)
        botdb.commit()
        return await ctx.message.channel.send(embed=embed)

@bot.command()
async def chat(ctx, *, spoke):
    await ctx.message.channel.send(chatbot.get_response(spoke))

@bot.command()
async def howmuch(ctx, stuff):
    bobao = stuff

    random.seed(ctx.message.author.id * int(bobao, 36) * 2)
    bobin = random.randint(0,100)

    embed=discord.Embed(title="How much?", description=ctx.message.author.mention + " is " + str(bobin) + "% " + bobao, color=0x8000ff)
    await ctx.message.channel.send(embed=embed)

    if (bobin == 100):
        await ctx.invoke(bot.get_command('request'), type='sfw', tags=bobao)

@bot.event
async def on_message(message):
    botdb = mysql.connector.connect(
        host="192.168.0.169",
        user="root",
        password=dbpassword,
        database="FurBot"
    )

    mycursor = botdb.cursor()

    sql = "SELECT * FROM Members WHERE ID = %s"
    val = (message.author.id, )

    mycursor.execute(sql, val)

    myresult = mycursor.fetchall()

    if myresult == []:
        sql = "INSERT INTO Members (ID, Credits, HornyJail, Likeness) VALUES (%s, %s, %s, %s)"
        val = (message.author.id, 0, 0, 50)
        mycursor.execute(sql, val)
        print("nodb")
        botdb.commit()
    
    if any(word in message.content for word in CringeList):
        curCredits = myresult[0][1]
        sql = "UPDATE Members SET Credits = %s WHERE ID = %s"
        val = (max(curCredits - 10, 0), message.author.id, )
        print(curCredits)

        mycursor.execute(sql, val)
        botdb.commit()

        
        await message.delete()
        return await message.channel.send(message.author.mention + ", bruh you just posted cringe, you are gonna lose credits!")

    if myresult[0][3] != None:
        like = myresult[0][3]
    else:
        like = 100
    
    anger = random.randint(1,(100 * ( 1 + like)))

    if (anger == 1):
        await message.delete()
        return await message.channel.send(message.author.mention + ", go suck a cock, i fucking hate you!")
    
    await bot.process_commands(message)

@bot.command()
async def rap(ctx):
    await VoicePlay(ctx, 'media/bad furry rap.ogg')

@bot.command()
async def doom(ctx):
    await VoicePlay(ctx, 'media/doom.ogg')

@bot.command()
async def nokia(ctx):
    await VoicePlay(ctx, 'media/nokia_ringtone.ogg')

@bot.command()
async def moan(ctx):
    await VoicePlay(ctx, random.choice(MoanList))

@bot.command()
async def owo(ctx):
    await VoicePlay(ctx, random.choice(owoList))

@bot.command()
async def obliterate(ctx, obliterated: discord.User):
    if (ctx.message.channel.type is discord.ChannelType.private):
        embed=discord.Embed(title="Error!", description="This command only works on servers!", color=0xff0000)
        return await ctx.message.channel.send(embed=embed)
    
    botdb = mysql.connector.connect(
        host="192.168.0.169",
        user="root",
        password=dbpassword,
        database="FurBot"
    )

    mycursor = botdb.cursor()

    sql = "SELECT * FROM Members WHERE ID = %s"
    val = (ctx.message.author.id, )

    mycursor.execute(sql, val)

    myresult = mycursor.fetchall()

    curCredits = myresult[0][1]
    if (curCredits < 200):
        embed=discord.Embed(title="Error!", description="Not enough credits!", color=0xff0000)
        return await ctx.message.channel.send(embed=embed)
    
    sql = "UPDATE Members SET Credits = %s WHERE ID = %s"
    val = (curCredits - 200, ctx.message.author.id, )

    mycursor.execute(sql, val)
    
    Tags = ["order:random"]
    for Tag in BlackList:
        Tags.append("-" + Tag)

    loop = asyncio.get_event_loop()
    asyncRequest = loop.run_in_executor(None, py621.public.getPosts, False, Tags, 1, 1, False)
    
    Posts = await asyncRequest

    if(len(Posts) == 0):
        return await ctx.message.channel.send("Orbital strike has failed!")
    
    Post = Posts[0]
    PostURL = Post["file"]["url"]

    try:
        if(obliterated.dm_channel == None):
            await obliterated.create_dm()
    
        if(obliterated.dm_channel == None):
            return await ctx.message.channel.send("Orbital strike has failed!")
    except:
        return await ctx.message.channel.send("Orbital strike has failed!")
    
    embed=discord.Embed(color=0x8000ff)
    embed.set_image(url="https://media1.giphy.com/media/3K0D1Dkqh9MOmLSjzW/giphy.gif")

    oldnickname = obliterated.display_name

    try:
        await obliterated.dm_channel.send("You have been obliterated by " + ctx.message.author.name + "!")
        message1 = await obliterated.dm_channel.send(PostURL)
        message2 = await obliterated.dm_channel.send(PostURL)
        message3 = await obliterated.dm_channel.send(PostURL)
        await ctx.message.channel.send(content=ctx.message.author.mention + " has obliterated " + obliterated.mention + "!",embed=embed)
        await asyncio.sleep(1) 
        await message1.delete()
        await message2.delete()
        await message3.delete()
        botdb.commit()
    except:
        print("uh")
        return await ctx.message.channel.send("Orbital strike has failed!")

@bot.command()
async def airstrike(ctx, airstriked: discord.User):
    obliterated = airstriked

    if (ctx.message.channel.type is discord.ChannelType.private):
        embed=discord.Embed(title="Error!", description="This command only works on servers!", color=0xff0000)
        return await ctx.message.channel.send(embed=embed)

    botdb = mysql.connector.connect(
        host="192.168.0.169",
        user="root",
        password=dbpassword,
        database="FurBot"
    )

    mycursor = botdb.cursor()

    sql = "SELECT * FROM Members WHERE ID = %s"
    val = (ctx.message.author.id, )

    mycursor.execute(sql, val)

    myresult = mycursor.fetchall()

    curCredits = myresult[0][1]
    if (curCredits < 100):
        embed=discord.Embed(title="Error!", description="Not enough credits!", color=0xff0000)
        return await ctx.message.channel.send(embed=embed)
    
    sql = "UPDATE Members SET Credits = %s WHERE ID = %s"
    val = (curCredits - 100, ctx.message.author.id, )

    mycursor.execute(sql, val)

    Tags = ["order:random"]
    for Tag in BlackList:
        Tags.append("-" + Tag)

    loop = asyncio.get_event_loop()
    asyncRequest = loop.run_in_executor(None, py621.public.getPosts, False, Tags, 1, 1, False)
    
    Posts = await asyncRequest

    if(len(Posts) == 0):
        return await ctx.message.channel.send("Airstrike has failed!")
    
    Post = Posts[0]
    PostURL = Post["file"]["url"]

    try:
        if(obliterated.dm_channel == None):
            await obliterated.create_dm()
    
        if(obliterated.dm_channel == None):
            return await ctx.message.channel.send("Airstrike has failed!")
    except:
        return await ctx.message.channel.send("Airstrike has failed!")
    
    embed=discord.Embed(color=0x8000ff)
    embed.set_image(url="https://thumbs.gfycat.com/AdmirableGrouchyBoto-small.gif")

    try:
        await obliterated.dm_channel.send("You have been airstriked by " + ctx.message.author.name + "!")
        message1 = await obliterated.dm_channel.send(PostURL)
        await ctx.message.channel.send(content=ctx.message.author.mention + " has airstriked " + obliterated.mention + "!",embed=embed)
        await asyncio.sleep(1) 
        await message1.delete()
        botdb.commit()
    except:
        return await ctx.message.channel.send("Airstrike has failed!")

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
    await ctx.message.channel.send("Updating and restarting bot!")

    IsAlive = False

    await bot.change_presence(status=discord.Status.dnd, activity=discord.Game(name="Updating..."))

    if (ctx.message.author.id not in MantainerList):
        embed=discord.Embed(title="Error!", description="This is a mantainer only command", color=0xff0000)
        return await ctx.message.channel.send(embed=embed)
    await bot.close()
    os.system("git pull")
    os.execv(__file__, sys.argv)

@bot.command()
async def restart(ctx):
    await ctx.message.channel.send("Restarting bot!")

    IsAlive = False

    await bot.change_presence(status=discord.Status.dnd, activity=discord.Game(name="Restarting..."))

    if (ctx.message.author.id not in MantainerList):
        embed=discord.Embed(title="Error!", description="This is a mantainer only command", color=0xff0000)
        return await ctx.message.channel.send(embed=embed)
    await bot.close()
    os.execv(__file__, sys.argv)

if __name__ == "__main__": 
    bot.run(token)