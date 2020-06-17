import asyncio
import itertools

import discord
from discord.ext import commands

from .utils.paginator import Pages

colour = 0x00dcff


class HelpPaginator(Pages):
    def __init__(self, help_command, ctx, entries, *, per_page=6):
        super().__init__(ctx, entries=entries, per_page=per_page)
        self.reaction_emojis.append(('\N{WHITE QUESTION MARK ORNAMENT}', self.show_bot_help))
        self.total = len(entries)
        self.help_command = help_command
        self.prefix = help_command.clean_prefix
        self.is_bot = False
    
    def get_bot_page(self, page):
        cog, description, commands = self.entries[page - 1]
        self.title = f'{cog} Commands'
        self.description = description
        return commands
    
    def prepare_embed(self, entries, page, *, first=False):
        self.embed.clear_fields()
        self.embed.description = self.description
        self.embed.title = self.title
        
        self.embed.set_footer(text=f'Use "{self.prefix}help <command/cog>" for more info!')
        
        for entry in entries:
            signature = f'{entry.qualified_name} {entry.signature}'
            self.embed.add_field(name=signature, value=entry.short_doc or "No help given", inline=False)
        
        if self.maximum_pages:
            self.embed.set_author(name=f'Page {page}/{self.maximum_pages} ({self.total} commands)')
    
    async def show_help(self):
        """shows this message"""
        
        self.embed.title = 'Paginator help'
        self.embed.description = 'Hello! Welcome to the help page.'
        
        messages = [f'{emoji} {func.__doc__}' for emoji, func in self.reaction_emojis]
        self.embed.clear_fields()
        self.embed.add_field(name='What are these reactions for?', value='\n'.join(messages), inline=False)
        
        self.embed.set_footer(text=f'We were on page {self.current_page} before this message.')
        await self.message.edit(embed=self.embed)
        
        async def go_back_to_current_page():
            await asyncio.sleep(30.0)
            await self.show_current_page()
        
        self.bot.loop.create_task(go_back_to_current_page())
    
    async def show_bot_help(self):
        """shows how to use the bot"""
        
        self.embed.title = 'Using the bot'
        self.embed.description = 'Hello! Welcome to the help page.'
        self.embed.clear_fields()
        
        entries = (
            ('<argument>', 'This means the argument is __**required**__.'),
            ('[argument]', 'This means the argument is __**optional**__.'),
            ('[A|B]', 'This means that it can be __**either A or B**__.'),
            ('[argument...]', 'This means you can have multiple arguments.\n')
        )
        
        self.embed.add_field(name='How do I use this bot?', value='Reading the bot signature is pretty simple.')
        
        for name, value in entries:
            self.embed.add_field(name=name, value=value, inline=False)
        
        self.embed.set_footer(text=f'We were on page {self.current_page} before this message.')
        await self.message.edit(embed=self.embed)
        
        async def go_back_to_current_page():
            await asyncio.sleep(30.0)
            await self.show_current_page()
        
        self.bot.loop.create_task(go_back_to_current_page())


class PaginatedHelpCommand(commands.HelpCommand):
    def __init__(self):
        super().__init__(command_attrs={
            'cooldown': commands.Cooldown(1, 3.0, commands.BucketType.member),
            'help': '≫ Shows help about the bot, a command, or a category'
        })
    
    async def on_help_command_error(self, ctx, error):
        if isinstance(error, commands.CommandInvokeError):
            await ctx.send(str(error.original))
    
    def get_command_signature(self, command):
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
    
    async def send_bot_help(self, mapping):
        def key(c):
            return c.cog_name or '\u200bNo Category'
        
        bot = self.context.bot
        entries = await self.filter_commands(bot.commands, sort=True, key=key)
        nested_pages = []
        per_page = 6
        total = 0
        
        for cog, commands in itertools.groupby(entries, key=key):
            commands = sorted(commands, key=lambda c: c.name)
            if len(commands) == 0:
                continue
            
            total += len(commands)
            actual_cog = bot.get_cog(cog)
            # get the description if it exists (and the cog is valid) or return Empty embed.
            description = (actual_cog and actual_cog.description) or discord.Embed.Empty
            nested_pages.extend((cog, description, commands[i:i + per_page]) for i in range(0, len(commands), per_page))
        
        # a value of 1 forces the pagination session
        pages = HelpPaginator(self, self.context, nested_pages, per_page=1)
        
        # swap the get_page implementation to work with our nested pages.
        pages.get_page = pages.get_bot_page
        pages.is_bot = True
        pages.total = total
        await pages.paginate()
    
    async def send_cog_help(self, cog):
        entries = await self.filter_commands(cog.get_commands(), sort=True)
        pages = HelpPaginator(self, self.context, entries)
        pages.title = f'{cog.qualified_name} Commands'
        pages.description = cog.description
        
        await pages.paginate()
    
    def common_command_formatting(self, page_or_embed, command):
        page_or_embed.title = self.get_command_signature(command)
        if command.description:
            page_or_embed.description = f'{command.description}\n\n{command.help}'
        else:
            page_or_embed.description = command.help or 'Help not provided.'
    
    async def send_command_help(self, command):
        # No pagination necessary for a single command.
        embed = discord.Embed(colour=0x00dcff)
        self.common_command_formatting(embed, command)
        await self.context.send(embed=embed)
    
    async def send_group_help(self, group):
        subcommands = group.commands
        if len(subcommands) == 0:
            return await self.send_command_help(group)
        
        entries = await self.filter_commands(subcommands, sort=True)
        pages = HelpPaginator(self, self.context, entries)
        self.common_command_formatting(pages, group)
        
        await pages.paginate()


class Info(commands.Cog):
    """Help Commands"""
    def __init__(self, client):
        self.client = client
        self.old_help_command = client.help_command
        client.help_command = PaginatedHelpCommand()
        client.help_command.cog = self
    
    def cog_unload(self):
        self.client.help_command = self.old_help_command
    
    @commands.command(help="≫ Shows you every cog")
    async def cogs(self, ctx):
        cogs = []
        for x in self.client.cogs:
            cogs.append(f"`{x}` • {self.client.cogs[x].description}")
        await ctx.send(embed=discord.Embed(colour=colour, title=f"All Cogs ({len(self.client.cogs)})",
                                           description=f"Do `{ctx.prefix}help <cog>` to know more about them!" + "\n\n" + "\n".join(cogs)))
    
    @commands.command(name="?", hidden=True)
    async def second_help(self, ctx, *cog):
        global halp
        try:
            walk_commands = []
            final_walk_command_list = []
            if not cog:
                """Cog listing.  What more?"""
                halp = discord.Embed(title='Help',
                                     description=f'Use `{ctx.prefix}help <cog>` to find out more about them!)',
                                     colour=colour)
                for y in self.client.walk_commands():
                    if not y.cog_name and not y.hidden:
                        walk_commands.append(f'`{y}`')
                for wc in walk_commands:
                    if wc not in final_walk_command_list:
                        final_walk_command_list.append(wc)
                halp.add_field(name="Uncategorized Commands", value=" • ".join(final_walk_command_list), inline=False)
                await ctx.send('', embed=halp)
            else:
                """Helps me remind you if you pass too many args."""
                if len(cog) > 1:
                    halp = discord.Embed(title='Error!', description='That is way too many cogs!',
                                         color=discord.Color.red())
                    await ctx.message.author.send('', embed=halp)
                else:
                    """Command listing within a cog."""
                    found = False
                    for x in self.client.cogs:
                        for y in cog:
                            if x == y:
                                halp = discord.Embed(colour=colour)
                                for c in self.client.get_cog(y).get_commands():
                                    if not c.hidden:
                                        halp.add_field(name=c.name, value=c.help, inline=False)
                                found = True
                    if not found:
                        pass
                    await ctx.send('', embed=halp)
        except Exception as error:
            await ctx.send(error)


def setup(client):
    client.add_cog(Info(client))
