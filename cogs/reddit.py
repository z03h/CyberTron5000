import datetime
import json
import random

import aiohttp
import discord
import humanize
import praw
from discord.ext import commands

from .utils.lists import emotes

reddit_colour = 0xff5700


def secrets():
    with open("secrets.json", "r") as f:
        return json.load(f)


client_id = secrets()['client_id']
client_secret = secrets()['client_secret']
username = "CyberTron5000"
password = secrets()['password']
user_agent = secrets()['user_agent']


class Reddit(commands.Cog):
    """Commands interacting with the Reddit API."""
    
    def __init__(self, client):
        self.reddit = praw.Reddit(
            client_id=client_id,
            client_secret=client_secret,
            username=username,
            password=password,
            user_agent=user_agent
        )
        self.client = client
        self.up = "<:upvote:718895913342337036>"
        self.share = "<:share:729813718086582402>"
    
    @commands.command(aliases=['f'], help="Shows you food")
    async def food(self, ctx):
        async with ctx.typing():
            subreddit = random.choice(['food', 'cheeseburger', 'cake', 'donuts', 'pizza', 'burger'])
            posts = []
            async with aiohttp.ClientSession() as cs:
                async with cs.get(f"https://www.reddit.com/r/{subreddit}/hot.json") as r:
                    res = await r.json()
                for i in res['data']['children']:
                    posts.append(i['data'])
                s = random.choice([p for p in posts if not p['stickied'] or p['is_self']])
                embed = discord.Embed(title=str(s['title']), colour=reddit_colour,
                                      url=f"https://reddit.com/{s['permalink']}",
                                      description=f"{self.up} **{s['score']:,}** :speech_balloon: **{s['num_comments']:,}** {self.share} **{s['num_crossposts']:,}** :medal: **{s['total_awards_received']}**")
                embed.set_author(name=s['author'])
                embed.set_footer(text=f"{s['upvote_ratio'] * 100:,}% upvote ratio | posted to r/{s['subreddit']}")
                embed.set_image(url=s['url'])
                return await ctx.send(embed=embed) if not s['over_18'] or s['over_18'] and ctx.channel.is_nsfw() else await ctx.send(f"<:warning:727013811571261540> **{ctx.author.name}**, NSFW Channel required!")
    
    # noinspection PyBroadException
    @commands.command(aliases=['rs', 'karma'], help="Shows your Reddit Stats.")
    async def redditstats(self, ctx, user):
        trophies = []
        i = []
        try:
            async with ctx.typing():
                async with aiohttp.ClientSession() as cs:
                    async with cs.get(f"https://www.reddit.com/user/{user}/trophies/.json") as r:
                        res = await r.json()
                    for item in res['data']['trophies']:
                        if str(item['data']['name']).lower() in emotes:
                            trophies.append(emotes[str(item['data']['name']).lower()])
                        else:
                            trophies.append(" ")
                    for t in trophies:
                        if t not in i:
                            i.append(t)
                async with aiohttp.ClientSession() as cs:
                    async with cs.get(f"https://www.reddit.com/user/{user}/about/.json") as r:
                        k = await r.json()
                embed = discord.Embed(
                    colour=reddit_colour, title=f"u/{k['data']['name']}", url=f"https://reddit.com/user/{user}",
                    description=f"{k['data']['subreddit']['public_description']}\n\n<:karma:704158558547214426> **Karma** • **{k['data']['link_karma'] + k['data']['comment_karma']:,}**\n:link: **Link** • **{k['data']['link_karma']:,}**\n:speech_balloon: **Comment** • **{k['data']['comment_karma']:,}**\n**Trophies (Total {len(i)})**\n" + "".join(
                        i)
                ).set_author(name=k['data']['subreddit']['title'])
                embed.set_footer(
                    text="Account created on " + datetime.datetime.utcfromtimestamp(k['data']['created_utc']).strftime(
                        "%B %d, %Y"))
                icon = k['data']['icon_img']
                icon = icon.split("?")[0]
                embed.set_thumbnail(url=icon)
                await ctx.send(embed=embed)
        except Exception as error:
            await ctx.send("Redditor not found.")
            await ctx.send(error)
    
    @commands.command(aliases=['m'], help="Shows you a meme from some of reddit's dankest places (and r/memes)")
    async def meme(self, ctx):
        subreddit = random.choice(['memes', 'dankmemes', 'okbuddyretard', 'memeeconomy', 'dankexchange', 'pewdiepiesubmissions', 'memes_of_the_dank'])
        posts = []
        async with ctx.typing():
            async with aiohttp.ClientSession() as cs:
                async with cs.get(f"https://www.reddit.com/r/{subreddit}/hot.json") as r:
                    res = await r.json()
                for i in res['data']['children']:
                    posts.append(i['data'])
                s = random.choice([p for p in posts if not p['stickied'] or p['is_self']])
                embed = discord.Embed(title=str(s['title']), colour=reddit_colour,
                                      url=f"https://reddit.com/{s['permalink']}",
                                      description=f"{self.up} **{s['score']:,}** :speech_balloon: **{s['num_comments']:,}** {self.share} **{s['num_crossposts']:,}** :medal: **{s['total_awards_received']}**")
                embed.set_author(name=s['author'])
                embed.set_footer(text=f"{s['upvote_ratio'] * 100:,}% upvote ratio | posted to r/{s['subreddit']}")
                embed.set_image(url=s['url'])
                return await ctx.send(embed=embed) if not s['over_18'] or s['over_18'] and ctx.channel.is_nsfw() else await ctx.send(f"<:warning:727013811571261540> **{ctx.author.name}**, NSFW Channel required!")
        
    @commands.command(aliases=['iu'], help="Shows you the banner or icon of a subreddit (on old Reddit).")
    async def icon(self, ctx, subreddit, choice="img"):
        async with ctx.typing():
            reddit = self.reddit.subreddit(subreddit)
            choices = ['img', 'banner']
            resp = [reddit.icon_img, reddit.banner_img]
            if choice in choices:
                embed = discord.Embed(title=f'r/{reddit.display_name}', colour=reddit_colour)
                await ctx.send(embed=embed.set_image(url=resp[choices.index(choice)]))
            else:
                return await ctx.send("Error! Please pick `banner` or `img`.")
    
    @commands.command(help="Shows you info about a subreddit.")
    async def subreddit(self, ctx, subreddit):
        s = self.reddit.subreddit(subreddit)
        ts = s.created_utc
        async with ctx.typing():
            mods = [f'[{mod.name}](https://reddit.com/user/{mod.name})' for mod in s.moderator()]
            embed = discord.Embed(title=f"r/{s.display_name}", url=f'https://reddit.com/r/{subreddit}',
                                  colour=reddit_colour, description=s.public_description or " ")
            embed.add_field(name="General",
                            value=f"Subscribers: **{s.subscribers:,}**\nCreated: **{datetime.datetime.utcfromtimestamp(ts).strftime('%B %d, %Y')}**")
            embed.add_field(name=f"Mods (Total {len(mods)})", value="\n".join(mods[:10]), inline=False)
            embed.set_thumbnail(url=s.icon_img)
            await ctx.send(embed=embed)
        
    @commands.command(help="Shows you a wiki page for a subreddit.")
    async def wiki(self, ctx, subreddit, *, page):
        try:
            async with ctx.typing():
                s = self.reddit.subreddit(subreddit)
                wikipage = s.wiki[page]
                em = discord.Embed(title="/{}".format(page), description=(wikipage.content_md[:2000]), colour=reddit_colour,
                                   timestamp=ctx.message.created_at)
                em.set_footer(text="r/" + s.display_name, icon_url=s.icon_img)
                await ctx.send(embed=em)
        except Exception as err:
            await ctx.send(err)
    
    @commands.command(aliases=['mod'])
    async def moderator(self, ctx, mod, subreddit):
        async with ctx.typing():
            perms = [m.mod_permissions for m in self.reddit.subreddit(subreddit).moderator(mod)]
            await ctx.send(embed=discord.Embed(title=f"Mod Perms for {mod}", colour=reddit_colour,
                                                   description="\n".join(
                                                       [f"• {perm.capitalize()}" for perm in perms[0]])).set_author(
                name=f"r/{subreddit}", icon_url=self.reddit.subreddit(subreddit).icon_img))
        
    @commands.command(aliases=['showerthought'], help="hmm :thinking:")
    async def thonk(self, ctx):
        posts = []
        async with ctx.typing():
            async with aiohttp.ClientSession() as cs:
                async with cs.get(f"https://www.reddit.com/r/ShowerThoughts/hot.json") as r:
                    res = await r.json()
                for i in res['data']['children']:
                    posts.append(i['data'])
                s = random.choice([p for p in posts if not p['stickied']])
                embed = discord.Embed(title=str(s['title']), colour=reddit_colour,
                                      url=f"https://reddit.com/{s['permalink']}",
                                      description=f"{self.up} **{s['score']:,}** :speech_balloon: **{s['num_comments']:,}** {self.share} **{s['num_crossposts']:,}** :medal: **{s['total_awards_received']}**")
                embed.set_author(name=s['author'])
                embed.set_footer(text=f"{s['upvote_ratio'] * 100:,}% upvote ratio | posted to r/{s['subreddit']}")
                return await ctx.send(embed=embed) if not s['over_18'] or s['over_18'] and ctx.channel.is_nsfw() else await ctx.send(f"<:warning:727013811571261540> **{ctx.author.name}**, NSFW Channel required!")
    
    # mod stats
    
    @commands.command(aliases=['ms'])
    async def modstats(self, ctx, user):
        """Shows you the moderated subreddits of a specific user."""
        try:
            async with ctx.typing():
                async with aiohttp.ClientSession() as cs:
                    async with cs.get(f"https://www.reddit.com/user/{user}/moderated_subreddits/.json") as r:
                        res = await r.json()
                    subreddits = res['data']
                    reddits = [
                        f"[{subreddit['sr_display_name_prefixed']}](https://reddit.com{subreddit['url']}) • <:member:716339965771907099> **{subreddit['subscribers']:,}**"
                        for subreddit in subreddits]
                    numbas = [s['subscribers'] for s in subreddits]
                    msg = "Top 15 Subreddits" if len(reddits) > 15 else "Moderated Subreddits"
                    modstats = [f"{i}. {v}" for i, v in enumerate(reddits, 1)]
                    final_ms = "\n".join(modstats)
                    zero_subs = len([item for item in numbas if item == 0])
                    one_subs = len([item for item in numbas if item == 1])
                    hundred_subs = len([item for item in numbas if item >= 100])
                    thousand_subs = len([item for item in numbas if item >= 1000])
                    hundred_thousand_subs = len([item for item in numbas if item >= 100_000])
                    million = len([item for item in numbas if item >= 1_000_000])
                    ten_million = len([item for item in numbas if item >= 10_000_000])
                    embed = discord.Embed(
                        description=f"u/{user} mods **{len(reddits):,}** subreddits with **{humanize.intcomma(sum(numbas))}** total readers\n\n*{msg}*\n\n{final_ms}",
                        colour=reddit_colour)
                    embed.add_field(name="Advanced Statistics",
                                    value=f"Subreddits with 0 subscribers: **{zero_subs}**\nSubreddits with 1 subscriber: **{one_subs}**\nSubreddits with 100 or more subscribers: **{hundred_subs}**\nSubreddits with 1,000 or more subscribers: **{thousand_subs}**\nSubreddits with 100,000 or more subscribers: **{hundred_thousand_subs}**\nSubreddits with 1,000,000 or more subscribers: **{million}**\nSubreddits with 10,000,000 or more subscribers: **{ten_million}**\n\nAverage Subscribers Per Subreddit: **{humanize.intcomma(round(sum(numbas) / len(numbas)))}**")
                await ctx.send(embed=embed)
        except Exception as error:
            await ctx.send(
                f"Moderator not found/Author not verified. To verify, do `{ctx.prefix}verify [reddit username]`")
            await ctx.send(error)
    
    @commands.command(aliases=['ask'])
    async def askreddit(self, ctx):
        """Ask Reddit..."""
        async with ctx.typing():
            posts = []
            comments = []
            for submission in self.reddit.subreddit("AskReddit").hot(limit=50):
                posts.append(submission)
            final_post = random.choice(posts)
            embed = discord.Embed(title=final_post.title, url=final_post.url,
                                  description=final_post.selftext + f"\n**{final_post.score:,}** <:upvote:718895913342337036> **{final_post.num_comments:,}** 💬",
                                  colour=reddit_colour)
            embed.set_author(name=final_post.author, icon_url=final_post.author.icon_img)
            for top_level_comment in final_post.comments:
                comments.append(top_level_comment)
            final_comment = random.choice(comments)
            embed.add_field(
                name=f"{final_comment.author} • **{final_comment.score:,}** <:upvote:718895913342337036> **{len(final_comment.replies):,}** 💬",
                value=final_comment.body)
            await ctx.send(embed=embed)
    
    @commands.command(help="Gets a post from a subreddit of your choosing.")
    async def post(self, ctx, subreddit, sort='hot'):
        posts = []
        sorts = ['new', 'hot', 'top', 'rising', 'controversial']
        if sort not in sorts:
            return await ctx.send(f"<:warning:727013811571261540> **{ctx.author.name}**, that isn't a valid sort! Valid sorts include {', '.join(sorts)}.")
        async with ctx.typing():
            async with aiohttp.ClientSession() as cs:
                async with cs.get(f"https://www.reddit.com/r/{subreddit}/{sort}.json") as r:
                    res = await r.json()
                for i in res['data']['children']:
                    posts.append(i['data'])
                s = random.choice([p for p in posts if not p['stickied'] or p['is_self']])
                embed = discord.Embed(title=str(s['title']), colour=reddit_colour,
                                      url=f"https://reddit.com/{s['permalink']}")
                embed.set_author(name=s['author'])
                embed.set_footer(text=f"{s['upvote_ratio'] * 100:,}% upvote ratio | posted to r/{s['subreddit']}")
                if s['is_self']:
                    embed.description = f"{s['selftext']}\n{self.up} **{s['score']:,}** :speech_balloon: **{s['num_comments']:,}** {self.share} **{s['num_crossposts']:,}** :medal: **{s['total_awards_received']}**"
                    return await ctx.send(embed=embed) if not s['over_18'] or s['over_18'] and ctx.channel.is_nsfw() else await ctx.send(f"<:warning:727013811571261540> **{ctx.author.name}**, NSFW Channel required!")
                else:
                    embed.set_image(url=s['url'])
                    embed.description = f"{self.up} **{s['score']:,}** :speech_balloon: **{s['num_comments']:,}** {self.share} **{s['num_crossposts']:,}** :medal: **{s['total_awards_received']}**"
                    return await ctx.send(embed=embed) if not s['over_18'] or s['over_18'] and ctx.channel.is_nsfw() else await ctx.send(f"<:warning:727013811571261540> **{ctx.author.name}**, NSFW Channel required!")


def setup(client):
    client.add_cog(Reddit(client))
