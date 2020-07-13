from discord.ext import commands


class Tags(commands.Cog):
    def __init__(self, client):
        self.client = client
    
    @commands.command()
    async def database(self, arg):
        await arg.send("You're mom")


def setup(client):
    client.add_cog(Tags(client))
