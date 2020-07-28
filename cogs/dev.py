import ast
import json
import os
import io
import subprocess
import sys
import textwrap
import asyncio
import aiohttp
import inspect

import discord
import praw
from discord.ext import commands

from .utils import cyberformat, checks

tick = "<:tick:733458499777855538>"
null = '<:ticknull:732660186057015317>'
redx = "<:x_:733458444346195990>"
reload = '<:reload:732674920873459712>'


def secrets():
    with open("secrets.json", "r") as f:
        return json.load(f)


class Developer(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.tick = ":tick:733458499777855538"
        self._ = None
    
    @commands.group(aliases=["e", "evaluate"], name='eval', invoke_without_command=True, help="Evaluates a function.")
    @commands.is_owner()
    async def eval_fn(self, ctx, *, cmd):
        global result
        try:
            fn_name = "_eval_expr"
            cmd = cyberformat.codeblock(cmd)
            cmd = cmd.strip("` ")
            cmd = "\n".join(f"    {i}" for i in cmd.splitlines())
            body = f"async def {fn_name}():\n{cmd}"
            parsed = ast.parse(body)
            body = parsed.body[0].body
            checks.insert_returns(body)
            env = {
                'me': ctx.guild.me,
                'bot': ctx.bot,
                'discord': discord,
                'commands': commands,
                'get': discord.utils.get,
                'ctx': ctx,
                'asyncio': asyncio,
                'session': aiohttp.ClientSession(loop=self.client.loop),
                '__import__': __import__,
                'author': ctx.author,
                'guild': ctx.guild,
                'channel': ctx.channel,
                '_': self._,
            }
            try:
                exec(compile(parsed, filename="<ast>", mode="exec"), env)
                result = (await eval(f"{fn_name}()", env))
            except Exception as error:
                return await ctx.send(embed=discord.Embed(color=self.client.colour,
                                                          description=f"{error.__class__.__name__}```py\n{error}\n```"))
        except Exception as error:
            return await ctx.send(embed=discord.Embed(color=self.client.colour,
                                                      description=f"{error.__class__.__name__}```py\n{error}\n```"))
        
        await ctx.message.add_reaction(emoji=self.tick)
        await ctx.send(f'{result}')
        self._ = result
    
    @commands.command()
    @commands.is_owner()
    async def repl(self, ctx):
        """Starts a REPL session"""
        global result
        await ctx.send(embed=discord.Embed(description="```Starting REPL Session```", colour=self.client.colour))
        while True:
            ms = await self.client.wait_for('message', check=lambda m: m.author == ctx.author)
            if ms.content.lower().startswith(f"{ctx.prefix}exit"):
                return await ctx.send(
                    embed=discord.Embed(description="```Exiting REPL Session```", color=self.client.colour))
            try:
                fn_name = "_eval_expr"
                cmd = cyberformat.codeblock(ms.content)
                cmd = cmd.strip("` ")
                cmd = "\n".join(f"    {i}" for i in cmd.splitlines())
                body = f"async def {fn_name}():\n{cmd}"
                parsed = ast.parse(body)
                body = parsed.body[0].body
                checks.insert_returns(body)
                env = {
                    'me': ctx.guild.me,
                    'bot': ctx.bot,
                    'discord': discord,
                    'commands': commands,
                    'get': discord.utils.get,
                    'ctx': ctx,
                    'asyncio': asyncio,
                    'session': aiohttp.ClientSession(),
                    '__import__': __import__,
                    'author': ctx.author,
                    'guild': ctx.guild,
                    'channel': ctx.channel,
                    '_': self._,
                }
                try:
                    exec(compile(parsed, filename="<ast>", mode="exec"), env)
                    result = (await eval(f"{fn_name}()", env))
                except Exception as error:
                    await ctx.send(embed=discord.Embed(color=self.client.colour,
                                                       description=f"{error.__class__.__name__}```py\n{error}\n```"))
                    continue
            except Exception as error:
                await ctx.send(embed=discord.Embed(color=self.client.colour,
                                                   description=f"{error.__class__.__name__}```py\n{error}\n```"))
                continue
            await ctx.send(f'{result}')
            self._ = result
    
    @commands.command(help="Loads Cogs", aliases=['l'])
    @commands.is_owner()
    async def load(self, ctx, *extension):
        if not extension:
            for filename in os.listdir('cogs'):
                if filename.endswith('.py'):
                    self.client.load_extension(f'cogs.{filename[:-3]}')
            
            embed = discord.Embed(
                description="\n".join([f"{tick} `cogs.{f[:-3]}`" for f in os.listdir("cogs") if f.endswith(".py")]),
                colour=self.client.colour)
            await ctx.send(embed=embed)
            await ctx.message.add_reaction(emoji=":tick:733458499777855538")
        
        else:
            cogs = [c[:-3] for c in os.listdir('cogs') if c.endswith(".py")]
            for i in extension:
                if i not in cogs:
                    return await ctx.send(f"**{i}** is not a valid cog!")
            
            for f in extension:
                try:
                    self.client.load_extension(f'cogs.{f}')
                except discord.ext.commands.ExtensionError:
                    pass
            a = []
            for x in cogs:
                if x in extension:
                    a.append(f"{tick} `cogs.{x}`")
                else:
                    a.append(f"{null} `cogs.{x}`")
            
            await ctx.message.add_reaction(emoji=":tick:733458499777855538")
            await ctx.send(embed=discord.Embed(description="\n".join(a), colour=self.client.colour))
    
    @commands.command(help="Unloads Cogs", aliases=['ul'])
    @commands.is_owner()
    async def unload(self, ctx, *extension):
        if not extension:
            for filename in os.listdir('cogs'):
                if filename.endswith('.py'):
                    self.client.unload_extension(f'cogs.{filename[:-3]}')
            
            embed = discord.Embed(
                description="\n".join([f"{redx} `cogs.{f[:-3]}`" for f in os.listdir("cogs") if f.endswith(".py")]),
                colour=self.client.colour)
            await ctx.send(embed=embed)
            await ctx.message.add_reaction(emoji=":tick:733458499777855538")
        
        else:
            cogs = [c[:-3] for c in os.listdir('cogs') if c.endswith(".py")]
            for i in extension:
                if i not in cogs:
                    return await ctx.send(f"**{i}** is not a valid cog!")
            
            for f in extension:
                self.client.unload_extension(f'cogs.{f}')
            a = []
            for x in cogs:
                if x in extension:
                    a.append(f"{redx} `cogs.{x}`")
                else:
                    a.append(f"{null} `cogs.{x}`")
            
            await ctx.message.add_reaction(emoji=":tick:733458499777855538")
            await ctx.send(embed=discord.Embed(description="\n".join(a), colour=self.client.colour))
    
    @commands.command(help="Reloads Cogs", aliases=['rl'])
    @commands.is_owner()
    async def reload(self, ctx, *extension):
        if not extension:
            for filename in os.listdir('cogs'):
                if filename.endswith('.py'):
                    self.client.reload_extension(f'cogs.{filename[:-3]}')
            
            embed = discord.Embed(
                description="\n".join([f"{reload} `cogs.{f[:-3]}`" for f in os.listdir("cogs") if f.endswith(".py")]),
                colour=self.client.colour)
            await ctx.send(embed=embed)
            await ctx.message.add_reaction(emoji=":tick:733458499777855538")
        
        elif len(extension) == 1 and extension[0] == "~":
            cogs = [c[:-3] for c in os.listdir('cogs') if c.endswith(".py")]
            for f in cogs:
                self.client.reload_extension(f'cogs.{f}')
            a = []
            for x in cogs:
                a.append(f"{reload} `cogs.{x}`")
            await ctx.message.add_reaction(emoji=":tick:733458499777855538")
            await ctx.send(embed=discord.Embed(description="\n".join(a), colour=self.client.colour))
        
        else:
            cogs = [c[:-3] for c in os.listdir('cogs') if c.endswith(".py")]
            for i in extension:
                if i not in cogs:
                    return await ctx.send(f"**{i}** is not a valid cog!")
            
            for f in extension:
                self.client.reload_extension(f'cogs.{f}')
            a = []
            for x in cogs:
                if x in extension:
                    a.append(f"{reload} `cogs.{x}`")
                else:
                    a.append(f"{null} `cogs.{x}`")
            
            await ctx.message.add_reaction(emoji=":tick:733458499777855538")
            await ctx.send(embed=discord.Embed(description="\n".join(a), colour=self.client.colour))
    
    @commands.command(help="Logs CyberTron5000 out.")
    @commands.is_owner()
    async def logout(self, ctx):
        await ctx.send(
            embed=discord.Embed(title=f"{self.client.user.name} logging out. Goodbye World! 🌍", color=self.client.colour))
        await self.client.logout()
    
    @commands.command()
    @commands.is_owner()
    async def restart(self, ctx):
        await ctx.message.add_reaction(emoji=self.tick)
        await self.client.logout()
        subprocess.call([sys.executable, "ct5k.py"])
    
    @commands.group(invoke_without_command=True)
    async def news(self, ctx):
        """View the current news."""
        embed = discord.Embed(colour=self.client.colour)
        news = await self.client.pg_con.fetch("SELECT message, number FROM news")
        if not news:
            embed.description = "There is no news currently. Come back soon."
        else:
            embed.description = news[0][0]
            embed.set_author(name=f"News update #{news[0][1]} for {self.client.user.name}",
                             icon_url=self.client.user.avatar_url)
        await ctx.send(embed=embed)
    
    @news.command()
    @commands.is_owner()
    async def update(self, ctx, *, message):
        """Update the current news."""
        number = await self.client.pg_con.fetch("SELECT number FROM news")
        number = number[0][0] or 0
        number += 1
        await self.client.pg_con.execute("UPDATE news SET message = $1, number = $2", message, number)
        await ctx.send(f"News updated to: ```{message}```")


def setup(client):
    client.add_cog(Developer(client))
