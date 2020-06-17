import datetime
import random

import discord
import humanize
from discord.ext import commands
from disputils import BotEmbedPaginator

from .utils.lists import REGIONS

colour = 0x00dcff


# ≫ •

class Profile(commands.Cog):
    """Commands interacting with a user or guild's profile."""
    def __init__(self, client):
        self.client = client
    
    @commands.command(aliases=["av"], help="≫ Gets the avatar of a user.")
    async def avatar(self, ctx, *, avamember: discord.Member = None):
        avamember = avamember or ctx.message.author
        await ctx.send(embed=discord.Embed(
            color=avamember.color, title=random.choice([
                "They do be looking cute tho :flushed:",
                "Very handsome :weary:",
                "lookin' like a snack:yum:",
                "a beaut :heart:",
            ]), timestamp=ctx.message.created_at
        ).set_image(url=avamember.avatar_url_as(static_format="png", size=2048)))
    
    @commands.command(aliases=['si', 'serverinfo', 'gi', 'guild', 'server'], help="≫ Gets the guild's info.")
    async def guildinfo(self, ctx):
        try:
            online = 0
            offline = 0
            idle = 0
            dnd = 0
            botno = 0
            for member in ctx.guild.members:
                if member.status == discord.Status.online:
                    online += 1
                elif member.status == discord.Status.offline:
                    offline += 1
                elif member.status == discord.Status.dnd:
                    dnd += 1
                elif member.status == discord.Status.idle:
                    idle += 1
            for member in ctx.guild.members:
                if member.bot is True:
                    botno += 1
            guild = ctx.guild
            emojis = [emoji for emoji in ctx.guild.emojis]
            em_list = []
            for emoji in emojis:
                em_list.append(str(emoji))
            text_channels = [text_channel for text_channel in guild.text_channels]
            voice_channels = [voice_channel for voice_channel in guild.voice_channels]
            categories = [category for category in guild.categories]
            emojis = [emoji for emoji in guild.emojis]
            region = REGIONS[f"{str(guild.region)}"]
            roles = [role for role in ctx.guild.roles]
            role_list = " ".join(role.mention for role in roles[::-1][:10] if role.id != ctx.guild.id)
            embed = discord.Embed(colour=colour, title=f'{guild}', description=f"**{ctx.guild.id}**"
                                                                               f"\n<:member:716339965771907099>**{len(ctx.guild.members):,}** | <:online:703903072824459265>**{online:,}** • <:dnd:703903073315192832>**{dnd:,}** • <:idle:703903072836911105>**{idle}** • <:offline:703918395518746735>**{offline:,}**\n**Owner:** {ctx.guild.owner.mention}\n**Region:** {region}\n\n<:category:716057680548200468> **{len(categories)}** | <:text_channel:703726554018086912>**{len(text_channels)}** • <:voice_channel:703726554068418560>**{len(voice_channels)}**\n😔🤔😳 **{len(emojis)}**\n<:bot:703728026512392312> **{botno}**")
            embed.set_thumbnail(url=guild.icon_url)
            if len(roles) > 10:
                msg = "Top 10 roles"
            else:
                msg = "Roles"
            embed.set_footer(
                text=f"Guild created {humanize.naturaltime(datetime.datetime.utcnow() - ctx.guild.created_at)}")
            embed.add_field(name=f"{msg} (Total {len(roles)})", value=role_list)
            embed.add_field(name="Emojis", value=" • ".join(em_list[:24]), inline=False)
            await ctx.send(embed=embed)
        except Exception as error:
            await ctx.send(error)
    
    @commands.command(aliases=['ov'],
                      help="≫ Gets an overview of a user, including their avatar, permissions in the channel and info.")
    async def overview(self, ctx, *, member: discord.Member = None):
        footer = f"You can also do {ctx.prefix}ui, {ctx.prefix}perms, {ctx.prefix}av for each of these."
        member = member or ctx.message.author
        perms = []
        negperms = []
        member = member or ctx.message.author
        if str(member.status) == "online":
            status_emoji = "<:online:703903072824459265>"
        elif str(member.status) == "offline":
            status_emoji = "<:offline:703918395518746735>"
        elif str(member.status) == "dnd":
            status_emoji = " <:dnd:703903073315192832>"
        else:
            status_emoji = "<:idle:703903072836911105>"
        if str(member.mobile_status) == "online":
            bruhmoji = "<:whiteiphone:703726679377575996>"
        elif str(member.mobile_status) == "idle":
            bruhmoji = "<:whiteiphone:703726679377575996>"
        elif str(member.mobile_status) == "dnd":
            bruhmoji = "<:whiteiphone:703726679377575996>"
        else:
            bruhmoji = "\u200b"
        if str(member.web_status) == "online":
            bruhmoji2 = "🌐"
        elif str(member.web_status) == "idle":
            bruhmoji2 = "🌐"
        elif str(member.web_status) == "dnd":
            bruhmoji2 = "🌐"
        else:
            bruhmoji2 = "\u200b"
        if str(member.desktop_status) == "online":
            bruhmoji3 = ":desktop:"
        elif str(member.desktop_status) == "idle":
            bruhmoji3 = ":desktop:"
        elif str(member.desktop_status) == "dnd":
            bruhmoji3 = ":desktop:"
        else:
            bruhmoji3 = "\u200b"
        if str(member.status) == "offline":
            bruhmoji = "\u200b"
            bruhmoji2 = "\u200b"
            bruhmoji3 = "\u200b"
        if member.bot is True:
            bot_bruh = "<:bot:703728026512392312>"
        else:
            bot_bruh = "\u200b"
        a = discord.Embed(
            colour=colour, timestamp=ctx.message.created_at, title=f"{member}",
            description=f"**{member.id}**\n**Joined At**: {member.joined_at.strftime('%B %d, %Y')}\n**Created Account**: {member.created_at.strftime('%B %d, %Y')}\n**Top Role:** {member.top_role.mention}\n{status_emoji}{bruhmoji}{bruhmoji2}{bruhmoji3}{bot_bruh}"
        )
        a.set_thumbnail(url=member.avatar_url)
        
        embedd = discord.Embed(colour=colour, timestamp=ctx.message.created_at,
                               title=f"{member.display_name} permissions for {ctx.guild}",
                               description=f"**Channel**: <#{ctx.message.channel.id}>")
        permissions = ctx.channel.permissions_for(member)
        for item, valueBool in permissions:
            if valueBool:
                value = ":white_check_mark:"
                perms.append(f'{value}{item}')
            else:
                value = '<:RedX:707949835960975411>'
                negperms.append(f'{value}{item}')
        
        embedd.add_field(name='Has', value='\n'.join(perms), inline=True)
        embedd.add_field(name='Does Not Have', value='\n'.join(negperms), inline=True)
        embedd.set_footer(text=footer)
        
        b = discord.Embed(colour=colour, title=f"{member.display_name}'s profile picture")
        b.set_image(url=member.avatar_url)
        b.set_footer(text=footer)
        
        embeds = [
            a,
            embedd,
            b,
            discord.Embed(title="Key:",
                          description=":track_previous: First page\n:track_next: Last page\n:arrow_backward: "
                                      "Back one page.\n:arrow_forward: Forward one page\n:stop_button: "
                                      "Close Paginator.\n",
                          colour=colour)
        ]
        paginator = BotEmbedPaginator(ctx, embeds)
        await paginator.run()
    
    @commands.command(aliases=['ui', 'user'], help="≫ Gets a user's info.")
    async def userinfo(self, ctx, *, member: discord.Member = None):
        try:
            member = member or ctx.message.author
            if str(member.status) == "online":
                status_emoji = "<:online:703903072824459265>"
            elif str(member.status) == "offline":
                status_emoji = "<:offline:703918395518746735>"
            elif str(member.status) == "dnd":
                status_emoji = " <:dnd:703903073315192832>"
            else:
                status_emoji = "<:idle:703903072836911105>"
            if str(member.mobile_status) == "online":
                bruhmoji = "<:whiteiphone:703726679377575996>"
            elif str(member.mobile_status) == "idle":
                bruhmoji = "<:whiteiphone:703726679377575996>"
            elif str(member.mobile_status) == "dnd":
                bruhmoji = "<:whiteiphone:703726679377575996>"
            else:
                bruhmoji = "\u200b"
            if str(member.web_status) == "online":
                bruhmoji2 = "🌐"
            elif str(member.web_status) == "idle":
                bruhmoji2 = "🌐"
            elif str(member.web_status) == "dnd":
                bruhmoji2 = "🌐"
            else:
                bruhmoji2 = "\u200b"
            if str(member.desktop_status) == "online":
                bruhmoji3 = ":desktop:"
            elif str(member.desktop_status) == "idle":
                bruhmoji3 = ":desktop:"
            elif str(member.desktop_status) == "dnd":
                bruhmoji3 = ":desktop:"
            else:
                bruhmoji3 = "\u200b"
            if str(member.status) == "offline":
                bruhmoji = "\u200b"
                bruhmoji2 = "\u200b"
                bruhmoji3 = "\u200b"
            if member.bot is True:
                bot_bruh = "<:bot:703728026512392312>"
            else:
                bot_bruh = "\u200b"
            stuff = []
            for activity in member.activities:
                stuff.append(str(activity))
                
            status_list = f"{status_emoji}{bruhmoji}{bruhmoji2}{bruhmoji3}{bot_bruh}"
            a = discord.Embed(
                colour=colour, timestamp=ctx.message.created_at, title=f"{member}",
                description=f"**{member.id}**\nJoined guild **{humanize.naturaltime(datetime.datetime.utcnow() - member.joined_at)}**\nCreated account **{humanize.naturaltime(datetime.datetime.utcnow()-member.created_at)}**\n**Top Role:** {member.top_role.mention}\n{status_list}"
            )
            a.set_thumbnail(url=member.avatar_url_as(static_format="png"))
            await ctx.send(embed=a)
        except Exception as error:
            await ctx.send(error)
    
    @commands.command(aliases=['perms'], help="≫ Gets a user's permissions in the current channel.")
    async def permissions(self, ctx, *, member: discord.Member = None):
        member = member or ctx.message.author
        perms = []
        negperms = []
        embedd = discord.Embed(colour=colour, timestamp=ctx.message.created_at,
                               title=f"{member.display_name}'s permissions for {ctx.guild}",
                               description=f"**Channel**: <#{ctx.message.channel.id}>")
        permissions = ctx.channel.permissions_for(member)
        for item, valueBool in permissions:
            if valueBool:
                value = ":white_check_mark:"
                perms.append(f'{value}{item}')
            else:
                value = '<:RedX:707949835960975411>'
                negperms.append(f'{value}{item}')
        
        embedd.add_field(name='Has', value='\n'.join(perms), inline=True)
        embedd.add_field(name='Does Not Have', value='\n'.join(negperms), inline=True)
        await ctx.send(embed=embedd)


def setup(client):
    client.add_cog(Profile(client))
