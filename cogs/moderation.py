# FurBot by BugadinhoGamers (https://github.com/BugadinhoGamers/FurBot)
# Licensed under GPLv3.0

import discord
import mysql.connector
import asyncio
from datetime import datetime
from datetime import date
from datetime import timezone
from discord.ext import commands

class Moderation(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self._last_member = None
    
    async def CheckServer(self, id):
        botdb = mysql.connector.connect(
            host="192.168.0.169",
            user="root",
            password=self.bot.dbpassword,
            database="FurBot"
        )
        mycursor = botdb.cursor()

        sql = "SELECT * FROM Servers WHERE ID = %s"
        val = (id, )

        mycursor.execute(sql, val)

        myresult = mycursor.fetchall()

        if myresult == []:
            sql = "INSERT INTO Servers (ID, LastCumLord, CumLord, JoinChannel, LeaveChannel, LogChannel, Language) VALUES (%s, %s, %s, %s, %s, %s, %s)"
            val = (id, None, None, None, None, None, None)
            mycursor.execute(sql, val)
            botdb.commit()
        
    async def GetJoinChannel(self, id):
        await self.CheckServer(id)

        botdb = mysql.connector.connect(
            host="192.168.0.169",
            user="root",
            password=self.bot.dbpassword,
            database="FurBot"
        )

        mycursor = botdb.cursor()

        sql = "SELECT * FROM Servers WHERE ID = %s"
        val = (id, )

        mycursor.execute(sql, val)

        myresult = mycursor.fetchall()
        
        return int(myresult[0][3])
    
    async def GetLeaveChannel(self, id):
        await self.CheckServer(id)

        botdb = mysql.connector.connect(
            host="192.168.0.169",
            user="root",
            password=self.bot.dbpassword,
            database="FurBot"
        )

        mycursor = botdb.cursor()

        sql = "SELECT * FROM Servers WHERE ID = %s"
        val = (id, )

        mycursor.execute(sql, val)

        myresult = mycursor.fetchall()
        
        return int(myresult[0][4])
    
    async def GetLogChannel(self, id):
        await self.CheckServer(id)

        botdb = mysql.connector.connect(
            host="192.168.0.169",
            user="root",
            password=self.bot.dbpassword,
            database="FurBot"
        )

        mycursor = botdb.cursor()

        sql = "SELECT * FROM Servers WHERE ID = %s"
        val = (id, )

        mycursor.execute(sql, val)

        myresult = mycursor.fetchall()
        
        return int(myresult[0][5])
    
    async def SetServerJoinChannel(self, id, value):
        await self.CheckServer(id)

        botdb = mysql.connector.connect(
            host="192.168.0.169",
            user="root",
            password=self.bot.dbpassword,
            database="FurBot"
        )

        mycursor = botdb.cursor()
        
        sql = "UPDATE Servers SET JoinChannel = %s WHERE ID = %s"
        val = (value, id, )

        mycursor.execute(sql, val)
        botdb.commit()
    
    async def SetServerLeaveChannel(self, id, value):
        await self.CheckServer(id)

        botdb = mysql.connector.connect(
            host="192.168.0.169",
            user="root",
            password=self.bot.dbpassword,
            database="FurBot"
        )

        mycursor = botdb.cursor()
        
        sql = "UPDATE Servers SET LeaveChannel = %s WHERE ID = %s"
        val = (value, id, )

        mycursor.execute(sql, val)
        botdb.commit()

    async def SetServerLogChannel(self, id, value):
        await self.CheckServer(id)

        botdb = mysql.connector.connect(
            host="192.168.0.169",
            user="root",
            password=self.bot.dbpassword,
            database="FurBot"
        )

        mycursor = botdb.cursor()
        
        sql = "UPDATE Servers SET LogChannel = %s WHERE ID = %s"
        val = (value, id, )

        mycursor.execute(sql, val)
        botdb.commit()

    @commands.Cog.listener()
    async def on_message_delete(self, message):
        if (message.channel.type is discord.ChannelType.private):
            return
        
        logChannel = await self.GetLogChannel(message.guild.id)

        if (logChannel == None):
            return
    
        Cl = self.bot.get_channel(int(logChannel))
    
        embed=discord.Embed(title=str(message.author.name) + "#" + str(message.author.discriminator) + " [" + str(message.author.id) + "]", description=str(message.id), color=0xff0000)
        embed.add_field(name="Files", value=str(len(message.attachments)), inline=False)
        embed.add_field(name="Time", value=datetime.now().strftime("%d/%m/%Y %H:%M:%S"), inline=False)
        embed.set_footer(text=message.content)
        await Cl.send(embed=embed)

    @commands.Cog.listener()
    async def on_member_join(self, member):
        # TODO: MAKE THIS FEATURE RESPECT SERVER LANGUAGE

        channel = await self.GetJoinChannel(member.guild.id)

        if (channel == None):
            return
    
        Cc = bot.get_channel(int(channel))
        await Cc.send('UwU OwO, um novo aluno chegou, <@' + str(member.id) + '>!')
    
    @commands.Cog.listener()
    async def on_member_remove(self, member):
        # TODO: MAKE THIS FEATURE RESPECT SERVER LANGUAGE

        channel = await self.GetLeaveChannel(member.guild.id)

        if (channel == None):
            return
    
        Cc = bot.get_channel(int(channel))
        await Cc.send(str(member.name) + '#' + member.discriminator + ' saiu...')

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def setlog(self, ctx, channel: discord.TextChannel):
        await self.SetServerLogChannel(ctx.message.guild.id, channel.id)
        await ctx.send("Channel set!")
    
    @commands.command()
    @commands.has_permissions(administrator=True)
    async def setjoin(self, ctx, channel: discord.TextChannel):
        await self.SetServerJoinChannel(ctx.message.guild.id, channel.id)
        await ctx.send("Channel set!")
    
    @commands.command()
    @commands.has_permissions(administrator=True)
    async def setleave(self, ctx, channel: discord.TextChannel):
        await self.SetServerLeaveChannel(ctx.message.guild.id, channel.id)
        await ctx.send("Channel set!")

def setup(bot):
    bot.add_cog(Moderation(bot))