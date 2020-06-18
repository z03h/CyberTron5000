import discord
from discord.ext import commands

colour = 0x00dcff


class Info(commands.Cog):
    """Help Commands"""
    
    def __init__(self, client):
        self.client = client
    
    @commands.command()
    async def cogs(self, ctx):
        cogs = []
        for x in self.client.cogs:
            cogs.append(f"`{x}` • {self.client.cogs[x].description}")
        await ctx.send(embed=discord.Embed(colour=colour, title=f"All Cogs ({len(self.client.cogs)})",
                                           description=f"Do `{ctx.prefix}help <cog>` to know more about them!" + "\n\n" + "\n".join(
                                               cogs)))
    
    @commands.command(aliases=['?'])
    async def help(self, ctx, *, command=None):
        """≫ Shows info about the bot, a command or category"""
        pre = ctx.prefix
        footer = f"Do '{pre}help [command/cog]' for more information!"
        list_of_cogs = []
        walk_commands = []
        final_walk_command_list = []
        sc = []
        try:
            for cog in self.client.cogs:
                list_of_cogs.append(cog)
            if command:
                cmd = self.client.get_command(command)
            else:
                cmd = None
            if not command:
                cog_doc = f"• {self.client.cogs[command].__doc__}" or " "
                embed = discord.Embed(colour=colour, title=f"{self.client.user.name} Help",
                                      description=f"You can do `{pre}help [category]` for more info on a category.\nYou can also do `{pre}help [command]` for more info on a command.\n\n**<argument>** means the argument is **required**\n**[argument]** means the argument is **optional**\n**[A|B]** means it could be either **A or B**\n**[argument...]** means you can have **multiple arguments**\n")
                for cog_name, cog_object in self.client.cogs.items():
                    cmds = []
                    for cmd in cog_object.get_commands():
                        if not cmd.hidden:
                            cmds.append(cmd.name)
                    embed.add_field(name=f'≫ {cog_name} {cog_doc}', value='\u200b' + " • ".join(sorted(cmds)), inline=False)
                    embed.set_footer(text=footer)
                for wc in self.client.walk_commands():
                    if not wc.cog_name and not wc.hidden:
                        if isinstance(wc, commands.Group):
                            walk_commands.append(wc.name)
                            for scw in wc.commands:
                                sc.append(scw.name)
                        else:
                            walk_commands.append(wc.name)
                for item in walk_commands:
                    if item not in final_walk_command_list and item not in sc:
                        final_walk_command_list.append(item)
                embed.add_field(name="≫ Uncategorized Commands", value=" • ".join(sorted(final_walk_command_list)))
                await ctx.send(embed=embed)
            elif command in list_of_cogs:
                cog_doc = self.client.cogs[command].__doc__ or " "
                embed = discord.Embed(title=f"Commands in {command}", colour=colour, description=cog_doc)
                for cmd in self.client.cogs[command].get_commands():
                    help_msg = cmd.help or "No help provided for this command"
                    embed.add_field(name=f"{cmd.name} {cmd.signature}", value=help_msg, inline=False)
                    embed.set_footer(text=footer)
                await ctx.send(embed=embed)
            elif command and cmd:
                help_msg = cmd.help or "No help provided for this command"
                parent = cmd.full_parent_name
                if len(cmd.aliases) > 0:
                    aliases = '•'.join(cmd.aliases)
                    cmd_alias_format = f'[{cmd.name}•{aliases}]'
                    if parent:
                        cmd_alias_format = f'{parent} {cmd_alias_format}'
                    alias = cmd_alias_format
                else:
                    alias = cmd.name if not parent else f'{parent} {cmd.name}'
                embed = discord.Embed(title=f"{pre}{alias} {cmd.signature}", description=help_msg, colour=colour)
                embed.set_footer(text=footer + " • ↠ indicates subcommands")
                if isinstance(cmd, commands.Group):
                    for sub_cmd in cmd.commands:
                        schm = sub_cmd.help or "No help provided for this command"
                        embed.add_field(name=f"↠ {cmd.name} {sub_cmd.name} {sub_cmd.signature}", value=schm, inline=False)
                await ctx.send(embed=embed)
    
            else:
                await ctx.send(f"Command/Cog `{command}` not found!")
        except Exception as er:
            await ctx.send(er)

def setup(client):
    client.add_cog(Info(client))
