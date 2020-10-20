# FurBot by BugadinhoGamers (https://github.com/BugadinhoGamers/FurBot)
# Licensed under GPLv3.0

import discord
import asyncio
import random
from discord.ext import commands

class Audio(commands.Cog):
    MoanList = ["media/moan 1.ogg", "media/moan 2.ogg", "media/moan 3.ogg", "media/moan 4.ogg", "media/moan 5.ogg", "media/moan 6.ogg"]
    owoList = ["media/OWO_1.ogg", "media/OWO_2.ogg", "media/OWO_3.ogg"]

    def __init__(self, bot):
        self.bot = bot
        self._last_member = None
    
    async def VoicePlay(self, ctx, audiopath):
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

    @commands.command()
    async def rap(self, ctx):
        await self.VoicePlay(ctx, 'media/bad furry rap.ogg')

    @commands.command()
    async def doom(self, ctx):
        await self.VoicePlay(ctx, 'media/doom.ogg')

    @commands.command()
    async def nokia(self, ctx):
        await self.VoicePlay(ctx, 'media/nokia_ringtone.ogg')

    @commands.command()
    async def moan(self, ctx):
        await self.VoicePlay(ctx, random.choice(self.MoanList))

    @commands.command()
    async def owo(self, ctx):
        await self.VoicePlay(ctx, random.choice(self.owoList))


def setup(bot):
    bot.add_cog(Audio(bot))