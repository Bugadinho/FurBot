# FurBot by BugadinhoGamers (https://github.com/BugadinhoGamers/FurBot)
# Licensed under GPLv3.0

import discord
import asyncio
from chatterbot import ChatBot
from chatterbot.trainers import ListTrainer
from chatterbot.trainers import ChatterBotCorpusTrainer
from discord.ext import commands

class AI(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self._last_member = None

        self.chatbot = ChatBot(
            self.bot.name,
            trainer='chatterbot.trainers.ChatterBotCorpusTrainer'
        )

    @commands.command()
    async def chat(self, ctx, *, spoke):
        await ctx.message.channel.send(await asyncio.get_event_loop().run_in_executor(None, self.chatbot.get_response, spoke))
    
    @commands.command()
    async def train(self, ctx, corpus):
        if (ctx.message.author.id not in self.bot.json["maintainers"]):
            embed=discord.Embed(title=self.bot.GetLocale(ctx.message.guild, "error1"), description=self.bot.GetLocale(ctx.message.guild, "error4"), color=0xff0000)
            return await ctx.message.channel.send(embed=embed)
        
        trainer = ChatterBotCorpusTrainer(self.chatbot)

        trainer.train(
            corpus
        )

def setup(bot):
    bot.add_cog(AI(bot))

    bot.helpCommand.append(["\n:computer:", "ai_ai", False])
    bot.helpCommand.append([":speech_left: f-chat", "ai_fchat", True])