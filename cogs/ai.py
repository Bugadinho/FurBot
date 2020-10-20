# FurBot by BugadinhoGamers (https://github.com/BugadinhoGamers/FurBot)
# Licensed under GPLv3.0

import discord
from chatterbot import ChatBot
from chatterbot.trainers import ListTrainer
from discord.ext import commands

chatbot = ChatBot(
    'FurBot',
    trainer='chatterbot.trainers.ChatterBotCorpusTrainer'
)

class AI(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self._last_member = None

    @commands.command()
    async def chat(self, ctx, *, spoke):
        await ctx.message.channel.send(chatbot.get_response(spoke))

def setup(bot):
    bot.add_cog(AI(bot))