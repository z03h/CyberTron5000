"""

For general bot commands, basic/meta stuff.

"""

import ast
import datetime
import json
import os
import subprocess
import sys
import humanize
import time
import praw

import discord
from discord.ext import commands

from .utils.funcs import insert_returns, check_admin_or_owner
from .utils import pyformat as pf

pyf = pf.Discord(bot_user_id=697678160577429584)

def secrets():
    with open("secrets.json", "r") as f:
        return json.load(f)

start_time = datetime.datetime.utcnow()
colour = 0x00dcff


# ≫


class Bot(commands.Cog):
    """Meta Bot commands"""
    
    def __init__(self, client):
        self.client = client
        self.tick = ":GreenTick:707950252434653184"
        self.version = "CyberTron5000 Alpha v2.0.2"
        self.x = "<:warning:727013811571261540>"
        self.x_r = ":warning:727013811571261540"
        self.softwares = ['<:dpy:708479036518694983>', '<:python:706850228652998667>', '<:JSON:710927078513442857>']
    
    @commands.command(help="Shows you how long the bot has been up for.")
    async def uptime(self, ctx):
        delta_uptime = datetime.datetime.utcnow() - start_time
        hours, remainder = divmod(int(delta_uptime.total_seconds()), 3600)
        minutes, seconds = divmod(remainder, 60)
        days, hours = divmod(hours, 24)
        embed = discord.Embed(colour=colour, description=f"I have been up since **{humanize.naturaltime(datetime.datetime.utcnow() - start_time)}!**\n**{days}** days\n**{hours}** hours\n**{minutes}** minutes\n**{seconds}** seconds")
        await ctx.send(embed=embed)

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        if isinstance(error, discord.ext.commands.CheckFailure):
            await ctx.message.add_reaction(emoji=self.x_r)
    
        if isinstance(error, discord.ext.commands.BadArgument):
            err = str(error.args[0]).lower()
            mem, msg = err.split('not')
            await ctx.send(
                f"{self.x} **{ctx.author.name}**, I looked where ever I could, but I couldn't find the **{mem}**anywhere!")
    
        if isinstance(error, discord.ext.commands.MissingRequiredArgument):
            await ctx.send(f"{self.x} **{ctx.author.name}**, you're missing the required argument **{error.param}**!")
    
        if isinstance(error, discord.ext.commands.MissingPermissions):
            await ctx.send(f'{self.x} **{ctx.author.name}**, {error}')

    @commands.command(help="Fetches the bot's invite link.")
    async def invite(self, ctx):
        embed = discord.Embed(
            colour=colour,
            title="Invite me to your server!",
            url="https://discordapp.com/oauth2/authorize?client_id=697678160577429584&permissions=8&scope=bot"
        )
        await ctx.send(embed=embed)

    @commands.group(aliases=["e", "evaluate"], name='eval', invoke_without_command=True, help="Evaluates a function.")
    @commands.is_owner()
    async def eval_fn(self, ctx, *, cmd):
        fn_name = "_eval_expr"
    
        cmd = pyf.codeblock(cmd)
        cmd = cmd.strip("` ")
        cmd = "\n".join(f"    {i}" for i in cmd.splitlines())
    
        body = f"async def {fn_name}():\n{cmd}"
    
        parsed = ast.parse(body)
        body = parsed.body[0].body
    
        insert_returns(body)
    
        env = {
            'client': ctx.bot,
            'discord': discord,
            'commands': commands,
            'ctx': ctx,
            '__import__': __import__,
            'reddit': praw.Reddit(client_id=secrets()['client_id'],
                                  client_secret=secrets()['client_secret'],
                                  username="CyberTron5000",
                                  password=secrets()['password'],
                                  user_agent=secrets()['user_agent'])
        }
        exec(compile(parsed, filename="<ast>", mode="exec"), env)
    
        await ctx.message.add_reaction(emoji=self.tick)
        result = (await eval(f"{fn_name}()", env))
        await ctx.send('{}'.format(result))

    @eval_fn.command(aliases=["rtrn", "r"], name='return', invoke_without_command=True,
                     help="Evaluates a function and returns output.")
    @commands.is_owner()
    async def r(self, ctx, *, cmd):
        try:
            fn_name = "_eval_expr"
        
            cmd = pyf.codeblock(cmd)
            cmd = cmd.strip("` ")
            cmd = "\n".join(f"    {i}" for i in cmd.splitlines())
        
            body = f"async def {fn_name}():\n{cmd}"
        
            parsed = ast.parse(body)
            body = parsed.body[0].body
        
            insert_returns(body)
        
            env = {
                'client': ctx.bot,
                'discord': discord,
                'commands': commands,
                'ctx': ctx,
                '__import__': __import__,
                'reddit': praw.Reddit(client_id=secrets()['client_id'],
                                      client_secret=secrets()['client_secret'],
                                      username="CyberTron5000",
                                      password=secrets()['password'],
                                      user_agent=secrets()['user_agent'])
            }
            exec(compile(parsed, filename="<ast>", mode="exec"), env)
        
            try:
                result = (await eval(f"{fn_name}()", env))
                await ctx.send(f'{result}')
                await ctx.message.add_reaction(emoji=self.tick)
            except Exception as error:
                await ctx.send(f'```python\n{error}\n```')
        except Exception as error:
            await ctx.send(embed=discord.Embed(description=f"\n\n```python\n{error}\n```", color=0x00dcff))
            await ctx.message.add_reaction(emoji="⚠️")

    @commands.command(help="Checks the bot's ping.")
    async def ping(self, ctx):
        start = time.perf_counter()
        message = await ctx.send("** **")
        end = time.perf_counter()
        duration = round((end - start) * 1000, 3)
        embe1d = discord.Embed(
            color=0x00dcff
        )
        embe1d.add_field(name='Pong! :ping_pong:',
                         value='🌐: **{}** ms\n⏱: **{:.3f}** ms'.format(
                             round(self.client.latency * 1000, 3), duration))
        await message.edit(embed=embe1d)
    
    @commands.command(aliases=["sourcecode", "src"], help="Shows source code for a given command")
    async def source(self, ctx, *, command=None):
        i = __import__('inspect')
        if command is None:
            return await ctx.send(embed=discord.Embed(title="Check out the full source code for this bot on GitHub!",
                                                      url="https://github.com/niztg/CyberTron5000/", colour=colour))
        cmd = self.client.get_command(command).callback
        src = str(i.getsource(cmd)).replace("```", "``")
        if len(src) > 2000:
            cmd = self.client.get_command(command).callback
            file = cmd.__code__.co_filename
            location = os.path.relpath(file)
            total, fl = i.getsourcelines(cmd)
            ll = fl + (len(total) - 1)
            await ctx.send(embed=discord.Embed(
                description=f"This code was too long for Discord, you can see it instead [on GitHub](<https://github.com/niztg/CyberTron5000/blob/master/{location}#L{fl}-L{ll}>)",
                colour=colour))
        else:
            await ctx.send(f"```py\n{src}\n```")
    
    @commands.group(invoke_without_command=True, help="Shows total lines of code used to make the bot.")
    async def lines(self, ctx):
        global count
        filename1 = "ct5k.py"
        nol = 0
        with open(filename1, 'r') as files:
            for i in files:
                nol += 1
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
        
        code = nol + count
        await ctx.send(
            embed=discord.Embed(title="CyberTron5000 was made with {:,.0f} lines of code!".format(code),
                                color=0x00dcff))
    
    @lines.command(invoke_without_command=True, help="Shows total lines in the main file.")
    async def main(self, ctx):
        filename = "ct5k.py"
        nol = 0
        with open(filename, 'r') as files:
            for i in files:
                nol += 1
        
        await ctx.send(
            embed=discord.Embed(title="File {} currently has {:,.0f} lines of code!".format(filename, nol),
                                color=0x00dcff))
    
    @lines.command(invoke_without_command=True, help="Shows total lines in the cogs.")
    async def cogs(self, ctx):
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
        
        await ctx.send(
            embed=discord.Embed(title="Cogs have a total of {:,.0f} lines of code!".format(count), color=0x00dcff))
    
    @lines.command(invoke_without_command=True, help="Shows total lines in a single cog.")
    async def cog(self, ctx, cog):
        global count
        line_count = {}
        directory = "./cogs"
        for filename in os.listdir(directory):
            if str(filename) == f"{cog.capitalize()}.py":
                _, ext = os.path.splitext(filename)
                if ext not in line_count:
                    line_count[ext] = 0
                for line in open(os.path.join(directory, filename)):
                    line_count[ext] += 1
            
            for ext, count in line_count.items():
                pass
        
        await ctx.send(
            embed=discord.Embed(title="{}.py has a total of {:,.0f} lines of code!".format(cog.capitalize(), count),
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
    
    @commands.command(help="Logs CyberTron5000 out.")
    @commands.is_owner()
    async def logout(self, ctx):
        await ctx.send(
            embed=discord.Embed(title=f"{self.client.user.name} logging out. Goodbye World! 🌍", color=0x00dcff))
        await self.client.logout()
    
    @commands.command()
    @commands.is_owner()
    async def restart(self, ctx):
        await ctx.message.add_reaction(emoji=self.tick)
        await self.client.logout()
        subprocess.call([sys.executable, "ct5k.py"])
    
    @commands.command(aliases=['info', 'ab', 'i'], help="Shows info on the bot.")
    async def about(self, ctx):
        owner = self.client.get_user(350349365937700864)
        global count
        filename1 = "ct5k.py"
        nol = 0
        with open(filename1, 'r') as files:
            for i in files:
                nol += 1
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
    
        code = nol + count
        embed = discord.Embed(colour=colour, title=f"About {self.client.user.name}",
                              description=f"{self.client.user.name} is a general purpose discord bot, and the best one! This project was started in April, around **{humanize.naturaltime(datetime.datetime.utcnow() - self.client.user.created_at)}**.\n\n• **[Invite me to your server!](https://discord.com/api/oauth2/authorize?client_id=697678160577429584&permissions=2081291511&scope=bot)**\n• **[Join our help server!](https://discord.gg/2fxKxJH)**\n<:github:724036339426787380> **[Support this project on GitHub!](https://github.com/niztg/CyberTron5000)**\n🌐 **[Check out the website!](https://cybertron-5k.netlify.app/index.html)**\n<:reddit:703931951769190410> **[Join the subreddit!](https://www.reddit.com/r/CyberTron5000/)**")
        embed.add_field(name="_Statistics_",
                        value=f"**{len(self.client.users):,}** users, **{len(self.client.guilds):,}** guilds • About **{round(len(self.client.users) / len(self.client.guilds)):,}** users per guild\n**{len(self.client.commands)}** commands, **{len(self.client.cogs)}** cogs • About **{round(len(self.client.commands) / len(self.client.cogs)):,}** commands per cog\n**{code:,}** lines of code • " + '|'.join(
                            self.softwares))
        embed.set_thumbnail(url=self.client.user.avatar_url_as(static_format="png"))
        embed.set_footer(text=f"discord.py {discord.__version__} • {self.version}")
        embed.set_author(name=f"Developed by {owner}", icon_url=owner.avatar_url)
        await ctx.send(embed=embed)
    
    @commands.group(aliases=["n", "changenickname", "nick"], invoke_without_command=True,
                    help="Change the bot's nickname to a custom one.")
    @check_admin_or_owner()
    async def nickname(self, ctx, *, nickname):
        name = "({}) {}".format(ctx.prefix, self.client.user.name)
        await ctx.guild.me.edit(nick=f"({ctx.prefix}) {nickname}")
        if name:
            await ctx.message.add_reaction(emoji=self.tick)
        else:
            await ctx.send("Successfully removed nickname")
    
    @nickname.command(invoke_without_command=True, help="Change the bot's nickname back to the default.")
    @check_admin_or_owner()
    async def default(self, ctx):
        await ctx.guild.me.edit(nick=f"({ctx.prefix}) {self.client.user.name}")
        await ctx.message.add_reaction(emoji=self.tick)
    
    @nickname.command(invoke_without_command=True,
                      help="Change the bot's nickname to the default, without the prefix.")
    @check_admin_or_owner()
    async def client(self, ctx):
        await ctx.guild.me.edit(nick=self.client.user.name)
        await ctx.message.add_reaction(emoji=self.tick)
    
    @commands.Cog.listener(name="on_message")
    async def on_user_mention(self, message):
        owner = self.client.get_user(350349365937700864)
        if "<@!697678160577429584>" == message.content:
            with open("prefixes.json", "r") as f:
                prefix = json.load(f)
                if str(message.guild.id) in prefix:
                    pre = prefix[str(message.guild.id)]
                    embed = discord.Embed(colour=colour,
                                          description=f'**My prefix for {message.guild} is** `{pre}`\n\n**Do** '
                                                      f'`{pre}help` **for a full list of commands.**\n\n'
                                                      f'[Invite me to your server!]'
                                                      f'(https://discord.com/api/oauth2/authorize?client_id=697678160577429584&permissions=2081291511&scope=bot)\n\n[Join our help server!](https://discord.gg/aa9p43W)')
                    embed.set_thumbnail(url=self.client.user.avatar_url)
                    embed.set_author(name=f"Developed by {owner}", icon_url=owner.avatar_url)
                    await message.channel.send(embed=embed)


def setup(client):
    client.add_cog(Bot(client))

#
