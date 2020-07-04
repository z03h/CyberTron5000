import datetime
import matplotlib

matplotlib.use('Agg')

import discord
import humanize
import matplotlib.pyplot as plt
from discord.ext import commands
from disputils import BotEmbedPaginator

from .utils.lists import REGIONS, sl, mlsl, wlsl, dlsl, channel_mapping, is_nsfw, status_mapping

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


class uiEmbed:
    def __init__(self, ctx):
        self.context = ctx
    
    def uiEmbed(self, member: discord.Member, opt: str):
        member = member or self.context.message.author
        perms = []
        negperms = []
        if opt == "ui":
            is_bot = "<:bot:703728026512392312>" if member.bot else "\u200b"
            join_position = sorted(self.context.guild.members, key=lambda member: member.joined_at).index(member)
            status_list = f"{sl[str(member.status)]}{mlsl[str(member.mobile_status)]}{wlsl[str(member.web_status)]}{dlsl[str(member.desktop_status)]}{is_bot}"
            if member.top_role.id == self.context.guild.id:
                top_role_msg = "\u200b"
            else:
                top_role_msg = f"\n**Top Role:** {member.top_role.mention}"
            embed = discord.Embed(
                colour=colour, timestamp=self.context.message.created_at,
                description=f"**{member.id}**\nJoined guild **{humanize.naturaltime(datetime.datetime.utcnow() - member.joined_at)}** • Join Position: **{join_position + 1:,}**\nCreated account **{humanize.naturaltime(datetime.datetime.utcnow() - member.created_at)}**{top_role_msg}\n{status_list}"
            )
            embed.set_author(name=member)
            embed.set_thumbnail(url=member.avatar_url_as(static_format="png"))
            return embed
        elif opt == "perms":
            embed = discord.Embed(colour=colour, timestamp=self.context.message.created_at,
                                  description=f"**Channel**: {self.context.channel.mention}")
            permissions = self.context.channel.permissions_for(member)
            for item, valueBool in permissions:
                if valueBool:
                    value = ":white_check_mark:"
                    perms.append(f'{value}{item}')
                else:
                    value = '<:RedX:707949835960975411>'
                    negperms.append(f'{value}{item}')
            embed.set_author(name=f"Permissions for {member}", icon_url=member.avatar_url)
            embed.add_field(name='Has', value='\n'.join(perms), inline=True)
            embed.add_field(name='Does Not Have', value='\n'.join(negperms), inline=True)
            return embed
        elif opt == "av":
            embed = discord.Embed(colour=colour).set_image(url=member.avatar_url_as(static_format='png'))
            embed.set_author(name=f"Showing the profile picture of {member}")
            return embed


class Profile(commands.Cog):
    """Commands interacting with a user or guild's profile."""
    
    def __init__(self, client):
        self.client = client

    @commands.command(aliases=["av"], help="Gets the avatar of a user.")
    async def avatar(self, ctx, *, avamember: discord.Member = None):
        await ctx.send(embed=uiEmbed(ctx).uiEmbed(member=avamember, opt="av"))

    @commands.group(aliases=['si', 'serverinfo', 'gi', 'guild', 'server'], help="Gets the guild's info.",
                    invoke_without_command=True)
    async def guildinfo(self, ctx):
        g = GuildStats(ctx).status_dict
        n = '\n'
        guild = ctx.guild
        people = [f"<:member:716339965771907099>**{len(ctx.guild.members):,}**", f"{sl['online']}**{g['online']:,}**",
                  f"{sl['dnd']}**{g['dnd']:,}**", f"{sl['idle']}**{g['idle']:,}**",
                  f"{sl['offline']}**{g['offline']:,}**", f"<:bot:703728026512392312> **{GuildStats(ctx).num_bot}**"]
        text_channels = [text_channel for text_channel in guild.text_channels]
        voice_channels = [voice_channel for voice_channel in guild.voice_channels]
        categories = [category for category in guild.categories]
        region = REGIONS[f"{str(guild.region)}"]
        embed = discord.Embed(colour=colour,
                              description=f"**{ctx.guild.id}**\n<:category:716057680548200468> **{len(categories)}** | <:text_channel:703726554018086912>**{len(text_channels)}** • <:voice_channel:703726554068418560>**{len(voice_channels)}**"
                                          f"\n{f'{n}'.join(people)}\n**Owner:** {ctx.guild.suggest.mention}\n**Region:** {region}")
        embed.set_author(name=guild, icon_url=guild.icon_url)
        embed.set_footer(
            text=f"Guild created {humanize.naturaltime(datetime.datetime.utcnow() - ctx.guild.created_at)}")
        await ctx.send(embed=embed)

    @guildinfo.command(aliases=['mods'], invoke_without_command=True)
    async def staff(self, ctx):
        """Shows you the mods of a guild"""
        n = "\n"
        owner = ctx.guild.suggest.mention
        members = [m for m in ctx.guild.members]
        admins = [admin for admin in members if admin.guild_permissions.administrator and admin.bot is False]
        mods = [mod for mod in members if mod.guild_permissions.kick_members and mod.bot is False]
        mod_bots = [bot for bot in members if bot.guild_permissions.kick_members and bot.bot is True]
        await ctx.send(
            embed=discord.Embed(description=f"👑 **OWNER:** {owner}\n"
                                            f"\n**ADMINS** (Total {len(admins)})\n {f'{n}'.join([f'🛡 {admin.mention} - {admin.top_role.mention}' for admin in admins[:10]])}"
                                            f"\n\n**MODERATORS** (Total {len(mods)})\n {f'{n}'.join([f'🛡 {mod.mention} - {mod.top_role.mention}' for mod in mods[:10]])}"
                                            f"\n\n**MOD BOTS** (Total {len(mod_bots)})\n {f'{n}'.join([f'🛡 {bot.mention} - {bot.top_role.mention}' for bot in mod_bots[:10]])}",
                                colour=colour).set_author(name=f"Staff Team for {ctx.guild}",
                                                          icon_url=ctx.guild.icon_url))

    @guildinfo.command(invoke_without_command=True, aliases=['stats'])
    async def statistics(self, ctx):
        """Shows you the stats of the guild"""
        role_list = " ".join(role.mention for role in ctx.guild.roles[::-1][:10] if role.id != ctx.guild.id)
        gs = GuildStats(ctx)
        msg = "Top 10 Roles" if len([r for r in ctx.guild.roles]) > 10 else "Roles"
        total_mem = ctx.guild.member_count
        embed = discord.Embed(colour=colour,
                              description=f"Out of **{total_mem:,}** members:\n•{sl['online']} **{gs.status_dict['online']:,} ({round(gs.status_dict['online'] / total_mem * 100, 1):,}%)** are **online**\n•{sl['dnd']} **{gs.status_dict['dnd']:,} ({round(gs.status_dict['dnd'] / total_mem * 100, 1):,}%)** are on **do not disturb**\n•{sl['idle']} **{gs.status_dict['idle']:,} ({round(gs.status_dict['idle'] / total_mem * 100, 1):,}%)** are **idle**\n•{sl['offline']} **{gs.status_dict['offline']:,} ({round(gs.status_dict['offline'] / total_mem * 100, 1):,}%)** are **offline**\n<:bot:703728026512392312> This guild has **{gs.num_bot:,}** bots. **({(round(gs.num_bot / total_mem * 100, 1)):,}%)**\n\nThis guild has **{gs.emojis_dict['total']:,}** total emojis, **{gs.emojis_dict['animated']}** of which **({round(gs.emojis_dict['animated'] / gs.emojis_dict['total'] * 100, 1):,}%)** are animated.\nOut of this guild's limit of **{gs.emojis_dict['limit']}** for non-animated emojis, it has used **{round(gs.emojis_dict['still'] / gs.emojis_dict['limit'] * 100, 1):,}%** of it. **({gs.emojis_dict['still']}/{gs.emojis_dict['limit']})**\n\n<:boost:726151031322443787> This guild has **{ctx.guild.premium_subscription_count}** Nitro Boosts and is Tier **{ctx.guild.premium_tier}**").set_author(
            name=f"Advanced Statistics for {ctx.guild}", icon_url=ctx.guild.icon_url)
        embed.set_image(url="attachment://guild.png")
        embed.add_field(name=f"{msg} (Total {len([r for r in ctx.guild.roles])})", value='\u200b' + role_list)
        embed.add_field(name=f"Emojis (Total {len([e for e in ctx.guild.emojis])})",
                        value='\u200b' + " • ".join([str(a) for a in ctx.guild.emojis][:24]), inline=False)
        await ctx.send(embed=embed, file=gs.guild_graph)

    @guildinfo.command(aliases=['chan'])
    async def channels(self, ctx):
        """Shows you the channels of a guild."""
        if ctx.guild.id == 653376332507643914:
            return await ctx.send("peanut no like :angry:")
        else:
            embed = discord.Embed(colour=colour).set_author(icon_url=ctx.guild.icon_url_as(format='png'),
                                                            name=f"Channels in {ctx.guild}")
            for c in ctx.guild.categories:
                x = []
                for i in c.text_channels:
                    x.append(f"{channel_mapping[str(i.type)]}{i.name}{is_nsfw[i.is_nsfw()]}")
                for j in c.voice_channels:
                    x.append(f"{channel_mapping[str(j.type)]}{j.name}")
                embed.add_field(name=f"{c}", value='\u200b' + "\n".join(x),
                                inline=False)
            y = [b for b in ctx.guild.categories]
            chl = [f"{channel_mapping[str(o.type)]}{o.name}{is_nsfw[o.is_nsfw()]}" for o in ctx.guild.channels if
                   not o.category and o not in y]
            embed.description = "\n".join(chl)
            await ctx.send(embed=embed)

    @commands.command(aliases=['ov'],
                      help="Gets an overview of a user, including their avatar, permissions in the channel and info.")
    async def overview(self, ctx, *, member: discord.Member = None):
        u = uiEmbed(ctx)
        embeds = [u.uiEmbed(member=member, opt="ui"), u.uiEmbed(member=member, opt="perms"), u.uiEmbed(member=member, opt="av")]
        paginator = BotEmbedPaginator(ctx, embeds)
        await paginator.run()

    @commands.command(aliases=['ui', 'user'], help="Gets a user's info.")
    async def userinfo(self, ctx, *, member: discord.Member = None):
        member = member or ctx.author
        em = uiEmbed(ctx).uiEmbed(member=member, opt="ui")
        activities = []
        m = ctx.guild.get_member(member.id)
        if not m.activities:
            pass
        else:
            for activity in m.activities:
                if isinstance(activity, discord.Spotify):
                    activity = 'Listening to **Spotify**'
                elif isinstance(activity, discord.Game):
                    activity = f'Playing **{activity.name}**'
                elif isinstance(activity, discord.Streaming):
                    activity = f'Streaming **{activity.name}**'
                else:
                    emoji = ''
                    if activity.emoji:
                        emoji = ':thinking:' if activity.emoji.is_custom_emoji() and not self.client.get_emoji(
                            activity.emoji.id) else activity.emoji
                        if str(emoji) == ":thinking:":
                            em.set_footer(text="🤔 indicates a custom emoji")
                    char = "\u200b" if activity.type == discord.ActivityType.custom else " "
                    if str(activity.name) == "None":
                        ac = "\u200b"
                    else:
                        ac = str(activity.name)
                    activity = f'{emoji} {status_mapping[activity.type]}{char}**{ac}**'
                activities.append(activity)
            em.add_field(name="Activities", value="\n".join(activities))
        await ctx.send(embed=em)

    @commands.command(aliases=['perms'], help="Gets a user's permissions in the current channel.")
    async def permissions(self, ctx, *, member: discord.Member = None):
        await ctx.send(embed=uiEmbed(ctx).uiEmbed(member=member, opt="perms"))


def setup(client):
    client.add_cog(Profile(client))

