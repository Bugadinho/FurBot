# FurBot by BugadinhoGamers (https://github.com/BugadinhoGamers/FurBot)
# Licensed under GPLv3.0

import discord
from discord.ext import commands

class Hello(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self._last_member = None

    @commands.command()
    async def hello(self, ctx):
        await ctx.send(self.bot.GetLocale(ctx.message.guild, "hello"))

def setup(bot):
    bot.add_cog(Hello(bot))