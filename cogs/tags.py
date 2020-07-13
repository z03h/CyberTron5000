from discord.ext import commands
from .utils import checks, paginator
import discord
import asyncio


class Tags(commands.Cog):
    def __init__(self, client):
        self.client = client
    
    @commands.command()
    async def database(self, arg):
        await arg.send("You're mom")
    
    @commands.group(invoke_without_command=True)
    @checks.betasquad()
    async def tag(self, ctx, *, name):
        tag = await self.client.pg_con.fetch("SELECT content FROM tags WHERE name = $1 AND guild_id = $2", name,
                                             str(ctx.guild.id))
        if not tag:
            await ctx.send("not found")
        else:
            await ctx.send(tag[0][0])
    
    @tag.command()
    @checks.betasquad()
    async def list(self, ctx):
        my_tags = await self.client.pg_con.fetch("SELECT name FROM tags WHERE user_id = $1 and guild_id = $2",
                                                 str(ctx.author.id), str(ctx.guild.id))
        le_tags = []
        for x in range(len(my_tags)):
            le_tags.append(my_tags[x][0])
        embed = discord.Embed(colour=0x00dcff).set_author(name=f'Tags in {ctx.guild} for {ctx.author}',
                                                          icon_url=ctx.author.avatar_url)
        source = paginator.IndexedListSource(le_tags, embed=embed)
        menu = paginator.CatchAllMenu(source=source)
        await menu.start(ctx)
    
    @tag.command(invoke_without_command=True)
    @checks.betasquad()
    async def create(self, ctx, *, contents: str):
        if "|" not in contents:
            return await ctx.send("Incorrect arguments! Please separate your tag name and content with `|`")
        elif contents.startswith("|"):
            return await ctx.send("You didn't define a name for your tag!")
        elif contents.endswith("|"):
            return await ctx.send("You didn't define the content of your tag!")
        else:
            name, content = contents.split("|")
        user_id = str(ctx.author.id)
        guild_id = str(ctx.guild.id)
        tag = await self.client.pg_con.fetch("SELECT * FROM tags WHERE name = $1 AND guild_id = $2", name, guild_id)
        if not tag:
            try:
                await ctx.send(
                    f"```Tag Name: {name}\nContent: {content}```\nIs this correct? [y/n]\nYou have 15 seconds to respond")
                msg = await self.client.wait_for('message', check=lambda m: m.author == ctx.author, timeout=15)
                if msg.content.startswith("y"):
                    await self.client.pg_con.execute(
                        "INSERT INTO tags (user_id, guild_id, name, content) VALUES ($1, $2, $3, $4)", user_id,
                        guild_id, name, content
                    )
                    await ctx.send(f"Success! Tag `{name}` created!")
                else:
                    await ctx.send("Sorry! Try again by using the `{0}tag create` command".format(ctx.prefix))
            except asyncio.TimeoutError:
                await ctx.send("You took too long, try again!")
        else:
            return await ctx.send("This tag already exists in this guild!")
    
    @tag.command()
    async def all_list(self, ctx):
        tags = await self.client.pg_con.fetch("SELECT name, user_id FROM tags WHERE guild_id = $1", str(ctx.guild.id))
        list = []
        for x in range(len(tags)):
            list.append(f"{tags[x][0]} - <@!{tags[x][1]}>")
        final = sorted(list)
        source = paginator.IndexedListSource(final, embed=discord.Embed(colour=self.client.colour).set_author(
            name="All Tags in discord.py", icon_url=ctx.guild.icon_url))
        menu = paginator.CatchAllMenu(source=source)
        await menu.start(ctx)


def setup(client):
    client.add_cog(Tags(client))
