from discord.ext import menus


class PlainTextMenu(menus.Menu):
    """
    Paginates Plain Text lists
    """
    def __init__(self, to_paginate):
        super().__init__()
        self.to_paginate: list = to_paginate
        
    @property
    def info_page(self):
        return f"Info:\n<:arrow_left:731310897989156884> • Go back one page\n<:arrow_right:731311292346007633> • Go forward one page\n<:last_page_left:731315722554310740> • Go the the first page\n<:last_page_right:731315722986324018> • Go to the last page\n<:stop_button:731316755485425744> • Stop the paginator\n<:info:731324830724390974> • Brings you here\nThis paginator has **{len(self.to_paginate)}** entries"
    
    async def send_initial_message(self, ctx, channel):
        return await channel.send(content=self.to_paginate[0])
    
    @menus.button('<:last_page_left:731315722554310740>')
    async def on_first_page(self, payload):
        await self.message.edit(content=self.to_paginate[0])
    
    @menus.button('<:arrow_left:731310897989156884>')
    async def on_left_arrow(self, payload):
        current = self.to_paginate.index(self.message.content)
        index = current - 1 if current else 0
        await self.message.edit(content=self.to_paginate[index])
    
    @menus.button('<:stop_button:731316755485425744>')
    async def on_stop(self, payload):
        self.stop()
        await self.message.delete()
    
    @menus.button('<:arrow_right:731311292346007633>')
    async def on_right_arrow(self, payload):
        current = self.to_paginate.index(self.message.content)
        index = current + 1 if current != len(self.to_paginate)-1 else current
        await self.message.edit(content=self.to_paginate[index])
    
    @menus.button('<:last_page_right:731315722986324018>')
    async def on_last_page(self, payload):
        await self.message.edit(content=self.to_paginate[-1])
    
    @menus.button('<:info:731324830724390974>')
    async def on_info(self, payload):
        await self.message.edit(content=self.info_page)
