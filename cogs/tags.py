from discord.ext import commands
from .utils import checks, paginator
import discord
import asyncio


class Tags(commands.Cog):
    """Tags are a way of storing data for later retrieval."""
    
    def __init__(self, client):
        self.client = client
    
    @commands.command()
    async def database(self, arg):
        await arg.send("You're mom")
    
    @commands.group(invoke_without_command=True)
    async def tag(self, ctx, *, name):
        """
        Invokes a tag
        """
        tag = await self.client.pg_con.fetch("SELECT content FROM tags WHERE name = $1 AND guild_id = $2", name,
                                             str(ctx.guild.id))
        if not tag:
            await ctx.send("not found")
        else:
            await ctx.send(tag[0][0])
            u = await self.client.pg_con.fetch("SELECT uses FROM tags WHERE name = $1 AND guild_id = $2", name,
                                               str(ctx.guild.id))
            if not u:
                await self.client.pg_con.execute("INSERT INTO tags (uses) VALUES ($1)", 0)
            else:
                u = u[0][0] or 0
                cu = u + 1
                await self.client.pg_con.execute("UPDATE tags SET uses = $1 WHERE name = $2 AND guild_id = $3", cu,
                                                 name, str(ctx.guild.id))
    
    @tag.command()
    async def list(self, ctx, member: discord.Member = None):
        """Lists all the tags that a member owns"""
        member = member or ctx.author
        tags = await self.client.pg_con.fetch("SELECT name, uses FROM tags WHERE guild_id = $1 AND user_id = $2",
                                              str(ctx.guild.id), str(member.id))
        uses = [0 if v[1] is None else v[1] for v in tags]
        names = [v[0] for v in tags]
        f = []
        for x, y in zip(names, uses):
            f.append((x, y))
        l = sorted(f, key=lambda b: b[1])
        final = [f"{a[0]} - {a[1]:,} uses" for a in l]
        source = paginator.IndexedListSource(final[::-1], embed=discord.Embed(colour=self.client.colour).set_author(
            name=f"All of {member}'s tags in {ctx.guild}", icon_url=ctx.guild.icon_url))
        menu = paginator.CatchAllMenu(source=source)
        await menu.start(ctx)
    
    @tag.command(invoke_without_command=True)
    async def create(self, ctx, *, name):
        """Creates a tag"""
        test = await self.client.pg_con.fetch("SELECT * FROM tags WHERE name = $1 AND guild_id = $2", name,
                                              str(ctx.guild.id))
        if test:
            return await ctx.send("This tag already exists in this guild!")
        await ctx.send(
            f"Your tag is called `{name}`. Please enter the content of your tag or type `{ctx.prefix}canel` to cancel.")
        try:
            message = await self.client.wait_for('message', timeout=15, check=lambda m: m.author == ctx.author)
            if message.content.lower().startswith(f"{ctx.prefix}cancel"):
                return await ctx.send("Ok, cancelled.")
        except asyncio.TimeoutError():
            return await ctx.send("You ran out of time!")
        user_id = str(ctx.author.id)
        guild_id = str(ctx.guild.id)
        try:
            await ctx.send(
                f"```Tag Name: {name}\nContent: {message.content}```\nIs this correct? [y/n]\nYou have 15 seconds to respond")
            msg = await self.client.wait_for('message', check=lambda m: m.author == ctx.author, timeout=15)
            if msg.content.lower().startswith("y"):
                await self.client.pg_con.execute(
                    "INSERT INTO tags (user_id, guild_id, name, content) VALUES ($1, $2, $3, $4)", user_id,
                    guild_id, name.strip(), message.content.strip()
                )
                await ctx.send(f"Success! Tag `{name}` created!")
            else:
                await ctx.send("Sorry! Try again by using the `{0}tag create` command".format(ctx.prefix))
        except asyncio.TimeoutError:
            await ctx.send("You took too long, try again!")
    
    @commands.command(aliases=['at', 'all-tags'])
    async def all_tags(self, ctx):
        """Lists all the tags in the guild"""
        tags = await self.client.pg_con.fetch("SELECT name, uses FROM tags WHERE guild_id = $1", str(ctx.guild.id))
        uses = [0 if v[1] is None else v[1] for v in tags]
        names = [v[0] for v in tags]
        f = []
        for x, y in zip(names, uses):
            f.append((x, y))
        l = sorted(f, key=lambda b: b[1])
        final = [f"{a[0]} - {a[1]:,} uses" for a in l]
        source = paginator.IndexedListSource(final[::-1], embed=discord.Embed(colour=self.client.colour).set_author(
            name=f"All Tags in {ctx.guild}", icon_url=ctx.guild.icon_url))
        menu = paginator.CatchAllMenu(source=source)
        await menu.start(ctx)
    
    @tag.command()
    async def edit(self, ctx, *, name):
        """Edits a tag"""
        await ctx.send(
            f"Your tag is called `{name}`. Please enter the content of your tag or type `{ctx.prefix}canel` to cancel.")
        try:
            message = await self.client.wait_for('message', timeout=15, check=lambda m: m.author == ctx.author)
            if message.content.startswith(f"{ctx.prefix}cancel"):
                return await ctx.send("Ok, cancelled.")
        except asyncio.TimeoutError():
            return await ctx.send("You ran out of time!")
        user_id = str(ctx.author.id)
        guild_id = str(ctx.guild.id)
        tag = await self.client.pg_con.fetch("SELECT * FROM tags WHERE name = $1 AND guild_id = $2", name, guild_id)
        if tag[0][0] != user_id:
            return await ctx.send("You do not own this tag!")
        if tag:
            try:
                await ctx.send(
                    f"```Tag Name: {name}\nContent: {message.content}```\nIs this correct? [y/n]\nYou have 15 seconds to respond")
                msg = await self.client.wait_for('message', check=lambda m: m.author == ctx.author, timeout=15)
                if msg.content.startswith("y"):
                    await self.client.pg_con.execute(
                        "UPDATE tags SET content = $1 WHERE name = $2 AND guild_id = $3",
                        message.content.strip(), name, guild_id
                    )
                    await ctx.send(f"Success! Tag `{name}` edited!")
                else:
                    await ctx.send("Sorry! Try again by using the `{0}tag create` command".format(ctx.prefix))
            except asyncio.TimeoutError:
                await ctx.send("You took too long, try again!")
        elif not tag:
            return await ctx.send("That tag doesnt exist!")
    
    @tag.command()
    @commands.is_owner()
    async def info(self, ctx, *, tag):
        tag = await self.client.pg_con.fetch("SELECT * FROM tags WHERE name = $1 AND guild_id = $2", tag,
                                             str(ctx.guild.id))
        if not tag:
            return await ctx.send("That tag was not found for this guild!")
        tags = await self.client.pg_con.fetch("SELECT * FROM tags WHERE guild_id = $1", str(ctx.guild.id))
        this = await self.client.pg_con.fetch("SELECT name, uses FROM tags WHERE guild_id = $1", str(ctx.guild.id))
        uses = [0 if v[1] is None else v[1] for v in this]
        names = [v[0] for v in this]
        f = []
        tup = (tag[0][2], tag[0][4] or 0)
        for x, y in zip(names, uses):
            f.append((x, y))
        s = sorted(f, key=lambda x: x[1])[::-1]
        rank = s.index(tup) + 1
        embed = discord.Embed(title=tag[0][2], colour=self.client.colour)
        owner = await self.client.fetch_user(int(tag[0][0]))
        embed.set_author(name=str(owner), icon_url=owner.avatar_url)
        embed.description = f'\nUses: **{tag[0][4] or 0}**'
        embed.description += f'\nRank: **{rank}**'
        embed.description += f'\nCreated Index: **{tags.index(tag[0]) + 1}**'
        await ctx.send(embed=embed)


def setup(client):
    client.add_cog(Tags(client))
