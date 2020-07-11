from discord.ext import menus
import discord
from cogs.utils import exceptions


class CatchAllMenu(menus.MenuPages):
    """
    Catch All Paginator
    """
    
    def __init__(self, source: list):
        super().__init__(check_embeds=True, source=source)
    
    @property
    def info_page(self):
        return f"Info:" \
               f"\n<:arrow_left:731310897989156884> • Go back one page" \
               f"\n<:arrow_right:731311292346007633> • Go forward one page" \
               f"\n<:last_page_left:731315722554310740> • Go the the first page" \
               f"\n<:last_page_right:731315722986324018> • Go to the last page" \
               f"\n<:stop_button:731316755485425744> • Stop the paginator" \
               f"\n<:1234:731401199797927986> • Go to a page of your choosing" \
               f"\n<:info:731324830724390974> • Brings you here" \
            # f"\nThis paginator has **{len(self.entries)}** entries"

    # async def send_initial_message(self, ctx, channel):
    #    return await channel.send(embed=self.entries[0])

    # @menus.button('<:last_page_left:731315722554310740>')
    # async def on_first_page(self, payload):
    #   await self.message.edit(embed=self.entries[0])

    # @menus.button('<:arrow_left:731310897989156884>')
    # async def on_left_arrow(self, payload):
    # print("bruh")
    # print(self.message.embeds[0])
    # current = self.entries.index(self.message.embeds[0])
    # index = current - 1 if current else 0
    # await self.message.edit(embed=self.entries[index])

    # @menus.button('<:stop_button:731316755485425744>')
    # async def on_stop(self, payload):
    #    self.stop()
    #    await self.message.delete()
    #    await self.ctx.message.add_reaction(emoji=":GreenTick:707950252434653184") if self.tick else None

    # @menus.button('<:arrow_right:731311292346007633>')
    # async def on_right_arrow(self, payload):
    # next(self.entries)
    # print(self.message.embeds[0])
    # print("••••••••••••••••••••")
    # current = self.entries.index(self.message.embeds[0])
    # index = current + 1 if current != len(self.entries) else current
    # try:
    #    await self.message.edit(embed=self.entries[index])
    # except IndexError:
    #    pass

    # @menus.button('<:last_page_right:731315722986324018>')
    # async def on_last_page(self, payload):
    # await self.message.edit(embed=self.entries[-1])

    # @menus.button('<:info:731324830724390974>')
    # async def on_info(self, payload):
    # await self.message.edit(embed=discord.Embed(description=self.info_page))

    # @menus.button('<:1234:731401199797927986>')
    # async def _1234(self, payload):
    # i = await self.ctx.send("What page would you like to go to?")
    # m = await self.ctx.bot.wait_for('message', check=lambda msg: msg.author == self.ctx.author)
    # page = 0
    # try:
    #    page += int(m.content)
    # except ValueError:
    #    await self.ctx.send(f"**{m.content}** is not a valid page!", delete_after=3)
    # if page >= (len(self.entries)):
    #    await self.ctx.send(f"There are only **{len(self.entries)}** pages!", delete_after=3)
    # elif page < 1:
    #    await self.ctx.send(f"There is no **{page}th** page!", delete_after=3)
    # else:
    #    index = page - 1
    #    await self.message.edit(embed=self.entries[index])
    #    await i.edit(content=f"Transported to page **{page}**!", delete_after=3)


class EmbedSource(menus.ListPageSource):
    def __init__(self, data):
        super().__init__(data, per_page=1)
    
    async def format_page(self, menu, entries):
        return entries