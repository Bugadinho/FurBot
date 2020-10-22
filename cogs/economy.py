# FurBot by BugadinhoGamers (https://github.com/BugadinhoGamers/FurBot)
# Licensed under GPLv3.0

import discord
import random
import mysql.connector
import asyncio
import py621
from discord.ext import commands

class Economy(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self._last_member = None
        
    async def CheckAccount(self, id):
        botdb = mysql.connector.connect(
            host=self.bot.json["dbip"],
            user=self.bot.json["dbuser"],
            password=self.bot.json["dbpassword"],
            database="FurBot"
        )
        mycursor = await asyncio.get_event_loop().run_in_executor(None, botdb.cursor)

        sql = "SELECT * FROM Members WHERE ID = %s"
        val = (id, )

        await asyncio.get_event_loop().run_in_executor(None, mycursor.execute, sql, val)

        myresult = await asyncio.get_event_loop().run_in_executor(None, mycursor.fetchall)

        if myresult == []:
            sql = "INSERT INTO Members (ID, Credits, HornyJail, Likeness) VALUES (%s, %s, %s, %s)"
            val = (id, 0, 0, 50)
            await asyncio.get_event_loop().run_in_executor(None, mycursor.execute, sql, val)
            await asyncio.get_event_loop().run_in_executor(None, botdb.commit)
    
    async def GetLike(self, id):
        await self.CheckAccount(id)

        botdb = mysql.connector.connect(
            host=self.bot.json["dbip"],
            user=self.bot.json["dbuser"],
            password=self.bot.json["dbpassword"],
            database="FurBot"
        )

        mycursor = await asyncio.get_event_loop().run_in_executor(None, botdb.cursor)

        sql = "SELECT * FROM Members WHERE ID = %s"
        val = (id, )

        await asyncio.get_event_loop().run_in_executor(None, mycursor.execute, sql, val)

        myresult = await asyncio.get_event_loop().run_in_executor(None, mycursor.fetchall)
        
        return int(myresult[0][3])
    
    async def GetCredits(self, id):
        await self.CheckAccount(id)

        botdb = mysql.connector.connect(
            host=self.bot.json["dbip"],
            user=self.bot.json["dbuser"],
            password=self.bot.json["dbpassword"],
            database="FurBot"
        )

        mycursor = await asyncio.get_event_loop().run_in_executor(None, botdb.cursor)

        sql = "SELECT * FROM Members WHERE ID = %s"
        val = (id, )

        await asyncio.get_event_loop().run_in_executor(None, mycursor.execute, sql, val)

        myresult = await asyncio.get_event_loop().run_in_executor(None, mycursor.fetchall)
        
        return int(myresult[0][1])

    async def TakeCredits(self, amount, id, requireAll):
        curCredits = await self.GetCredits(id)

        botdb = mysql.connector.connect(
            host=self.bot.json["dbip"],
            user=self.bot.json["dbuser"],
            password=self.bot.json["dbpassword"],
            database="FurBot"
        )

        mycursor = await asyncio.get_event_loop().run_in_executor(None, botdb.cursor)
        
        if requireAll == True:
            if curCredits < amount:
                return False
        
        sql = "UPDATE Members SET Credits = %s WHERE ID = %s"
        val = (max(curCredits - amount, 0), id, )

        await asyncio.get_event_loop().run_in_executor(None, mycursor.execute, sql, val)
        await asyncio.get_event_loop().run_in_executor(None, botdb.commit)

        return True
    
    async def GiveCredits(self, amount, id):
        curCredits = await self.GetCredits(id)

        botdb = mysql.connector.connect(
            host=self.bot.json["dbip"],
            user=self.bot.json["dbuser"],
            password=self.bot.json["dbpassword"],
            database="FurBot"
        )

        mycursor = await asyncio.get_event_loop().run_in_executor(None, botdb.cursor)
        
        sql = "UPDATE Members SET Credits = %s WHERE ID = %s"
        val = (max(curCredits + amount, 0), id, )

        await asyncio.get_event_loop().run_in_executor(None, mycursor.execute, sql, val)
        await asyncio.get_event_loop().run_in_executor(None, botdb.commit)

    @commands.Cog.listener()
    async def on_message(self, message):
        if any(word in message.content for word in self.bot.CringeList):
            await self.TakeCredits(10, message.author.id, False)

        
            await message.delete()
            return await message.channel.send(message.author.mention + ", bruh you just posted cringe, you are gonna lose credits!")

        like = await self.GetLike(message.author.id)
    
        anger = random.randint(1,(100 * ( 1 + like)))

        if (anger == 1):
            await message.delete()
            return await message.channel.send(message.author.mention + ", go suck a cock, i fucking hate you!")
    
    
    @commands.command()
    async def balance(self, ctx):
        Credits = await self.GetCredits(ctx.message.author.id)

        embed=discord.Embed(title=ctx.message.author.name + "'s balance", description=str(Credits) + " credits", color=0x80ecff)
    
        await ctx.message.channel.send(embed=embed)
    
    @commands.command()
    async def roulette(self, ctx):
        if (ctx.message.channel.type is discord.ChannelType.private):
            embed=discord.Embed(title="Error!", description="This command only works on servers!", color=0xff0000)
            return await ctx.message.channel.send(embed=embed)

        bullet = random.randint(1,6)
        if (bullet == 6):
            embed=discord.Embed(title="Russian Roulette", description="You lost!", color=0xff0000)
            await self.TakeCredits(60, ctx.message.author.id, False)

            return await ctx.message.channel.send(embed=embed)
        else:
            embed=discord.Embed(title="Russian Roulette", description="You won!", color=0x00ff88)
            await self.GiveCredits(10, ctx.message.author.id)

            return await ctx.message.channel.send(embed=embed)
    
    @commands.command()
    async def obliterate(self, ctx, obliterated: discord.User):
        if (ctx.message.channel.type is discord.ChannelType.private):
            embed=discord.Embed(title="Error!", description="This command only works on servers!", color=0xff0000)
            return await ctx.message.channel.send(embed=embed)
        
        curCredits = await self.GetCredits(ctx.message.author.id)

        if (curCredits < 200):
            embed=discord.Embed(title="Error!", description="Not enough credits!", color=0xff0000)
            return await ctx.message.channel.send(embed=embed)
    
        esix = self.bot.get_cog("ESix")
        Tags = ["order:random"]
        for Tag in esix.BlackList:
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
            await self.TakeCredits(200, ctx.message.author.id, True)
        except:
            print("uh")
            return await ctx.message.channel.send("Orbital strike has failed!")
    
    @commands.command()
    async def MoneyAdd(self, ctx, id, amount):
        if (ctx.message.author.id not in self.bot.json["maintainers"]):
            embed=discord.Embed(title="Error!", description="This is a maintainer only command", color=0xff0000)
            return await ctx.message.channel.send(embed=embed)
        await self.GiveCredits(int(amount), id)

def setup(bot):
    bot.add_cog(Economy(bot))

    #bot.helpCommand.append(["", "", False])
    #bot.helpCommand.append(["", "", True])