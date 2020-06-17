"""

For general bot commands, basic/meta stuff.

"""

import ast
import datetime
import inspect
import json
import os
import subprocess
import sys
import time

import discord
from discord.ext import commands

from .utils.funcs import insert_returns, check_admin_or_owner

start_time = time.time()
colour = 0x00dcff


# ≫


class Bot(commands.Cog):
    """Meta Bot commands"""
    
    def __init__(self, client):
        self.client = client
        self.tick = ":GreenTick:707950252434653184"
        self.version = "CyberTron5000 Alpha v2.0.2"
    
    @commands.command(help="≫ Shows you how long the bot has been up for.")
    async def uptime(self, ctx):
        current_time = time.time()
        difference = int(round(current_time - start_time))
        text = str(datetime.timedelta(seconds=difference))
        e = discord.Embed(color=0x0ff00, title="Bot has been up for:" + f' **{text}**')
        await ctx.send(embed=e)
    
    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        if isinstance(error, discord.ext.commands.CheckFailure):
            await ctx.message.add_reaction(emoji="⚠")
            embed = discord.Embed(color=0xff0000)
            embed.set_author(name=f'{error}')
            await ctx.send(embed=embed)
        if isinstance(error, discord.ext.commands.BadArgument):
            await ctx.message.add_reaction(emoji="⚠")
            embed = discord.Embed(
                color=0xff0000
            )
            embed.set_author(
                name=f"{error}. Check for spelling, capitalization, etc.")
            await ctx.send(embed=embed)
        if isinstance(error, discord.ext.commands.TooManyArguments):
            await ctx.message.add_reaction(emoji="⚠")
            embed = discord.Embed(
                color=0xff0000
            )
            await ctx.send(embed=embed)
        if isinstance(error, discord.ext.commands.MissingRequiredArgument):
            embed = discord.Embed(color=0xFF0000)
            await ctx.message.add_reaction(emoji="⚠")
            embed.set_author(name=f'{error}')
            await ctx.send(embed=embed)
        
        if isinstance(error, discord.ext.commands.BotMissingPermissions):
            embed = discord.Embed(color=0xff0000)
            await ctx.message.add_reaction(emoji="⚠")
            embed.set_author(name=f'{error}')
            await ctx.send(embed=embed)
        
        if isinstance(error, discord.ext.commands.NSFWChannelRequired):
            embed = discord.Embed(color=0xff0000)
            embed.set_author(name=f'{error}')
            await ctx.send(embed=embed)
    
    @commands.command(help="≫ Fetches the bot's invite link.")
    async def invite(self, ctx):
        embed = discord.Embed(
            colour=colour,
            title="Invite me to your server!",
            url="https://discordapp.com/oauth2/authorize?client_id=697678160577429584&permissions=8&scope=bot"
        )
        await ctx.send(embed=embed)
    
    @commands.group(aliases=["e", "evaluate"], name='eval', invoke_without_command=True, help="≫ Evaluates a function.")
    @commands.is_owner()
    async def eval_fn(self, ctx, *, cmd):
        fn_name = "_eval_expr"
        
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
            '__import__': __import__
        }
        exec(compile(parsed, filename="<ast>", mode="exec"), env)
        
        try:
            await ctx.message.add_reaction(emoji=self.tick)
            result = (await eval(f"{fn_name}()", env))
            await ctx.send('{:,.3f}'.format(result))
        except Exception as error:
            await ctx.send('{:,.3f}'.format(error))
    
    @eval_fn.command(aliases=["rtrn", "r"], name='return', invoke_without_command=True,
                     help="≫ Evaluates a function and returns output.")
    @commands.is_owner()
    async def r(self, ctx, *, cmd):
        try:
            fn_name = "_eval_expr"
            
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
                '__import__': __import__
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
    
    @commands.command(help="≫ Checks the bot's ping.")
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
    
    @commands.command(aliases=["sourcecode", "src"], help="≫ Shows source code for a given command")
    async def source(self, ctx, *, command):
        cmd = self.client.get_command(command).callback
        src = inspect.getsource(cmd)
        real_src = str(src).replace("`", "'")
        await ctx.send(f" Showing source for command `{ctx.prefix + command}` (\` have been replaced with ')"
                       f"\n\n```python\n{real_src}\n```")
    
    @commands.group(invoke_without_command=True, help="≫ Shows total lines of code used to make the bot.")
    async def lines(self, ctx):
        global count
        filename1 = "ct5k.py"
        nol = 0
        with open(filename1, 'r') as files:
            for i in files:
                nol += 1
        
        filename2 = "prefixes.json"
        nol2 = 0
        with open(filename2, 'r') as files:
            for i in files:
                nol2 += 1
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
        
        code = nol + count + nol2
        await ctx.send(
            embed=discord.Embed(title="CyberTron5000 was made with {:,.0f} lines of code!".format(code),
                                color=0x00dcff))
    
    @lines.command(invoke_without_command=True, help="≫ Shows total lines in the main file.")
    async def main(self, ctx):
        filename = "ct5k.py"
        nol = 0
        with open(filename, 'r') as files:
            for i in files:
                nol += 1
        
        await ctx.send(
            embed=discord.Embed(title="File {} currently has {:,.0f} lines of code!".format(filename, nol),
                                color=0x00dcff))
    
    @lines.command(invoke_without_command=True, help="≫ Shows total lines in the cogs.")
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
    
    @lines.command(invoke_without_command=True, help="≫ Shows total lines in a single cog.")
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
    
    @lines.command(invoke_without_command=True, help="≫ Shows total lines in miscellaneous files.")
    async def misc(self, ctx):
        try:
            filename2 = "prefixes.json"
            nol2 = 0
            with open(filename2, 'r') as files:
                for i in files:
                    nol2 += 1
            
            await ctx.send(
                embed=discord.Embed(title="Miscellaneous files currently have {:,.0f} lines of code!".format(nol2),
                                    color=0x00dcff))
        except Exception as error:
            await ctx.send(error)
    
    @commands.command(help="≫ Logs CyberTron5000 out.")
    @commands.is_owner()
    async def logout(self, ctx):
        await ctx.send(
            embed=discord.Embed(title=f"{self.client.user.name} logging out. Goodbye World! 🌍", color=0x00dcff))
        await self.client.logout()
    
    @commands.command()
    @commands.is_owner()
    async def restart(self, ctx):
        try:
            await ctx.message.add_reaction(emoji=self.tick)
            await self.client.logout()
            subprocess.call([sys.executable, "ct5k.py"])
        except Exception as error:
            await ctx.send(error)
    
    @commands.command(aliases=['info', 'ab', 'i'], help="≫ Shows info on the bot.")
    async def about(self, ctx):
        try:
            owner = self.client.get_user(350349365937700864)
            global count
            filename1 = "ct5k.py"
            nol = 0
            with open(filename1, 'r') as files:
                for i in files:
                    nol += 1
            
            filename2 = "prefixes.json"
            nol2 = 0
            with open(filename2, 'r') as files:
                for i in files:
                    nol2 += 1
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
            
            code = nol + count + nol2
            embed = discord.Embed(colour=colour, title=f"About {self.client.user.name}",
                                  description=f"[`Invite me to your server!`](https://discord.com/api/oauth2/authorize?client_id=697678160577429584&permissions=2081291511&scope=bot)")
            
            embed.add_field(name="General",
                            value=f"**Guilds**: {len(self.client.guilds)} \n**Members**: {len(self.client.users)}"
                                  f"\n **Emojis**: {len(self.client.emojis)}")
            embed.add_field(name="Bot Info",
                            value=f"**Cogs**: {len(self.client.cogs)} "
                                  f"\n**Commands and Subcommands**: {len(self.client.commands)}\n**Cached Messages**: {len(self.client.cached_messages)}")
            embed.add_field(name=f"\u200b",
                            value=f"About **{round(int(len(self.client.users))/int(len(self.client.guilds)))}** users per guild\n**Lines of Code**: {code:,} | <:dpy:708479036518694983><:python:706850228652998667><:JSON:710927078513442857>\n**Want more info?** [Join the CT5k support server!](https://discord.gg/aa9p43W)",
                            inline=False)
            embed.set_thumbnail(
                url=self.client.user.avatar_url)
            embed.set_footer(text=f"discord.py {discord.__version__} • {self.version}")
            embed.set_author(name=f"Developed by {owner}",
                             icon_url=owner.avatar_url)
            await ctx.send(embed=embed)
        except Exception as error:
            print(error)
    
    @commands.group(aliases=["n", "changenickname", "nick"], invoke_without_command=True,
                    help="≫ Change the bot's nickname to a custom one.")
    @check_admin_or_owner()
    async def nickname(self, ctx, *, nickname):
        name = "({}) {}".format(ctx.prefix, self.client.user.name)
        await ctx.guild.me.edit(nick=f"({ctx.prefix}) {nickname}")
        if name:
            await ctx.message.add_reaction(emoji=self.tick)
        else:
            await ctx.send("Successfully removed nickname")
    
    @nickname.command(invoke_without_command=True, help="≫ Change the bot's nickname back to the default.")
    @check_admin_or_owner()
    async def default(self, ctx):
        await ctx.guild.me.edit(nick=f"({ctx.prefix}) {self.client.user.name}")
        await ctx.message.add_reaction(emoji=self.tick)
    
    @nickname.command(invoke_without_command=True,
                      help="≫ Change the bot's nickname to the default, without the prefix.")
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
                                          description=f'**My prefix for {message.guild} is** `{pre}`\n\n**Do** `{pre}help` **for a full list of commands.**\n\n[Invite me to your server!](https://discord.com/oauth2/authorize?client_id=697678160577429584&permissions=8&scope=bot)\n\n[Join our help server!](https://discord.gg/aa9p43W)')
                    embed.set_thumbnail(url=self.client.user.avatar_url)
                    embed.set_author(name=f"Developed by {owner}", icon_url=owner.avatar_url)
                    await message.channel.send(embed=embed)


def setup(client):
    client.add_cog(Bot(client))
