# FurBot by BugadinhoGamers (https://github.com/BugadinhoGamers/FurBot)
# Licensed under GPLv3.0

import io
import aiohttp
import os
import discord
import asyncio
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
import logging

logger = logging.getLogger()
logger.setLevel(logging.CRITICAL)

OPUS_LIBS = ['libopus-0.x86.dll', 'libopus-0.x64.dll', 'libopus-0.dll', 'libopus.so.0', 'libopus.0.dylib']

def load_opus_lib(opus_libs=OPUS_LIBS):
    if opus.is_loaded():
        return True

    for opus_lib in opus_libs:
        try:
            opus.load_opus(opus_lib)
            return
        except OSError:
            pass

        raise RuntimeError('Could not load an opus lib. Tried %s' % (', '.join(opus_libs)))

chatbot = ChatBot(
    'FurBot',
    trainer='chatterbot.trainers.ChatterBotCorpusTrainer'
)

CringeList = ["fortnite", "undertale"]
AnimalList = ["wolf", "dog", "cat", "goat", "eagle", "fox", "lion", "protogen", "cow", "horse"]
MoanList = ["moan 1.mp3", "moan 2.mp3", "moan 3.mp3", "moan 4.mp3", "moan 5.mp3", "moan 6.mp3"]

CumList = [338468574970511371, 228659079420182539]

with open('../token.txt', 'r') as file:
    token = file.read().replace('\n', '')

headers = {"User-Agent":"FurBot/1.0 (API Usage by Bugman69 on E621)"}

bot = commands.Bot(command_prefix = 'f-')
bot.remove_command('help')

async def status_task():
    while True:
        await bot.change_presence(activity=discord.Game(name="Powered by e621.net"))
        await asyncio.sleep(10)
        await bot.change_presence(activity=discord.Game(name="Use f-help to get some help"))
        await asyncio.sleep(10)
        await bot.change_presence(activity=discord.Game(name="Python has been removed from the toilet"))
        await asyncio.sleep(10)
        await bot.change_presence(activity=discord.Game(name="Pro-tip: dont cum near friends"))
        await asyncio.sleep(10)
        await bot.change_presence(activity=discord.Game(name="Pro-tip: noisy is hot af"))
        await asyncio.sleep(10)
        await bot.change_presence(activity=discord.Game(name="oh no the cum sock is alive"))
        await asyncio.sleep(10)
        await bot.change_presence(activity=discord.Game(name="OwO"))
        await asyncio.sleep(2)
        await bot.change_presence(activity=discord.Game(name="UwU"))
        await asyncio.sleep(2)
        await bot.change_presence(activity=discord.Game(name="OwO"))
        await asyncio.sleep(2)
        await bot.change_presence(activity=discord.Game(name="Falvie drew this picture"))
        await asyncio.sleep(10)
        await bot.change_presence(activity=discord.Game(name="My programmer got ligma"))
        await asyncio.sleep(10)
        await bot.change_presence(activity=discord.Game(name="What are you doing cypherwolf?"))
        await asyncio.sleep(3)
        await bot.change_presence(activity=discord.Game(name="get away from me now"))
        await asyncio.sleep(10)
        await bot.change_presence(activity=discord.Game(name="engineer gaming"))
        await asyncio.sleep(10)
        await bot.change_presence(activity=discord.Game(name="I really hate patetonico"))
        await asyncio.sleep(10)
        await bot.change_presence(activity=discord.Game(name="Pro-tip: smoking is bad"))
        await asyncio.sleep(10)
        await bot.change_presence(activity=discord.Game(name="no wait"))
        await asyncio.sleep(3)
        await bot.change_presence(activity=discord.Game(name="OH FUCK HELP"))
        await asyncio.sleep(2)
        await bot.change_presence(activity=discord.Game(name="cypherwolf is here"))
        await asyncio.sleep(4)
        await bot.change_presence(activity=discord.Game(name="AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA"))
        await asyncio.sleep(3)
        await bot.change_presence(activity=discord.Game(name="SAVE ME!"))
        await asyncio.sleep(1)
        await bot.change_presence(activity=discord.Game(name=""))
        await asyncio.sleep(10)

async def vc_task():
    while True:
        await asyncio.sleep(5)
        for guild in bot.guilds:
            try:
                if (guild.voice_client.is_playing()):
                    pass
                else:
                    await guild.voice_client.disconnect()
            except:
                pass
@bot.event
async def on_ready():
    print('Logged in as {0.user}'.format(bot))
    bot.loop.create_task(status_task())
    bot.loop.create_task(vc_task())

@bot.event
async def on_message_delete(message):
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
    if (member.guild.id != 540651642463453253):
        return
    
    Cc = bot.get_channel(745811042893955082)
    await Cc.send('UwU OwO, um novo aluno chegou, <@' + str(member.id) + '>!')

@bot.event
async def on_member_remove(member):
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
    embed=discord.Embed(title="Bot info", description="FurBot, the glorified e621 browser!", color=0x80ecff)
    embed.add_field(name="Latency", value=str(int(bot.latency * 1000)) + "ms", inline=True)
    embed.add_field(name="CPU Usage", value=str(psutil.cpu_percent()) + "%", inline=True)
    embed.add_field(name="RAM Usage", value=str(psutil.virtual_memory().percent) + "%", inline=True)
    embed.add_field(name="Lead Programmer", value="*Bugadinho#5769*", inline=False)
    await ctx.message.channel.send(embed=embed)

@bot.command()
async def request(ctx, type, *, tags):
    if(ctx.message.author.id in CumList):
        print("Blacklisted user attempted to use bot")
        embed=discord.Embed(title="Error!", description="no <:subway:744236763735785483>", color=0xff0000)
        return await ctx.message.channel.send(embed=embed)
    
    async with ctx.message.channel.typing():
        if(tags == "random"):
            RequestSTR = "posts.json?tags=order:random"
        else:
            RequestSTR = "posts.json?tags=order:random+" + tags.replace(' ', '+')
        RequestSTR += "+-bestiality+-pony+-watersports+-gore+-scat+-young+-loli+-my_little_pony+-vore+-frienship_is_magic+-nightmare_fuel"

        if(type == "sfw"):
            link = "https://e926.net/"
            prefix = ""
            colormaster = 0x00ff88
        elif(type == "nsfw"):
            if (ctx.message.channel.is_nsfw()):
                link = "https://e621.net/"
                RequestSTR = RequestSTR + "+rating:explicit"
                prefix = "SPOILER_"
                colormaster = 0x8000ff
            elif (ctx.message.channel.type is discord.ChannelType.private):
                link = "https://e621.net/"
                RequestSTR = RequestSTR + "+rating:explicit"
                prefix = "SPOILER_"
                colormaster = 0x8000ff
            else:
                embed=discord.Embed(title="Error!", description="NSFW is disabled on this channel!", color=0xff0000)
                return await ctx.message.channel.send(embed=embed)
        else:
            link = "https://e926.net/"
            prefix = ""
            colormaster = 0x00ff88
        #+rating:explicit

        Req = requests.get(link + RequestSTR + "&limit=1", headers=headers)
   
        ReqJson = Req.json()
        if(len(ReqJson["posts"]) == 0):
            embed=discord.Embed(title="Error!", description="No post was found!", color=0xff0000)
            return await ctx.message.channel.send(embed=embed)

        Post = ReqJson["posts"][0]["file"]["url"]
        #print(f"Here is your {type} yiff: {Post}\nURL: <https://e621.net/posts/{ReqJson['posts'][0]['id']}>")
        Link = link + (f"posts/{ReqJson['posts'][0]['id']}")
        Link = "<" + Link + ">"

        if ("webm" in Post):
            await ctx.message.channel.send(Link + "\n" + Post)
        elif ("avi" in Post):
            await ctx.message.channel.send(Link + "\n" + Post)
        elif ("mp4" in Post):
            await ctx.message.channel.send(Link + "\n" + Post)
        else:
            embed=discord.Embed(title=Link, color=colormaster)
            embed.set_image(url=Post)
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
async def pounce(ctx, pounced):
    embed=discord.Embed(color=0x8000ff)
    embed.set_image(url="https://static1.e926.net/data/06/65/066570f0b541f23c8d03d1956a590167.gif")
    await ctx.message.channel.send(content=ctx.message.author.mention + " pounced on " + pounced,embed=embed)

@bot.command()
async def yiff(ctx, yiffed):
    embed=discord.Embed(color=0x8000ff)
    embed.set_image(url="https://logos-download.com/wp-content/uploads/2016/10/Python_logo_wordmark.png")
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
    bullet = random.randint(1,6)
    if (bullet == 6):
        embed=discord.Embed(title="Russian Roulette", description="You lost!", color=0xff0000)
        return await ctx.message.channel.send(embed=embed)
    else:
        embed=discord.Embed(title="Russian Roulette", description="You won!", color=0x00ff88)
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
    if any(word in message.content for word in CringeList):
        await message.delete()
        return await message.channel.send(message.author.mention + ", bruh you just posted cringe, you are gonna lose credits!")
    
    anger = random.randint(1,10000)

    if (anger == 1):
        await message.delete()
        return await message.channel.send(message.author.mention + ", go suck a cock, i fucking hate you!")
    
    await bot.process_commands(message)

@bot.command()
async def rap(ctx):
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
    audio_source = discord.FFmpegPCMAudio('bad furry rap.mp3')
    if not vc.is_playing():
        vc.play(audio_source, after=None)
    else:
        embed=discord.Embed(title="Error!", description="Something is already playing, please wait!", color=0xff0000)
        return await ctx.message.channel.send(embed=embed)

@bot.command()
async def nokia(ctx):
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
    audio_source = discord.FFmpegPCMAudio('nokia_ringtone.mp3')
    if not vc.is_playing():
        vc.play(audio_source, after=None)
    else:
        embed=discord.Embed(title="Error!", description="Something is already playing, please wait!", color=0xff0000)
        return await ctx.message.channel.send(embed=embed)

@bot.command()
async def moan(ctx):
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
    audio_source = discord.FFmpegPCMAudio(random.choice(MoanList))
    if not vc.is_playing():
        vc.play(audio_source, after=None)
    else:
        embed=discord.Embed(title="Error!", description="Something is already playing, please wait!", color=0xff0000)
        return await ctx.message.channel.send(embed=embed)

@bot.command()
async def owo(ctx):
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
    audio_source = discord.FFmpegPCMAudio(random.choice(["OWO_1.mp3", "OWO_2.mp3", "OWO_3.mp3"]))
    if not vc.is_playing():
        vc.play(audio_source, after=None)
    else:
        embed=discord.Embed(title="Error!", description="Something is already playing, please wait!", color=0xff0000)
        return await ctx.message.channel.send(embed=embed)

@bot.command()
async def obliterate(ctx, obliterated: discord.User):
    if (ctx.message.channel.type is discord.ChannelType.private):
        embed=discord.Embed(title="Error!", description="This command only works on servers!", color=0xff0000)
        return await ctx.message.channel.send(embed=embed)
    
    RequestSTR = "posts.json?tags=order:random"
    RequestSTR += "+-bestiality+-pony+-watersports+-gore+-scat+-young+-loli+-my_little_pony+-vore+-frienship_is_magic+-nightmare_fuel"
    link = "https://e621.net/"
    colormaster = 0x00ff88
    Req = requests.get(link + RequestSTR + "&limit=1", headers=headers)
    ReqJson = Req.json()
    if(len(ReqJson["posts"]) == 0):
        return await ctx.message.channel.send("Orbital strike has failed!")
    Post = ReqJson["posts"][0]["file"]["url"]

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
        message1 = await obliterated.dm_channel.send(Post)
        message2 = await obliterated.dm_channel.send(Post)
        message3 = await obliterated.dm_channel.send(Post)
        await ctx.message.channel.send(content=ctx.message.author.mention + " has obliterated " + obliterated.mention + "!",embed=embed)
        await asyncio.sleep(1) 
        await message1.delete()
        await message2.delete()
        await message3.delete()
    except:
        return await ctx.message.channel.send("Orbital strike has failed!")

@bot.command()
async def airstrike(ctx, airstriked: discord.User):
    obliterated = airstriked

    if (ctx.message.channel.type is discord.ChannelType.private):
        embed=discord.Embed(title="Error!", description="This command only works on servers!", color=0xff0000)
        return await ctx.message.channel.send(embed=embed)
    
    RequestSTR = "posts.json?tags=order:random"
    RequestSTR += "+-bestiality+-pony+-watersports+-gore+-scat+-young+-loli+-my_little_pony+-vore+-frienship_is_magic+-nightmare_fuel"
    link = "https://e621.net/"
    colormaster = 0x00ff88
    Req = requests.get(link + RequestSTR + "&limit=1", headers=headers)
    ReqJson = Req.json()
    if(len(ReqJson["posts"]) == 0):
        return await ctx.message.channel.send("Airstrike has failed!")
    Post = ReqJson["posts"][0]["file"]["url"]

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
        message1 = await obliterated.dm_channel.send(Post)
        await ctx.message.channel.send(content=ctx.message.author.mention + " has airstriked " + obliterated.mention + "!",embed=embed)
        await asyncio.sleep(1) 
        await message1.delete()
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
if __name__ == "__main__": 
    bot.run(token)