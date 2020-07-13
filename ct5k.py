"""
Aw shucks do i have to write a license? Uhh any of you can steal/copy/modify/distribute/sell this code for any purpose
whatsoever

no crediting required at all


"""

import json
import os

import discord
from discord.ext import commands

def get_token():
    with open("secrets.json", "r") as f:
        res = json.load(f)
    return res['bot_token']


# ⤗

async def get_prefix(client, message):
    with open("prefixes.json", "r") as f:
        data = json.load(f)
    if message.guild:
        try:
            pref = str(data[str(message.guild.id)])
            command_prefix = commands.when_mentioned_or(pref)(client, message)
        except KeyError:
            command_prefix = commands.when_mentioned_or("=")(client, message)
        return command_prefix
    else:
        return "="


# client = commands.Bot(command_prefix=get_prefix, pm_help=None)
# client.remove_command('help')
# client.colour = 0x00dcff


# client.load_extension("jishaku")

class CyberTron5000(commands.Bot):
    def __init__(self):
        super().__init__(command_prefix=get_prefix, pm_help=None,
                         allowed_mentions=discord.AllowedMentions(everyone=False, roles=True, users=True))
        
        self.colour = 0x00dcff
    
    async def on_guild_join(self, guild):
        with open("prefixes.json", "r") as f:
            prefixes = json.load(f)
        prefixes[str(guild.id)] = "="
        with open("prefixes.json", "w") as f:
            json.dump(prefixes, f, indent=4)
    
    async def on_guild_remove(self, guild):
        with open("prefixes.json", "r") as f:
            prefixes = json.load(f)
        prefixes.pop(str(guild.id))
        with open("prefixes.json", "w") as f:
            json.dump(prefixes, f, indent=4)
    
    async def on_ready(self):
        print("online!")
        for filename in os.listdir('cogs'):
            if filename.endswith('.py'):
                self.load_extension('cogs.{}'.format(filename[:-3]))
        print("Online!")
        await self.change_presence(
            activity=discord.Activity(type=discord.ActivityType.listening,
                                      name=f"{len(self.users):,} users in {len(self.guilds):,} guilds"))


client = CyberTron5000()
client.run(get_token())
