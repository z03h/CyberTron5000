import asyncio
import json
import random
from html import unescape as unes

import aiohttp
import discord
from async_timeout import timeout
from discord.ext import commands

from .utils import cyberformat, lists


def dagpi():
    with open("secrets.json", "r") as f:
        res = json.load(f)
    return res['dagpi_token']


class Games(commands.Cog):
    """Games!"""
    
    def __init__(self, client):
        self.client = client
        self.daggy = 491174779278065689
        self.session = aiohttp.ClientSession()
    
    # rock paper scissors, shoot
    
    @commands.command(aliases=['rps'], help="Rock paper scissors shoot")
    async def rockpaperscissors(self, ctx):
        # an outcome of 0 is a win, 1 is a draw and 2 is  a loss.
        choice = random.choice(['rock', 'paper', 'scissors'])
        embed = discord.Embed(colour=self.client.colour, description="**Choose one** :point_down:")
        msg = await ctx.send("** **", embed=embed)
        rps = ['🗿', '📄', '✂']
        for e in rps:
            await msg.add_reaction(e)
        
        def check(reaction, user):
            return str(reaction.emoji) in rps and user == ctx.author and msg.id == reaction.message.id
        
        async with timeout(30):
            reaction, user = await self.client.wait_for(
                'reaction_add',
                timeout=30.0,
                check=check
            )
            
            if str(reaction.emoji) == "🗿":
                if choice == 'scissors':
                    final_outcome = 0
                else:
                    final_outcome = 1 if choice == 'rock' else 2
            elif str(reaction.emoji) == "📄":
                if choice == 'rock':
                    final_outcome = 0
                else:
                    final_outcome = 1 if choice == 'paper' else 2
            elif str(reaction.emoji) == "✂":
                if choice == 'paper':
                    final_outcome = 0
                else:
                    final_outcome = 1 if choice == 'scissors' else 2
            if not final_outcome:
                await msg.edit(
                    embed=discord.Embed(colour=self.client.colour).set_author(name=f"You won! I drew {choice}!"))
            else:
                await msg.edit(embed=discord.Embed(colour=self.client.colour).set_author(
                    name=f"You lost! I drew {choice}!")) if final_outcome == 2 else await msg.edit(
                    embed=discord.Embed(colour=self.client.colour).set_author(
                        name=f"It was a draw! We both drew {choice}!"))
    
    # kiss marry kill command
    
    @commands.command(help="Kiss, marry, kill.", aliases=['kmk'])
    async def kissmarrykill(self, ctx):
        member1 = random.choice(ctx.guild.members)
        member2 = random.choice(ctx.guild.members)
        member3 = random.choice(ctx.guild.members)
        if member1 == member2:
            member1 = random.choice(ctx.guild.members)
        elif member3 == member2:
            member3 = random.choice(ctx.guild.members)
        embed = discord.Embed(colour=self.client.colour,
                              description=f"**Would you kiss (😘), marry (👫), or kill(🔪) {member1.display_name}?**")
        embed.add_field(name=member1.display_name, value="\u200b")
        embed.add_field(name=member2.display_name, value="\u200b")
        embed.add_field(name=member3.display_name, value="\u200b")
        embed.set_author(name=ctx.message.author.display_name, icon_url=ctx.message.author.avatar_url)
        msg = await ctx.send(embed=embed)
        
        kmk = ['😘', '👫', '🔪']
        
        def check(reaction, user):
            return str(reaction.emoji) in kmk and user == ctx.author
        
        for emoji in kmk:
            await msg.add_reaction(emoji)
        async with timeout(30):
            reaction, user = await self.client.wait_for(
                'reaction_add',
                timeout=30.0,
                check=check
            )
            if str(reaction.emoji) == "😘":
                
                embed1 = discord.Embed(colour=self.client.colour,
                                       description=f"**Would you marry (👫), or kill(🔪) {member2.display_name}?**")
                embed1.add_field(name=member1.display_name, value="😘")
                embed1.add_field(name=member2.display_name, value="\u200b")
                embed1.add_field(name=member3.display_name, value="\u200b")
                embed1.set_author(name=ctx.message.author.display_name, icon_url=ctx.message.author.avatar_url)
                msg1 = await ctx.send(embed=embed1)
                await msg1.add_reaction(emoji='👫')
                await msg1.add_reaction(emoji="🔪")
                await asyncio.sleep(0.1)
                async with timeout(30):
                    reaction, user = await self.client.wait_for(
                        'reaction_add',
                        timeout=30.0,
                        check=check
                    )
                    if str(reaction.emoji) == "👫":
                        
                        embed2 = discord.Embed(colour=self.client.colour, description=f"**Results**")
                        embed2.add_field(name=member1.display_name, value="😘")
                        embed2.add_field(name=member2.display_name, value="👫")
                        embed2.add_field(name=member3.display_name, value="🔪")
                        embed2.set_author(name=ctx.message.author.display_name,
                                          icon_url=ctx.message.author.avatar_url)
                        await ctx.send(embed=embed2)
                    elif str(reaction.emoji) == "🔪":
                        
                        embed2 = discord.Embed(colour=self.client.colour,
                                               description=f"**Results**")
                        embed2.add_field(name=member1.display_name, value="😘")
                        embed2.add_field(name=member2.display_name, value="🔪")
                        embed2.add_field(name=member3.display_name, value="👫")
                        embed2.set_author(name=ctx.message.author.display_name,
                                          icon_url=ctx.message.author.avatar_url)
                        await ctx.send(embed=embed2)
            elif str(reaction.emoji) == "👫":
                
                embed1 = discord.Embed(colour=self.client.colour,
                                       description=f"**Would you kiss (😘), or kill(🔪) {member2.display_name}?**")
                embed1.add_field(name=member1.display_name, value="👫")
                embed1.add_field(name=member2.display_name, value="\u200b")
                embed1.add_field(name=member3.display_name, value="\u200b")
                embed1.set_author(name=ctx.message.author.display_name, icon_url=ctx.message.author.avatar_url)
                msg1 = await ctx.send(embed=embed1)
                for e in ['🔪']:
                    await msg1.add_reaction(e)
                await msg1.add_reaction(emoji='😘')
                await asyncio.sleep(0.1)
                async with timeout(30):
                    reaction, user = await self.client.wait_for(
                        'reaction_add',
                        timeout=30.0,
                        check=check
                    )
                    if str(reaction.emoji) == "😘":
                        
                        embed2 = discord.Embed(colour=self.client.colour,
                                               description=f"**Results**")
                        embed2.add_field(name=member1.display_name, value="👫")
                        embed2.add_field(name=member2.display_name, value="😘")
                        embed2.add_field(name=member3.display_name, value="🔪")
                        embed2.set_author(name=ctx.message.author.display_name,
                                          icon_url=ctx.message.author.avatar_url)
                        await ctx.send(embed=embed2)
                    elif str(reaction.emoji) == "🔪":
                        
                        embed2 = discord.Embed(colour=self.client.colour,
                                               description=f"**Results**")
                        embed2.add_field(name=member1.display_name, value="👫")
                        embed2.add_field(name=member2.display_name, value="🔪")
                        embed2.add_field(name=member3.display_name, value="😘")
                        embed2.set_author(name=ctx.message.author.display_name,
                                          icon_url=ctx.message.author.avatar_url)
                        await ctx.send(embed=embed2)
            elif str(reaction.emoji) == "🔪":
                
                embed1 = discord.Embed(colour=self.client.colour,
                                       description=f"**Would you kiss (😘), or marry (👫) {member2.display_name}?**")
                embed1.add_field(name=member1.display_name, value="🔪")
                embed1.add_field(name=member2.display_name, value="\u200b")
                embed1.add_field(name=member3.display_name, value="\u200b")
                embed1.set_author(name=ctx.message.author.display_name, icon_url=ctx.message.author.avatar_url)
                msg1 = await ctx.send(embed=embed1)
                await msg1.add_reaction(emoji='😘')
                await msg1.add_reaction(emoji='👫')
                await asyncio.sleep(0.1)
                async with timeout(30):
                    reaction, user = await self.client.wait_for(
                        'reaction_add',
                        timeout=30.0,
                        check=check
                    )
                    if str(reaction.emoji) == "😘":
                        
                        embed2 = discord.Embed(colour=self.client.colour,
                                               description=f"**Results**")
                        embed2.add_field(name=member1.display_name, value="🔪")
                        embed2.add_field(name=member2.display_name, value="😘")
                        embed2.add_field(name=member3.display_name, value="👫")
                        embed2.set_author(name=ctx.message.author.display_name,
                                          icon_url=ctx.message.author.avatar_url)
                        await ctx.send(embed=embed2)
                    elif str(reaction.emoji) == "👫":
                        
                        embed2 = discord.Embed(colour=self.client.colour,
                                               description=f"**Results**")
                        embed2.add_field(name=member1.display_name, value="🔪")
                        embed2.add_field(name=member2.display_name, value="👫")
                        embed2.add_field(name=member3.display_name, value="😘")
                        embed2.set_author(name=ctx.message.author.display_name,
                                          icon_url=ctx.message.author.avatar_url)
                        
                        await ctx.send(embed=embed2)
    
    @commands.group(aliases=['wtp'], invoke_without_command=True)
    async def whosthatpokemon(self, ctx):
        """
        Who's that pokemon!?
        """
        try:
            dutchy = self.client.get_user(171539705043615744) or await self.client.fetch_user(171539705043615744)
            daggy = self.client.get_user(self.daggy) or await self.client.fetch_user(self.daggy)
            async with ctx.typing():
                resp = {'token': dagpi()}
                async with self.session as cs:
                    async with cs.get('https://dagpi.tk/api/wtp', headers=resp) as r:
                        resp = await r.json()
                    pokemon = resp['pokemon']
                    print(pokemon)
                    async with cs.get(f"https://some-random-api.ml/pokedex?pokemon={pokemon['name']}") as r:
                        res = await r.json()
                    await cs.close()
                evo_line = []
                for e in res[0]['family']['evolutionLine']:
                    if str(e).lower() == pokemon['name'].lower():
                        evo_line.append("???")
                    else:
                        evo_line.append(e)
                embed = discord.Embed(colour=self.client.colour)
                embed.set_image(url=resp['question_image'])
                embed.set_footer(
                    text=f"Much thanks to {str(daggy)} for this amazing API, and {str(dutchy)} for the wonderful idea!")
                embed.title = "Who's that Pokémon?"
                embed.description = f"You have 3 attempts | You have 30 seconds\nYou can ask for a hint by doing `{ctx.prefix}hint`, or cancel by doing `{ctx.prefix}cancel`!"
                await ctx.send(embed=embed)
                dashes = await cyberformat.better_random_char(pokemon['name'], '_')
                hints = [
                    discord.Embed(colour=self.client.colour, title="Types", description=', '.join(pokemon['type'])),
                    discord.Embed(title=f"`{dashes}`", colour=self.client.colour),
                    discord.Embed(colour=self.client.colour, title="Evolution Line", description=" → ".join(evo_line)),
                    discord.Embed(title="Pokédex Entry",
                                  description=res[0]['description'].lower().replace(pokemon['name'].lower(), "???"),
                                  colour=self.client.colour),
                    discord.Embed(colour=self.client.colour, title="Species", description=" ".join(res[0]['species']))]
            try:
                for x in range(3):
                    msg = await self.client.wait_for('message',
                                                     check=lambda m: m.author == ctx.author and not m.author.bot,
                                                     timeout=30.0)
                    if msg.content.lower() == str(resp['pokemon']['name']).lower():
                        embed = discord.Embed(title=f"Correct! The answer was {resp['pokemon']['name']}",
                                              colour=self.client.colour)
                        embed.set_image(url=resp['answer_image'])
                        return await ctx.send(embed=embed)
                    elif msg.content.lower().startswith(f"{ctx.prefix}hint"):
                        await ctx.send(
                            embed=random.choice(hints))
                        continue
                    elif msg.content.lower().startswith(f"{ctx.prefix}cancel"):
                        embed = discord.Embed(title=f"{resp['pokemon']['name']}", colour=self.client.colour)
                        embed.set_image(url=resp['answer_image'])
                        embed.set_author(name="The correct answer was....")
                        return await ctx.send(embed=embed)
                    else:
                        continue
                embed = discord.Embed(title=f"{resp['pokemon']['name']}", colour=self.client.colour)
                embed.set_image(url=resp['answer_image'])
                embed.set_author(name="Incorrect! The correct answer was....")
                return await ctx.send(embed=embed)
            except asyncio.TimeoutError:
                embed = discord.Embed(title=f"{resp['pokemon']['name']}", colour=self.client.colour)
                embed.set_image(url=resp['answer_image'])
                embed.set_author(name="You ran out of time! The answer was...")
                return await ctx.send(embed=embed)
        except Exception as erro:
            await ctx.send(erro)
    
    @commands.command(help="Get's you a trivia question.", aliases=['tr', 't'])
    async def trivia(self, ctx, difficulty: str = None):
        try:
            an = []
            difficulty = difficulty if difficulty and difficulty.lower() in ['easy', 'medium',
                                                                             'hard'] else random.choice(
                ['easy', 'medium', 'hard'])
            async with self.session as cs:
                async with cs.get("https://opentdb.com/api.php?amount=1",
                                  params={"amount": 1, "difficulty": difficulty}) as r:
                    res = await r.json()
                data = res['results'][0]
                await cs.close()
                answers = [unes(answer) for answer in data['incorrect_answers']]
                answers.append(unes(data['correct_answer']))
                random.shuffle(answers)
                for numb, ans in enumerate(answers, 1):
                    an.append(f'{lists.NUMBER_ALPHABET[numb]}) **{ans}**')
                yup = '\n'.join(an)
                embed = discord.Embed(title=unes(data["question"]),
                                      description=f"{yup}",
                                      colour=self.client.colour)
                embed.set_author(name=f"{ctx.author.display_name}'s question:",
                                 icon_url=ctx.author.avatar_url)
                embed.add_field(name="Question Info",
                                value=f"This question about **{unes(data['category'])}** is of **{unes(data['difficulty']).capitalize()}** difficulty")
                embed.set_footer(text="https://opentdb.com")
                letter_ans = lists.NUMBER_ALPHABET[answers.index(''.join(unes(data['correct_answer']))) + 1]
                lower = str(letter_ans).lower()
                message = await ctx.send("** **", embed=embed)
                async with timeout(15):
                    m = await self.client.wait_for(
                        'message',
                        timeout=15.0,
                        check=lambda m: m.author == ctx.author)
                    if str(lower) == m.content:
                        await ctx.send("Correct!")
                    elif str(letter_ans) == m.content:
                        await ctx.send("Correct!")
                    else:
                        await ctx.send(
                            f"Incorrect! The correct answer was {letter_ans}, {unes(data['correct_answer'])}.")
        except Exception as error:
            if isinstance(error, IndexError):
                return await ctx.send(
                    f"<:warning:727013811571261540> **{ctx.author.display_name}**, invalid difficulty! Valid difficulties include easy, medium, hard.")
            elif isinstance(error, asyncio.TimeoutError) or isinstance(error, asyncio.CancelledError):
                await message.edit(embed=discord.Embed(colour=self.client.colour).set_author(
                    name=f"Times up! The correct answer was {unes(data['correct_answer'])}."))
            else:
                await ctx.send(error.__class__.__name__)
    
    @commands.group(aliases=['gl', 'gtl'], invoke_without_command=True)
    async def guesslogo(self, ctx):
        """
        Guess a random logo!
        """
        td = {
            True: "<:tick:733458499777855538>",
            False: "<:x_:733458444346195990>",
        }
        daggy = self.client.get_user(self.daggy) or await self.client.fetch_user(self.daggy)
        async with ctx.typing():
            resp = {'token': dagpi()}
            async with self.session as cs:
                async with cs.get('https://dagpi.tk/api/logogame', headers=resp) as r:
                    resp = await r.json()
                await cs.close()
            easy = bool(resp['easy'])
            hard = not easy
            
            embed = discord.Embed(
                title="Which company is this?", colour=self.client.colour).set_image(
                url=resp['question']).set_footer(
                text=f"Much thanks to {str(daggy)} for this amazing API!", icon_url=daggy.avatar_url)
            embed.add_field(name=f'**Difficulty**', value=f'{td[easy]} | **Easy?**\n{td[hard]} | **Hard?**')
            try:
                embed.add_field(name="**Company Description**", value=resp['clue'])
            except KeyError:
                pass
            embed.description = f"Do `{ctx.prefix}hint` to see a hint, or `{ctx.prefix}cancel` to cancel."
            await ctx.send(embed=embed)
        try:
            for x in range(3):
                msg = await self.client.wait_for('message', check=lambda m: m.author == ctx.author and not m.author.bot,
                                                 timeout=30.0)
                if msg.content.lower() == str(resp['brand']).lower():
                    embed = discord.Embed(title=f"Correct! The answer was {resp['brand']}",
                                          colour=self.client.colour)
                    embed.set_image(url=resp['answer'])
                    return await ctx.send(embed=embed)
                elif msg.content.lower().startswith(f"{ctx.prefix}hint"):
                    embed = discord.Embed(title=f"`{resp['hint']}`",
                                          colour=self.client.colour)
                    await ctx.send(embed=embed)
                    continue
                elif msg.content.lower().startswith(f"{ctx.prefix}cancel"):
                    embed = discord.Embed(title=f"The answer was {resp['brand']}",
                                          colour=self.client.colour)
                    embed.set_image(url=resp['answer'])
                    return await ctx.send(embed=embed)
                else:
                    continue
            embed = discord.Embed(title=f"The answer was {resp['brand']}",
                                  colour=self.client.colour)
            embed.set_image(url=resp['answer'])
            return await ctx.send(embed=embed)
        except asyncio.TimeoutError:
            embed = discord.Embed(title=f"{resp['brand']}", colour=self.client.colour)
            embed.set_image(url=resp['answer'])
            embed.set_author(name="You ran out of time! The answer was...")
            return await ctx.send(embed=embed)


def setup(client):
    client.add_cog(Games(client))