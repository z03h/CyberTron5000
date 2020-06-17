from discord.ext import commands


class Images(commands.Cog):
    """Image manipulation commands."""
    def __init__(self, client):
        self.client = client
        self.tick = ":GreenTick:707950252434653184"


def setup(client):
    client.add_cog(Images(client))
