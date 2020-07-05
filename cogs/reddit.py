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
        self.loading = "https://media1.tenor.com/images/8f7a28e62f8242b264c8a39ba8bea261/tenor.gif?itemid=15922897"
    
    @commands.command(aliases=['f'], help="Shows you food")
    async def food(self, ctx):
        embedd = discord.Embed(
            colour=reddit_colour, title="Loading..."
        )
        embedd.set_image(
            url=self.loading)
        message = await ctx.send(embed=embedd)
        post = []
        for submission in self.reddit.subreddit(
                'food+sushi+cheeseburger+pasta+cake+lasagna+burger+pizza+fries+spaghetti+dumplings+rice+noodles+pho').top(
            'day'):
            if not submission.stickied:
                post.append(submission)
        submission = random.choice(post)
        ts = int(submission.created_utc)
        embed = discord.Embed(title=submission.title, url=f'https://www.reddit.com{submission.permalink}',
                              colour=reddit_colour,
                              description="**{:,.0f}** <:upvote:718895913342337036> **{:,.0f}** 💬\n{}"
                              .format(submission.score, submission.num_comments,
                                      datetime.datetime.fromtimestamp(ts).strftime('%B %d, %Y')),
                              timestamp=ctx.message.created_at)
        embed.set_author(name=submission.author.name, icon_url=submission.author.icon_img)
        embed.set_image(url=submission.url)
        embed.set_footer(text=f'r/{submission.subreddit}', icon_url=submission.subreddit.icon_img)
        await message.edit(embed=embed)
    
    # noinspection PyBroadException
    @commands.command(aliases=['rs', 'karma'], help="Shows your Reddit Stats.")
    async def redditstats(self, ctx, user):
        trophies = []
        i = []
        try:
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
            embedd = discord.Embed(
                colour=reddit_colour, title="Loading..."
            )
            embedd.set_image(
                url=self.loading)
            message = await ctx.send(embed=embedd)
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
            await message.edit(embed=embed)
        except Exception as error:
            await ctx.send("Redditor not found.")
            await ctx.send(error)
    
    @commands.command(aliases=['m'])
    async def meme(self, ctx):
        """Gets a random meme from some of reddit's dankest places (and r/memes)"""
        message = await ctx.send(
            embed=discord.Embed(colour=reddit_colour, title="Loading...").set_image(url=self.loading))
        reddit = self.reddit.subreddit(
            'dankmemes+memes+okbuddyretard+comedyheaven+memeeconomy+dankexchange+memes_of_the_dank+pewdiepiesubmissions+dankexchange')
        reddits = [reddit.new(limit=50), reddit.controversial(limit=50), reddit.rising(limit=50), reddit.top(limit=150),
                   reddit.top(limit=1), reddit.hot(limit=80), reddit.controversial(limit=1)]
        posts = [x for x in reddits[5] if not x.stickied]
        submission = random.choice(posts)
        if submission.is_self:
            embed = discord.Embed(title=submission.title, url=f'https://www.reddit.com{submission.permalink}',
                                  colour=reddit_colour,
                                  description="{}\n**{:,.0f}** <:upvote:718895913342337036> **{:,.0f}** 💬".format(
                                      submission.selftext, submission.score, submission.num_comments))
        else:
            embed = discord.Embed(title=submission.title, url=f'https://www.reddit.com{submission.permalink}',
                                  colour=reddit_colour,
                                  description="**{:,.0f}** <:upvote:718895913342337036> **{:,.0f}** 💬".format(
                                      submission.score, submission.num_comments))
            embed.set_image(url=submission.url)
        ts = int(submission.created_utc)
        embed.set_author(name=f"{submission.author.name}", icon_url=submission.author.icon_img)
        embed.set_footer(
            text='r/{} • {}'.format(submission.subreddit, datetime.datetime.fromtimestamp(ts).strftime('%B %d, %Y')),
            icon_url=submission.subreddit.icon_img)
        await message.edit(
            embed=embed) if not submission.over_18 or submission.over_18 and ctx.channel.is_nsfw() else await ctx.send(
            f"<:warning:727013811571261540> **{ctx.author.name}**, NSFW Channel required!")
    
    @commands.command(aliases=['iu'], help="Shows you the banner or icon of a subreddit (on old Reddit).")
    async def icon(self, ctx, subreddit, choice="img"):
        message = await ctx.send("** **", embed=discord.Embed(title="Loading...", colour=reddit_colour).set_image(
            url=self.loading))
        reddit = self.reddit.subreddit(subreddit)
        choices = ['img', 'banner']
        resp = [reddit.icon_img, reddit.banner_img]
        if choice in choices:
            embed = discord.Embed(title=f'r/{reddit.display_name}', colour=reddit_colour)
            await message.edit(embed=embed.set_image(url=resp[choices.index(choice)]))
        else:
            return await ctx.send("Error! Please pick `banner` or `img`.")
    
    @commands.command(help="Shows you info about a subreddit.")
    async def subreddit(self, ctx, subreddit):
        s = self.reddit.subreddit(subreddit)
        ts = s.created_utc
        message = await ctx.send(
            embed=discord.Embed(title="Loading...", colour=reddit_colour).set_image(url=self.loading))
        mods = [f'[{mod.name}](https://reddit.com/user/{mod.name})' for mod in s.moderator()]
        embed = discord.Embed(title=f"r/{s.display_name}", url=f'https://reddit.com/r/{subreddit}',
                              colour=reddit_colour, description=s.public_description or " ")
        embed.add_field(name="General",
                        value=f"Subscribers: **{s.subscribers:,}**\nCreated: **{datetime.datetime.utcfromtimestamp(ts).strftime('%B %d, %Y')}**")
        embed.add_field(name=f"Mods (Total {len(mods)})", value="\n".join(mods[:10]), inline=False)
        embed.set_thumbnail(url=s.icon_img)
        await message.edit(embed=embed)
    
    @commands.command(help="Shows you a wiki page for a subreddit.")
    async def wiki(self, ctx, subreddit, *, page):
        try:
            embedd = discord.Embed(
                colour=reddit_colour, title="Loading..."
            )
            embedd.set_image(
                url=self.loading)
            message = await ctx.send(embed=embedd)
            s = self.reddit.subreddit(subreddit)
            wikipage = s.wiki[page]
            em = discord.Embed(title="/{}".format(page), description=(wikipage.content_md[:2000]), colour=reddit_colour,
                               timestamp=ctx.message.created_at)
            em.set_footer(text="r/" + s.display_name, icon_url=s.icon_img)
            await message.edit(embed=em)
        except Exception as err:
            await ctx.send(err)
    
    @commands.command(aliases=['mod'])
    async def moderator(self, ctx, mod, subreddit):
        message = await ctx.send(
            embed=discord.Embed(colour=reddit_colour, title="Loading...").set_image(url=self.loading))
        perms = [m.mod_permissions for m in self.reddit.subreddit(subreddit).moderator(mod)]
        await message.edit(embed=discord.Embed(title=f"Mod Perms for {mod}", colour=reddit_colour,
                                               description="\n".join(
                                                   [f"• {perm.capitalize()}" for perm in perms[0]])).set_author(
            name=f"r/{subreddit}", icon_url=self.reddit.subreddit(subreddit).icon_img))
    
    @commands.command(help="hmmmmm <:thonking:667528766439817216>")
    async def thonk(self, ctx):
        embedd = discord.Embed(colour=reddit_colour, title="Loading...")
        embedd.set_image(url=self.loading)
        message = await ctx.send(embed=embedd)
        post = []
        for submission in self.reddit.subreddit(
                "ShowerThoughts").top("day"):
            if not submission.stickied:
                post.append(submission)
        submission = random.choice(post)
        embed = discord.Embed(title=submission.title,
                              url=f'https://www.reddit.com{submission.permalink}',
                              colour=reddit_colour,
                              description="{}\n**{:,.0f}** <:upvote:718895913342337036> **{:,.0f}** 💬"
                              .format(submission.selftext, submission.score,
                                      submission.num_comments))
        ts = submission.created_utc
        embed.set_author(name=submission.author.name, icon_url=submission.author.icon_img)
        embed.set_footer(
            text=f"r/{submission.subreddit} • {datetime.datetime.fromtimestamp(ts).strftime('%B %d, %Y')}",
            icon_url=submission.subreddit.icon_img)
        await message.edit(
            embed=embed) if not submission.over_18 or submission.over_18 and ctx.channel.is_nsfw() else await ctx.send(
            f"<:warning:727013811571261540> **{ctx.author.name}**, NSFW Channel required!")
    
    # mod stats
    
    @commands.command(aliases=['ms'])
    async def modstats(self, ctx, user):
        """Shows you the moderated subreddits of a specific user."""
        try:
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
        embedd = discord.Embed(colour=reddit_colour, title="Loading...")
        embedd.set_image(url=self.loading)
        message = await ctx.send("** **", embed=embedd)
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
        await message.edit(embed=embed)
    
    @commands.command()
    async def post(self, ctx, subreddit, sort='hot'):
        """Gets a random post from a subreddit"""
        try:
            message = await ctx.send(
                embed=discord.Embed(colour=reddit_colour, title="Loading...").set_image(url=self.loading))
            reddit = self.reddit.subreddit(subreddit)
            sorts = ['new', 'controversial', 'rising', 'top', 'topever', 'hot', 'controversialever']
            reddits = [reddit.new(limit=50), reddit.controversial(limit=50), reddit.rising(limit=50),
                       reddit.top(limit=150), reddit.top(limit=1), reddit.hot(limit=80), reddit.controversial(limit=1)]
            if sort in sorts:
                posts = [x for x in reddits[sorts.index(sort)] if not x.stickied]
            else:
                return await ctx.send(
                    f"<:warning:727013811571261540> **{ctx.author.name}**, that isn't a valid sort! Valid sorts include {', '.join(sorts)}.")
            submission = random.choice(posts)
            if submission.is_self:
                embed = discord.Embed(title=submission.title, url=f'https://www.reddit.com{submission.permalink}',
                                      colour=reddit_colour,
                                      description="{}\n**{:,.0f}** <:upvote:718895913342337036> **{:,.0f}** 💬".format(
                                          submission.selftext, submission.score, submission.num_comments))
            else:
                embed = discord.Embed(title=submission.title, url=f'https://www.reddit.com{submission.permalink}',
                                      colour=reddit_colour,
                                      description="**{:,.0f}** <:upvote:718895913342337036> **{:,.0f}** 💬".format(
                                          submission.score, submission.num_comments))
                embed.set_image(url=submission.url)
            ts = int(submission.created_utc)
            embed.set_author(name=f"{submission.author.name}", icon_url=submission.author.icon_img)
            embed.set_footer(text='r/{} • {}'.format(submission.subreddit,
                                                     datetime.datetime.fromtimestamp(ts).strftime('%B %d, %Y')),
                             icon_url=submission.subreddit.icon_img)
            await message.edit(
                embed=embed) if not submission.over_18 or submission.over_18 and ctx.channel.is_nsfw() else await ctx.send(
                f"<:warning:727013811571261540> **{ctx.author.name}**, NSFW Channel required!")
        except Exception as e:
            await ctx.send(e)


def setup(client):
    client.add_cog(Reddit(client))
