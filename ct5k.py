import datetime
import json
import os

import discord
import humanize
from discord.ext import commands

colour = 0x00dcff

# ⤗

REGIONS = {
    "europe": "Europe",
    "us-east": "US-East",
    "india": "India",
    "brazil": "Brazil",
    "japan": "Japan",
    "russia": "Russia",
    "singapore": "Singapore",
    "southafrica": "South Africa",
    "sydney": "Sydney",
    "hongkong": "Hong Kong",
    "us-central": "US-Central",
    "us-south": "US-South",
    "us-west": "US-West"
}


def check_guild(guild):
    def predicate(ctx):
        if ctx.guild.id == guild:
            return True
        else:
            return False
    
    return commands.check(predicate)


def get_token():
    with open("secrets.txt", "r") as f:
        secrets = f.readlines()
        return secrets[0].strip()


def check_admin_or_owner():
    def predicate(ctx):
        if ctx.message.author.id == 350349365937700864:
            return True
        elif ctx.message.author.permissions_in(channel=ctx.message.channel).administrator:
            return True
        elif ctx.message.author.id == 675806911194464306:
            return False
        else:
            return False
    
    return commands.check(predicate)


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
    owner = client.get_user(id=350349365937700864)
    mod_list = [member for member in guild.members if member.guild_permissions.administrator]
    ml = "\n".join([f"{member.mention} • `{member.top_role.name}`" for member in mod_list if member.bot is False])
    with open("prefixes.json", "r") as f:
        prefixes = json.load(f)
    
    prefixes[str(guild.id)] = "="
    
    with open("prefixes.json", "w") as f:
        json.dump(prefixes, f, indent=4)
        
        online = 0
        offline = 0
        idle = 0
        dnd = 0
        botno = 0
        for member in guild.members:
            if str(member.status) == "online":
                online += 1
            elif str(member.status) == "offline":
                offline += 1
            elif str(member.status) == "dnd":
                dnd += 1
            elif str(member.status) == "idle":
                idle += 1
        for member in guild.members:
            if member.bot is True:
                botno += 1
        text_channels = [text_channel for text_channel in guild.text_channels]
        voice_channels = [voice_channel for voice_channel in guild.voice_channels]
        categories = [category for category in guild.categories]
        emojis = [emoji for emoji in guild.emojis]
        region = REGIONS[f"{str(guild.region)}"]
        embed = discord.Embed(colour=colour, title=f'{guild}', description=f"**{guild.id}**"
                                                                           f"\n<:member:716339965771907099>**{len(guild.members):,}** | <:online:703903072824459265>**{online:,}** • <:dnd:703903073315192832>**{dnd:,}** • <:idle:703903072836911105>**{idle:,}** • <:offline:703918395518746735>**{offline:,}**\n**Owner:** {guild.owner.mention}\n**Region:** {region}\n\n<:category:716057680548200468> **{len(categories)}** | <:text_channel:703726554018086912>**{len(text_channels)}** • <:voice_channel:703726554068418560>**{len(voice_channels)}**\n😔🤔😳 **{len(emojis)}**\n<:bot:703728026512392312> **{botno}**\n**Admins:**\n{ml}")
        
        embed.set_thumbnail(url=guild.icon_url)
        embed.set_footer(
            text=f"Guild created {humanize.naturaltime(datetime.datetime.utcnow() - guild.created_at)}")
        await owner.send("Joined Guild!", embed=embed)
        await guild.me.edit(nick=f"(=) {client.user.name}")


@client.event
async def on_guild_remove(guild):
    owner = client.get_user(id=350349365937700864)
    with open("prefixes.json", "r") as f:
        prefixes = json.load(f)
    
    prefixes.pop(str(guild.id))
    
    with open("prefixes.json", "w") as f:
        json.dump(prefixes, f, indent=4)
    
    online = 0
    offline = 0
    idle = 0
    dnd = 0
    botno = 0
    for member in guild.members:
        if str(member.status) == "online":
            online = online + 1
        elif str(member.status) == "offline":
            offline = offline + 1
        elif str(member.status) == "dnd":
            dnd = dnd + 1
        elif str(member.status) == "idle":
            idle = idle + 1
    for member in guild.members:
        if member.bot is True:
            botno = botno + 1
    text_channels = [text_channel for text_channel in guild.text_channels]
    voice_channels = [voice_channel for voice_channel in guild.voice_channels]
    categories = [category for category in guild.categories]
    emojis = [emoji for emoji in guild.emojis]
    region = REGIONS[f"{str(guild.region)}"]
    embed = discord.Embed(colour=colour, title=f'{guild}', description=f"**{guild.id}**"
                                                                       f"\n<:member:716339965771907099>**{len(guild.members):,}** | <:online:703903072824459265>**{online:,}** • <:dnd:703903073315192832>**{dnd:,}** • <:idle:703903072836911105>**{idle:,}** • <:offline:703918395518746735>**{offline:,}**\n**Owner:** {guild.owner.mention}\n**Region:** {region}\n\n<:category:716057680548200468> **{len(categories)}** | <:text_channel:703726554018086912>**{len(text_channels)}** • <:voice_channel:703726554068418560>**{len(voice_channels)}**\n😔🤔😳 **{len(emojis)}**\n<:bot:703728026512392312> **{botno}**")
    embed.set_thumbnail(url=guild.icon_url)
    embed.set_footer(
        text=f"Guild created {humanize.naturaltime(datetime.datetime.utcnow() - guild.created_at)}")
    await owner.send("Left guild.", embed=embed)


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
    for filename in os.listdir('./cogs'):
        if filename.endswith('.py'):
            client.load_extension(f'cogs.{filename[:-3]}')
    
    print("All cogs preloaded")
    await client.change_presence(
        activity=discord.Activity(type=discord.ActivityType.watching, name=f"{len(client.users):,} users"))
    print("botttttttttttt ready")


# Reaction Roles for Vibe School

@client.event
async def on_raw_reaction_add(payload):
    message_id = payload.message_id
    if message_id == 708807550782406716:
        guild_id = payload.guild_id
        guild = discord.utils.find(lambda g: g.id == guild_id, client.guilds)
        
        if payload.emoji.name == "discordpy":
            role = discord.utils.get(guild.roles, name="Bot Updates")
        else:
            role = discord.utils.get(guild.roles, name=payload.emoji.name)
        
        if role is not None:
            member = discord.utils.find(lambda m: m.id == payload.user_id, guild.members)
            if member is not None:
                await member.add_roles(role)
                await member.send(f"Role added: {role}")
            else:
                print("Bruh")
        else:
            print("role not found")
    
    elif message_id == 708806388947746858:
        guild_id = payload.guild_id
        guild = discord.utils.find(lambda g: g.id == guild_id, client.guilds)
        
        role = discord.utils.get(guild.roles, name=payload.emoji.name)
        
        if role is not None:
            member = discord.utils.find(lambda m: m.id == payload.user_id, guild.members)
            if member is not None:
                await member.add_roles(role)
                print("Success!")
            else:
                print("Bruh")
        else:
            print("role not found")
    
    elif message_id == 709969815254597703:
        guild_id = payload.guild_id
        guild = discord.utils.find(lambda g: g.id == guild_id, client.guilds)
        
        role = discord.utils.get(guild.roles, name=payload.emoji.name)
        
        if role is not None:
            member = discord.utils.find(lambda m: m.id == payload.user_id, guild.members)
            if member is not None:
                await member.add_roles(role)
                print("Success!")
            else:
                print("Bruh")
        else:
            print("role not found")
            
            # 712490824272969808
    
    elif message_id == 712490824272969808:
        try:
            guild_id = payload.guild_id
            guild = discord.utils.find(lambda g: g.id == guild_id, client.guilds)
            
            role = discord.utils.get(guild.roles, name=payload.emoji.name)
            
            if role is not None:
                member = discord.utils.find(lambda m: m.id == payload.user_id, guild.members)
                if member is not None:
                    await member.add_roles(role)
                    print("Success!")
                else:
                    print("Bruh")
            else:
                print("role not found")
        except Exception as error:
            raise error
    
    elif message_id == 716477091520184397:
        try:
            guild_id = payload.guild_id
            guild = discord.utils.find(lambda g: g.id == guild_id, client.guilds)
            
            if payload.emoji.name == "ServerUpdates":
                role = discord.utils.get(guild.roles, name="Server Updates")
            else:
                role = discord.utils.get(guild.roles, name=payload.emoji.name)
            
            if role is not None:
                member = discord.utils.find(lambda m: m.id == payload.user_id, guild.members)
                if member is not None:
                    await member.add_roles(role)
                    await member.send("You will now be updated for CyberTron5000 announcements")
                else:
                    print("Bruh")
            else:
                print("role not found")
        except Exception as error:
            raise error
    
    # 716477091520184397


@client.event
async def on_raw_reaction_remove(payload):
    message_id = payload.message_id
    if message_id == 708807550782406716:
        guild_id = payload.guild_id
        guild = discord.utils.find(lambda g: g.id == guild_id, client.guilds)
        
        if payload.emoji.name == "discordpy":
            role = discord.utils.get(guild.roles, name="Bot Updates")
        else:
            role = discord.utils.get(guild.roles, name=payload.emoji.name)
        
        if role is not None:
            member = discord.utils.find(lambda m: m.id == payload.user_id, guild.members)
            if member is not None:
                await member.remove_roles(role)
                await member.send(f"Role removed: {role}")
            else:
                print("Bruh")
        else:
            print("role not found")
    
    elif message_id == 708806388947746858:
        guild_id = payload.guild_id
        guild = discord.utils.find(lambda g: g.id == guild_id, client.guilds)
        
        role = discord.utils.get(guild.roles, name=payload.emoji.name)
        
        if role is not None:
            member = discord.utils.find(lambda m: m.id == payload.user_id, guild.members)
            if member is not None:
                await member.remove_roles(role)
                print(f"{member}")
            else:
                print("Bruh")
        else:
            print("role not found")
    
    
    elif message_id == 709969815254597703:
        guild_id = payload.guild_id
        guild = discord.utils.find(lambda g: g.id == guild_id, client.guilds)
        
        role = discord.utils.get(guild.roles, name=payload.emoji.name)
        
        if role is not None:
            member = discord.utils.find(lambda m: m.id == payload.user_id, guild.members)
            if member is not None:
                await member.remove_roles(role)
                print(f"{member}")
            else:
                print("Bruh")
        else:
            print("role not found")
    
    elif message_id == 712490824272969808:
        guild_id = payload.guild_id
        guild = discord.utils.find(lambda g: g.id == guild_id, client.guilds)
        
        role = discord.utils.get(guild.roles, name=payload.emoji.name)
        
        if role is not None:
            member = discord.utils.find(lambda m: m.id == payload.user_id, guild.members)
            if member is not None:
                await member.remove_roles(role)
                print(f"{member}")
            else:
                print("Bruh")
        else:
            print("role not found")
    
    elif message_id == 716477091520184397:
        guild_id = payload.guild_id
        guild = discord.utils.find(lambda g: g.id == guild_id, client.guilds)
        
        if payload.emoji.name == "ServerUpdates":
            role = discord.utils.get(guild.roles, name="Server Updates")
        else:
            role = discord.utils.get(guild.roles, name=payload.emoji.name)
        
        if role is not None:
            member = discord.utils.find(lambda m: m.id == payload.user_id, guild.members)
            if member is not None:
                await member.remove_roles(role)
                await member.send("You will no longer be updated for CyberTron5000 announcements")
            else:
                print("Bruh")
        else:
            print("role not found")
            
# Reaction Roles Finish


@client.group(invoke_without_command=True)
async def owner(ctx, *, idea):
    """Suggest an idea for the bot."""
    owner = client.get_user(id=350349365937700864)
    try:
        await owner.send(f"Idea: ```{idea}```")
        await ctx.message.add_reaction(emoji=":GreenTick:707950252434653184")
    except Exception as error:
        await ctx.send(error)


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
