import random
import asyncio

import discord
from discord.ext import commands
from async_timeout import timeout

from .utils.lists import INDICATOR_LETTERS
from .utils import pyformat as pf

pyf = pf.NativePython()

colour = 0x00dcff


# ≫


class Fun(commands.Cog):
    """Fun commands"""
    def __init__(self, client):
        self.client = client
        self.tick = ":GreenTick:707950252434653184"

    @commands.group(invoke_without_command=True, help="Replies with what you said and deletes your message.",
                    aliases=['say'])
    async def reply(self, ctx, *, message):
        await ctx.send(
            pyf.hyper_replace(text=message, old=['@everyone', '@here'], new=['@\u200beveryone', '@\u200bhere']))

    @reply.command(invoke_without_command=True,
                   help="Replies with what you said and deletes your message, but in an embed.")
    async def embed(self, ctx, *, message):
        await ctx.send(embed=discord.Embed(title=message, colour=colour))

    @reply.command(invoke_without_command=True,
                   help="Replies with what you said and deletes your message, but in a different channel.")
    async def echo(self, ctx, channel: discord.TextChannel, *, message):
        await channel.send(
            pyf.hyper_replace(text=message, old=['@everyone', '@here'], new=['@\u200beveryone', '@\u200bhere']))
        await ctx.message.add_reaction(emoji=":GreenTick:707950252434653184")

    @reply.command(invoke_without_command=True, help="Replies with what you said and deletes your message, but UwU.")
    async def owo(self, ctx, *, message):
        await ctx.send(pyf.hyper_replace(text=message, old=['r', 'l', 'R', 'L'], new=['w', 'w', "W", "W"]))

    @reply.command(help="🅱", invoke_without_command=True)
    async def b(self, ctx, *, message):
        await ctx.send(pyf.hyper_replace(text=message, old=['b', 'B', 'D', 'd'], new=['🅱', '🅱', "🅱", "🅱"]))

    @reply.command(aliases=['msg'], help="Message a user something. ", invoke_without_command=True)
    async def message(self, ctx, user: discord.Member, *, message):
        person = self.client.get_user(user.id)
        await person.send(f"{message}\n\n*(Sent by {ctx.message.author})*")
        await ctx.message.add_reaction(emoji=":GreenTick:707950252434653184")

    @reply.command(help="Spams a message.", invoke_without_command=True)
    async def spam(self, ctx, *, message):
        l = ['@u200beveryone', '@\u200bhere']
        await ctx.send(f"{pyf.hyper_replace(text=message, old=['@everyone', '@here'], new=l)} " * 15)

    @reply.command(invoke_without_command=True)
    async def indicator(self, ctx, *, message):
        """reply in emojis"""
        letters = []
        alphabet = ['A', 'B', 'C', 'D',
                    'E',
                    'F',
                    'G',
                    'H',
                    'I',
                    'J',
                    'K',
                    'L',
                    'M',
                    'N',
                    'O',
                    'P',
                    'Q',
                    'R',
                    'S',
                    'T',
                    'U',
                    'V',
                    'W',
                    'X',
                    'Y',
                    'Z'
                    ]
        numbers = ["1", "2", "3", "4", "5", "6", "7", "8", "9", "0"]
        for letter in message:
            if letter.upper() in alphabet:
                letters.append(f":regional_indicator_{letter.lower()}:")
            elif letter in numbers:
                letters.append(INDICATOR_LETTERS[letter])
            elif letter.upper() not in alphabet:
                letters.append(letter)
                
        await ctx.send("\u200b".join(letters))
    
    @commands.command(help="Asks the mystical Ouija Board a question...")
    async def askouija(self, ctx, *, question):
        ouija_responses = [
            'Help',
            'Bruh',
            'You gay lmao',
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
    async def coinflip(self, ctx, *, clause=None):
        author = ctx.message.author
        if clause is None:
            embed = discord.Embed(
                colour=colour, title="Tails!"
            )
            tails = embed.set_image(
                url='https://upload.wikimedia.org/wikipedia/en/thumb/3/37/Quarte'
                    'r_Reverse_2010.png/220px-Quarter_Reverse_2010.png')
            choice = random.choice([
                'Heads!',
                'Tails!'
            ])
            if choice == 'Tails!':
                await ctx.send(embed=tails)
            embed = discord.Embed(
                colour=colour, title="Heads!"
            )
            heads = embed.set_image(
                url='https://upload.wikimedia.org/wikipedia/en/thumb/8/8a/Quarter_Obvers'
                    'e_2010.png/220px-Quarter_Obverse_2010.png')
            if choice == 'Heads!':
                await ctx.send(embed=heads)
        else:
            embed = discord.Embed(
                colour=colour, title="Tails!"
            )
            tails = embed.set_image(
                url='https://upload.wikimedia.org/wikipedia/en/thumb/3/37/Quar'
                    'ter_Reverse_2010.png/220px-Quarter_Reverse_2010.png')
            embed.set_author(name=f'"{clause}"', icon_url=author.avatar_url)
            choice = random.choice([
                'Heads!',
                'Tails!'
            ])
            if choice == 'Tails!':
                await ctx.send(embed=tails)
            embed = discord.Embed(
                colour=colour, title="Heads!"
            )
            heads = embed.set_image(
                url='https://upload.wikimedia.org/wikipedia/en/thumb/'
                    '8/8a/Quarter_Obverse_2010.png/220px-Quarter_Obverse_2010.png')
            embed.set_author(name=f'"{clause}"', icon_url=author.avatar_url)
            if choice == 'Heads!':
                await ctx.send(embed=heads)
    
    @commands.command(help="How bigbrain are you? Find out.")
    async def iq(self, ctx, *, member: discord.Member = None):
        member = member or ctx.message.author
        embed = discord.Embed(
            colour=colour, title='IQ Rating Machine <:bigbrain:703735142509969408>',
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
                colour=colour, title='Fight Results! :crossed_swords:', timestamp=ctx.message.created_at
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
            colour=colour, title=f"Answer: {member.display_name}", timestamp=ctx.message.created_at
        )
        if not question:
            embed.set_author(name=f'Who?', icon_url=ctx.message.author.avatar_url)
        else:
            embed.set_author(name=f'Who {question}', icon_url=ctx.message.author.avatar_url)
        embed.set_image(url=member.avatar_url)
        await ctx.send(embed=embed)
    
    @commands.command(aliases=["em"], help="do an emoji from a different server that cybertron is in.")
    async def emoji(self, ctx, emoji: discord.Emoji, react=None):
        if react is None:
            await ctx.send(emoji)
        else:
            await ctx.message.add_reaction(emoji=emoji)
            
    @commands.command(aliases=['gt'])
    async def greentext(self, ctx):
        """Write a greentext story"""
        try:
            story = []
            await ctx.send("Greentext story starting! Type `quit` or `exit` to stop the session, or `finish` to see your final story!")
            while True:
                message = await self.client.wait_for('message', check=lambda m: m.author == ctx.author, timeout=500)
                async with timeout(500):
                    if message.content == "quit" and message.author == ctx.author:
                        await ctx.send("Session exited.")
                        return
                    elif message.content == "exit" and message.author == ctx.author:
                        await ctx.send("Session exited.")
                        return
                    elif message.content == "finish" and message.author == ctx.author:
                        final_story = "\n".join(story)
                        await ctx.send(f"**{ctx.author}**'s story\n```css\n" + final_story + "```")
                        return
                    else:
                        story.append(">" + message.content)
                        await message.add_reaction(emoji=self.tick)
        except asyncio.TimeoutError:
            await ctx.send("You ran out of time!")

def setup(client):
    client.add_cog(Fun(client))
