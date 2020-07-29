import asyncio
import random
import string

import aiohttp
import discord
from async_timeout import timeout
from discord.ext import commands
from uuid import uuid4
from jikanpy import AioJikan

from .utils import cyberformat, paginator
from .utils.lists import INDICATOR_LETTERS


class Fun(commands.Cog):
    """Fun commands"""
    
    def __init__(self, client):
        self.client = client
        self.tick = ":tick:733458499777855538"
        self.owner = self.client.get_user(350349365937700864)
    
    @commands.command()
    async def horror(self, ctx, limit: int = 5):
        """spoopy"""
        posts = []
        async with aiohttp.ClientSession() as cs:
            async with cs.get(f"https://www.reddit.com/r/twosentencehorror/hot.json") as r:
                res = await r.json()
            for i in res['data']['children']:
                posts.append(i['data'])
            counter = 0
            embeds = []
            async with ctx.typing():
                for s in random.sample(posts, len(posts)):
                    text = cyberformat.shorten(f"{s['title']}\n{s['selftext']}")
                    embeds.append(discord.Embed(description=text[:2000], colour=self.client.colour))
                    counter += 1
                    if counter == limit:
                        break
                    else:
                        continue
        p = paginator.CatchAllMenu(paginator.EmbedSource(embeds))
        await p.start(ctx)
    
    @commands.command()
    async def pfpcycle(self, ctx):
        """if you're reading this it probably isnt your business"""
        pfps = ['http://tinyurl.com/y8ccnxm3',
                'https://images-ext-1.discordapp.net/external/6HjseNKji1C5wbK9Wb_jnIluzFWrCRW6xqhfboNtDDI/%3Fsize%3D1024/https/cdn.discordapp.com/avatars/350349365937700864/bbbff13a570231108b7afa383416b62a.png',
                'http://tinyurl.com/ycjuvusq',
                'https://cdn.discordapp.com/avatars/350349365937700864/f38bc11cf4360a9267a55962fcd71809.png?size=1024',
                'https://media.discordapp.net/attachments/381963689470984203/732283634190516304/coolweavile.png?width=962&height=962',
                'https://images-ext-1.discordapp.net/external/XVtT9nLyPYTWfNw4GSjvRMKibuKafi6_VCyVwSfW4C8/%3Fsize%3D1024/https/cdn.discordapp.com/avatars/350349365937700864/d027959b2a204f7587092a7a249e7377.png?width=962&height=962',
                'https://media.discordapp.net/attachments/735325249138065468/735681377785348156/image0.png',
                'https://media.discordapp.net/attachments/735325249138065468/735681378292596736/image1.png',
                'https://media.discordapp.net/attachments/735325249138065468/735681378867478528/image2.png',
                'https://media.discordapp.net/attachments/735325249138065468/735681379387441152/image3.png',
                'https://media.discordapp.net/attachments/735325249138065468/735682125239681074/image0.png'
                'http://i.some-random-api.ml/pokemon/weavile.png']
        embeds = [discord.Embed(colour=self.client.colour).set_image(url=p) for p in pfps]
        a = paginator.CatchAllMenu(paginator.EmbedSource(embeds))
        await a.start(ctx)
    
    @commands.group(invoke_without_command=True, help="Replies with what you said and deletes your message.",
                    aliases=['say'])
    async def reply(self, ctx, *, message):
        await ctx.send(
            cyberformat.hyper_replace(text=message, old=['@everyone', '@here'], new=['@\u200beveryone', '@\u200bhere']))
    
    @reply.command(invoke_without_command=True,
                   help="Replies with what you said and deletes your message, but in an embed.")
    async def embed(self, ctx, *, message):
        await ctx.send(embed=discord.Embed(title=message, colour=self.client.colour))
    
    @reply.command(invoke_without_command=True,
                   help="Replies with what you said and deletes your message, but in a different channel.")
    async def echo(self, ctx, channel: discord.TextChannel, *, message):
        await channel.send(
            cyberformat.hyper_replace(text=message, old=['@everyone', '@here'], new=['@\u200beveryone', '@\u200bhere']))
        await ctx.message.add_reaction(emoji=":tick:733458499777855538")
    
    @reply.command(invoke_without_command=True, help="Replies with what you said and deletes your message, but UwU.")
    async def owo(self, ctx, *, message):
        await ctx.send(cyberformat.hyper_replace(text=message, old=['r', 'l', 'R', 'L'], new=['w', 'w', "W", "W"]))
    
    @reply.command(help="🅱", invoke_without_command=True)
    async def b(self, ctx, *, message):
        await ctx.send(cyberformat.hyper_replace(text=message, old=['b', 'B', 'D', 'd'], new=['🅱', '🅱', "🅱", "🅱"]))
    
    @reply.command(aliases=['msg'], help="Message a user something. ", invoke_without_command=True)
    async def message(self, ctx, user: discord.Member, *, message):
        person = self.client.get_user(user.id)
        await person.send(f"{message}\n\n*(Sent by {ctx.message.author})*")
        await ctx.message.add_reaction(emoji=":tick:733458499777855538")
    
    @reply.command(help="Spams a message.", invoke_without_command=True)
    async def spam(self, ctx, *, message):
        l = ['@\u200beveryone', '@\u200bhere']
        await ctx.send(f"{cyberformat.hyper_replace(text=message, old=['@everyone', '@here'], new=l)} " * 15)
    
    @reply.command(invoke_without_command=True)
    async def indicator(self, ctx, *, message):
        """reply in emojis"""
        letters = []
        alphabet = list(string.ascii_uppercase)
        numbers = ["1", "2", "3", "4", "5", "6", "7", "8", "9", "0"]
        for letter in message:
            if letter.upper() in alphabet:
                letters.append(f":regional_indicator_{letter.lower()}:")
            elif letter in numbers:
                letters.append(INDICATOR_LETTERS[letter])
            elif letter.upper() not in alphabet:
                letters.append(letter)
        
        await ctx.send("\u200b".join(letters))
    
    @reply.command()
    async def mock(self, ctx, *, message):
        """Like that spongebob meme"""
        await ctx.send(await cyberformat.better_random_char(message))
    
    @commands.command(help="Asks the mystical Ouija Board a question...")
    async def askouija(self, ctx, *, question):
        ouija_responses = [
            'Help',
            'Bruh',
            'dumb',
            'You dumb',
            'Hey gamers'
            'Infinity',
            'God damn ur ugly',
            'Gamers',
            'Gamers Unite',
            'Fricken amateur',
            'Fricken doofus',
            'Yo',
            'Joe mama',
            'No',
            'yes',
            'perhaps',
            'Waluigi',
            'Bruh Moment',
            'Moment of the Bruh',
            'Puh-leaze',
            'Vibe Check']
        ouija_choice = random.choice(ouija_responses)
        ouija_says = str("You asked me... '_{}_'... I respond... {}".format(question, ouija_choice))
        await ctx.send(ouija_says)
    
    @commands.command(aliases=['cf'], help="Flips a coin.")
    async def coinflip(self, ctx, *, clause: str = None):
        tails = discord.Embed(title="Tails!", colour=self.client.colour).set_image(
            url='https://upload.wikimedia.org/wikipedia/en/thumb/3/37/Quarter_Reverse_2010.png/220px-Quarter_Reverse_2010.png')
        heads = discord.Embed(title="Heads!", colour=self.client.colour).set_image(
            url='https://upload.wikimedia.org/wikipedia/en/thumb/8/8a/Quarter_Obverse_2010.png/220px-Quarter_Obverse_2010.png')
        embed = random.choice([heads, tails])
        embed.set_author(name=clause, icon_url=ctx.author.avatar_url) if clause else None
        await ctx.send(embed=embed)
    
    @commands.command(help="How bigbrain are you? Find out.")
    async def iq(self, ctx, *, member: discord.Member = None):
        member = member or ctx.message.author
        embed = discord.Embed(
            colour=self.client.colour, title='IQ Rating Machine <:bigbrain:703735142509969408>',
            timestamp=ctx.message.created_at
        )
        embed.set_author(name="{}".format(member.display_name), icon_url=member.avatar_url)
        embed.add_field(name="What is your IQ?",
                        value=f"{member.display_name} has an IQ of {random.randint(1, 101)}.")
        await ctx.send(embed=embed)
    
    @commands.command(help="Fite")
    async def fight(self, ctx, opponent: discord.Member, *, weapon):
        author = ctx.message.author
        if opponent == author:
            await ctx.send("You can't fight yourself. Snap out of it. The accident was three years ago.")
        else:
            enemy_weapon = random.choice([
                " Sword of Mega Doom",
                " Epic Gun",
                " Mega Epic Gun",
                " Grenade",
                " Amazing Bruh Machine",
                " Gun Lmao",
                " Hyper Epic Gun",
                " 'Not even trying at this point' Rifle",
                " Grand Sword of Chaos",
                " Excalibur",
                " Master Sword",
                " Storm Pegasus",
                " Rock Leone",
                " Lightning L-Drago"
            ])
            run = random.choice([
                " but they miraculously fight back with their fists and beat you to the ground! You Lose!",
                " and they get scared and flee! You Win!"
            ])
            possibilities = random.choice([
                " but they escape! You lose!",
                " and they get rekt, m8. You win!",
                " and they get blasted into the Shadow Realm! You win!",
                " but they retaliate with their**{}**! You knock it out of their hands,{}".format(enemy_weapon, run),
                " but they fight back with their**{}**! They use it to knock your **{}** "
                "out of your hands, and finish you off with their**{}**! You Lose!".format(
                    enemy_weapon, weapon, enemy_weapon),
                " but they fight back with their**{}**! You two have a hard clash, but you end up losing! You Lose!".format(
                    enemy_weapon),
                " but they fight back with their**{}**! You two have a hard clash, and you end up winning! You Win!".format(
                    enemy_weapon),
                " and you pounce at them, but activate their trap card,**{}**. Chances "
                "look slim for you, but... they end up destroying your **{}** and win. You Lose!".format(
                    enemy_weapon, weapon),
                " and you pounce at them, but activate their trap card,**{}**. Chances "
                "look slim for you, but... in the nick of time, you end up Yeeting them with your **{}**! You Win!".format(
                    enemy_weapon, weapon),
                " and they drop their**{}**! You pick it up and use both the **{}** and**{}** to "
                "yeet them! You Win!".format(
                    enemy_weapon, weapon, enemy_weapon),
                " and they drop their**{}**! You pick it up and use both the **{}** and**{}**, "
                "but they sneak up from behind and steal your own **{}**. You two have a hard "
                "fight, but they best you! You Lose!".format(
                    enemy_weapon, weapon, enemy_weapon, weapon),
                " and they drop their**{}**! You pick it up and use both the **{}** and**{}**, "
                "but they sneak up from behind and steal both weapons! Things are looking bleak "
                "for you, so you engage in a fist fight with them, and after a few minutes, "
                "you're both found lying on the floor. It's a draw!".format(
                    enemy_weapon, weapon, enemy_weapon),
                " and trigger their PTSD. You Win!",
                " but you guys decide to make peace. It's a draw!"
            ])
            embed = discord.Embed(
                colour=self.client.colour, title='Fight Results! :crossed_swords:', timestamp=ctx.message.created_at
            )
            
            embed.set_author(name="{} vs {}".format(author.display_name, opponent.display_name),
                             icon_url=author.avatar_url)
            embed.add_field(name="_Who Won?_",
                            value="You fight **{}** with **{}**,{}".format(opponent.display_name, weapon,
                                                                           possibilities))
            await ctx.send(embed=embed)
    
    @commands.command(help="Ask the Bot about your peers")
    async def who(self, ctx, *, question=None):
        member = random.choice(ctx.guild.members)
        embed = discord.Embed(
            colour=self.client.colour,
            title=f"Answer: {member.display_name}",
        )
        question = question or "?"
        embed.set_author(name="Who " + question)
        embed.set_image(url=member.avatar_url)
        await ctx.send(embed=embed)
    
    @commands.group(invoke_without_command=True, aliases=["em"],
                    help="do an emoji from a different server that cybertron is in.")
    async def emoji(self, ctx, *emoji: discord.Emoji):
        a = []
        for item in emoji:
            a.append(self.client.get_emoji(item.id))
        await ctx.send("".join([str(a) for a in a]))
    
    @emoji.command()
    async def url(self, ctx, *emoji: discord.Emoji):
        a = []
        for item in emoji:
            a.append(self.client.get_emoji(item.id))
        await ctx.send(" ".join([str(a.url) for a in a]))
    
    @commands.command(aliases=['gt'])
    async def greentext(self, ctx):
        """Write a greentext story"""
        story = []
        await ctx.send(
            f"Greentext story starting! Type `{ctx.prefix}quit` or `{ctx.prefix}exit` to stop the session, or `{ctx.prefix}finish` to see your final story!")
        try:
            while True:
                message = await self.client.wait_for('message', check=lambda m: m.author == ctx.author, timeout=500)
                async with timeout(500):
                    if message.content == f"{ctx.prefix}quit":
                        await ctx.send("Session exited.")
                        return
                    elif message.content == f"{ctx.prefix}exit":
                        await ctx.send("Session exited.")
                        return
                    elif message.content == f"{ctx.prefix}finish":
                        final_story = "\n".join(story)
                        await ctx.send(f"**{ctx.author}**'s story\n```css\n" + final_story + "```")
                        return
                    else:
                        story.append(">" + message.content)
                        await message.add_reaction(emoji=self.tick)
        except asyncio.TimeoutError:
            final_story = "\n".join(story)
            await ctx.send(f"**{ctx.author}**'s story\n```css\n" + final_story + "```")
    
    @commands.command(aliases=['bin'])
    async def binary(self, ctx, *, message):
        """Convert text to binary."""
        async with aiohttp.ClientSession() as cs:
            async with cs.get(f"https://some-random-api.ml/binary?text={message}") as r:
                res = await r.json()
            await ctx.send(f'{res["binary"]}')
    
    @commands.command(aliases=['fb', 'from-bin'])
    async def from_binary(self, ctx, *, message):
        """Convert text from binary"""
        async with aiohttp.ClientSession() as cs:
            async with cs.get(f"https://some-random-api.ml/binary?decode={message}") as r:
                res = await r.json()
            await ctx.send(f'{res["text"]}')
    
    @commands.group(invoke_without_command=True)
    async def todo(self, ctx):
        """Shows you todo commands"""
        result = await self.client.pg_con.fetch("SELECT * FROM todo WHERE user_id = $1", ctx.author.id)
        final = [f"{a[1]} (ID: {a[0]})" for a in
                 result]
        source = paginator.IndexedListSource(embed=discord.Embed(color=self.client.colour).set_author(
            name=f"{ctx.author}'s todo list (Total {len(result)})", icon_url=ctx.author.avatar_url),
            data=final)
        return await paginator.CatchAllMenu(source=source).start(ctx)
    
    @todo.command()
    async def list(self, ctx):
        """Shows you your todo list"""
        result = await self.client.pg_con.fetch("SELECT * FROM todo WHERE user_id = $1", ctx.author.id)
        final = [f"{a[1]} (ID: {a[0]})" for a in
                 result]
        source = paginator.IndexedListSource(embed=discord.Embed(color=self.client.colour).set_author(
            name=f"{ctx.author}'s todo list (Total {len(result)})", icon_url=ctx.author.avatar_url),
            data=final)
        return await paginator.CatchAllMenu(source=source).start(ctx)
    
    @todo.command()
    async def add(self, ctx, *, item):
        """Adds an item to your todo list"""
        id = str(uuid4())[:8]
        await self.client.pg_con.execute("INSERT INTO todo (user_id, id, item) VALUES ($1, $2, $3)", ctx.author.id, id,
                                         item)
        await ctx.send(f"Added `{item}` to your todo list with the id `{id}`.")
    
    @todo.command(aliases=['rm', 'r', 'remove'])
    async def resolve(self, ctx, id: str, *, reason=None):
        """Resolves an item from your todo list"""
        a = await self.client.pg_con.fetch("SELECT item FROM todo WHERE id = $1", id)
        if not a:
            return await ctx.send("Item not found. Note that you have to remove items by their **id**, not their name.")
        await self.client.pg_con.execute("DELETE FROM todo WHERE id = $1", id)
        await ctx.send(
            f"<:tick:733458499777855538> | Item {id}, `{a[0][0]}` has been removed from your todo list:\n{reason}")
    
    @commands.command()
    async def owner(self, ctx):
        """Shows you who made this bot"""
        return await ctx.send(f"it is {self.owner}")
    
    @commands.command()
    async def wink(self, ctx, *, member: discord.Member = None):
        """Wink at someone! 😉"""
        async with aiohttp.ClientSession() as cs:
            async with cs.get("https://some-random-api.ml/animu/wink") as f:
                res = await f.json()
            if member:
                await ctx.send(embed=discord.Embed(color=self.client.colour).set_image(url=res['link']).set_author(
                    name=f"😉 {ctx.author} winked at {member}!"))
            else:
                await ctx.send(embed=discord.Embed(color=self.client.colour).set_image(url=res['link']).set_author(
                    name=f"😉 {ctx.author} winked!"))
    
    @commands.command()
    async def pat(self, ctx, *, member: discord.Member):
        """Pat someone!"""
        async with aiohttp.ClientSession() as cs:
            async with cs.get("https://some-random-api.ml/animu/pat") as f:
                res = await f.json()
            await ctx.send(embed=discord.Embed(color=self.client.colour).set_image(url=res['link']).set_author(
                name=f"{ctx.author} patted {member}!"))
    
    @commands.command()
    async def hug(self, ctx, *, member: discord.Member):
        """Hug someone! 💗"""
        async with aiohttp.ClientSession() as cs:
            async with cs.get("https://some-random-api.ml/animu/hug") as f:
                res = await f.json()
            await ctx.send(embed=discord.Embed(color=self.client.colour).set_image(url=res['link']).set_author(
                name=f"{ctx.author} hugged {member}!"))
    
    @commands.command()
    async def anime(self, ctx, *, query):
        async with AioJikan() as a:
            naruto = await a.search(search_type='anime', query=query)
        res = naruto['results'][0]
        print(naruto['results'])
        o = []
        embed = discord.Embed(color=self.client.colour)
        embed.set_thumbnail(url=res['image_url'])
        embed.title = f"{res['title']}"
        embed.url = f"{res['url']}"
        embed.description = f"{naruto['results'][0]['synopsis']}"
        embed.add_field(name="Info",
                        value=f"Type | **{res['type']}**\n📺 | **{res['episodes']}**\n:star:️ | **{res['score']}**\n<:member:731190477927219231> | **{res['members']:,}**")
        for x in range(2, len(naruto['results'])):
            o.append(f"**{naruto['results'][x]['title']}**")
        embed.add_field(name="Other Entries", value=f"\n".join(o[:5]))
        await ctx.send(embed=embed)
    
    @commands.command(aliases=['choice'])
    @commands.cooldown(1, 45, commands.BucketType.user)
    async def chose(self, ctx, *choices):
        c = random.choice(choices)
        embed = discord.Embed(color=self.client.colour).set_author(name="Choice-O-Matic")
        m = await ctx.send(embed=embed)
        a = m.embeds[0]
        for choice in random.sample(choices, len(choices)):
            a.description = f"`{choice}`"
            await m.edit(embed=a)
            await asyncio.sleep(0.44)
        await m.edit(embed=discord.Embed(color=self.client.colour, description=f"`{c}`").set_author(
            name="Choice-O-Matic").add_field(name="My Choice", value=f'`{c}`!'))


# @commands.Cog.listener()
# async def on_message(self, message):
#   if message.guild.id == 700660205721223264:
#     chance = random.randint(1, 20)
#      if chance is not 0:
#       if "fuck" in message.content:
#            a, b = str(message.content).split("fuck")
#          if not a or not b:
#             pass
#        else:
#           await message.channel.send(
#              f"Guy named \"{a.strip()}\": :smirk:\nGirl named \"{b.strip()}\": :flushed:")


def setup(client):
    client.add_cog(Fun(client))
