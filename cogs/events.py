import json

import async_cleverbot
import discord
import humanize
from discord.ext import commands

from .utils import cyberformat


def secrets():
    with open("secrets.json", "r") as f:
        return json.load(f)


class Events(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.x_r = ":warning:727013811571261540"
        self.bot = async_cleverbot.Cleverbot(secrets()['cleverbot'])
        self.bot.set_context(async_cleverbot.DictContext(self.bot))
    
    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        if isinstance(error, discord.ext.commands.CheckFailure):
            await ctx.message.add_reaction(emoji=self.x_r)
        
        elif isinstance(error, discord.ext.commands.BadArgument):
            await ctx.send(
                f"<{self.x_r}> **{ctx.author.name}**, {cyberformat.minimalize(str(error))}")
        
        elif isinstance(error, discord.ext.commands.MissingRequiredArgument):
            await ctx.send(
                f"<{self.x_r}> **{ctx.author.name}**, you're missing the required argument **{error.param.name}**!")
        
        elif isinstance(error, discord.ext.commands.MissingPermissions):
            await ctx.send(f'<{self.x_r}> **{ctx.author.name}**, {cyberformat.minimalize(str(error))}')
        
        elif isinstance(error, commands.CommandNotFound) or isinstance(error, commands.NotOwner):
            pass
        
        elif isinstance(error, commands.BotMissingPermissions):
            await ctx.send(f'<{self.x_r}> **{ctx.author.name}**, {cyberformat.minimalize(str(error))}')
        
        elif isinstance(error, commands.BadUnionArgument):
            await ctx.send(f'<{self.x_r}> **{ctx.author.name}**, {cyberformat.minimalize(str(error))}')
        else:
            await ctx.message.add_reaction(self.x_r)
            await self.client.get_channel(730556685214548088).send(
                embed=discord.Embed(colour=self.client.colour, title="Error!",
                                    description=f"Error on `{ctx.command}`: {error.__class__.__name__}\n```py\n{error}```\n**Server:** {ctx.guild}\n**Author:** {ctx.author}\n[URL]({ctx.message.jump_url})"))
    
    @commands.Cog.listener(name="on_message")
    async def on_user_mention(self, message):
        owner = await self.client.fetch_user(350349365937700864)
        if "<@!697678160577429584>" == message.content:
            with open("prefixes.json", "r") as f:
                prefix = json.load(f)
                try:
                    pre = prefix[str(message.guild.id)]
                except KeyError:
                    pre = "="
                embed = discord.Embed(colour=self.client.colour,
                                      description=f'**My prefix for {message.guild} is** `{pre}`\n\n**Do** '
                                                  f'`{pre}help` **for a full list of commands.**\n\n'
                                                  f'[Invite me to your server!]'
                                                  f'(https://cybertron-5k.netlify.app/invite)\n\n[Join our help server!](https://discord.gg/aa9p43W)')
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
        embed = discord.Embed(colour=0x00ff00, title=f'{guild}',
                              description=f"**{guild.id}**"f"\n<:member:716339965771907099>**{len(guild.members):,}\n**Owner:** {guild.owner.mention}\n\n<:category:716057680548200468> **{len(categories)}** | <:text_channel:703726554018086912>**{len(text_channels)}** • <:voice_channel:703726554068418560>**{len(voice_channels)}**\n😔🤔😳 **{len(emojis)}**\n<:bot:703728026512392312> **{botno}**\n**Admins:**\n{ml}")
        embed.set_thumbnail(url=guild.icon_url)
        embed.set_footer(text=f"Guild created"
                              f"{humanize.naturaltime(__import__('datetime').datetime.utcnow() - guild.created_at)}")
        await c.send(f"Joined Guild! This is guild **#{len(self.client.guilds)}**", embed=embed)
        await guild.me.edit(nick=f"(c$) {self.client.user.name}")
        channels = sorted([t for t in guild.text_channels if t.permissions_for(guild.me).send_messages],
                          key=lambda x: x.position)
        await channels[0].send(embed=discord.Embed(color=self.client.colour,
                                                   description="Hi, thanks for inviting me! My default prefix is `c$`, but you can change it by doing `c$changeprefix <new prefix>`.\n→ [Invite](https://cybertron-5k.netlify.app/invite) | [Support](https://cybertron-5k.netlify.app/server) | <:github:724036339426787380> [GitHub](https://github.com/niztg/CyberTron5000) | <:cursor_default:734657467132411914>[Website](https://cybertron-5k.netlify.app) | <:karma:704158558547214426> [Reddit](https://reddit.com/r/CyberTron5000)\n"))
    
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
        embed = discord.Embed(colour=discord.Colour.red(), title=f'{guild}',
                              description=f"**{guild.id}**"f"\n<:member:716339965771907099>**{len(guild.members):,}**\n**Owner:** {guild.owner.mention}\n\n<:category:716057680548200468> **{len(categories)}** | <:text_channel:703726554018086912>**{len(text_channels)}** • <:voice_channel:703726554068418560>**{len(voice_channels)}**\n😔🤔😳 **{len(emojis)}**\n<:bot:703728026512392312> **{botno}**\n**Admins:**{ml}")
        embed.set_thumbnail(url=guild.icon_url)
        embed.set_footer(
            text=f"Guild created {humanize.naturaltime(__import__('datetime').datetime.utcnow() - guild.created_at)}")
        await c.send(f"Left guild. We're down to **{len(self.client.guilds)}** guilds", embed=embed)
    
    @commands.Cog.listener(name="on_message")
    async def cleverbot_session(self, message):
        if (message.channel.id == 730486269468999741) or (message.channel.id == 730570845013147708):
            if message.author == self.client.user:
                return
            async with message.channel.typing():
                if len(message.content) < 2 or len(message.content) > 100:
                    return await message.channel.send(
                        f"**{message.author.name}**, text must be below 100 characters and over 2.")
                resp = await self.bot.ask(message.content, message.author.id)
                r = str(resp) if str(resp).startswith("I") else cyberformat.minimalize(str(resp))
                if str(r)[-1] not in ['.', '?', '!']:
                    suff = "?" if any(s in str(r) for s in ['who', 'what', 'when', 'where', 'why', 'how']) else "."
                else:
                    suff = "\u200b"
                send = cyberformat.hyper_replace(str(r), old=[' i ', "i'm", "i'll"], new=[' I ', "I'm", "I'll"])
                await message.channel.send(f"**{message.author.name}**, {send}{suff}")


def setup(client):
    client.add_cog(Events(client))
