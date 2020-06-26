import datetime
import random

import matplotlib

matplotlib.use('Agg')

import discord
import humanize
import matplotlib.pyplot as plt
from discord.ext import commands
from disputils import BotEmbedPaginator

from .utils.lists import REGIONS, sl, mlsl, wlsl, dlsl

colour = 0x00dcff


# •

class GuildStats:
    def __init__(self, ctx):
        self.context = ctx
    
    @property
    def num_bot(self):
        return len([m for m in self.context.guild.members if m.bot])
    
    @property
    def status_dict(self):
        return {
            "online": len([m for m in self.context.guild.members if m.status == discord.Status.online]),
            "offline": len([m for m in self.context.guild.members if m.status == discord.Status.offline]),
            "idle": len([m for m in self.context.guild.members if m.status == discord.Status.idle]),
            "dnd": len([m for m in self.context.guild.members if m.status == discord.Status.dnd])
        }
    
    @property
    def guild_graph(self):
        labels = f'Online ({self.status_dict["online"]:,})', f'Do Not Disturb ({self.status_dict["dnd"]:,})', f'Idle ({self.status_dict["idle"]:,})', f'Offline ({self.status_dict["offline"]:,})'
        sizes = [self.status_dict['online'], self.status_dict['dnd'], self.status_dict['idle'],
                 self.status_dict['offline']]
        colors = ['#42B581', '#E34544', '#FAA619', '#747F8D']
        explode = (0.0, 0, 0, 0)
        
        patches, texts = plt.pie(sizes, colors=colors, shadow=False, startangle=90)
        plt.legend(patches, labels, loc="best")
        plt.pie(sizes, explode=explode, colors=colors,
                autopct='%1.1f%%', shadow=False, startangle=140)
        
        plt.axis('equal')
        plt.title(f"Total guild members: {len(self.context.guild.members):,}",
                  bbox={'facecolor': '0.8', 'pad': 5})
        fig = plt.savefig("guild.png", transparent=True)
        plt.close(fig=fig)
        return discord.File("guild.png", filename="guild.png")
    
    @property
    def emojis_dict(self):
        return {
            "animated": len([e for e in self.context.guild.emojis if e.animated]),
            "still": len([e for e in self.context.guild.emojis if not e.animated]),
            "total": len(self.context.guild.emojis),
            "limit": self.context.guild.emoji_limit,
        }


class Profile(commands.Cog):
    """Commands interacting with a user or guild's profile."""
    
    def __init__(self, client):
        self.client = client
    
    @commands.command(aliases=["av"], help="Gets the avatar of a user.")
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
    
    @commands.group(aliases=['si', 'serverinfo', 'gi', 'guild', 'server'], help="Gets the guild's info.",
                    invoke_without_command=True)
    async def guildinfo(self, ctx):
        try:
            g = GuildStats(ctx).status_dict
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
            embed = discord.Embed(colour=colour, title=f'{guild}',
                                  description=f"**{ctx.guild.id}**\n<:category:716057680548200468> **{len(categories)}** | <:text_channel:703726554018086912>**{len(text_channels)}** • <:voice_channel:703726554068418560>**{len(voice_channels)}**"
                                              f"\n<:member:716339965771907099>**{len(ctx.guild.members):,}** | {sl['online']}**{g['online']:,}** • {sl['dnd']}**{g['dnd']:,}** • {sl['idle']}**{g['idle']:,}** • {sl['offline']}**{g['offline']:,}** | <:bot:703728026512392312> **{GuildStats(ctx).num_bot}**\n**Owner:** {ctx.guild.owner.mention}\n**Region:** {region}")
            embed.set_thumbnail(url=guild.icon_url)
            if len(roles) > 10:
                msg = "Top 10 roles"
            else:
                msg = "Roles"
            embed.set_footer(
                text=f"Guild created {humanize.naturaltime(datetime.datetime.utcnow() - ctx.guild.created_at)}")
            embed.add_field(name=f"{msg} (Total {len(roles)})", value='\u200b' + role_list)
            embed.add_field(name=f"Emojis (Total {len(emojis)})", value='\u200b' + " • ".join(em_list[:24]),
                            inline=False)

            await ctx.send(embed=embed)
        except Exception as error:
            await ctx.send(error)
    
    @guildinfo.command(aliases=['mods'], invoke_without_command=True)
    async def staff(self, ctx):
        """Shows you the mods of a guild"""
        try:
            n = "\n"
            owner = ctx.guild.owner.mention
            admins = [admin for admin in ctx.guild.members if
                      admin.guild_permissions.administrator and admin.bot is False]
            mods = [mod for mod in ctx.guild.members if mod.guild_permissions.kick_members and mod.bot is False]
            mod_bots = [bot for bot in ctx.guild.members if bot.guild_permissions.kick_members and bot.bot is True]
            await ctx.send(
                embed=discord.Embed(title=f"🛡 Staff Team for {ctx.guild}", description=f"👑 **OWNER:** {owner}\n"
                                                                                        f"\n**ADMINS** (Total {len(admins)})\n {f'{n}'.join([f'🛡 {admin.mention} - {admin.top_role.mention}' for admin in admins[:10]])}"
                                                                                        f"\n\n**MODERATORS** (Total {len(mods)})\n {f'{n}'.join([f'🛡 {mod.mention} - {mod.top_role.mention}' for mod in mods[:10]])}"
                                                                                        f"\n\n**MOD BOTS** (Total {len(mod_bots)})\n {f'{n}'.join([f'🛡 {bot.mention} - {bot.top_role.mention}' for bot in mod_bots[:10]])}",
                                    colour=colour).set_thumbnail(url=ctx.guild.icon_url))
        except Exception as error:
            await ctx.send(error)
    
    @guildinfo.command(invoke_without_command=True, aliases=['stats'])
    async def statistics(self, ctx):
        """Shows you the stats of the guild"""
        try:
            gs = GuildStats(ctx)
            total_mem = ctx.guild.member_count
            embed = discord.Embed(title=f"Advanced Statistics for {ctx.guild}", colour=colour,
                                  description=f"Out of **{total_mem:,}** members:\n•{sl['online']} **{gs.status_dict['online']:,} ({round(gs.status_dict['online'] / total_mem * 100, 1):,}%)** are **online**\n•{sl['dnd']} **{gs.status_dict['dnd']:,} ({round(gs.status_dict['dnd'] / total_mem * 100, 1):,}%)** are on **do not disturb**\n•{sl['idle']} **{gs.status_dict['idle']:,} ({round(gs.status_dict['idle'] / total_mem * 100, 1):,}%)** are **idle**\n•{sl['offline']} **{gs.status_dict['offline']:,} ({round(gs.status_dict['offline'] / total_mem * 100, 1):,}%)** are **offline**\n<:bot:703728026512392312> This guild has **{gs.num_bot:,}** bots. **({(round(gs.num_bot / total_mem * 100, 1)):,}%)**\n\nThis guild has **{gs.emojis_dict['total']:,}** total emojis, **{gs.emojis_dict['animated']}** of which **({round(gs.emojis_dict['animated'] / gs.emojis_dict['total'] * 100, 1):,}%)** are animated.\nOut of this guild's limit of **{gs.emojis_dict['limit']}** for non-animated emojis, it has used **{round(gs.emojis_dict['still'] / gs.emojis_dict['limit'] * 100, 1):,}%** of it. **({gs.emojis_dict['still']}/{gs.emojis_dict['limit']})**\n\n<:boost:726151031322443787> This guild has **{ctx.guild.premium_subscription_count}** Nitro Boosts and is Tier **{ctx.guild.premium_tier}**")
            embed.set_thumbnail(url=ctx.guild.icon_url_as(format='png'))
            embed.set_image(url="attachment://guild.png")
            await ctx.send(embed=embed, file=gs.guild_graph)
        except Exception as e:
            await ctx.send(e)
    
    @commands.command(aliases=['ov'],
                      help="Gets an overview of a user, including their avatar, permissions in the channel and info.")
    async def overview(self, ctx, *, member: discord.Member = None):
        footer = f"You can also do {ctx.prefix}ui, {ctx.prefix}perms, {ctx.prefix}av for each of these."
        member = member or ctx.message.author
        perms = []
        negperms = []
        member = member or ctx.message.author
        if member.bot is True:
            is_bot = "<:bot:703728026512392312>"
        else:
            is_bot = "\u200b"
        join_position = sorted(ctx.guild.members, key=lambda member: member.joined_at).index(member)
        status_list = f"{sl[str(member.status)]}{mlsl[str(member.mobile_status)]}{wlsl[str(member.web_status)]}{dlsl[str(member.desktop_status)]}{is_bot}"
        if member.top_role.id == ctx.guild.id:
            top_role_msg = "\u200b"
        else:
            top_role_msg = f"\n**Top Role:** {member.top_role.mention}"
        a = discord.Embed(
            colour=colour, timestamp=ctx.message.created_at, title=f"{member}",
            description=f"**{member.id}**\nJoined guild **{humanize.naturaltime(datetime.datetime.utcnow() - member.joined_at)}** • Join Position: **{join_position + 1:,}**\nCreated account **{humanize.naturaltime(datetime.datetime.utcnow() - member.created_at)}**\nGuilds shared with bot: **{len([g for g in self.client.guilds if g.get_member(member.id)])}**{top_role_msg}\n{status_list}"
        )
        a.set_thumbnail(url=member.avatar_url_as(static_format="png"))
        embedd = discord.Embed(colour=colour, timestamp=ctx.message.created_at,
                               title=f"{member.name}'s permissions for {ctx.guild}",
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
        
        b = discord.Embed(colour=colour, title=f"{member.name}'s profile picture")
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
    
    @commands.command(aliases=['ui', 'user'], help="Gets a user's info.")
    async def userinfo(self, ctx, *, member: discord.Member = None):
        try:
            member = member or ctx.message.author
            if member.bot is True:
                is_bot = "<:bot:703728026512392312>"
            else:
                is_bot = "\u200b"
            join_position = sorted(ctx.guild.members, key=lambda member: member.joined_at).index(member)
            status_list = f"{sl[str(member.status)]}{mlsl[str(member.mobile_status)]}{wlsl[str(member.web_status)]}{dlsl[str(member.desktop_status)]}{is_bot}"
            if member.top_role.id == ctx.guild.id:
                top_role_msg = "\u200b"
            else:
                top_role_msg = f"\n**Top Role:** {member.top_role.mention}"
            a = discord.Embed(
                colour=colour, timestamp=ctx.message.created_at, title=f"{member}",
                description=f"**{member.id}**\nJoined guild **{humanize.naturaltime(datetime.datetime.utcnow() - member.joined_at)}** • Join Position: **{join_position + 1:,}**\nCreated account **{humanize.naturaltime(datetime.datetime.utcnow() - member.created_at)}**{top_role_msg}\n{status_list}"
            )
            a.set_thumbnail(url=member.avatar_url_as(static_format="png"))
            await ctx.send(embed=a)
        except Exception as error:
            await ctx.send(error)
    
    @commands.command(aliases=['perms'], help="Gets a user's permissions in the current channel.")
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


def setup(client):
    client.add_cog(Profile(client))

