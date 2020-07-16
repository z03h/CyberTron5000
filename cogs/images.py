import json

import aiohttp
import discord
from discord.ext import commands


def dagpi():
    with open("secrets.json", "r") as f:
        res = json.load(f)
    return res['dagpi_token']


class Images(commands.Cog):
    """these are not working for the time being"""
    
    def __init__(self, client):
        self.client = client
        self.tick = ":tick:733458499777855538"
        self.daggy = 491174779278065689
    
    @commands.command()
    async def wanted(self, ctx, *, member: discord.Member = None):
        """
        Wanted...
        """
        daggy = await self.client.fetch_user(self.daggy)
        member = member or ctx.author
        async with ctx.typing():
            resp = {'token': dagpi(), 'url': str(member.avatar_url_as(static_format='png'))}
            async with aiohttp.ClientSession() as cs:
                async with cs.post('https://dagpi.tk/api/wanted', headers=resp) as r:
                    resp = await r.json()
            res = resp['url']
            embed = discord.Embed(colour=self.client.colour)
            embed.set_image(url=res)
            embed.set_footer(text=f"Much thanks to {str(daggy)} for this amazing API!", icon_url=daggy.avatar_url)
            await ctx.send(embed=embed)
    
    @commands.command()
    async def obama(self, ctx, *, member: discord.Member = None):
        """
        I'm just great.
        """
        daggy = await self.client.fetch_user(self.daggy)
        member = member or ctx.author
        async with ctx.typing():
            resp = {'token': dagpi(), 'url': str(member.avatar_url_as(static_format='png'))}
            async with aiohttp.ClientSession() as cs:
                async with cs.post('https://dagpi.tk/api/obamameme', headers=resp) as r:
                    resp = await r.json()
            res = resp['url']
            embed = discord.Embed(colour=self.client.colour)
            embed.set_image(url=res)
            embed.set_footer(text=f"Much thanks to {str(daggy)} for this amazing API!", icon_url=daggy.avatar_url)
            await ctx.send(embed=embed)
    
    @commands.command()
    async def bad(self, ctx, *, member: discord.Member = None):
        """
        Bad boy! Bad boy!
        """
        daggy = await self.client.fetch_user(self.daggy)
        member = member or ctx.author
        async with ctx.typing():
            resp = {'token': dagpi(), 'url': str(member.avatar_url_as(static_format='png'))}
            async with aiohttp.ClientSession() as cs:
                async with cs.post('https://dagpi.tk/api/bad', headers=resp) as r:
                    resp = await r.json()
            res = resp['url']
            embed = discord.Embed(colour=self.client.colour)
            embed.set_image(url=res)
            embed.set_footer(text=f"Much thanks to {str(daggy)} for this amazing API!", icon_url=daggy.avatar_url)
            await ctx.send(embed=embed)
    
    @commands.command()
    async def hitler(self, ctx, *, member: discord.Member = None):
        """
        What a monster
        """
        member = member or ctx.author
        daggy = await self.client.fetch_user(self.daggy)
        async with ctx.typing():
            resp = {'token': dagpi(), 'url': str(member.avatar_url_as(static_format='png'))}
            async with aiohttp.ClientSession() as cs:
                async with cs.post('https://dagpi.tk/api/hitler', headers=resp) as r:
                    resp = await r.json()
            res = resp['url']
            embed = discord.Embed(colour=self.client.colour)
            embed.set_image(url=res)
            embed.set_footer(text=f"Much thanks to {str(daggy)} for this amazing API!", icon_url=daggy.avatar_url)
            await ctx.send(embed=embed)
    
    @commands.command()
    async def tweet(self, ctx, member: discord.Member, *, tweet: str):
        """
        Yeah i use twitter
        """
        daggy = await self.client.fetch_user(self.daggy)
        member = member or ctx.author
        async with ctx.typing():
            resp = {'token': dagpi(), 'url': str(member.avatar_url_as(static_format='png')),
                    'text': tweet, 'name': member.display_name}
            async with aiohttp.ClientSession() as cs:
                async with cs.post('https://dagpi.tk/api/tweet', headers=resp) as r:
                    resp = await r.json()
            res = resp['url']
            embed = discord.Embed(colour=self.client.colour)
            embed.set_image(url=res)
            embed.set_footer(text=f"Much thanks to {str(daggy)} for this amazing API!", icon_url=daggy.avatar_url)
            await ctx.send(embed=embed)
    
    @commands.command()
    async def quote(self, ctx, member: discord.Member, *, quote: str):
        """
        'Stop believing internet quotes' - God
        """
        daggy = await self.client.fetch_user(self.daggy)
        member = member or ctx.author
        async with ctx.typing():
            resp = {'token': dagpi(), 'url': str(member.avatar_url_as(static_format='png')),
                    'text': quote, 'name': member.display_name}
            async with aiohttp.ClientSession() as cs:
                async with cs.post('https://dagpi.tk/api/quote', headers=resp) as r:
                    resp = await r.json()
            res = resp['url']
            embed = discord.Embed(colour=self.client.colour)
            embed.set_image(url=res)
            embed.set_footer(text=f"Much thanks to {str(daggy)} for this amazing API!", icon_url=daggy.avatar_url)
            await ctx.send(embed=embed)
    
    @commands.command()
    async def triggered(self, ctx, *, member: discord.Member = None):
        """
        Brrrr
        """
        daggy = await self.client.fetch_user(self.daggy)
        member = member or ctx.author
        async with ctx.typing():
            resp = {'token': dagpi(), 'url': str(member.avatar_url_as(static_format='png'))}
            async with aiohttp.ClientSession() as cs:
                async with cs.post('https://dagpi.tk/api/triggered', headers=resp) as r:
                    resp = await r.json()
            res = resp['url']
            embed = discord.Embed(colour=self.client.colour)
            embed.set_image(url=res)
            embed.set_footer(text=f"Much thanks to {str(daggy)} for this amazing API!", icon_url=daggy.avatar_url)
            await ctx.send(embed=embed)
    
    @commands.command()
    async def gay(self, ctx, *, member: discord.Member = None):
        """
        :rainbow_flag:
        """
        daggy = await self.client.fetch_user(self.daggy)
        member = member or ctx.author
        async with ctx.typing():
            resp = {'token': dagpi(), 'url': str(member.avatar_url_as(static_format='png'))}
            async with aiohttp.ClientSession() as cs:
                async with cs.post('https://dagpi.tk/api/gay', headers=resp) as r:
                    resp = await r.json()
            res = resp['url']
            embed = discord.Embed(colour=self.client.colour)
            embed.set_image(url=res)
            embed.set_footer(text=f"Much thanks to {str(daggy)} for this amazing API!", icon_url=daggy.avatar_url)
            await ctx.send(embed=embed)
    
    @commands.command()
    async def paint(self, ctx, *, member: discord.Member = None):
        """
        Paint a masterpiece
        """
        daggy = await self.client.fetch_user(self.daggy)
        member = member or ctx.author
        async with ctx.typing():
            resp = {'token': dagpi(), 'url': str(member.avatar_url_as(static_format='png'))}
            async with aiohttp.ClientSession() as cs:
                async with cs.post('https://dagpi.tk/api/paint', headers=resp) as r:
                    resp = await r.json()
            res = resp['url']
            embed = discord.Embed(colour=self.client.colour)
            embed.set_image(url=res)
            embed.set_footer(text=f"Much thanks to {str(daggy)} for this amazing API!", icon_url=daggy.avatar_url)
            await ctx.send(embed=embed)


def setup(client):
    client.add_cog(Images(client))
