import discord
import asyncio
import json
import humanize

from discord.ext import commands

from .utils.checks import check_admin_or_owner
from .utils import lists, paginator


# ≫


class Moderation(commands.Cog):
    """Commands for Moderation"""
    
    def __init__(self, client):
        self.client = client
        self.tick = ":GreenTick:707950252434653184"
    
    @commands.command(aliases=['clear'])
    @commands.has_permissions(manage_messages=True)
    async def purge(self, ctx, amount=5):
        """ Purges a given amount of messages with the default being 5 """
        await ctx.message.delete()
        await ctx.channel.purge(limit=int(amount))
        await ctx.send(f"{amount} messages have been cleared.", delete_after=3)
    
    @commands.command()
    @commands.has_permissions(kick_members=True)
    async def kick(self, ctx, member: discord.Member, *, reason=None):
        """Kick a member from a guild."""
        r = "No reason specified" if not reason else reason
        await member.kick(reason=r)
        await member.send(
            f"Hello, you have been kicked from participating in {ctx.guild}. Please see your reason for removal: `{r}`")
        await ctx.message.add_reaction(self.tick)
    
    @commands.command(help="Ban a member.")
    @commands.has_permissions(ban_members=True)
    async def ban(self, ctx, member: discord.Member, *, reason=None):
        """Ban a member from a guild."""
        r = "No reason specified" if not reason else reason
        await member.ban(reason=r)
        await member.send(
            f"Hello, you have been kicked from participating in {ctx.guild}. Please see your reason for removal: `{r}`")
        await ctx.message.add_reaction(self.tick)
    
    @commands.command(help="Unban a member.")
    @commands.has_permissions(ban_members=True)
    async def unban(self, ctx, *, member):
        banned = await ctx.guild.bans()
        member_name, member_discriminator = member.split("#")
        for ban_entry in banned:
            user = ban_entry.user
            
            if (user.name, user.discriminator) == (member_name, member_discriminator):
                await ctx.guild.unban(user)
                await ctx.message.add_reaction(emoji=":GreenTick:707950252434653184")
    
    @commands.group(help="Vote on something.", invoke_without_command=True)
    async def vote(self, ctx, *, message):
        valid_emojis = ['⬆️', '⬇️']
        author = ctx.message.author
        embed = discord.Embed(
            colour=self.client.colour, timestamp=ctx.message.created_at, title="Poll:", description=message
        )
        embed.set_footer(text=f"Started by {author}", icon_url=author.avatar_url)
        embed.add_field(name="Upvotes", value="1", inline=False)
        embed.add_field(name="Downvotes", value="1", inline=False)
        e = await ctx.send(embed=embed)
        for r in valid_emojis:
            await e.add_reaction(r)
        while True:
            names = ['Upvotes', 'Downvotes']
            done, pending = await asyncio.wait([
                self.client.wait_for("reaction_add"),
                self.client.wait_for("reaction_remove")
            ], return_when=asyncio.FIRST_COMPLETED)
            m = await ctx.channel.fetch_message(e.id)
            res = done.pop().result()
            print(res)
            if res[0].emoji not in valid_emojis:
                return
            else:
                index = valid_emojis.index(res[0].emoji)
                p = (len(m.reactions)) - res[0].count
                percent = round(p / len(m.reactions) * 100, 2)
                embed.set_field_at(index=index, name=names[index], value=f"{res[0].count} | {percent}%", inline=False)
                await e.edit(embed=embed)
                continue
    
    @vote.command(invoke_without_command=True)
    @commands.is_owner()
    async def ct5k(self, ctx, *, message):
        """Voting only in the CyberTron5000 help server (https://discord.gg/2fxKxJH)"""
        author = ctx.message.author
        embed = discord.Embed(
            colour=self.client.colour, timestamp=ctx.message.created_at, title="Poll:", description=message
        )
        embed.set_footer(text=f"Started by {author}", icon_url=author.avatar_url)
        await ctx.message.delete()
        string = str("<@&724429718882877531>")
        e = await ctx.send(string, embed=embed)
        for r in [':upvote:718895913342337036', ':downvote:718895842404335668']:
            await e.add_reaction(r)
    
    @commands.group(name='user-nick', help="Change a user's nickname.", aliases=['usernick', 'UnitedNations', 'un'],
                    invoke_without_command=True)
    @commands.has_permissions(administrator=True)
    async def user_nick(self, ctx, member: discord.Member, *, name):
        await ctx.guild.get_member(member.id).edit(nick=name)
        await ctx.message.add_reaction(emoji=":GreenTick:707950252434653184")
    
    @user_nick.command(invoke_without_command=True)
    @commands.has_permissions(administrator=True)
    async def default(self, ctx, member: discord.Member):
        """Change nickname back to default."""
        await ctx.guild.get_member(member.id).edit(nick=member.name)
        await ctx.message.add_reaction(emoji=":GreenTick:707950252434653184")
    
    @commands.command()
    @check_admin_or_owner()
    async def leave(self, ctx):
        """Makes bot leave server"""
        await self.client.get_guild(ctx.guild.id).leave()
    
    @commands.group(invoke_without_command=True, help="Change the guild's prefix", aliases=['prefix', 'pre'])
    @check_admin_or_owner()
    async def changeprefix(self, ctx, *, prefix):
        with open("prefixes.json", "r") as f:
            prefixes = json.load(f)
        
        prefixes[str(ctx.guild.id)] = prefix
        
        with open("prefixes.json", "w") as f:
            json.dump(prefixes, f, indent=4)
        await ctx.message.add_reaction(emoji=":GreenTick:707950252434653184")
        await ctx.guild.me.edit(nick=f"({prefix}) {self.client.user.name}")
    
    @changeprefix.command(invoke_without_command=True, help="Make your prefix end in a space.", aliases=['sp'])
    @check_admin_or_owner()
    async def spaceprefix(self, ctx, *, prefix):
        with open("prefixes.json", "r") as f:
            prefixes = json.load(f)
        prefixes[str(ctx.guild.id)] = f"{prefix} "
        with open("prefixes.json", "w") as f:
            json.dump(prefixes, f, indent=4)
        await ctx.message.add_reaction(emoji=":GreenTick:707950252434653184")
        await ctx.guild.me.edit(nick=f"({prefix}) {self.client.user.name}")
    
    @commands.command(aliases=['audit'])
    @commands.has_permissions(view_audit_log=True)
    async def auditlog(self, ctx, limit: int = 20):
        try:
            actions = []
            async for x in ctx.guild.audit_logs(limit=limit):
                actions.append(
                    f"{x.user.name} {lists.audit_actions[x.action]} {x.target} ({humanize.naturaltime(__import__('datetime').datetime.utcnow() - x.created_at)})")
            source = paginator.IndexedListSource(embed=discord.Embed(colour=self.client.colour).set_author(
                name=f"Last Audit Log Actions for {ctx.guild}", icon_url=ctx.guild.icon_url), data=actions)
            menu = paginator.CatchAllMenu(source=source)
            await menu.start(ctx)
        except Exception as er:
            await ctx.send(f'{er.__class__.__name__}, {er}')


def setup(client):
    client.add_cog(Moderation(client))
