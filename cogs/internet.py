import asyncio
import datetime
import random
import json
import async_cleverbot
from html import unescape as unes

import aiohttp
import aiogoogletrans
import discord
from async_timeout import timeout
from discord.ext import commands

from .utils.lists import STAT_NAMES, NUMBER_ALPHABET, TYPES
from .utils import cyberformat


# ≫

def secrets():
    with open("secrets.json", "r") as f:
        return json.load(f)


class Internet(commands.Cog):
    """Interact with various API's"""
    
    def __init__(self, client):
        self.client = client
        self.pypi = "https://raw.githubusercontent.com/github/explore/666de02829613e0244e9441b114edb85781e972c/topics/pip/pip.png"
        self.bot = async_cleverbot.Cleverbot(secrets()['cleverbot'])
        self.bot.set_context(async_cleverbot.DictContext(self.bot))
    
    @commands.command(aliases=['kitty'], help="haha kitty go meow meow.")
    async def cat(self, ctx):
        async with aiohttp.ClientSession() as cs:
            async with cs.get('https://aws.random.cat/meow') as r:
                res = await r.json()
        em = discord.Embed(colour=self.client.colour, title="OwO", url=res['file'])
        em.set_image(url=res['file'])
        await cs.close()
        em.set_footer(text="https://aws.random.cat/meow")
        await ctx.send(embed=em)
    
    @commands.command(aliases=['puppy', 'pup', 'pupper'], help="haha puppy go woof woof")
    async def dog(self, ctx):
        async with aiohttp.ClientSession() as cs:
            async with cs.get('https://random.dog/woof.json') as r:
                res = await r.json()
                res = res['url']
                await cs.close()
        em = discord.Embed(colour=self.client.colour, title="Woof!", url=res)
        em.set_image(url=res)
        em.set_footer(text="https://random.dog/woof.json")
        await ctx.send(embed=em)
    
    @commands.command(help="Get's you a trivia question.", aliases=['tr', 't'])
    async def trivia(self, ctx, difficulty: str = None):
        try:
            an = []
            difficulty = random.choice(['easy', 'medium', 'hard']) if not difficulty else difficulty
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
                                      colour=self.client.colour)
                embed.set_author(name=f"{ctx.message.author.display_name}'s question:",
                                 icon_url=ctx.message.author.avatar_url)
                embed.add_field(name="Question Info",
                                value=f"This question about **{unes(data['category'])}** is of **{unes(data['difficulty']).capitalize()}** difficulty")
                embed.set_footer(text="https://opentdb.com")
                letter_ans = NUMBER_ALPHABET[answers.index(''.join(unes(data['correct_answer']))) + 1]
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
                    f"<:warning:727013811571261540> **{ctx.author.name}**, invalid difficulty! Valid difficulties include easy, medium, hard.")
            elif isinstance(error, asyncio.TimeoutError) or isinstance(error, asyncio.CancelledError):
                await message.edit(embed=discord.Embed(colour=self.client.colour).set_author(
                    name=f"Times up! The correct answer was {unes(data['correct_answer'])}."))
            else:
                await ctx.send(error.__class__.__name__)
    
    @commands.command(aliases=['ily'], help="compliment your friends :heart:")
    async def compliment(self, ctx, *, user: discord.Member = None):
        try:
            user = user or ctx.message.author
            async with aiohttp.ClientSession() as cs:
                async with cs.get("https://complimentr.com/api") as r:
                    comp = await r.json()
                    await cs.close()
            
            await ctx.send(
                embed=discord.Embed(description=f"{user.name}, {unes(comp['compliment'])}",
                                    colour=self.client.colour).set_footer(
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
                    await cs.close()
                topic = res['weather'][0]
                kelv_temp = round(res['main']['temp'], 1)
                cels_temp = round(kelv_temp - 273.15, 1)
                faren_temp = round(cels_temp * 1.8 + 32, 1)
                ts = res['sys']['sunrise']
                te = res['sys']['sunset']
                town = res['name']
                sunrise = datetime.datetime.fromtimestamp(ts).strftime("%H:%M")
                sunset = datetime.datetime.fromtimestamp(te).strftime("%H:%M")
                embed = discord.Embed(colour=self.client.colour,
                                      description="**" + unes(topic['main']) + "**" + '\n' + unes(
                                          topic['description']).capitalize())
                embed.add_field(name="Info",
                                value=f"*Temperature:* **{cels_temp}**° C • **{faren_temp}**° F • **{kelv_temp}**° K\n*Sunrise:* **{sunrise} UTC**\n*Sunset:* **{sunset} UTC**")
                embed.set_footer(text=f"Weather for {town} • http://api.openweathermap.org")
                await ctx.send(embed=embed)
        except KeyError:
            await ctx.send(
                f"<:warning:727013811571261540> **{ctx.author.name}**, city probably not found. You can specify even more by adding your country as well. eg:\n`{ctx.prefix}weather <city name>,<country name>`")
    
    @commands.command(help="Shows you info about a Pokémon", aliases=['pokemon', 'poke', 'pokémon', 'pokédex'])
    async def pokedex(self, ctx, pokemon):
        try:
            async with aiohttp.ClientSession() as cs:
                async with cs.get(f"https://some-random-api.ml/pokedex?pokemon={pokemon.lower()}") as r:
                    res = await r.json()
                if r.status != 200:
                    return await ctx.send("Error!")
                embed = discord.Embed(title=f"{res[0]['name'].title()} • #{res[0]['id']}", colour=self.client.colour)
                embed.set_author(name=f'The {" ".join(res[0]["species"])}')
                embed.set_thumbnail(url=res[0]['sprites']['normal'])
                evo_line = []
                for e in res[0]['family']['evolutionLine']:
                    if str(e).lower() == pokemon:
                        evo_line.append(f"**{e}**")
                    else:
                        evo_line.append(e)
                n = '\n'
                embed.description = f" ".join([TYPES[item.lower()] for item in res[0]['type']])
                embed.description += f'\n<:pokeball:715599637079130202> {res[0]["description"]}\n**{res[0]["height"]}**\n**{res[0]["weight"]}**'
                embed.add_field(name='Evolution Line', value=f'{" → ".join(evo_line)}' or "**{0.capitalize()}**".format(str(pokemon)), inline=False)
                embed.add_field(name='Abilities', value=', '.join([f'**{i}**' for i in res[0]['abilities']]), inline=False)
                embed.add_field(name='Base Stats', value=f"{f'{n}'.join([f'**{STAT_NAMES[key]}:** `{value}`' for key, value in res[0]['stats'].items()])}", inline=False)
                await ctx.send(embed=embed)
        except IndexError:
            await ctx.send(
                f"<:warning:727013811571261540> **{ctx.author.name}**, error, Pokémon not found!")
    
    @commands.command(help="Urban Dictionary", aliases=['urban', 'define', 'def'])
    async def urbandict(self, ctx, *, terms):
        try:
            async with aiohttp.ClientSession() as cs:
                async with cs.get('http://api.urbandictionary.com/v0/define', params={'term': terms}) as r:
                    res = await r.json()
                term = res['list'][0]['definition']
                defin = res['list'][0]['example']
                term = cyberformat.hyper_replace(term, ['[', ']'], ['', ''])
                example = cyberformat.hyper_replace(defin, ['[', ']'], ['', ''])
                await cs.close()
                await ctx.send(
                    embed=discord.Embed(title=terms, description=term[:2000] + f"\n\n**Example:**\n{example}",
                                        colour=self.client.colour))
        except(IndexError, KeyError, ValueError):
            await ctx.send(f"<:warning:727013811571261540> **{ctx.author.name}**, term not found on urban dictionary.")
    
    @commands.command()
    async def fact(self, ctx):
        """Random fact"""
        async with aiohttp.ClientSession() as cs:
            async with cs.get("https://useless-facts.sameerkumar.website/api") as r:
                res = await r.json()
                await cs.close()
        await ctx.send(embed=discord.Embed(title=res['data'], colour=self.client.colour))
    
    @commands.command()
    async def pypi(self, ctx, *, package):
        try:
            async with aiohttp.ClientSession() as cs:
                async with cs.get(f"https://pypi.org/pypi/{package}/json") as r:
                    res = await r.json()
        except Exception as er:
            if isinstance(er, aiohttp.ContentTypeError):
                return await ctx.send(
                    f"<:warning:727013811571261540> **{ctx.author.name}**, package not found! Check for spelling.")
            else:
                return await ctx.send(f"Unknown error occured: {er.__class__.__name__}. Code: {r.status}")
        char = '\u200b' if not res['info']['author_email'] else f' • {res["info"]["author_email"]}'
        embed = discord.Embed(title=res['info']['name'], url=res['info']['project_url'], colour=self.client.colour,
                              description=f"{res['info']['summary']}\n:scales: **{res['info']['license']}**\n[Home Page]({res['info']['home_page']})\n[Package URL]({res['info']['package_url']})",
                              timestamp=ctx.message.created_at)
        embed.set_footer(text=f"{res['info']['name']} version {res['info']['version']}")
        embed.set_author(name=res['info']['author'] + char, icon_url=self.pypi)
        embed.add_field(name="Python Requirements", value=res['info']['requires_python'].replace("*", ""),
                        inline=False) if res['info']['requires_python'] else None
        pm = '\u200b' if len(res['info']['requires_dist']) <= 5 else "\n..."
        pm2 = '\u200b' if len(res['info']['classifiers']) <= 5 else "\n..."
        embed.add_field(name=f"Requires (Total {len(res['info']['requires_dist'])})",
                        value="\n".join([f"• {i}" for i in res['info']['requires_dist']][:5]) + pm, inline=False) if \
            res['info']['requires_dist'] else None
        embed.add_field(name=f"Classifiers (Total {len(res['info']['classifiers'])})",
                        value="\n".join([f"• {i}" for i in res['info']['classifiers']][:5]) + pm2, inline=False) if \
            res['info']['classifiers'] else None
        await ctx.send(embed=embed)
    
    @commands.command(aliases=['cb'])
    async def cleverbot(self, ctx, *, text: str):
        """
        Ask the clever bot a question.
        """
        async with ctx.typing():
            if len(ctx.message.content) < 2 or len(ctx.message.content) > 60:
                return await ctx.send(
                    f"**{ctx.author.name}**, text must be below 60 characters and over 2.")
            resp = await self.bot.ask(text, ctx.author.id)
            r = str(resp) if str(resp).startswith("I") else cyberformat.minimalize(str(resp))
            if str(r)[-1] not in ['.', '?', '!']:
                suff = "?" if any(s in str(r) for s in ['who', 'what', 'when', 'where', 'why', 'how']) else "."
            else:
                suff = "\u200b"
            send = cyberformat.hyper_replace(str(r), old=[' i ', "i'm", "i'll"], new=[' I ', "I'm", "I'll"])
            await ctx.send(f"**{ctx.author.name}**, {send}{suff}")
    
    @commands.group(invoke_without_command=True, aliases=['trans'])
    async def translate(self, ctx, message):
        translator = aiogoogletrans.Translator()
        res = await translator.translate(message)
        from_lang = aiogoogletrans.LANGUAGES[res.src]
        to_lang = aiogoogletrans.LANGUAGES[res.dest]
        embed = discord.Embed(colour=self.client.colour,
                              description=f"**{from_lang.title()}**\n{message}\n\n**{to_lang.title()}**\n{res.text}\n\n**Pronunciation**\n{res.pronunciation}").set_author(
            name='Translated Text')
        return await ctx.send(embed=embed.set_footer(text=f"{round(res.confidence * 100)}% confident"))
    
    @translate.command(name='to', invoke_without_command=True)
    async def to(self, ctx, target_lang, message):
        translator = aiogoogletrans.Translator()
        try:
            res = await translator.translate(message, dest=target_lang)
        except ValueError:
            return await ctx.send(
                f"<:warning:727013811571261540> **{ctx.author.name}**, `{target_lang}` is not a valid langauge!")
        from_lang = aiogoogletrans.LANGUAGES[res.src]
        to_lang = aiogoogletrans.LANGUAGES[res.dest]
        embed = discord.Embed(colour=self.client.colour,
                              description=f"**{from_lang.capitalize()}**\n{message}\n\n**{to_lang.capitalize()}**\n{res.text}\n\n**Pronunciation**\n{res.pronunciation}").set_author(
            name='Translated Text')
        return await ctx.send(embed=embed.set_footer(text=f"{res.confidence * 100}% confident"))


def setup(client):
    client.add_cog(Internet(client))
