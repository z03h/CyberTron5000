from discord.ext import commands
from cogs.utils.lists import REGIONS
from .utils import cyberformat
import discord
import async_cleverbot
import humanize
import json

colour = 0x00dcff


class Events(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.x_r = ":warning:727013811571261540"
        self.bot = async_cleverbot.Cleverbot("OVbZ10+q,G#vU_-)67/T")
        self.bot.set_context(async_cleverbot.DictContext(self.bot))

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        if isinstance(error, discord.ext.commands.CheckFailure):
            await ctx.message.add_reaction(emoji=self.x_r)
    
        elif isinstance(error, discord.ext.commands.BadArgument):
            await ctx.send(
                f"<{self.x_r}> **{ctx.author.name}**, {cyberformat.minimalize(str(error))}!")
    
        elif isinstance(error, discord.ext.commands.MissingRequiredArgument):
            await ctx.send(
                f"<{self.x_r}> **{ctx.author.name}**, you're missing the required argument **{error.param.name}**!")
    
        elif isinstance(error, discord.ext.commands.MissingPermissions):
            await ctx.send(f'<{self.x_r}> **{ctx.author.name}**, {cyberformat.minimalize(str(error))}!')
    
        elif isinstance(error, commands.CommandNotFound) or isinstance(error, commands.NotOwner):
            pass
    
        else:
            await ctx.message.add_reaction(self.x_r)
            await self.client.get_channel(730556685214548088).send(embed=discord.Embed(colour=colour, title="Error!",
                                                                                       description=f"Error on `{ctx.command}`:\n```py\n{error}```").set_author(
                name=ctx.author, icon_url=ctx.author.avatar_url))

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
        embed = discord.Embed(colour=0x00ff00, title=f'{guild}',
                              description=f"**{guild.id}**"f"\n<:member:716339965771907099>**{len(guild.members):,}\n**Owner:** {guild.owner.mention}\n**Region:** {region}\n\n<:category:716057680548200468> **{len(categories)}** | <:text_channel:703726554018086912>**{len(text_channels)}** • <:voice_channel:703726554068418560>**{len(voice_channels)}**\n😔🤔😳 **{len(emojis)}**\n<:bot:703728026512392312> **{botno}**\n**Admins:**\n{ml}")
        embed.set_thumbnail(url=guild.icon_url)
        embed.set_footer(text=f"Guild created"
                              f"{humanize.naturaltime(__import__('datetime').datetime.utcnow() - guild.created_at)}")
        await c.send(f"Joined Guild! This is guild **#{len(self.client.guilds)}**", embed=embed)
        await guild.me.edit(nick=f"(=) {self.client.user.name}")
        # stole this from dutchy ↓ ↓ ↓ https://github.com/iDutchy/Charles/blob/master/cogs/Events.py#L286-L303
        to_send = sorted([chan for chan in guild.channels if
                          chan.permissions_for(guild.me).send_messages and isinstance(chan, discord.TextChannel)],
                         key=lambda x: x.position)[0]
        if to_send.permissions_for(guild.me).embed_links:
            e = discord.Embed(colour=colour, title=self.client.user.name)
            tips = "My default prefix is `=`, but you can change it using `=changeprefix <newprefix>`\n[Join our help server for updates!](https://cybertron-5k.netlify.app/server)\n\n"
            e.description = f"Thank you for adding me to your server!\n{tips}"
            await to_send.send(embed=e)
        else:
            msg = "Thank you for adding me to your server! I will do my best to make your work here as easy as possible.\n"
            msg += "My default prefix is `=`, but you can change it using `=changeprefix <newprefix>\n[Join our help server for updates!](https://cybertron-5k.netlify.app/server)\n\n"
            await to_send.send(msg)

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
        embed = discord.Embed(colour=discord.Colour.red(), title=f'{guild}',
                              description=f"**{guild.id}**"f"\n<:member:716339965771907099>**{len(guild.members):,}**\n**Owner:** {guild.owner.mention}\n**Region:** {region}\n\n<:category:716057680548200468> **{len(categories)}** | <:text_channel:703726554018086912>**{len(text_channels)}** • <:voice_channel:703726554068418560>**{len(voice_channels)}**\n😔🤔😳 **{len(emojis)}**\n<:bot:703728026512392312> **{botno}**\n**Admins:**{ml}")
        embed.set_thumbnail(url=guild.icon_url)
        embed.set_footer(
            text=f"Guild created {humanize.naturaltime(__import__('datetime').datetime.utcnow() - guild.created_at)}")
        await c.send(f"Left guild. We're down to **{len(self.client.guilds)}** guilds", embed=embed)

    @commands.Cog.listener(name="on_message")
    async def cleverbot_session(self, message):
        if message.channel.id == 730486269468999741:
            if message.author == self.client.user:
                return
            async with message.channel.typing():
                if len(message.content) < 2 or len(message.content) > 60:
                    return await message.channel.send(
                        f"**{message.author.name}**, text must be below 60 characters and over 2.")
                resp = await self.bot.ask(message.content, message.author.id)
                r = str(resp) if str(resp).startswith("I") else cyberformat.minimalize(str(resp))
                if str(r)[-1] not in ['.', '?', '!']:
                    suff = "?" if any(s in str(r) for s in ['who', 'what', 'when', 'where', 'why', 'how']) else "."
                else:
                    suff = "\u200b"
                send = cyberformat.hyper_replace(str(r), old=[' i ', "i'm", "i'll"], new=[' I ', "I'm", "I'll"])
                await message.channel.send(f"**{message.author.name}**, {send}{suff}")
        await self.client.process_commands(message)


def setup(client):
    client.add_cog(Events(client))
