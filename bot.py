import io
import aiohttp
import os
import discord
import asyncio
from discord.ext import commands, tasks
from discord.utils import get
from discord import Game
import json
import requests
from datetime import datetime
import psutil
import random

CringeList = ["fortnite", "undertale"]

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

@bot.event
async def on_ready():
    print('Logged in as {0.user}'.format(bot))
    bot.loop.create_task(status_task())

@bot.event
async def on_message_delete(message):
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

@bot.command()
async def help(ctx):
    embed=discord.Embed(title=":book: Help", description="These are the commands and how to use them, please keep in mind that the list is very big!", color=0xe5ff24)
    embed.add_field(name=":globe_with_meridians: f-request", value="Looks up content on e621 or e926\nUsage: f-request nsfw dick | f-request sfw random", inline=False)
    embed.add_field(name="<:impressive:744230514994708590> f-meme", value="Looks up a meme on e926\nUsage: f-meme", inline=False)
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
            return await ctx.message.channel.send('Nothing found!')

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
async def measuredick(ctx):
    random.seed(ctx.message.author.id * 2)
    await ctx.message.channel.send("Your cock is about " + str(random.randint(0,200) / 10) + "cm")

@bot.command()
async def roulette(ctx):
    bullet = random.randint(1,6)
    if (bullet == 6):
        await ctx.message.channel.send("You lost!")
    else:
        await ctx.message.channel.send("You win!")

@bot.command()
async def howmuch(ctx, bobao):
    random.seed(ctx.message.author.id * int(bobao, 36) * 2)
    bobin = random.randint(0,100)
    await ctx.message.channel.send(ctx.message.author.mention + " is " + str(bobin) + "% " + bobao)
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

bot.run(token)