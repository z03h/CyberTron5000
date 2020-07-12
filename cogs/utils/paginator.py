from discord.ext import menus
import discord


class CatchAllMenu(menus.MenuPages, inherit_buttons=False):
    
    @menus.button('<:last_page_left:731315722554310740>', position=menus.First(0))
    async def go_to_first_page(self, payload):
        """go to the first page"""
        await self.show_page(0)
    
    @menus.button('<:arrow_left:731310897989156884>', position=menus.First(1))
    async def go_to_previous_page(self, payload):
        """go to the previous page"""
        await self.show_checked_page(self.current_page - 1)
    
    @menus.button('<:stop_button:731316755485425744>', position=menus.Last(2))
    async def stop_pages(self, payload):
        """stops the pagination session."""
        self.stop()
    
    @menus.button('<:arrow_right:731311292346007633>', position=menus.Last(0))
    async def go_to_next_page(self, payload):
        """go to the next page"""
        await self.show_checked_page(self.current_page + 1)
    
    @menus.button('<:last_page_right:731315722986324018>', position=menus.Last(1))
    async def go_to_last_page(self, payload):
        await self.show_page(self._source.get_max_pages() - 1)
    
    @menus.button('<:1234:731401199797927986>', position=menus.Last())
    async def _1234(self, payload):
        i = await self.ctx.send("What page would you like to go to?")
        msg = await self.ctx.bot.wait_for('message', check=lambda m: m.author == self.ctx.author)
        page = 0
        try:
            page += int(msg.content)
        except ValueError:
            return await self.ctx.send(
                f"**{self.ctx.author.name}**, **{msg.content}** could not be turned into an integer! Please try again!",
                delete_after=3)
        
        if page > (self._source.get_max_pages()):
            await self.ctx.send(f"There are only **{self._source.get_max_pages()}** pages!", delete_after=3)
        elif page < 1:
            await self.ctx.send(f"There is no **{page}th** page!", delete_after=3)
        else:
            index = page - 1
            await self.show_checked_page(index)
            await i.edit(content=f"Transported to page **{page}**!", delete_after=3)
    
    @menus.button('<:info:731324830724390974>', position=menus.Last(1))
    async def on_info(self, payload):
        await self.message.edit(embed=discord.Embed(description=self.info_page, colour=self.ctx.bot.colour))
    
    @property
    def info_page(self):
        return f"Info:" \
               f"\n<:arrow_left:731310897989156884> • Go back one page" \
               f"\n<:arrow_right:731311292346007633> • Go forward one page" \
               f"\n<:last_page_left:731315722554310740> • Go the the first page" \
               f"\n<:last_page_right:731315722986324018> • Go to the last page" \
               f"\n<:stop_button:731316755485425744> • Stop the paginator" \
               f"\n<:1234:731401199797927986> • Go to a page of your choosing" \
               f"\n<:info:731324830724390974> • Brings you here"
 
class EmbedSource(menus.ListPageSource):
    def __init__(self, data):
        super().__init__(data, per_page=1)
    
    async def format_page(self, menu, entries: discord.Embed):
        entries.set_footer(text=f'({menu.current_page + 1}/{menu._source.get_max_pages()})')
        return entries
