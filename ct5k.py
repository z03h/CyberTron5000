"""
CyberTron5000 is free and unencumbered software released into the public domain.

Anyone is free to copy, modify, publish, use, compile, sell, or
distribute this software, either in source code form or as a compiled
binary, for any purpose, commercial or non-commercial, and by any
means.

In jurisdictions that recognize copyright laws, the author or authors
of this software dedicate any and all copyright interest in the
software to the public domain. We make this dedication for the benefit
of the public at large and to the detriment of our heirs and
successors. We intend this dedication to be an overt act of
relinquishment in perpetuity of all present and future rights to this
software under copyright law.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
IN NO EVENT SHALL THE AUTHORS BE LIABLE FOR ANY CLAIM, DAMAGES OR
OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE,
ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR
OTHER DEALINGS IN THE SOFTWARE.

For more information, please refer to <https://unlicense.org>
"""

import json
import os
import asyncpg

import discord
from discord.ext import commands

def get_token():
    with open("secrets.json", "r") as f:
        res = json.load(f)
    return res


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
        
    async def create_db_pool(self):
        self.pg_con = await asyncpg.create_pool(user='postgres', password=get_token()['psql_password'], database='MyDB')
    
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
client.loop.run_until_complete(client.create_db_pool())
client.run(get_token()['bot_token'])
