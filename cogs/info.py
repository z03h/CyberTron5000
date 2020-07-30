import itertools

import discord
from discord.ext import commands

from .utils import paginator


class CyberTronHelpCommand(commands.HelpCommand):
    """
    Subclassed help FTW!
    """
    
    def __init__(self):
        """
        Sets some attributes.
        """
        super().__init__(
            command_attrs={
                'help': 'Shows info about the bot, a command, or a category',
                'aliases': ['?']
            }
        )
        self._help_dict = {"<argument>": "This means the argument is **required**",
                           "[argument]": "This means the argument is **optional**",
                           "[A|B]": "This means it could be either **A or B**",
                           "[argument...]": "This means you can have **multiple arguments**"}
    
    def get_command_signature(self, command):
        """
        Copied from R.Danny ;picardy;
        Formats the command signature for command help.
        :param command:
        :return:
        """
        parent = command.full_parent_name
        if len(command.aliases) > 0:
            aliases = '•'.join(command.aliases)
            fmt = f'[{command.name}•{aliases}]'
            if parent:
                fmt = f'{parent} {fmt}'
            alias = fmt
        else:
            alias = command.name if not parent else f'{parent} {command.name}'
        return f'{alias} {command.signature}'
    
    def command_not_found(self, string):
        """
        Just makes a custom error when command is not found.
        :param string:
        :return:
        """
        return f"Command/category `{string}` not found!"
    
    async def send_bot_help(self, mapping):
        """
        Sends the actual help message
        :param mapping:
        :return:
        """
        
        def key(c):
            return c.cog_name or '\u200bUncategorized Commands'
        
        total = 0
        embed = discord.Embed(colour=self.context.bot.colour,
                              description=f'You can do `{self.clean_prefix}help [command/category]` for more info.\n\n')
        entries = await self.filter_commands(self.context.bot.commands, sort=True, key=key)
        for cg, cm in itertools.groupby(entries, key=key):
            cats = []
            cm = sorted(cm, key=lambda c: c.name)
            cats.append(f'**{cg}**\n{" • ".join([f"{c.name}" for c in cm])}\n')
            embed.description += "\n".join(cats)
            total += len([c for c in cm])
        embed.set_author(name=f"CyberTron5000 Commands (Total {total})")
        await self.context.send(embed=embed)
    
    async def send_cog_help(self, cog):
        """
        Help for a cog.
        :param cog:
        :return:
        """
        cog_doc = cog.__doc__ or " "
        entries = await self.filter_commands(cog.get_commands(), sort=True)
        foo = [f"→ `{c.name} {c.signature}` | {c.help or 'No help provided for this command'}" for c in entries]
        embed = discord.Embed(description=f"{cog_doc}", colour=self.context.bot.colour).set_author(
            name=f"{cog.qualified_name} Commands (Total {len(entries)})")
        if entries:
            source = paginator.IndexedListSource(show_index=False, embed=embed, data=foo, per_page=6, title='Commands')
            menu = paginator.CatchAllMenu(source=source)
            menu.add_info_fields(self._help_dict)
            await menu.start(self.context)
        else:
            await self.context.send(embed=embed)
    
    async def send_command_help(self, command):
        """
        Help for a command.
        :param command:
        :return:
        """
        embed = discord.Embed(title=self.get_command_signature(command), colour=self.context.bot.colour,
                              description=command.help or "No help provided for this command.")
        await self.context.send(embed=embed)
    
    async def send_group_help(self, group):
        """
        Help for a subcommand group.
        :param group:
        :return:
        """
        sc = []
        u = '\u200b'
        entries = await self.filter_commands(group.commands)
        embed = discord.Embed(title=self.get_command_signature(group), colour=self.context.bot.colour)
        for c in entries:
            char = "\u200b" if not c.aliases else "|"
            sc.append(f"→ `{group.name} {c.name}{char}{'|'.join(c.aliases)} {c.signature or f'{u}'}` | {c.help}")
        embed.description = f"{group.help}"
        if entries:
            source = paginator.IndexedListSource(show_index=False, data=sc, embed=embed, per_page=6,
                                                 title='Subcommands')
            menu = paginator.CatchAllMenu(source=source)
            menu.add_info_fields(self._help_dict)
            await menu.start(self.context)
        else:
            await self.context.send(embed=embed)


class Info(commands.Cog):
    """Help Commands"""
    
    def __init__(self, client):
        """
        Sets up the whole help command thing
        :param client:
        """
        self.client = client
        self._original_help_command = client.help_command
        client.help_command = CyberTronHelpCommand()
        client.help_command.cog = self
    
    def cog_unload(self):
        """
        ah yes, this.
        :return:
        """
        self.client.help_command = self._original_help_command
    
    @commands.group(invoke_without_command=True)
    async def cogs(self, ctx):
        """Shows you every cog"""
        await ctx.send(embed=discord.Embed(colour=self.client.colour, title=f"All Cogs ({len(self.client.cogs)})",
                                           description=f"Do `{ctx.prefix}help <cog>` to know more about them!" + "\n\n" + "\n".join(
                                               [i for i in self.client.cogs.keys()])))
    
    @cogs.command()
    @commands.is_owner()
    async def status(self, ctx):
        """Shows you the status of each cog"""
        cogs = []
        for filename in __import__('os').listdir('cogs'):
            if filename.endswith('.py'):
                try:
                    self.client.reload_extension(f'cogs.{filename[:-3]}')
                    cogs.append(f"<:on:732805104620797965> `cogs.{filename[:-3]}`")
                except commands.ExtensionNotLoaded:
                    cogs.append(f"<:off:732805190582927410> `cogs.{filename[:-3]}`")
        
        embed = discord.Embed(colour=self.client.colour)
        embed.description = "\n".join(cogs)
        await ctx.send(embed=embed)
    
    @commands.command(name='paginated_help', aliases=['phelp'])
    async def phelp(self, ctx, *, command=None):
        """
        If you don't like the regular help command

        """
        embeds = []
        use = self.client.get_command(command) if command else None
        lcogs = [str(cog) for cog in self.client.cogs]
        if not command:
            for name, obj in self.client.cogs.items():
                embed = discord.Embed(title=f"{name} Commands", colour=self.client.colour)
                cmds = []
                for cmd in obj.get_commands():
                    cmds.append(f"→ `{cmd.name} {cmd.signature}` | {cmd.help}")
                embed.description = '\n'.join(cmds)
                if cmds:
                    embeds.append(embed)
                else:
                    continue
            pages = paginator.CatchAllMenu(paginator.EmbedSource([discord.Embed(colour=self.client.colour,
                                                                                title=f'{self.client.user.name} Help',
                                                                                description=f'Do `{ctx.prefix}help command/cog` for more info').set_image(
                url=self.client.user.avatar_url)] + embeds))
            await pages.start(ctx)
        elif command in lcogs:
            embed = discord.Embed(colour=self.client.colour, title=f'{command.capitalize()} Help')
            embed.description = '\n'.join(
                [f"→ `{cmd.name} {cmd.signature}` | {cmd.help}" for cmd in self.client.cogs[command].get_commands()])
            await ctx.send(embed=embed)
        elif command and use:
            help_msg = use.help or "No help provided for this command"
            parent = use.full_parent_name
            if len(use.aliases) > 0:
                aliases = '|'.join(use.aliases)
                cmd_alias_format = f'{use.name}|{aliases}'
                if parent:
                    cmd_alias_format = f'{parent} {cmd_alias_format}'
                alias = cmd_alias_format
            else:
                alias = use.name if not parent else f'{parent} {use.name}'
            embed = discord.Embed(title=f"{alias} {use.signature}", description=help_msg, colour=self.client.colour)
            if isinstance(use, commands.Group):
                embed = discord.Embed(title=f"{alias} {use.signature}", description=help_msg,
                                      colour=self.client.colour)
                for sub_cmd in use.commands:
                    u = '\u200b'
                    embed.add_field(
                        name=f"{use.name} {sub_cmd.name}{'|' if sub_cmd.aliases else u}{'| '.join(sub_cmd.aliases)} {sub_cmd.signature}",
                        value=f"{sub_cmd.help}", inline=False)
                await ctx.send(embed=embed)
            else:
                await ctx.send(embed=embed)
        elif command not in lcogs or command and not use:
            await ctx.send("not found")


def setup(client):
    client.add_cog(Info(client))
