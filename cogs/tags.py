import asyncio

import discord
from discord.ext import commands

from .utils import paginator
from .utils.lists import engineer_bagdes, legend_badges, popular_badges


class Tags(commands.Cog):
    """Tags are a way of storing data for later retrieval."""
    
    def __init__(self, client):
        self.client = client
    
    @commands.command()
    async def database(self, arg):
        await arg.send("You're mom")
    
    @commands.group(invoke_without_command=True)
    async def tag(self, ctx, *, name=None):
        """
        Invokes a tag
        """
        if not name:
            final = [f"`{ctx.prefix}{ctx.command} {c.name} {c.signature}` • {c.help or 'No help provided'}" for c in
                     ctx.command.commands]
            final.append(f"`{ctx.prefix}all_tags` • Shows you all the tags in the guild")
            source = paginator.IndexedListSource(embed=discord.Embed(color=self.client.colour, title="Tag Commands"),
                                                 data=final)
            return await paginator.CatchAllMenu(source=source).start(ctx)
        tag = await self.client.pg_con.fetch("SELECT content, uses FROM tags WHERE name = $1 AND guild_id = $2", name,
                                             str(ctx.guild.id))
        if not tag:
            await ctx.send("not found")
        else:
            await ctx.send(tag[0][0])
            await self.client.pg_con.execute("UPDATE tags SET uses = $1 WHERE name = $2 AND guild_id = $3", (tag[0][1] or 0)+1,
                                             name, str(ctx.guild.id))
            #u = await self.client.pg_con.fetch("SELECT uses FROM tags WHERE name = $1 AND guild_id = $2", name,
            #                                   str(ctx.guild.id))
            #if not u:
            #    await self.client.pg_con.execute("INSERT INTO tags (uses) VALUES ($1)", 0)
            #else:
            #    u = u[0][0] or 0
            #    cu = u + 1
            #    await self.client.pg_con.execute("UPDATE tags SET uses = $1 WHERE name = $2 AND guild_id = $3", cu,
            #                                    name, str(ctx.guild.id))
    
    @tag.command()
    async def list(self, ctx, member: discord.Member = None):
        """Lists all the tags that a member owns"""
        member = member or ctx.author
        tags = await self.client.pg_con.fetch("SELECT name, uses FROM tags WHERE guild_id = $1 AND user_id = $2",
                                              str(ctx.guild.id), str(member.id))
        f = [(v[0], v[1] or 0) for v in tags]
        l = sorted(f, key=lambda b: b[1])
        final = [f"{a[0]} - {a[1]:,} uses" for a in l]
        source = paginator.IndexedListSource(final[::-1], embed=discord.Embed(colour=self.client.colour).set_author(
            name=f"All of {member}'s tags in {ctx.guild} (Total {len(final)})", icon_url=ctx.guild.icon_url))
        menu = paginator.CatchAllMenu(source=source)
        await menu.start(ctx)
    
    @commands.command()
    async def tags(self, ctx, member: discord.Member = None):
        """Lists all the tags that a member owns"""
        member = member or ctx.author
        tags = await self.client.pg_con.fetch("SELECT name, uses FROM tags WHERE guild_id = $1 AND user_id = $2",
                                              str(ctx.guild.id), str(member.id))
        f = [(v[0], v[1] or 0) for v in tags]
        l = sorted(f, key=lambda b: b[1])
        final = [f"{a[0]} - {a[1]:,} uses" for a in l]
        source = paginator.IndexedListSource(final[::-1], embed=discord.Embed(colour=self.client.colour).set_author(
            name=f"All of {member}'s tags in {ctx.guild} (Total {len(final)})", icon_url=ctx.guild.icon_url))
        menu = paginator.CatchAllMenu(source=source)
        await menu.start(ctx)
    
    @tag.command(invoke_without_command=True, aliases=['make'])
    @commands.cooldown(1, 30, commands.BucketType.user)
    async def create(self, ctx, *, name):
        """Creates a tag"""
        if len(name) > 100:
            return await ctx.send("That name is too long!")
        test = await self.client.pg_con.fetch("SELECT * FROM tags WHERE name = $1 AND guild_id = $2", name,
                                              str(ctx.guild.id))
        if test:
            return await ctx.send("This tag already exists in this guild!")
        await ctx.send(
            f"Your tag is called `{name}`. Please enter the content of your tag or type `{ctx.prefix}cancel` to cancel.")
        try:
            message = await self.client.wait_for('message', timeout=30, check=lambda m: m.author == ctx.author)
            if message.content.lower().startswith(f"{ctx.prefix}cancel"):
                return await ctx.send("Ok, cancelled.")
            user_id = str(ctx.author.id)
            guild_id = str(ctx.guild.id)
            try:
                await ctx.send(
                    f"```Tag Name: {name}\nContent: {message.content}```\nIs this correct? [y/n]\nYou have 15 seconds to respond")
                msg = await self.client.wait_for('message', check=lambda m: m.author == ctx.author, timeout=15)
                if msg.content.lower().startswith("y"):
                    await self.client.pg_con.execute(
                        "INSERT INTO tags (user_id, guild_id, name, content, uses) VALUES ($1, $2, $3, $4, $5)", user_id,
                        guild_id, name.strip(), message.content.strip(), 0
                    )
                    await ctx.send(f"Success! Tag `{name}` created!")
                else:
                    await ctx.send("Sorry! Try again by using the `{0}tag create` command".format(ctx.prefix))
            except asyncio.TimeoutError():
                return await ctx.send("You ran out of time!")
        except asyncio.TimeoutError:
            await ctx.send("You took too long, try again!")
    
    @commands.command(aliases=['at', 'all-tags'])
    async def all_tags(self, ctx):
        """Lists all the tags in the guild"""
        tags = await self.client.pg_con.fetch("SELECT name, uses FROM tags WHERE guild_id = $1", str(ctx.guild.id))
        f = [(v[0], v[1] or 0) for v in tags]
        l = sorted(f, key=lambda b: b[1])
        final = [f"{a[0]} - {a[1]:,} uses" for a in l]
        source = paginator.IndexedListSource(final[::-1], embed=discord.Embed(colour=self.client.colour).set_author(
            name=f"All Tags in {ctx.guild} (Total {len(f)})", icon_url=ctx.guild.icon_url))
        menu = paginator.CatchAllMenu(source=source)
        await menu.start(ctx)
    
    @tag.command()
    async def edit(self, ctx, *, name):
        """Edits a tag"""
        user_id = str(ctx.author.id)
        guild_id = str(ctx.guild.id)
        tag = await self.client.pg_con.fetch("SELECT * FROM tags WHERE name = $1 AND guild_id = $2", name, guild_id)
        if not tag:
            return await ctx.send("That tag doesnt exist!")
        if tag[0][0] != user_id:
            return await ctx.send("You do not own this tag!")
        await ctx.send(
            f"Your tag is called `{name}`. Please enter the content of your tag or type `{ctx.prefix}cancel` to cancel.")
        try:
            message = await self.client.wait_for('message', timeout=15, check=lambda m: m.author == ctx.author)
            if message.content.startswith(f"{ctx.prefix}cancel"):
                return await ctx.send("Ok, cancelled.")
        except asyncio.TimeoutError():
            return await ctx.send("You ran out of time!")
        if tag:
            try:
                await ctx.send(
                    f"```Tag Name: {name}\nContent: {message.content}```\nIs this correct? [y/n]\nYou have 15 seconds to respond")
                msg = await self.client.wait_for('message', check=lambda m: m.author == ctx.author, timeout=30)
                if msg.content.lower().startswith("y"):
                    await self.client.pg_con.execute(
                        "UPDATE tags SET content = $1 WHERE name = $2 AND guild_id = $3",
                        message.content.strip(), name, guild_id
                    )
                    await ctx.send(f"Success! Tag `{name}` edited!")
                else:
                    await ctx.send("Sorry! Try again by using the `{0}tag edit` command".format(ctx.prefix))
            except asyncio.TimeoutError:
                await ctx.send("You took too long, try again!")
        elif not tag:
            return await ctx.send("That tag doesnt exist!")
    
    @tag.command()
    async def info(self, ctx, *, tag):
        """Shows you info about a tag"""
        tag = await self.client.pg_con.fetch("SELECT * FROM tags WHERE name = $1 AND guild_id = $2", tag,
                                             str(ctx.guild.id))
        if not tag:
            return await ctx.send("That tag was not found for this guild!")
        this = await self.client.pg_con.fetch("SELECT name, uses FROM tags WHERE guild_id = $1", str(ctx.guild.id))
        f = [(v[0], v[1] or 0) for v in this]
        tup = (tag[0][2], tag[0][4] or 0)
        s = sorted(f, key=lambda x: x[1])[::-1]
        rank = s.index(tup) + 1
        embed = discord.Embed(title=tag[0][2], colour=self.client.colour)
        owner = self.client.get_user(int(tag[0][0])) or await self.client.fetch_user(int(tag[0][0]))
        embed.set_author(name=str(owner), icon_url=owner.avatar_url)
        embed.description = f'\nUses: **{tag[0][4] or 0}**'
        embed.description += f'\nRank: **{rank}**'
        embed.description += f'\nCreated Index: **{f.index(tup) + 1}**'
        await ctx.send(embed=embed)
    
    async def get_user_badges(self, ctx, member: discord.Member):
        num_tags = await self.client.pg_con.fetch("SELECT * FROM tags WHERE user_id = $1 AND guild_id = $2",
                                                  str(member.id), str(ctx.guild.id))
        if not num_tags:
            return ''
        if len(num_tags) < 10:
            et = []
        elif 10 <= len(num_tags) <= 25:
            et = engineer_bagdes[:1]
        elif 26 <= len(num_tags) <= 50:
            et = engineer_bagdes[:2]
        elif 51 <= len(num_tags) <= 250:
            et = engineer_bagdes[:2]
        else:
            et = engineer_bagdes
        uses = [(r.get('uses') for r in num_tags)]
        #uses = await self.client.pg_con.fetch("SELECT uses FROM tags WHERE user_id = $1 AND guild_id = $2",
        #                                      str(member.id), str(ctx.guild.id))
        il = sorted([v[0] or 0 for v in uses])[::-1][0]
        if il < 10:
            pt = []
        elif 10 <= il <= 25:
            pt = popular_badges[:1]
        elif 26 <= il <= 50:
            pt = popular_badges[:2]
        elif 51 <= il <= 250:
            pt = popular_badges[:3]
        else:
            pt = popular_badges
        this = [(r.get('name'), r.get('uses')) for r in num_tags]
        #this = await self.client.pg_con.fetch("SELECT name, uses FROM tags WHERE guild_id = $1 and user_id = $2",
        #                                      str(ctx.guild.id), str(member.id))
        guild_tags = await self.client.pg_con.fetch("SELECT name, uses FROM tags WHERE guild_id = $1",
                                                    str(ctx.guild.id))
        f = [(v[0], v[1] or 0) for v in this]
        a = [(x[0], x[1] or 0) for x in guild_tags]

        s = sorted(f, key=lambda x: x[1])[::-1]
        n = sorted(a, key=lambda y: y[1])[::-1]
        nf = n.index(s[0]) + 1
        if nf > 51:
            lt = []
        elif 26 <= nf <= 50:
            lt = legend_badges[:1]
        elif 11 <= nf <= 25:
            lt = legend_badges[:2]
        elif 4 <= nf <= 10:
            lt = legend_badges[:3]
        elif nf <= 3:
            lt = legend_badges
        else:
            lt = []
        print(nf)
        return ' '.join(et) + ' ' + ' '.join(pt) + ' ' + ' '.join(lt)
    
    @tag.command()
    @commands.has_permissions(kick_members=True)
    async def delete(self, ctx, *, name: str):
        """Delete a tag"""
        await self.client.pg_con.execute("DELETE FROM tags WHERE name = $1 AND guild_id = $2", name, str(ctx.guild.id))
        await ctx.send(f"Tag {name} deleted.")
    
    @tag.command(aliases=['tb'])
    async def badges(self, ctx, *, member: discord.Member = None):
        member = member or ctx.author
        embed = discord.Embed(colour=self.client.colour)
        embed.set_author(name=f"Tag Badges For {member.display_name}", icon_url=member.avatar_url)
        embed.add_field(name='Engineer Badges',
                        value=f"{engineer_bagdes[0]} **Engineer 1** - Create 10 tags\n{engineer_bagdes[1]} **Engineer 2** - Create 25 tags\n{engineer_bagdes[2]} **Engineer 3** - Create 100 tags\n{engineer_bagdes[3]} **Engineer 4** - Create 250 tags",
                        inline=False)
        embed.add_field(name='Popularity Badges',
                        value=f"{popular_badges[0]} **Popular 1** - Create a tag with 10 uses\n{popular_badges[1]} **Popular 2** - Create a tag with 25 uses\n{popular_badges[2]} **Popular 3** - Create a tag with 100 uses\n{popular_badges[3]} **Popular 4** - Create a tag with 250 uses",
                        inline=False)
        embed.add_field(name='Legendary Badges',
                        value=f"{legend_badges[0]} **Legend 1** - Create a tag in the guild's top 50\n{legend_badges[1]} **Legend 2** - Create a tag in the guild's top 25\n{legend_badges[2]} **Legend 3** - Create a tag in the guild's top 10\n{legend_badges[3]} **Legend 4** - Create a tag in the guild's top 3",
                        inline=False)
        value = await self.get_user_badges(member=member, ctx=ctx)
        embed.add_field(name=f'{member.display_name}\'s Badges', value='\u200b' + value)
        await ctx.send(embed=embed)
    
    @tag.command(aliases=['ui', 'user'])
    async def userinfo(self, ctx, *, member: discord.Member = None):
        member = member or ctx.author
        user_id = str(member.id)
        embed = discord.Embed(colour=self.client.colour).set_author(name=f'{member}', icon_url=member.avatar_url)


def setup(client):
    client.add_cog(Tags(client))
