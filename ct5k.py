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


# ⤗


# client = commands.Bot(command_prefix=get_prefix, pm_help=None)
# client.remove_command('help')
# client.colour = 0x00dcff


# client.load_extension("jishaku")

class CyberTron5000(commands.Bot):
    def __init__(self):
        super().__init__(command_prefix=self.get_prefix, pm_help=None,
                         allowed_mentions=discord.AllowedMentions(everyone=False, roles=False, users=False), case_insensitive=True)
        
        self.colour = 0x00dcff
        self.tick = "<:tick:733458499777855538>"
        self.x = "<:x:733458444346195990>"
        self.load_extension(name='jishaku')
    
    async def create_db_pool(self):
        self.pg_con = await asyncpg.create_pool(user=get_token()['psql_user'], password=get_token()['psql_password'],
                                                database=get_token()['psql_db'])
        
    async def get_prefix(self, message):
        resp = await self.pg_con.fetch("SELECT prefix FROM prefixes WHERE guild_id = $1", message.guild.id)
        if not resp:
            await self.pg_con.execute("INSERT INTO prefixes (guild_id, prefix) VALUES ($1, $2)", message.guild.id, "c$")
            resp = await self.pg_con.fetch("SELECT prefix FROM prefixes WHERE guild_id = $1", message.guild.id)
            a = [p[0] for p in resp]
        else:
            a = [p[0] for p in resp]
        return commands.when_mentioned_or(*a)(self, message)
    
    async def on_guild_join(self, guild):
        await self.pg_con.execute("INSERT INTO prefixes (guild_id, prefix) VALUES ($1, $2)", guild.id, "c$")

    async def on_guild_remove(self, guild):
        await self.pg_con.execute("DELETE FROM prefixes WHERE guild_id = $1", guild.id)

    async def on_ready(self):
        print("online!")
        for filename in os.listdir('cogs'):
            if filename.endswith('.py'):
                self.load_extension('cogs.{}'.format(filename[:-3]))
        print("Online!")
        await self.change_presence(
            activity=discord.Activity(type=discord.ActivityType.watching,
                                      name=f"VIBE SCHOOL being rebuilt!"))


client = CyberTron5000()
client.loop.run_until_complete(client.create_db_pool())
client.run(get_token()['bot_token'])
