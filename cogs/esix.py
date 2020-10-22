# FurBot by BugadinhoGamers (https://github.com/BugadinhoGamers/FurBot)
# Licensed under GPLv3.0

import asyncio
import discord
import py621
from discord.ext import commands

class ESix(commands.Cog):
    BlackList = ["bestiality", "pony", "watersports", "gore", "scat", "young", "loli", "my_little_pony", "vore", "friendship_is_magic", "nightmare_fuel"]

    def __init__(self, bot):
        self.bot = bot
        self._last_member = None

    @commands.command()
    async def request(self, ctx, type, *, tags):
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
                    embed=discord.Embed(title=self.bot.GetLocale(ctx.message.guild, "error1"), description=self.bot.GetLocale(ctx.message.guild, "esix_nsfw"), color=0xff0000)
                    return await ctx.message.channel.send(embed=embed)
            else:
                link = "https://e926.net/"
                colormaster = 0x00ff88
                Safe = True
        
            for Tag in tags.split():
                Tags.append(Tag)
        
            for Tag in self.BlackList:
                Tags.append("-" + Tag)

            loop = asyncio.get_event_loop()
            asyncRequest = loop.run_in_executor(None, py621.public.getPosts, Safe, Tags, 1, 1, False)

            #Posts = py621.public.getPosts(Safe, Tags, 1, 1, False)
            Posts = await asyncRequest

            if(len(Posts) == 0):
                embed=discord.Embed(title=self.bot.GetLocale(ctx.message.guild, "error1"), description=self.bot.GetLocale(ctx.message.guild, "esix_nopost"), color=0xff0000)
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
    
    @commands.command()
    async def meme(self, ctx):
        await ctx.invoke(bot.get_command('request'), type='sfw', tags="meme")

def setup(bot):
    bot.add_cog(ESix(bot))
    
    bot.helpCommand.append(["\n<:die:747162817714454570>", "esix_esix", False])
    bot.helpCommand.append([":globe_with_meridians: f-request", "esix_frequest", True])
    bot.helpCommand.append(["<:impressive:744230514994708590> f-meme", "esix_fmeme", True])