from discord.ext import commands
from cogs.utils.lists import REGIONS
import discord
import humanize
import json

colour = 0x00dcff


class Events(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.x = "<:warning:727013811571261540>"
        self.x_r = ":warning:727013811571261540"
    
    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        if isinstance(error, discord.ext.commands.CheckFailure):
            await ctx.message.add_reaction(emoji=self.x_r)
        
        if isinstance(error, discord.ext.commands.BadArgument):
            err = str(error.args[0])
            mem, msg = err.split('not')
            await ctx.send(
                f"{self.x} **{ctx.author.name}**, I looked where ever I could, but I couldn't find the **{mem}**anywhere!")
        
        if isinstance(error, discord.ext.commands.MissingRequiredArgument):
            await ctx.send(f"{self.x} **{ctx.author.name}**, you're missing the required argument **{error.param}**!")
        
        if isinstance(error, discord.ext.commands.MissingPermissions):
            await ctx.send(f'{self.x} **{ctx.author.name}**, {error}')
    
    @commands.Cog.listener(name="on_message")
    async def on_user_mention(self, message):
        owner = await self.client.fetch_user(350349365937700864)
        if "<@!697678160577429584>" == message.content:
            with open("prefixes.json", "r") as f:
                prefix = json.load(f)
                if str(message.guild.id) in prefix:
                    pre = prefix[str(message.guild.id)]
                    embed = discord.Embed(colour=colour,
                                          description=f'**My prefix for {message.guild} is** `{pre}`\n\n**Do** '
                                                      f'`{pre}help` **for a full list of commands.**\n\n'
                                                      f'[Invite me to your server!]'
                                                      f'(https://discord.com/api/oauth2/authorize?client_id=697678160577429584&permissions=2081291511&scope=bot)\n\n[Join our help server!](https://discord.gg/aa9p43W)')
                    embed.set_thumbnail(url=self.client.user.avatar_url)
                    embed.set_author(name=f"Developed by {owner}", icon_url=owner.avatar_url)
                    await message.channel.send(embed=embed)

    @commands.Cog.listener()
    async def on_guild_join(self, guild):
        c = self.client.get_channel(727277234666078220)
        mod_list = [member for member in guild.members if member.guild_permissions.administrator]
        ml = "\n".join([f"{member.mention} • `{member.top_role.name}`" for member in mod_list if member.bot is False])
        botno = len([member for member in guild.members if member.bot])
        text_channels = [text_channel for text_channel in guild.text_channels]
        voice_channels = [voice_channel for voice_channel in guild.voice_channels]
        categories = [category for category in guild.categories]
        emojis = [emoji for emoji in guild.emojis]
        region = REGIONS[f"{str(guild.region)}"]
        embed = discord.Embed(colour=0x00ff00, title=f'{guild}', description=f"**{guild.id}**"f"\n<:member:716339965771907099>**{len(guild.members):,}\n**Owner:** {guild.owner.mention}\n**Region:** {region}\n\n<:category:716057680548200468> **{len(categories)}** | <:text_channel:703726554018086912>**{len(text_channels)}** • <:voice_channel:703726554068418560>**{len(voice_channels)}**\n😔🤔😳 **{len(emojis)}**\n<:bot:703728026512392312> **{botno}**\n**Admins:**\n{ml}")
        embed.set_thumbnail(url=guild.icon_url)
        embed.set_footer(text=f"Guild created {humanize.naturaltime(__import__('datetime').datetime.utcnow() - guild.created_at)}")
        await c.send(f"Joined Guild! This is guild **#{len(self.client.guilds)}**", embed=embed)

    @commands.Cog.listener()
    async def on_guild_remove(self, guild):
        c = self.client.get_channel(727277234666078220)
        mod_list = [member for member in guild.members if member.guild_permissions.administrator]
        ml = "\n".join([f"{member.mention} • `{member.top_role.name}`" for member in mod_list if member.bot is False])
        botno = len([member for member in guild.members if member.bot])
        text_channels = [text_channel for text_channel in guild.text_channels]
        voice_channels = [voice_channel for voice_channel in guild.voice_channels]
        categories = [category for category in guild.categories]
        emojis = [emoji for emoji in guild.emojis]
        region = REGIONS[f"{str(guild.region)}"]
        embed = discord.Embed(colour=discord.Colour.red(), title=f'{guild}', description=f"**{guild.id}**"f"\n<:member:716339965771907099>**{len(guild.members):,}**\n**Owner:** {guild.owner.mention}\n**Region:** {region}\n\n<:category:716057680548200468> **{len(categories)}** | <:text_channel:703726554018086912>**{len(text_channels)}** • <:voice_channel:703726554068418560>**{len(voice_channels)}**\n😔🤔😳 **{len(emojis)}**\n<:bot:703728026512392312> **{botno}**\n**Admins:**{ml}")
        embed.set_thumbnail(url=guild.icon_url)
        embed.set_footer(text=f"Guild created {humanize.naturaltime(__import__('datetime').datetime.utcnow() - guild.created_at)}")
        await c.send(f"Left guild. We're down to **{len(self.client.guilds)}** guilds", embed=embed)


def setup(client):
    client.add_cog(Events(client))
