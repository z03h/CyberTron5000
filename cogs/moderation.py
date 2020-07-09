import discord
from discord.ext import commands

from .utils.checks import check_admin_or_owner

colour = 0x00dcff


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
        author = ctx.message.author
        embed = discord.Embed(
            colour=colour, timestamp=ctx.message.created_at, title="Poll:", description=message
        )
        embed.set_footer(text=f"Started by {author}", icon_url=author.avatar_url)
        await ctx.message.delete()
        string = str("Vote Here!")
        e = await ctx.send(string, embed=embed)
        for r in ['⬆️', '⬇️']:
            await e.add_reaction(r)
    
    @vote.command(invoke_without_command=True)
    @commands.is_owner()
    async def ct5k(self, ctx, *, message):
        """Voting only in the CyberTron5000 help server (https://discord.gg/2fxKxJH)"""
        author = ctx.message.author
        embed = discord.Embed(
            colour=colour, timestamp=ctx.message.created_at, title="Poll:", description=message
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


def setup(client):
    client.add_cog(Moderation(client))
