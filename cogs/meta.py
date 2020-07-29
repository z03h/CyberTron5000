"""

For general bot commands, basic/meta stuff.

"""

import asyncio
import datetime
import json
import os
import platform
import time
from uuid import uuid4
from collections import Counter

import aiohttp
import async_timeout
import discord
import humanize
import psutil
from discord.ext import commands
from tabulate import tabulate as tb

from .utils import cyberformat, paginator
from .utils.checks import check_admin_or_owner, beta_squad
from .utils.lists import sl
import codecs

start_time = datetime.datetime.utcnow()

servers = {
    "CyberTron5000 Emotes 1": "https://discord.gg/29vqZfm",
    "CyberTron5000 Emotes 2": "https://discord.gg/Qn7VYg8",
    "CyberTron5000 Emotes 3": "https://discord.gg/Xgddz6W"
}

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


async def lines_utils():
    """
    Same thing
    """
    global count
    line_count = {}
    directory = "./cogs/utils"
    for filename in os.listdir(directory):
        if filename.endswith(".py"):
            _, ext = os.path.splitext(filename)
            if ext not in line_count:
                line_count[ext] = 0
            for line in open(os.path.join(directory, filename)):
                line_count[ext] += 1
        
        for ext, count in line_count.items():
            pass
    return count


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
        return await lines_main() + count + await lines_utils()
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
        self.version = f"{self.client.user.name} Beta v3.0.0"
        self.softwares = ['<:dpy:708479036518694983>', '<:python:706850228652998667>', '<:JSON:710927078513442857>',
                          '<:psql:733848802334736395>']
            
    @commands.command()
    async def usage(self, ctx):
        data = sorted([[str(key), value] for key, value in self.client.cmd_usage.items()], key=lambda x: x[1], reverse=True)[:10]
        headers = ["Command Name", "Usage"]
        embed = discord.Embed(description=f"```\n{tb(data, headers, tablefmt='fancy_grid')}\n```", color=self.client.colour)
        total = sum([value for key, value in self.client.cmd_usage.items()])
        user = sorted([(key, value) for key, value in self.client.cmd_users.items()], key=lambda x: x[1])[0]
        user = ctx.guild.get_member(user[0]) or await self.client.fetch_user(user[0])
        embed.set_author(name=f"Command Usage Stats")
        embed.description = f"Total commands used since start: **{total}**\nHighest Command User: **{str(user)}**" + embed.description
        await ctx.send(embed=embed)
    
    @commands.command()
    async def uptime(self, ctx):
        delta_uptime = datetime.datetime.utcnow() - start_time
        hours, remainder = divmod(int(delta_uptime.total_seconds()), 3600)
        minutes, seconds = divmod(remainder, 60)
        days, hours = divmod(hours, 24)
        a = f"**{days}** days\n**{hours}** hours\n**{minutes}** minutes\n**{seconds}** seconds"
        await ctx.send(embed=discord.Embed(description=a, colour=self.client.colour).set_author(
            name=f"I have been up for {str(humanize.naturaltime(datetime.datetime.utcnow() - start_time)).split('ago')[0]}"))
    
    @commands.command(help="Checks the bot's ping.")
    async def ping(self, ctx):
        websocket = round(self.client.latency*1000, 3)
        start = time.perf_counter()
        embed = discord.Embed(color=self.client.colour, description=f"**Pong! :ping_pong:**\nWebsocket Latency **{websocket}**")
        message = await ctx.send(embed=embed)
        end = time.perf_counter()
        duration = round((end - start) * 1000, 3)
        embed.description += f"\nResponse Time **{duration}**"
        await message.edit(embed=embed)
    
    @commands.command(aliases=["sourcecode", "src"], help="Shows source code for a given command")
    async def source(self, ctx, *, command=None):
        # inspired by r.danny https://github.com/Rapptz/RoboDanny/blob/rewrite/cogs/meta.py#L328-L366
        u = '\u200b'
        if not command:
            embed = discord.Embed(color=self.client.colour,
                                  title="<:star:737736250718421032> Check out the source code on GitHub!",
                                  url="https://github.com/niztg/CyberTron5000")
            embed.description = "Star the GitHub repository to support the bot!"
            embed.add_field(name="<:license:737733205645590639> LICENSE",
                            value=f"[AGPLv3](https://www.gnu.org/licenses/)")
            embed.set_thumbnail(url=self.client.user.avatar_url)
            embed.set_image(
                url='https://media.discordapp.net/attachments/381963689470984203/737734220755107900/Screen_Shot_2020-07-28_at_2.12.15_PM.png')
            return await ctx.send(embed=embed)
        elif command == "help":
            await ctx.send(embed=discord.Embed(
                description=f"This code was too long for Discord, you can see it instead [on GitHub](https://github.com/niztg/CyberTron5000/blob/master/cogs/info.py#L9-L109)",
                colour=self.client.colour))
        else:
            src = f"```py\n{str(__import__('inspect').getsource(self.client.get_command(command).callback)).replace('```', f'{u}')}```"
            if len(src) > 2000:
                cmd = self.client.get_command(command)
                if not cmd:
                    return await ctx.send("Command not found.")
                file = cmd.callback.__code__.co_filename
                location = os.path.relpath(file)
                total, fl = __import__('inspect').getsourcelines(cmd.callback)
                ll = fl + (len(total) - 1)
                url = f"https://github.com/niztg/CyberTron5000/blob/master/{location}#L{fl}-L{ll}"
                if not cmd.aliases:
                    char = '\u200b'
                else:
                    char = '/'
                embed = discord.Embed(color=self.client.colour,
                                      title=f"<:star:737736250718421032> Sourcecode for command {cmd.name}{char}{'/'.join(cmd.aliases)}",
                                      url=url)
                embed.description = "Star the GitHub repository to support the bot!"
                embed.add_field(name="<:license:737733205645590639> LICENSE",
                                value=f"[AGPLv3](https://www.gnu.org/licenses/)")
                embed.set_thumbnail(url=self.client.user.avatar_url)
                embed.set_image(
                    url='https://media.discordapp.net/attachments/381963689470984203/737734220755107900/Screen_Shot_2020-07-28_at_2.12.15_PM.png')
                await ctx.send(embed=embed)
                
            else:
                await ctx.send(src)
    
    @commands.group(invoke_without_command=True, help="Shows total lines of code used to make the bot.")
    async def lines(self, ctx):
        await ctx.send(
            embed=discord.Embed(
                title="CyberTron5000 was made with {:,.0f} lines of code!".format(await lines_of_code()),
                color=self.client.colour))
    
    @lines.command(invoke_without_command=True, help="Shows total lines in the main file.")
    async def main(self, ctx):
        await ctx.send(
            embed=discord.Embed(title="File ct5k.py currently has {:,.0f} lines of code!".format(await lines_main()),
                                color=self.client.colour))
    
    @lines.command(invoke_without_command=True, help="Shows total lines in the cogs.")
    async def cogs(self, ctx):
        await ctx.send(
            embed=discord.Embed(
                title="Cogs have a total of {:,.0f} lines of code!".format(await lines_of_code() - await lines_main()),
                color=self.client.colour))
    
    @lines.command(invoke_without_command=True, help="Shows total lines in a single cog.")
    async def cog(self, ctx, cog):
        await ctx.send(
            embed=discord.Embed(
                title="{}.py has a total of {:,.0f} lines of code!".format(cog.lower(), await lines_of_code(cog=cog)),
                color=self.client.colour))
    
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
                                    color=self.client.colour))
        except Exception as err:
            await ctx.send(err)
    
    @lines.command()
    async def utils(self, ctx):
        await ctx.send(
            embed=discord.Embed(
                title="Utils have a total of {:,.0f} lines of code!".format(await lines_utils()),
                color=self.client.colour))
    
    async def get_commits(self, limit: int = 3, names: bool = True, author: bool = True):
        async with aiohttp.ClientSession() as cs:
            async with cs.get("https://api.github.com/repos/niztg/CyberTron5000/commits") as r:
                res = await r.json()
            commits = []
            for item in res:
                msg = f"[`{item['sha'][0:7]}`](https://github.com/niztg/CyberTron5000/commit/{item['sha']})"
                if names:
                    msg += f" {item['commit']['message']}"
                if author:
                    msg += f" - {item['commit']['committer']['name']}"
                commits.append(msg)
            return commits[:limit]
    
    @commands.command(aliases=['ab', 'info'])
    async def about(self, ctx):
        """Shows you information regarding the bot"""
        owner = await self.client.fetch_user(350349365937700864)
        delta_uptime = datetime.datetime.utcnow() - start_time
        hours, remainder = divmod(int(delta_uptime.total_seconds()), 3600)
        minutes, seconds = divmod(remainder, 60)
        days, hours = divmod(hours, 24)
        a = f"**{days}** days, **{hours}** hours, **{minutes}** minutes, **{seconds}** seconds"
        vc = tc = cc = 0
        for g in self.client.guilds:
            for c in g.channels:
                if isinstance(c, discord.VoiceChannel):
                    vc += 1
                elif isinstance(c, discord.TextChannel):
                    tc += 1
                elif isinstance(c, discord.CategoryChannel):
                    cc += 1
        news = await self.client.pg_con.fetch("SELECT message, number FROM news")
        embed = discord.Embed(colour=self.client.colour)
        embed.set_author(name=f"About {self.version}", icon_url=self.client.user.avatar_url)
        embed.description = f"→ [Invite](https://cybertron-5k.netlify.app/invite) | [Support](https://cybertron-5k.netlify.app/server) | <:github:724036339426787380> [GitHub](https://github.com/niztg/CyberTron5000) | <:cursor_default:734657467132411914>[Website](https://cybertron-5k.netlify.app) | <:karma:704158558547214426> [Reddit](https://reddit.com/r/CyberTron5000)\n"
        embed.description += f"→ Latest Commits: {'|'.join(await self.get_commits(limit=3, author=False, names=False))}\n"
        embed.description += f"→ Used Memory | {cyberformat.bar(stat=psutil.virtual_memory()[2], max=100, filled='<:loading_filled:730823516059992204>', empty='<:loading_empty:730823515862859897>')}\n→ CPU | {cyberformat.bar(stat=psutil.cpu_percent(), max=100, filled='<:loading_filled:730823516059992204>', empty='<:loading_empty:730823515862859897>')}"
        embed.description += f"\n→ Uptime | {a}"
        embed.description += f"\n**{(await lines_of_code()):,}** lines of code | **{len([f for f in os.listdir('cogs') if f.endswith('.py')]) + 1 + (len([a for a in os.listdir('cogs/utils') if a.endswith('.py')]))}** files\n{self.softwares[0]} {discord.__version__}\n{self.softwares[1]} {platform.python_version()}"
        embed.add_field(name=f"<:news:730866149109137520> News Update #{news[0][1]}", value=news[0][0], inline=False)
        embed.set_footer(
            text=f"Developed by {str(owner)} | Bot created {humanize.naturaltime(datetime.datetime.utcnow() - self.client.user.created_at)}",
            icon_url=owner.avatar_url)
        await ctx.send(embed=embed)
    
    @commands.group(aliases=["n", "changenickname", "nick"], invoke_without_command=True,
                    help="Change the bot's nickname to a custom one.")
    @check_admin_or_owner()
    async def nickname(self, ctx, *, nickname=None):
        if nickname:
            await ctx.guild.me.edit(nick=f"{nickname}")
            await ctx.message.add_reaction(emoji=self.tick)
        else:
            await ctx.guild.me.edit(nick=self.client.user.name)
            await ctx.message.add_reaction(emoji=self.tick)
    
    @nickname.command(invoke_without_command=True, help="Change the bot's nickname back to the default.")
    @check_admin_or_owner()
    async def default(self, ctx):
        await ctx.guild.me.edit(nick=f"{self.client.user.name}")
        await ctx.message.add_reaction(emoji=self.tick)
    
    @nickname.command(invoke_without_command=True, help="Change the bot's nickname to the default, without the prefix.")
    @check_admin_or_owner()
    async def client(self, ctx):
        await ctx.guild.me.edit(nick=self.client.user.name)
        await ctx.message.add_reaction(emoji=self.tick)
    
    @commands.command(name='git_commits', aliases=['gitc', 'commits', 'git'])
    async def _git_commits(self, ctx, limit: int = 5):
        """Shows you recent github commits"""
        if limit < 1 or limit > 15:
            return await ctx.send(
                f"<:warning:727013811571261540> **{ctx.author.name}**, limit must be greater than 0 and less than 16!")
        commits = [f"{index}. {commit}" for index, commit in
                   enumerate(await self.get_commits(limit, author=False, names=True), 1)]
        await ctx.send(embed=discord.Embed(description="\n".join(commits), colour=self.client.colour).set_author(
            name=f"Last {limit} GitHub Commit(s) for CyberTron5000",
            icon_url="https://www.pngjoy.com/pngl/52/1164606_telegram-icon-github-icon-png-white-png-download.png",
            url="https://github.com/niztg/CyberTron5000"))
    
    @commands.group(invoke_without_command=True)
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def suggest(self, ctx, *, idea):
        """Suggest an idea for the bot."""
        tick = "<:tick:733458499777855538>"
        redx = "<:x_:733458444346195990>"
        c = self.client.get_channel(727277234666078220)
        sugid = str(uuid4())[:8]
        embed = discord.Embed(title=f"Suggestion → {sugid}", description=f"```diff\n! {idea}\n```",
                              colour=self.client.colour)
        embed.set_author(name=str(ctx.author), icon_url=ctx.author.avatar_url)
        embed.set_footer(text=f'Do "suggest follow {sugid}" to follow this suggestion!')
        mes = await c.send(embed=embed)
        for r in ['⬆️', '⬇️']:
            await mes.add_reaction(r)
        with open("suggestions.json", "r") as f:
            res = json.load(f)
        res[str(sugid)] = []
        with open("suggestions.json", "w") as f:
            json.dump(res, f, indent=4)
        ms = await ctx.send(
            f"Do you want to follow this suggestion? If you follow it, you will recieve updates on it's status.\nIf you want to unfollow this suggestion, do `{ctx.prefix}suggest unfollow {sugid}`.\n{tick} | **Yes**\n{redx} | **No**\n(You have 15 seconds)")
        await self.client.pg_con.execute("INSERT INTO suggestions (msg_id, suggest_id) VALUES ($1, $2)", mes.id, sugid)
        try:
            async with async_timeout.timeout(15):
                await ms.add_reaction(tick)
                await ms.add_reaction(redx)
                r, u = await self.client.wait_for('reaction_add', timeout=15, check=lambda r, u: u.bot is False)
                if r.emoji.name == "tick":
                    with open("suggestions.json", "r") as f:
                        res = json.load(f)
                    res[str(sugid)].append(ctx.author.id)
                    with open("suggestions.json", "w") as f:
                        json.dump(res, f, indent=4)
                    await ctx.send("Followed suggestion!")
                else:
                    await ctx.send(
                        f"Ok, suggestion not followed. If you ever want to follow it, simply do `{ctx.prefix}suggest follow {sugid}`")
        except asyncio.TimeoutError:
            await ms.edit(
                content=f"You ran out of time! Suggestion not followed. If you want to follow this suggestion, do `{ctx.prefix}suggest follow {sugid}`")
            if ctx.guild.me.permissions_in(ctx.channel).manage_messages:
                await ms.clear_reactions()
    
    @suggest.command()
    async def follow(self, ctx, id: str):
        """Follow a suggestion"""
        try:
            with open("suggestions.json", "r") as f:
                res = json.load(f)
            res[str(id)].append(ctx.author.id)
            with open("suggestions.json", "w") as f:
                json.dump(res, f, indent=4)
            await ctx.send(f"You have successfully followed suggestion `{id}`")
        except KeyError:
            await ctx.send("That suggestion was not found!")
    
    @suggest.command()
    async def unfollow(self, ctx, id: str):
        """Unfollow a suggestion"""
        try:
            with open("suggestions.json", "r") as f:
                res = json.load(f)
            try:
                index = res[str(id)].index(ctx.author.id)
            except (ValueError, KeyError):
                return await ctx.send("That suggestion was not found, or you aren't following it!")
            res[str(id)].pop(index)
            with open("suggestions.json", "w") as f:
                json.dump(res, f, indent=4)
            await ctx.send(f"You have successfully unfollowed suggestion `{id}`")
        except KeyError:
            await ctx.send("That suggestion was not found!")
    
    @suggest.command()
    @commands.is_owner()
    async def resolve(self, ctx, id: str, *, reason):
        data = await self.client.pg_con.fetch("SELECT msg_id FROM suggestions WHERE suggest_id = $1", id)
        if not data:
            return await ctx.send("Not a valid suggestion.")
        msg = await ctx.fetch_message(data[0][0])
        embed = msg.embeds[0]
        embed.add_field(name=f"Reply from {ctx.author}", value=reason)
        await msg.edit(embed=embed)
        with open('suggestions.json', 'r') as f:
            res = json.load(f)
        for i in res[str(id)]:
            a = await self.client.fetch_user(i)
            await a.send(content=f"Suggestion **{id}** has been resolved!", embed=embed)
        res.pop(str(id))
        with open("suggestions.json", "w") as f:
            json.dump(res, f, indent=4)
        await self.client.pg_con.execute("DELETE FROM suggestions WHERE suggest_id = $1", id)
    
    @suggest.command(invoke_without_command=True)
    async def error(self, ctx, *, error):
        """Report an error for this bot."""
        owner = self.client.get_user(id=350349365937700864)
        await owner.send(f"You should fix ```{error}```")
        await ctx.message.add_reaction(emoji=":tick:733458499777855538")

    
    @commands.command(aliases=['stats'])
    async def statistics(self, ctx):
        """Shows you statistics. ([inspired by peanut#7343](https://github.com/spinfish/michael-bot/blob/master/cogs/help.py/#L240-#L279))"""
        cc = coro = func = cls = cmts = 0
        for filename in os.listdir("cogs"):
            if not filename.endswith(".py"):
                continue
            with codecs.open(f"./cogs/{str(filename)}", "r") as f:
                for l in f:
                    l = l.strip()
                    if not len(l):
                        continue
                    if l.startswith('#'):
                        cmts += 1
                    if l.startswith('def'):
                        func += 1
                    if l.startswith('async def'):
                        coro += 1
                    if l.startswith('class'):
                        cls += 1
        for filename in os.listdir("cogs/utils"):
            if not filename.endswith(".py"):
                continue
            with codecs.open(f"./cogs/utils/{str(filename)}", "r") as f:
                for l in f:
                    l = l.strip()
                    if not len(l):
                        continue
                    if l.startswith('#'):
                        cmts += 1
                    if l.startswith('def'):
                        func += 1
                    if l.startswith('async def'):
                        coro += 1
                    if l.startswith('class'):
                        cls += 1
        for g in self.client.guilds:
            for c in g.channels:
                    cc += 1
        embed = discord.Embed(colour=self.client.colour).set_author(name=f"Stats for {self.client.user.name}", icon_url=self.client.user.avatar_url)
        embed.add_field(name="Statistics", value=f"<:class:735360032434290830> Classes | **{cls:,}**\n<:function:735517201561288775> Functions | **{func+coro:,}**\n<:coroutine:735520608183648337> Coroutines | **{coro:,}**\n:speech_balloon: Comments | **{cmts:,}**")
        embed.add_field(name="\u200b", value=f'<:Discord:735530547992068146> Servers | **{len(self.client.guilds)}**\n<:text_channel:703726554018086912> Channels | **{cc:,}**\n<:member:731190477927219231> Members | **{len(self.client.users):,}**\n:gear: Cogs **{len(self.client.cogs)}** | Commands **{len([c for c in self.client.commands])}**')
        embed.set_footer(text=f"{await lines_of_code():,} lines of code")
        await ctx.send(embed=embed)
        
    @commands.command()
    async def credits(self, ctx):
        """The amazing peeps who make ct5k what it is"""
        embed = discord.Embed(colour=self.client.colour)
        embed.set_author(name=f"The People who make {self.client.user.name} what it is today!", icon_url=self.client.user.avatar_url)
        embed.description = f"<@!561688948259422228> - Thank you for drawing {self.client.user.name}'s amazing avatar!\n\n"
        embed.description += f"<@!357918459058978816> - Thank you for helping me in the beginning and teaching me the ropes!\n[His Bot](https://discord.com/oauth2/authorize?client_id=675542011457044512&permissions=1611000896&scope=bot) | [GitHub](https://github.com/DankDumpster) | [Support Server](https://discord.com/invite/TWjxyhC)\n\n"
        embed.description += f"<@!574870314928832533> - Thank you for helping and giving inspiration for many commands on the bot!\n[Their Bot](https://discord.com/oauth2/authorize?client_id=628824408521441291&scope=bot&permissions=1476521159) | [GitHub](https://github.com/spinfish) | [Support Server](https://discord.gg/q3eVHeU)\n\n"
        embed.description += f"<@!491174779278065689> - Thank you for helping a bunch on the bot and inspiring the Images cog!\n[His Bot](https://discord.com/oauth2/authorize?client_id=675589737372975124&permissions=1611000896&scope=bot) | [GitHub](https://github.com/Daggy1234) | [Support Server](https://discord.com/invite/5Y2ryNq)"
        embed.add_field(name="And thanks to the Beta Squad for testing ct5k's beta commands!", value='\n'.join([f'<@{a}>' for a in beta_squad]))
        await ctx.send(embed=embed)
        
    @commands.command()
    async def invite(self, ctx):
        """Invite me to your server!"""
        embed = discord.Embed(color=self.client.colour, title=f"Invite me to your guilds today!", url="https://cybertron-5k.netlify.app/invit")
        embed.add_field(name="Other Links", value=f"[`No Permissions (0)`](https://discord.com/oauth2/authorize?client_id=697678160577429584&scope=bot&permissions=0)\n[`Chose your own permissions`](https://discord.com/api/oauth2/authorize?client_id=697678160577429584&permissions=2147483639&scope=bot)\n[`Administrator Permissions`](https://discord.com/api/oauth2/authorize?client_id=697678160577429584&permissions=8&scope=bot)")
        embed.set_thumbnail(url=self.client.user.avatar_url)
        await ctx.send(embed=embed)
        
    @commands.command()
    async def support(self, ctx):
        """Join our help server!"""
        embed = discord.Embed(colour=self.client.colour, title="Join the Support Server", url="https://cybertron-5k.netlify.app/server")
        embed.description = f"Join the support server to get regular updates on {self.client.user.name}!"
        embed.add_field(name=f"CyberTron5000 Emote Servers", value=f"\n".join([f"[`{key}`]({value})" for key, value in servers.items()]))
        embed.set_footer(text=f"Note: You must be in the main support server to add your bot to the emote servers!")
        embed.set_thumbnail(url=self.client.user.avatar_url)
        await ctx.send(embed=embed)
        
    @commands.command()
    async def github(self, ctx):
        """View the sourcecode for CyberTron5000!"""
        embed = discord.Embed(color=self.client.colour, title="<:star:737736250718421032> Check out the source code on GitHub!", url="https://github.com/niztg/CyberTron5000")
        embed.description = "Star the GitHub repository to support the bot!"
        embed.add_field(name="<:license:737733205645590639> LICENSE", value=f"[AGPLv3](https://www.gnu.org/licenses/)")
        embed.set_thumbnail(url=self.client.user.avatar_url)
        embed.set_image(url='https://media.discordapp.net/attachments/381963689470984203/737734220755107900/Screen_Shot_2020-07-28_at_2.12.15_PM.png')
        await ctx.send(embed=embed)
        
    


def setup(client):
    client.add_cog(Meta(client))
