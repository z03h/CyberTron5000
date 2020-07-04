import discord
import itertools

from discord.ext import commands

colour = 0x00dcff


class CyberTronHelpCommand(commands.HelpCommand):
    def __init__(self):
        super().__init__(
            command_attrs={
                'help': 'Shows info about the bot, a command, or a category'
            }
        )
    
    def get_command_signature(self, command):
        parent = command.full_parent_name
        if len(command.aliases) > 0:
            aliases = '•'.join(command.aliases)
            fmt = f'{command.name}•{aliases}'
            if parent:
                fmt = f'{parent} {fmt}'
            alias = fmt
        else:
            alias = command.name if not parent else f'{parent} {command.name}'
        return f'{alias} {command.signature}'
    
    def command_not_found(self, string):
        return f"Command/category `{string}` not found!"
    
    async def send_bot_help(self, mapping):
        def key(c):
            return c.cog_name or '\u200bUncategorized Commands'
        
        total = 0
        embed = discord.Embed(colour=colour,
                              description=f'You can do `{self.clean_prefix}help [command/category]` for more info.\n\n')
        entries = await self.filter_commands(self.context.bot.commands, sort=True, key=key)
        for cog, cmds in itertools.groupby(entries, key=key):
            cats = []
            cmds = sorted(cmds, key=lambda c: c.name)
            cats.append(f'➤ **{cog}**\n{"•".join([f"`{c.name}`" for c in cmds])}\n')
            embed.description += "\n".join(cats)
            total += len([c for c in cmds])
        embed.set_author(name=f"CyberTron5000 Commands (Total {total})")
        await self.context.send(embed=embed)
    
    async def send_cog_help(self, cog):
        i = []
        cog_doc = cog.__doc__ or " "
        for cmd in cog.get_commands():
            char = "\u200b" if not cmd.aliases else "•"
            help_msg = cmd.help or "No help provided for this command"
            i.append(f"→ `{cmd.name}{char}{'•'.join(cmd.aliases)} {cmd.signature}` • {help_msg}")
        await self.context.send(
            embed=discord.Embed(colour=colour, description=cog_doc + "\n\n" + "\n".join(i)).set_author(
                name=f"{cog.qualified_name} Cog"))
    
    async def send_command_help(self, command):
        embed = discord.Embed(title=self.get_command_signature(command), colour=colour,
                              description=command.help or "No help provided for this command.")
        await self.context.send(embed=embed)
    
    async def send_group_help(self, group):
        sc = []
        u = '\u200b'
        embed = discord.Embed(title=self.get_command_signature(group), colour=colour)
        for c in group.commands:
            char = "\u200b" if not c.aliases else "•"
            sc.append(f"→ `{group.name} {c.name}{char}{'•'.join(c.aliases)} {c.signature or f'{u}'}` • {c.help}")
        embed.description = f"{group.help}\n\n" + "\n".join(sc)
        await self.context.send(embed=embed)


class Info(commands.Cog):
    """Help Commands"""
    
    def __init__(self, client):
        self.client = client
        self._original_help_command = client.help_command
        client.help_command = CyberTronHelpCommand()
        client.help_command.cog = self
    
    def cog_unload(self):
        self.client.help_command = self._original_help_command
    
    @commands.command()
    async def cogs(self, ctx):
        """Shows you every cog"""
        cogs = []
        for x in self.client.cogs:
            cogs.append(f"`{x}` • {self.client.cogs[x].description}")
        await ctx.send(embed=discord.Embed(colour=colour, title=f"All Cogs ({len(self.client.cogs)})",
                                           description=f"Do `{ctx.prefix}help <cog>` to know more about them!" + "\n\n" + "\n".join(
                                               cogs)))


def setup(client):
    client.add_cog(Info(client))
