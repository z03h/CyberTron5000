import datetime
import json
import os

import discord
import humanize
from discord.ext import commands
from cogs.utils.lists import REGIONS, sl
from cogs.utils.funcs import check_admin_or_owner

colour = 0x00dcff


def get_token():
    with open("secrets.txt", "r") as f:
        secrets = f.readlines()
        return secrets[0].strip()


def prefix(client, message):
    with open("prefixes.json", 'r') as f:
        sad = json.load(f)
        if str(message.guild.id) in sad:
            return commands.when_mentioned_or(sad[str(message.guild.id)])(client, message)
        else:
            sad[str(message.guild.id)] = "="
            with open("prefixes.json", "w") as f:
                a = json.dump(sad, f, indent=4)
                return commands.when_mentioned_or(a)(client, message)


client = commands.Bot(command_prefix=prefix, pm_help=None)
client.remove_command('help')


@client.event
async def on_guild_join(guild):
    c = client.get_channel(727277234666078220)
    mod_list = [member for member in guild.members if member.guild_permissions.administrator]
    ml = "\n".join([f"{member.mention} • `{member.top_role.name}`" for member in mod_list if member.bot is False])
    with open("prefixes.json", "r") as f:
        prefixes = json.load(f)
    
    prefixes[str(guild.id)] = "="
    
    with open("prefixes.json", "w") as f:
        json.dump(prefixes, f, indent=4)
        
        online = len([member for member in guild.members if member.status == discord.Status.online])
        offline = len([member for member in guild.members if member.status == discord.Status.offline])
        idle = len([member for member in guild.members if member.status == discord.Status.idle])
        dnd = len([member for member in guild.members if member.status == discord.Status.dnd])
        botno = len([member for member in guild.members if member.bot is True])
        text_channels = [text_channel for text_channel in guild.text_channels]
        voice_channels = [voice_channel for voice_channel in guild.voice_channels]
        categories = [category for category in guild.categories]
        emojis = [emoji for emoji in guild.emojis]
        region = REGIONS[f"{str(guild.region)}"]
        embed = discord.Embed(colour=0x00ff00, title=f'{guild}',
                              description=f"**{guild.id}**"f"\n<:member:716339965771907099>**{len(guild.members):,}** | {sl['online']}**{online:,}** • {sl['dnd']}**{dnd:,}** • {sl['idle']}**{idle:,}** • {sl['offline']}**{offline:,}**\n**Owner:** {guild.owner.mention}\n**Region:** {region}\n\n<:category:716057680548200468> **{len(categories)}** | <:text_channel:703726554018086912>**{len(text_channels)}** • <:voice_channel:703726554068418560>**{len(voice_channels)}**\n😔🤔😳 **{len(emojis)}**\n<:bot:703728026512392312> **{botno}**\n**Admins:**\n{ml}")
        embed.set_thumbnail(url=guild.icon_url)
        embed.set_footer(
            text=f"Guild created {humanize.naturaltime(datetime.datetime.utcnow() - guild.created_at)}")
        await c.send(f"Joined Guild! This is guild **#{len(client.guilds)}**", embed=embed)
        await guild.me.edit(nick=f"(=) {client.user.name}")


@client.event
async def on_guild_remove(guild):
    c = client.get_channel(727277234666078220)
    with open("prefixes.json", "r") as f:
        prefixes = json.load(f)
    
    prefixes.pop(str(guild.id))
    
    with open("prefixes.json", "w") as f:
        json.dump(prefixes, f, indent=4)
    
    online = len([member for member in guild.members if member.status == discord.Status.online])
    offline = len([member for member in guild.members if member.status == discord.Status.offline])
    idle = len([member for member in guild.members if member.status == discord.Status.idle])
    dnd = len([member for member in guild.members if member.status == discord.Status.dnd])
    botno = len([member for member in guild.members if member.bot is True])
    text_channels = [text_channel for text_channel in guild.text_channels]
    voice_channels = [voice_channel for voice_channel in guild.voice_channels]
    categories = [category for category in guild.categories]
    emojis = [emoji for emoji in guild.emojis]
    region = REGIONS[f"{str(guild.region)}"]
    embed = discord.Embed(colour=discord.Colour.red(), title=f'{guild}',
                          description=f"**{guild.id}**"f"\n<:member:716339965771907099>**{len(guild.members):,}** | {sl['online']}**{online:,}** • {sl['dnd']}**{dnd:,}** • {sl['idle']}**{idle:,}** • {sl['offline']}**{offline:,}**\n**Owner:** {guild.owner.mention}\n**Region:** {region}\n\n<:category:716057680548200468> **{len(categories)}** | <:text_channel:703726554018086912>**{len(text_channels)}** • <:voice_channel:703726554068418560>**{len(voice_channels)}**\n😔🤔😳 **{len(emojis)}**\n<:bot:703728026512392312> **{botno}**\n**Admins:**")
    embed.set_thumbnail(url=guild.icon_url)
    embed.set_footer(text=f"Guild created {humanize.naturaltime(datetime.datetime.utcnow() - guild.created_at)}")
    await c.send(f"Left guild. We're down to **{len(client.guilds)}** guilds", embed=embed)


@client.group(invoke_without_command=True, help="Change the guild's prefix", aliases=['prefix', 'pre'])
@check_admin_or_owner()
async def changeprefix(ctx, *, prefix):
    with open("prefixes.json", "r") as f:
        prefixes = json.load(f)
    
    prefixes[str(ctx.guild.id)] = prefix
    
    with open("prefixes.json", "w") as f:
        json.dump(prefixes, f, indent=4)
    await ctx.message.add_reaction(emoji=":GreenTick:707950252434653184")
    await ctx.guild.me.edit(nick=f"({prefix}) {client.user.name}")


@changeprefix.command(invoke_without_command=True, help="Make your prefix end in a space.", aliases=['sp'])
@check_admin_or_owner()
async def spaceprefix(ctx, *, prefix):
    with open("prefixes.json", "r") as f:
        prefixes = json.load(f)
    
    prefixes[str(ctx.guild.id)] = f"{prefix} "
    
    with open("prefixes.json", "w") as f:
        json.dump(prefixes, f, indent=4)
    await ctx.message.add_reaction(emoji=":GreenTick:707950252434653184")
    await ctx.guild.me.edit(nick=f"({prefix}) {client.user.name}")


@client.event
async def on_ready():
    c = client.get_channel(727277234666078220)
    for filename in os.listdir('./cogs'):
        if filename.endswith('.py'):
            client.load_extension(f'cogs.{filename[:-3]}')
    print("Online!")
    msg = await c.send("** **")
    await msg.edit(embed=discord.Embed(colour=colour, title=f"CyberTron5000 logging in for {msg.created_at}",
                                       description=f"Logged in as: {client.user.name}\nDiscriminator: {client.user.discriminator}\nID: {client.user.id}\nVisible Guilds: {len(client.guilds):,}\nVisible Users: {len(client.users):,}\n"))
    await client.change_presence(
        activity=discord.Activity(type=discord.ActivityType.listening,
                                  name=f"to {len(client.users)} users in {len(client.guilds)} guilds"))


@client.group(invoke_without_command=True)
async def owner(ctx, *, idea):
    """Suggest an idea for the bot."""
    owner = client.get_user(id=350349365937700864)
    await owner.send(f"Idea: ```{idea}```")
    await ctx.message.add_reaction(emoji=":GreenTick:707950252434653184")


@owner.command(invoke_without_command=True)
async def error(ctx, *, error):
    """Report an error for this bot."""
    owner = client.get_user(id=350349365937700864)
    await owner.send(f"You should fix ```{error}```")
    await ctx.message.add_reaction(emoji=":GreenTick:707950252434653184")


@client.command(help="Loads Cogs.")
@commands.is_owner()
async def load(ctx, extension=None):
    if not extension:
        for filename in os.listdir('./cogs'):
            if filename.endswith('.py'):
                client.load_extension(f'cogs.{filename[:-3]}')
        
        await ctx.message.add_reaction(emoji=":GreenTick:707950252434653184")
    
    else:
        client.load_extension(f'cogs.{extension}')
        await ctx.message.add_reaction(emoji=":GreenTick:707950252434653184")


@client.command(help="Unloads Cogs.")
@commands.is_owner()
async def unload(ctx, extension=None):
    if not extension:
        for filename in os.listdir('./cogs'):
            if filename.endswith('.py'):
                client.unload_extension(f'cogs.{filename[:-3]}')
        
        await ctx.message.add_reaction(emoji=":GreenTick:707950252434653184")
    
    else:
        client.unload_extension(f'cogs.{extension}')
        await ctx.message.add_reaction(emoji=":GreenTick:707950252434653184")


@client.command(help="Reloads Cogs")
@commands.is_owner()
async def reload(ctx, extension=None):
    if not extension:
        for filename in os.listdir('./cogs'):
            if filename.endswith('.py'):
                client.unload_extension(f'cogs.{filename[:-3]}')
                client.load_extension(f'cogs.{filename[:-3]}')
        
        await ctx.message.add_reaction(emoji=":GreenTick:707950252434653184")
    
    else:
        client.unload_extension(f'cogs.{extension}')
        client.load_extension(f'cogs.{extension}')
        await ctx.message.add_reaction(emoji=":GreenTick:707950252434653184")


client.run(get_token())

# yeet yeet yeet 1995
