from discord.ext import commands
import json
import aiohttp
import discord

colour = discord.Colour.purple()


def dagpi():
    with open("secrets.json", "r") as f:
        res = json.load(f)
    return res['dagpi_token']


class Images(commands.Cog):
    """Image manipulation commands."""
    
    def __init__(self, client):
        self.client = client
        self.tick = ":GreenTick:707950252434653184"
        self.loading = "https://media1.tenor.com/images/8f7a28e62f8242b264c8a39ba8bea261/tenor.gif?itemid=15922897"
        self.daggy = 491174779278065689
    
    @commands.command()
    async def wanted(self, ctx, *, member: discord.Member = None):
        """
        Wanted...
        """
        daggy = await self.client.fetch_user(self.daggy)
        member = member or ctx.author
        embedd = discord.Embed(
            colour=colour, title="Loading..."
        )
        embedd.set_image(
            url=self.loading)
        message = await ctx.send(embed=embedd)
        data = {'token': dagpi(), 'url': str(member.avatar_url_as(static_format='png'))}
        async with aiohttp.ClientSession() as cs:
            async with cs.post('https://dagpi.tk/api/wanted', headers=data) as r:
                data = await r.json()
        response = data['url']
        embed = discord.Embed(color=colour)
        embed.set_image(url=response)
        embed.set_footer(text=f"Much thanks to {str(daggy)} for this amazing API!", icon_url=daggy.avatar_url)
        await message.edit(embed=embed)
    
    @commands.command()
    async def obama(self, ctx, *, member: discord.Member = None):
        """
        I'm just great.
        """
        daggy = await self.client.fetch_user(self.daggy)
        member = member or ctx.author
        embedd = discord.Embed(
            colour=colour, title="Loading..."
        )
        embedd.set_image(
            url=self.loading)
        message = await ctx.send(embed=embedd)
        data = {'token': dagpi(), 'url': str(member.avatar_url_as(static_format='png'))}
        async with aiohttp.ClientSession() as cs:
            async with cs.post('https://dagpi.tk/api/obamameme', headers=data) as r:
                data = await r.json()
        response = data['url']
        embed = discord.Embed(color=colour)
        embed.set_image(url=response)
        embed.set_footer(text=f"Much thanks to {str(daggy)} for this amazing API!", icon_url=daggy.avatar_url)
        await message.edit(embed=embed)
    
    @commands.command()
    async def bad(self, ctx, *, member: discord.Member = None):
        """
        Bad boy! Bad boy!
        """
        daggy = await self.client.fetch_user(self.daggy)
        member = member or ctx.author
        embedd = discord.Embed(
            colour=colour, title="Loading..."
        )
        embedd.set_image(
            url=self.loading)
        message = await ctx.send(embed=embedd)
        data = {'token': dagpi(), 'url': str(member.avatar_url_as(static_format='png'))}
        async with aiohttp.ClientSession() as cs:
            async with cs.post('https://dagpi.tk/api/bad', headers=data) as r:
                data = await r.json()
        response = data['url']
        embed = discord.Embed(color=colour)
        embed.set_image(url=response)
        embed.set_footer(text=f"Much thanks to {str(daggy)} for this amazing API!", icon_url=daggy.avatar_url)
        await message.edit(embed=embed)
    
    @commands.command()
    async def hitler(self, ctx, *, member: discord.Member = None):
        """
        What a monster
        """
        daggy = await self.client.fetch_user(self.daggy)
        member = member or ctx.author
        embedd = discord.Embed(
            colour=colour, title="Loading..."
        )
        embedd.set_image(
            url=self.loading)
        message = await ctx.send(embed=embedd)
        data = {'token': dagpi(), 'url': str(member.avatar_url_as(static_format='png'))}
        async with aiohttp.ClientSession() as cs:
            async with cs.post('https://dagpi.tk/api/hitler', headers=data) as r:
                data = await r.json()
        response = data['url']
        embed = discord.Embed(color=colour)
        embed.set_image(url=response)
        embed.set_footer(text=f"Much thanks to {str(daggy)} for this amazing API!", icon_url=daggy.avatar_url)
        await message.edit(embed=embed)
    
    @commands.command()
    async def tweet(self, ctx, member: discord.Member, *, tweet: str):
        """
        Yeah i use twitter
        """
        daggy = await self.client.fetch_user(self.daggy)
        member = member or ctx.author
        embedd = discord.Embed(
            colour=colour, title="Loading..."
        )
        embedd.set_image(
            url=self.loading)
        message = await ctx.send(embed=embedd)
        data = {'token': dagpi(), 'url': str(member.avatar_url_as(static_format='png')),
                'text': tweet, 'name': member.display_name}
        async with aiohttp.ClientSession() as cs:
            async with cs.post('https://dagpi.tk/api/tweet', headers=data) as r:
                data = await r.json()
        response = data['url']
        embed = discord.Embed(color=0x00dcff)
        embed.set_image(url=response)
        embed.set_footer(text=f"Much thanks to {str(daggy)} for this amazing API!", icon_url=daggy.avatar_url)
        await message.edit(embed=embed)
    
    @commands.command()
    async def quote(self, ctx, member: discord.Member, *, quote: str):
        """
        'Stop believing internet quotes' - God
        """
        daggy = await self.client.fetch_user(self.daggy)
        member = member or ctx.author
        embedd = discord.Embed(
            colour=colour, title="Loading..."
        )
        embedd.set_image(
            url=self.loading)
        message = await ctx.send(embed=embedd)
        data = {'token': dagpi(), 'url': str(member.avatar_url_as(static_format='png')),
                'text': quote, 'name': member.display_name}
        async with aiohttp.ClientSession() as cs:
            async with cs.post('https://dagpi.tk/api/quote', headers=data) as r:
                data = await r.json()
        response = data['url']
        embed = discord.Embed(color=0x00dcff)
        embed.set_image(url=response)
        embed.set_footer(text=f"Much thanks to {str(daggy)} for this amazing API!", icon_url=daggy.avatar_url)
        await message.edit(embed=embed)
    
    @commands.command()
    async def triggered(self, ctx, *, member: discord.Member = None):
        """
        Brrrr
        """
        daggy = await self.client.fetch_user(self.daggy)
        member = member or ctx.author
        embedd = discord.Embed(
            colour=colour, title="Loading..."
        )
        embedd.set_image(
            url=self.loading)
        message = await ctx.send(embed=embedd)
        data = {'token': dagpi(), 'url': str(member.avatar_url_as(static_format='png'))}
        async with aiohttp.ClientSession() as cs:
            async with cs.post('https://dagpi.tk/api/triggered', headers=data) as r:
                data = await r.json()
        response = data['url']
        embed = discord.Embed(color=0x00dcff)
        embed.set_image(url=response)
        embed.set_footer(text=f"Much thanks to {str(daggy)} for this amazing API!", icon_url=daggy.avatar_url)
        await message.edit(embed=embed)
    
    @commands.command()
    async def gay(self, ctx, *, member: discord.Member = None):
        """
        :rainbow_flag:
        """
        daggy = await self.client.fetch_user(self.daggy)
        member = member or ctx.author
        embedd = discord.Embed(
            colour=colour, title="Loading..."
        )
        embedd.set_image(
            url=self.loading)
        message = await ctx.send(embed=embedd)
        data = {'token': dagpi(), 'url': str(member.avatar_url_as(static_format='png'))}
        async with aiohttp.ClientSession() as cs:
            async with cs.post('https://dagpi.tk/api/gay', headers=data) as r:
                data = await r.json()
        response = data['url']
        embed = discord.Embed(color=colour)
        embed.set_image(url=response)
        embed.set_footer(text=f"Much thanks to {str(daggy)} for this amazing API!", icon_url=daggy.avatar_url)
        await message.edit(embed=embed)
    
    @commands.command()
    async def paint(self, ctx, *, member: discord.Member = None):
        """
        Paint a masterpiece
        """
        daggy = await self.client.fetch_user(self.daggy)
        member = member or ctx.author
        embedd = discord.Embed(
            colour=colour, title="Loading..."
        )
        embedd.set_image(
            url=self.loading)
        message = await ctx.send(embed=embedd)
        data = {'token': dagpi(), 'url': str(member.avatar_url_as(static_format='png'))}
        async with aiohttp.ClientSession() as cs:
            async with cs.post('https://dagpi.tk/api/paint', headers=data) as r:
                data = await r.json()
        response = data['url']
        embed = discord.Embed(color=colour)
        embed.set_image(url=response)
        embed.set_footer(text=f"Much thanks to {str(daggy)} for this amazing API!", icon_url=daggy.avatar_url)
        await message.edit(embed=embed)


def setup(client):
    client.add_cog(Images(client))

