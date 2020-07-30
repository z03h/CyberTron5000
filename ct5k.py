
"""
CyberTron5000 Discord Bot
Copyright (C) 2020  nizcomix
This program is free software: you can redistribute it and/or modify
it under the terms of the GNU Affero General Public License as
published by the Free Software Foundation, either version 3 of the
License, or (at your option) any later version.
This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU Affero General Public License for more details.
You should have received a copy of the GNU Affero General Public License
along with this program.  If not, see <https://www.gnu.org/licenses/>.
"""

import json
import os

import asyncpg
import discord
from discord.ext import commands
print(discord.__version__)


def get_token():
    with open("secrets.json", "r") as f:
        res = json.load(f)
    return res

class CyberTron5000(commands.Bot):
    def __init__(self):
        super().__init__(command_prefix=self.get_prefix, pm_help=None,
                         allowed_mentions=discord.AllowedMentions(everyone=False, roles=False, users=False), case_insensitive=True,
                         activity=discord.Activity(type=discord.ActivityType.watching, name=f"VIBE SCHOOL being rebuilt!"))
        
        self.colour = 0x00dcff
        self.tick = "<:tick:733458499777855538>"
        self.x = "<:x:733458444346195990>"
        self.load_extension(name='jishaku')
        self.ready = False
        self.prefixes = {}
        self.cmd_usage = {}
    
    async def create_db_pool(self):
        tokens = get_token()
        self.pg_con = await asyncpg.create_pool(user=tokens['psql_user'], password=tokens['psql_password'],
                                                database=tokens['psql_db'])
        
    async def get_prefix(self, message):
        DEFAULT_PREFIX = ["c$"]
        prefixes = self.prefixes.get(message.guild.id, DEFAULT_PREFIX)
        return commands.when_mentioned_or(*prefixes)(self, message)
    
    async def on_guild_join(self, guild):
        await self.pg_con.execute("INSERT INTO prefixes (guild_id, prefix) VALUES ($1, $2)", guild.id, "c$")
        self.prefixes[guild.id] = ['c$']

    async def on_guild_remove(self, guild):
        await self.pg_con.execute("DELETE FROM prefixes WHERE guild_id = $1", guild.id)
        self.prefixes.pop(guild.id)

    async def on_ready(self):
        if not self.ready:
            print("online!")
            for filename in os.listdir('cogs'):
                if filename.endswith('.py'):
                    self.load_extension('cogs.{}'.format(filename[:-3]))
            print("Online!")
            prefix_data = await self.pg_con.fetch("SELECT guild_id, array_agg(prefix) FROM prefixes GROUP BY guild_id")
            for entry in prefix_data:
                self.prefixes[entry['guild_id']] = entry['array_agg']
            self.ready = True

    async def on_command(self, ctx):
        try:
            self.cmd_usage[str(ctx.command)] += 1
        except KeyError:
            self.cmd_usage[str(ctx.command)] = 1

client = CyberTron5000()
client.loop.run_until_complete(client.create_db_pool())
client.run(get_token()['bot_token'])
