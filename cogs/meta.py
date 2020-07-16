"""

For general bot commands, basic/meta stuff.

"""

import datetime
import os
import platform
import time

import aiohttp
import discord
import humanize
import psutil
from discord.ext import commands

from .utils import cyberformat
from .utils.checks import check_admin_or_owner

start_time = datetime.datetime.utcnow()


# ≫

async def lines_main():
    """
    So I only have to do this once
    :return:
    """
    filename1 = "ct5k.py"
    nol = 0
    with open(filename1, 'r') as files:
        for i in files:
            nol += 1
    return nol


async def lines_of_code(cog=None):
    """
    Same thing
    :param cog:
    :return:
    """
    if not cog:
        global count
        line_count = {}
        directory = "./cogs"
        for filename in os.listdir(directory):
            if filename.endswith(".py"):
                _, ext = os.path.splitext(filename)
                if ext not in line_count:
                    line_count[ext] = 0
                for line in open(os.path.join(directory, filename)):
                    line_count[ext] += 1
            
            for ext, count in line_count.items():
                pass
        return await lines_main() + count
    elif cog:
        global counts
        line_count = {}
        directory = "./cogs"
        for filename in os.listdir(directory):
            if str(filename) == f"{cog.lower()}.py":
                _, ext = os.path.splitext(filename)
                if ext not in line_count:
                    line_count[ext] = 0
                for line in open(os.path.join(directory, filename)):
                    line_count[ext] += 1
            
            for ext, counts in line_count.items():
                pass
        return counts


class Meta(commands.Cog):
    """Meta Bot commands"""
    
    def __init__(self, client):
        self.client = client
        self.tick = ":tick:733458499777855538"
        self.version = "CyberTron5000 Alpha v2.5.2"
        self.counter = 0
        self.softwares = ['<:dpy:708479036518694983>', '<:python:706850228652998667>', '<:JSON:710927078513442857>']
    
    @commands.Cog.listener()
    async def on_command_completion(self, ctx):
        self.counter += 1
    
    @commands.command()
    async def uptime(self, ctx):
        delta_uptime = datetime.datetime.utcnow() - start_time
        hours, remainder = divmod(int(delta_uptime.total_seconds()), 3600)
        minutes, seconds = divmod(remainder, 60)
        days, hours = divmod(hours, 24)
        a = f"**{days}** days\n**{hours}** hours\n**{minutes}** minutes\n**{seconds}** seconds"
        await ctx.send(embed=discord.Embed(description=a, colour=self.client.colour).set_author(
            name=f"I have been up for {str(humanize.naturaltime(datetime.datetime.utcnow() - start_time)).split('ago')[0]}"))
    
    @commands.command(help="Fetches the bot's invite link.")
    async def invite(self, ctx):
        embed = discord.Embed(
            colour=self.client.colour,
            title="Invite me to your server!",
            url="https://cybertron-5k.netlify.app/invite"
        )
        await ctx.send(embed=embed)
    
    @commands.command(help="Checks the bot's ping.")
    async def ping(self, ctx):
        start = time.perf_counter()
        message = await ctx.send("** **")
        end = time.perf_counter()
        duration = round((end - start) * 1000, 3)
        await message.edit(
            content=f"```diff\n- Websocket Latency\n{round(self.client.latency * 1000, 3)} ms\n- Response Time\n{duration} ms```")
    
    @commands.command(aliases=["sourcecode", "src"], help="Shows source code for a given command")
    async def source(self, ctx, *, command=None):
        # inspired by r.danny https://github.com/Rapptz/RoboDanny/blob/rewrite/cogs/meta.py#L328-L366
        u = '\u200b'
        if not command:
            return await ctx.send(
                embed=discord.Embed(colour=self.client.colour).set_author(
                    name=f"⭐️ Check out the full sourcecode on GitHub!",
                    url=f"https://github.com/niztg/CyberTron5000",
                    icon_url="https://www.pngjoy.com/pngl/52/1164606_telegram-icon-github-icon-png-white-png-download.png"))
        elif command == "help":
            await ctx.send(embed=discord.Embed(
                description=f"This code was too long for Discord, you can see it instead [on GitHub](https://github.com/niztg/CyberTron5000/blob/master/cogs/info.py#L9-L109)",
                colour=self.client.colour))
        else:
            src = f"```py\n{str(__import__('inspect').getsource(self.client.get_command(command).callback)).replace('```', f'{u}')}```"
            if len(src) > 2000:
                cmd = self.client.get_command(command).callback
                if not cmd:
                    return await ctx.send("Command not found.")
                file = cmd.__code__.co_filename
                location = os.path.relpath(file)
                total, fl = __import__('inspect').getsourcelines(cmd)
                ll = fl + (len(total) - 1)
                await ctx.send(embed=discord.Embed(
                    description=f"This code was too long for Discord, you can see it instead [on GitHub](https://github.com/niztg/CyberTron5000/blob/master/{location}#L{fl}-L{ll})",
                    colour=self.client.colour))
            else:
                await ctx.send(src)
    
    @commands.group(invoke_without_command=True, help="Shows total lines of code used to make the bot.")
    async def lines(self, ctx):
        await ctx.send(
            embed=discord.Embed(
                title="CyberTron5000 was made with {:,.0f} lines of code!".format(await lines_of_code()),
                color=0x00dcff))
    
    @lines.command(invoke_without_command=True, help="Shows total lines in the main file.")
    async def main(self, ctx):
        await ctx.send(
            embed=discord.Embed(title="File ct5k.py currently has {:,.0f} lines of code!".format(await lines_main()),
                                color=0x00dcff))
    
    @lines.command(invoke_without_command=True, help="Shows total lines in the cogs.")
    async def cogs(self, ctx):
        await ctx.send(
            embed=discord.Embed(
                title="Cogs have a total of {:,.0f} lines of code!".format(await lines_of_code() - await lines_main()),
                color=0x00dcff))
    
    @lines.command(invoke_without_command=True, help="Shows total lines in a single cog.")
    async def cog(self, ctx, cog):
        await ctx.send(
            embed=discord.Embed(
                title="{}.py has a total of {:,.0f} lines of code!".format(cog.lower(), await lines_of_code(cog=cog)),
                color=0x00dcff))
    
    @lines.command(aliases=['cmd'], invoke_without_command=True)
    async def command(self, ctx, *, command):
        """Lines for a specific command"""
        try:
            cmd = self.client.get_command(command)
            src_cmd = cmd.callback
            total, fl = __import__('inspect').getsourcelines(src_cmd)
            ll = fl + (len(total) - 1)
            await ctx.send(
                embed=discord.Embed(title="{} command has a total of {:,.0f} lines of code!".format(cmd.name, ll - fl),
                                    color=0x00dcff))
        except Exception as err:
            await ctx.send(err)
    
    async def get_commits(self, limit: int = 3):
        async with aiohttp.ClientSession() as cs:
            async with cs.get("https://api.github.com/repos/niztg/CyberTron5000/commits") as r:
                res = await r.json()
            commits = [
                f"[`{item['sha'][0:7]}`](https://github.com/niztg/CyberTron5000/commit/{item['sha']}) {item['commit']['message']} - {item['commit']['committer']['name']}"
                for item in res]
            return commits[:limit]
    
    @commands.command(aliases=['info', 'ab', 'i'], help="Shows info on the bot.")
    async def about(self, ctx):
        delta_uptime = datetime.datetime.utcnow() - start_time
        hours, remainder = divmod(int(delta_uptime.total_seconds()), 3600)
        minutes, seconds = divmod(remainder, 60)
        days, hours = divmod(hours, 24)
        a = f"**{days}** days, **{hours}** hours, **{minutes}** minutes, **{seconds}** seconds"
        owner = await self.client.fetch_user(350349365937700864)
        embed = discord.Embed(colour=self.client.colour, title=f"About {self.client.user.name}",
                              description=f"{self.client.user.name} is a general purpose discord bot, and the best one! This project was started in April, around **{humanize.naturaltime(datetime.datetime.utcnow() - self.client.user.created_at)}**.\n\n• **[Invite me to your server!](https://cybertron-5k.netlify.app/invite)**\n• **[Join our help server!](https://discord.gg/2fxKxJH)**\n<:github:724036339426787380> **[Support this project on GitHub!](https://github.com/niztg/CyberTron5000)**\n🌐 **[Check out the website!](https://cybertron-5k.netlify.app/index.html)**\n<:reddit:703931951769190410> **[Join the subreddit!](https://www.reddit.com/r/CyberTron5000/)**\n\nCommands used since start: **{self.counter}** (cc <@!574870314928832533>)\nUptime: {a}\nUsed Memory: {cyberformat.bar(stat=psutil.virtual_memory()[2], max=100, filled='<:loading_filled:730823516059992204>', empty='<:loading_empty:730823515862859897>')}\nCPU: {cyberformat.bar(stat=psutil.cpu_percent(), max=100, filled='<:loading_filled:730823516059992204>', empty='<:loading_empty:730823515862859897>')}\n")
        embed.add_field(name="_Statistics_",
                        value=f"**{len(self.client.users):,}** users, **{len(self.client.guilds):,}** guilds • About **{round(len(self.client.users) / len(self.client.guilds)):,}** users per guild\n**{len(self.client.commands)}** commands, **{len(self.client.cogs)}** cogs • About **{round(len(self.client.commands) / len(self.client.cogs)):,}** commands per cog\n**{await lines_of_code():,}** lines of code • " + '|'.join(
                            self.softwares) + f"\ndiscord.py {discord.__version__} | Python {platform.python_version()}")
        embed.set_thumbnail(url=self.client.user.avatar_url_as(static_format="png"))
        embed.add_field(name="_Latest Commits_", value="\n".join(await self.get_commits()), inline=False)
        embed.set_footer(text=self.version)
        embed.set_author(name=f"Developed by {owner}", icon_url=owner.avatar_url)
        await ctx.send(embed=embed)
    
    @commands.group(aliases=["n", "changenickname", "nick"], invoke_without_command=True,
                    help="Change the bot's nickname to a custom one.")
    @check_admin_or_owner()
    async def nickname(self, ctx, *, nickname=None):
        if nickname:
            await ctx.guild.me.edit(nick=f"({ctx.prefix}) {nickname}")
            await ctx.message.add_reaction(emoji=self.tick)
        else:
            await ctx.guild.me.edit(nick=self.client.user.name)
            await ctx.message.add_reaction(emoji=self.tick)
    
    @nickname.command(invoke_without_command=True, help="Change the bot's nickname back to the default.")
    @check_admin_or_owner()
    async def default(self, ctx):
        await ctx.guild.me.edit(nick=f"({ctx.prefix}) {self.client.user.name}")
        await ctx.message.add_reaction(emoji=self.tick)
    
    @nickname.command(invoke_without_command=True, help="Change the bot's nickname to the default, without the prefix.")
    @check_admin_or_owner()
    async def client(self, ctx):
        await ctx.guild.me.edit(nick=self.client.user.name)
        await ctx.message.add_reaction(emoji=self.tick)
    
    @commands.command(aliases=['commits', 'git'])
    async def github(self, ctx, limit: int = 5):
        """Shows you recent github commits"""
        if limit < 1 or limit > 15:
            return await ctx.send(
                f"<:warning:727013811571261540> **{ctx.author.name}**, limit must be greater than 0 and less than 16!")
        commits = [f"{index}. {commit}" for index, commit in enumerate(await self.get_commits(limit), 1)]
        await ctx.send(embed=discord.Embed(description="\n".join(commits), colour=self.client.colour).set_author(
            name=f"Last {limit} GitHub Commit(s) for CyberTron5000",
            icon_url="https://www.pngjoy.com/pngl/52/1164606_telegram-icon-github-icon-png-white-png-download.png",
            url="https://github.com/niztg/CyberTron5000"))
    
    @commands.group(invoke_without_command=True)
    async def suggest(self, ctx, *, idea):
        """Suggest an idea for the bot."""
        owner = self.client.get_user(id=350349365937700864)
        await owner.send(f"Idea: ```{idea}```")
        await ctx.message.add_reaction(emoji=":tick:733458499777855538")
    
    @suggest.command(invoke_without_command=True)
    async def error(self, ctx, *, error):
        """Report an error for this bot."""
        owner = self.client.get_user(id=350349365937700864)
        await owner.send(f"You should fix ```{error}```")
        await ctx.message.add_reaction(emoji=":tick:733458499777855538")


def setup(client):
    client.add_cog(Meta(client))
