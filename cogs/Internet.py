import asyncio
import datetime
import random
from html import unescape as unes

import aiohttp
import discord
from async_timeout import timeout
from discord.ext import commands
from googletrans import LANGUAGES
from googletrans import Translator
from random_word import RandomWords

from .utils.lists import STAT_NAMES, NUMBER_ALPHABET, TYPES

colour = 0x00dcff


# ≫


class Internet(commands.Cog):
    """Interact with various API's"""
    def __init__(self, client):
        self.client = client
        self.session = aiohttp.ClientSession()
    
    @commands.group(invoke_without_command=True, aliases=['trans'], help="Translate something to English.")
    async def translate(self, ctx, *, message):
        
        try:
            translator = Translator()
            result = translator.translate(message)
            lang = LANGUAGES[f"{result.src}"]
            embed = discord.Embed(colour=colour, title="Translate",
                                  description=f"**{lang.capitalize()}**\n{message}\n\n**English**\n{result.text}")
            await ctx.send(embed=embed)
        except Exception as err:
            await ctx.send(err)
    
    @translate.command(invoke_without_command=True, help="Translate something to a language of your choice.")
    async def to(self, ctx, language, *, message):
        try:
            translator = Translator()
            result = translator.translate(message, dest=language)
            lang = LANGUAGES[f"{result.src}"]
            embed = discord.Embed(colour=colour, title="Translate",
                                  description=f"**{lang.capitalize()}**\n{message}\n\n**{language.capitalize()}**"
                                              f"\n{result.text}")
            await ctx.send(embed=embed)
        except Exception as err:
            await ctx.send(err)
    
    @commands.command(aliases=['wotd', 'word'], help="Get the word of the day.")
    async def wordoftheday(self, ctx):
        try:
            random_word = RandomWords()
            await ctx.send(random_word.get_random_word())
        except Exception as error:
            await ctx.send(error)
    
    @commands.command(aliases=['kitty'], help="haha kitty go meow meow.")
    async def cat(self, ctx):
        try:
            async with aiohttp.ClientSession() as cs:
                async with cs.get('https://aws.random.cat/meow') as r:
                    res = await r.json()
                    await cs.close()
            em = discord.Embed(colour=colour, title="OwO", url=res['file'])
            em.set_image(url=res['file'])
            em.set_footer(text="https://aws.random.cat/meow")
            await ctx.send(embed=em)
        except Exception as er:
            await ctx.send(er)
    
    @commands.command(aliases=['puppy', 'pup', 'pupper'], help="haha puppy go woof woof")
    async def dog(self, ctx):
        try:
            async with aiohttp.ClientSession() as cs:
                async with cs.get('https://random.dog/woof.json') as r:
                    res = await r.json()
                    res = res['url']
                    await cs.close()
            em = discord.Embed(colour=colour, title="Woof!", url=res)
            em.set_image(url=res)
            em.set_footer(text="https://random.dog/woof.json")
            await ctx.send(embed=em)
        except Exception as er:
            await ctx.send(er)
    
    @commands.command(help="Get's you a trivia question.", aliases=['tr', 't'])
    async def trivia(self, ctx):
        try:
            an = []
            difficulty = random.choice(['easy', 'medium', 'hard'])
            async with aiohttp.ClientSession() as cs:
                async with cs.get("https://opentdb.com/api.php?amount=1",
                                  params={"amount": 1, "difficulty": difficulty}) as r:
                    res = await r.json()
                data = res['results'][0]
                await cs.close()
                answers = [unes(answer) for answer in data['incorrect_answers']]
                answers.append(unes(data['correct_answer']))
                random.shuffle(answers)
                for numb, ans in enumerate(answers, 1):
                    an.append(f'{NUMBER_ALPHABET[numb]}) **{ans}**')
                yup = '\n'.join(an)
                embed = discord.Embed(title=unes(data["question"]),
                                      description=f"{yup}",
                                      colour=colour)
                embed.set_author(name=f"{ctx.message.author.display_name}'s question:",
                                 icon_url=ctx.message.author.avatar_url)
                embed.add_field(name="Question Info",
                                value=f"This question about **{unes(data['category'])}** is of **{unes(data['difficulty']).capitalize()}** difficulty")
                embed.set_footer(text="https://opentdb.com")
                letter_ans = NUMBER_ALPHABET[answers.index(''.join(unes(data['correct_answer']))) + 1]
                lower = str(letter_ans).lower()
                message = await ctx.send("** **", embed=embed)
                async with timeout(15):
                    try:
                        m = await self.client.wait_for(
                            'message',
                            timeout=15.0,
                            check=lambda m: m.author == ctx.author)
                        if str(lower) == m.content:
                            await ctx.send("Correct!")
                        elif str(letter_ans) == m.content:
                            await ctx.send("Correct!")
                        else:
                            await ctx.send(f"Incorrect! The correct answer was {letter_ans}, {unes(data['correct_answer'])}.")
                    except Exception as error:
                        await ctx.send(error)
        except (asyncio.TimeoutError, asyncio.CancelledError):
            await message.edit(embed=discord.Embed(colour=colour).set_author(
                name=f"Times up! The correct answer was {unes(data['correct_answer'])}."))
    
    @commands.command(aliases=['ily'], help="compliment your friends :heart:")
    async def compliment(self, ctx, *, user: discord.Member = None):
        try:
            user = user or ctx.message.author
            user_name, user_discriminator = str(user).split("#")
            async with aiohttp.ClientSession() as cs:
                async with cs.get("https://complimentr.com/api") as r:
                    comp = await r.json()
                    await cs.close()
            
            await ctx.send(
                embed=discord.Embed(description=f"{user_name}, {unes(comp['compliment'])}", colour=colour).set_footer(
                    text="https://complimentr.com/api"))
        except Exception as error:
            await ctx.send(f"```py\n{error}```")
    
    @commands.group(help="Shows the weather in your city.", invoke_without_command=True)
    async def weather(self, ctx, city):
        try:
            async with aiohttp.ClientSession() as cs:
                async with cs.get(
                        f"http://api.openweathermap.org/data/2.5/weather?appid=2a5e00144cd0454e62a99f975c701c4e&q={city}") as r:
                    res = await r.json()
                topic = res['weather'][0]
                kelv_temp = round(res['main']['temp'], 1)
                cels_temp = round(kelv_temp - 273.15, 1)
                faren_temp = round(cels_temp * 1.8 + 32, 1)
                ts = res['sys']['sunrise']
                te = res['sys']['sunset']
                town = res['name']
                sunrise = datetime.datetime.fromtimestamp(ts).strftime("%H:%M")
                sunset = datetime.datetime.fromtimestamp(te).strftime("%H:%M")
                embed = discord.Embed(colour=colour, description="**" + unes(topic['main']) + "**" + '\n' + unes(
                    topic['description']).capitalize())
                embed.add_field(name="Info",
                                value=f"*Temperature:* **{cels_temp}**° C • **{faren_temp}**° F • **{kelv_temp}**° K\n*Sunrise:* **{sunrise} UTC**\n*Sunset:* **{sunset} UTC**")
                embed.set_footer(text=f"Weather for {town} • http://api.openweathermap.org")
                await ctx.send(embed=embed)
        except Exception:
            await ctx.send(
                "City probably not found. You can specify even more by adding your country as well. eg:\n`{}weather <city name>,<country name>`".format(
                    ctx.prefix))
    
    @commands.command(help="Shows you info about a Pokémon", aliases=['pokemon', 'poke', 'pokémon', 'pokédex'])
    async def pokedex(self, ctx, pokemon):
        abilities = []
        lst = []
        stats = []
        numlist = []
        try:
            async with self.session.get(f'https://pokeapi.co/api/v2/pokemon/{pokemon.lower()}') as r:
                res = await r.json()
                await self.session.close()
            sprite = res['sprites']['front_default']
            abils = res['abilities']
            s_s = res['stats']
            ts = res['types']
            for item in s_s:
                stats.append(f"**{STAT_NAMES[item['stat']['name']]}:** `{item['base_stat']}`")
            for ability in abils:
                abilities.append(f"**{ability['ability']['name'].capitalize()}**")
            for a in ts:
                lst.append(TYPES[a['type']['name']])
            for b in s_s:
                numlist.append(b['base_stat'])
            types = " ".join(lst[::-1])
            async with self.session.get(f"https://pokeapi.co/api/v2/pokemon-species/{res['id']}/") as r:
                data = await r.json()
                await self.session.close()
            embed = discord.Embed(color=colour, title=f"{pokemon.capitalize()} • #{res['id']}",
                                  description=f"{types}\n**Height:** {res['height'] / 10} m\n\n<:pokeball:715599637079130202> {unes(data['flavor_text_entries'][0]['flavor_text'])}")
            embed.add_field(name="Abilities", value="\n".join(abilities[::-1]), inline=False)
            embed.add_field(name="Stats", value="\n".join(stats[::-1]) + f"\n**Total**: `{sum(numlist)}`",
                            inline=False)
            embed.set_thumbnail(url=sprite)
            embed.set_footer(text="https://pokeapi.co/")
            await ctx.send(embed=embed)
        except Exception as error:
            await ctx.send(f"Error, Pokemon not found! (Note that the API does not yet support Generation 8)")
            await ctx.send(error)
    
    @commands.command(help="Urban Dictionary")
    async def urbandict(self, ctx, *, terms):
        try:
            async with self.session.get('http://api.urbandictionary.com/v0/define', params={'term': terms}) as r:
                res = await r.json()
                await self.session.close()
            term = res['list'][0]['definition']
            defin = res['list'][0]['example']
            trom = str(term).replace("[", "_")
            trom2 = str(trom).replace("]", "_")
            deph = str(defin).replace("[", "_")
            deph2 = str(deph).replace("]", "_")
            await ctx.send(
                embed=discord.Embed(title=terms, description=trom2, colour=colour))
        except Exception as error:
            await ctx.send(error)
            
    @commands.command()
    async def fact(self, ctx):
        """Random fact"""
        async with self.session.get("https://useless-facts.sameerkumar.website/api") as r:
            res = await r.json()
            await self.session.close()
        await ctx.send(embed=discord.Embed(title=res['data'], colour=colour))

def setup(client):
    client.add_cog(Internet(client))
