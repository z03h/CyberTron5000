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
                embedd = discord.Embed(
                colour=reddit_colour, title="Loading..."
            )
            async with aiohttp.ClientSession() as cs:
                async with cs.get(f"https://www.reddit.com/user/{user}/about/.json") as r:
                    k = await r.json()
            embedd.set_image(
                url=self.loading)
            message = await ctx.send(embed=embedd)
            embed = discord.Embed(
                colour=reddit_colour, title=f"u/{k['data']['name']}", url=f"https://reddit.com/user/{user}",
                description=f"<:karma:704158558547214426> **Karma** • **{k['data']['link_karma'] + k['data']['comment_karma']:,}**\n:link: **Link** • **{k['data']['link_karma']:,}**\n:speech_balloon: **Comment** • **{k['data']['comment_karma']:,}**\n**Trophies (Total {len(i)})**\n" + "".join(i)
            ).set_author(name=k['data']['subreddit']['title'])
            embed.set_footer(text="Account created on " + datetime.datetime.utcfromtimestamp(k['data']['created_utc']).strftime("%B %d, %Y"))
            icon = k['data']['icon_img']
            icon = icon.split("?")[0]
            embed.set_thumbnail(url=icon)
        except Exception:
            await ctx.send("Redditor not found.")

    @commands.command(aliases=['m'], help="Gets a meme from some of reddit's dankest places (and r/memes).")
    async def meme(self, ctx):
        embedd = discord.Embed(
            colour=reddit_colour, title="Loading..."
        )
        embedd.set_image(
            url=self.loading)
        message = await ctx.send(embed=embedd)
        post = []
        for submission in self.reddit.subreddit(
                'dankmemes+memes+okbuddyretard+comedyheaven+memeeconomy+dankexchange+memes_of_the_dank+pewdiepiesubmissions+dankexchange').top(
            'day'):
            if not submission.stickied:
                post.append(submission)
        submission = random.choice(post)
        if submission.over_18:
            if ctx.message.channel.is_nsfw():
                if submission.is_self:
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
                    await message.edit(embed=embed)
                else:
                    ts = int(submission.created_utc)
                    embed = discord.Embed(title=submission.title,
                                          url=f'https://www.reddit.com{submission.permalink}',
                                          colour=reddit_colour,
                                          description="**{:,.0f}** <:upvote:718895913342337036> **{:,.0f}** 💬"
                                          .format(submission.score, submission.num_comments))
            
                    embed.set_image(url=submission.url)
                    embed.set_author(name=f"{submission.author.name}", icon_url=submission.author.icon_img)
                    embed.set_footer(text='r/{} • {}'.format(submission.subreddit,
                                                             datetime.datetime.fromtimestamp(ts).strftime(
                                                                 '%B %d, %Y')),
                                     icon_url=submission.subreddit.icon_img)
        
                await message.edit(embed=embed)
            else:
                await message.edit(
                    embed=discord.Embed(colour=reddit_colour).set_author(name="NSFW Channel required for this!"))
        else:
            if submission.is_self:
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
                await message.edit(embed=embed)
            else:
                ts = int(submission.created_utc)
                embed = discord.Embed(title=submission.title,
                                      url=f'https://www.reddit.com{submission.permalink}',
                                      colour=reddit_colour,
                                      description="**{:,.0f}** <:upvote:718895913342337036> **{:,.0f}** 💬"
                                      .format(submission.score, submission.num_comments))
        
                embed.set_image(url=submission.url)
                embed.set_author(name=f"{submission.author.name}", icon_url=submission.author.icon_img)
                embed.set_footer(text='r/{} • {}'.format(submission.subreddit,
                                                         datetime.datetime.fromtimestamp(ts).strftime(
                                                             '%B %d, %Y')),
                                 icon_url=submission.subreddit.icon_img)
    
            await message.edit(embed=embed)

    @commands.command(aliases=['iu'], help="Shows you the banner or icon of a subreddit (on old Reddit).")
    async def icon(self, ctx, subreddit, banner_or_img="img"):
        embedd = discord.Embed(
            colour=reddit_colour, title="Loading..."
        )
        embedd.set_image(
            url=self.loading)
        message = await ctx.send(embed=embedd)
        s = self.reddit.subreddit(subreddit)
        if banner_or_img == "img":
            try:
                b = s.icon_img
                a = discord.Embed(colour=reddit_colour, title="r/{}".format(s), url=f"https://reddit.com/r/{subreddit}")
                if s is None:
                    a.add_field(name="Subreddit does not have Icon.", value="rip")
                    await message.edit(embed=a)
                else:
                    a.set_image(url=b)
                    await message.edit(embed=a)
            except Exception as err:
                k = discord.Embed(color=0xff0000)
                k.set_author(name=f"Couldn't find subreddit r/{subreddit}")
                await ctx.message.add_reaction(emoji="⚠️")
                await ctx.send(embed=k)
                await message.delete()
        elif banner_or_img == "banner":
            try:
                b = s.banner_img
                a = discord.Embed(colour=reddit_colour, title="r/{}".format(s), url=f"https://reddit.com/r/{subreddit}")
                if s is None:
                    a.add_field(name="Subreddit does not have Banner.", value="rip")
                    await message.edit(embed=a)
            
                else:
                    a.set_image(url=b)
                    await message.edit(embed=a)
            except Exception as err:
                k = discord.Embed(color=0xff0000)
                k.set_author(name=f"Couldn't find subreddit r/{subreddit}")
                await ctx.message.add_reaction(emoji="⚠️")
                await ctx.send(embed=k)
                await message.delete()
        
        elif banner_or_img is None:
            try:
                b = s.icon_img
                a = discord.Embed(colour=reddit_colour, title="r/{}".format(s), url=f"https://reddit.com/r/{subreddit}")
                if s is None:
                    a.add_field(name="Subreddit does not have Icon.", value="rip")
                    await message.edit(embed=a)
                
                else:
                    a.set_image(url=b)
                    await message.edit(embed=a)
            except Exception as err:
                k = discord.Embed(color=0xff0000)
                k.set_author(name=f"Couldn't find subreddit r/{subreddit}")
                await ctx.message.add_reaction(emoji="⚠️")
                await ctx.send(embed=k)
                await message.delete()
    
    @commands.command(help="Shows you info about a subreddit.")
    async def subreddit(self, ctx, subreddit):
        mods = []
        try:
            embedd = discord.Embed(
                colour=reddit_colour, title="Loading..."
            )
            embedd.set_image(
                url=self.loading)
            message = await ctx.send(embed=embedd)
            s = self.reddit.subreddit(subreddit)
            ts = s.created_utc
            for moderator in s.moderator():
                mods.append(f"[{moderator.name}](https://reddit.com/user/{moderator.name})")
            
            if s.public_description is not None:
                redditEmbed = discord.Embed(colour=reddit_colour, title="r/" + s.display_name,
                                            url=f"https://reddit.com/r/{subreddit}", description=s.public_description,
                                            timestamp=ctx.message.created_at)
            else:
                redditEmbed = discord.Embed(colour=reddit_colour, title="r/" + s.display_name,
                                            url=f"https://reddit.com/r/{subreddit}", timestamp=ctx.message.created_at)
            redditEmbed.set_thumbnail(url=s.icon_img)
            redditEmbed.set_footer(icon_url=s.banner_img, text=s.display_name)
            redditEmbed.add_field(name=f"**General**",
                                  value="**Created** {}\n**Subscribers**: {:,.0f}\n**ID**: {}"
                                  .format(datetime.datetime.fromtimestamp(ts).strftime("%B %d, %Y"), s.subscribers,
                                          s.id))
            mod = "\n".join(mods[:10])
            redditEmbed.add_field(name="<:Mods:713500789670281216> **Mods**",
                                  value=f"**Total**: {len(mods)}\n**Mods**:\n{mod}", inline=False)
            await message.edit(embed=redditEmbed)
        except Exception as error:
            await ctx.send(error)
    
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
    
    @commands.command(aliases=['mod'], help="Shows you moderator permissions for a subreddit.")
    async def moderator(self, ctx, subreddit, mod):
        mp = []
        try:
            try:
                embedd = discord.Embed(
                    colour=reddit_colour, title="Loading..."
                )
                embedd.set_image(
                    url=self.loading)
                message = await ctx.send(embed=embedd)
                m = self.reddit.redditor(mod)
                sub = self.reddit.subreddit(subreddit)
                for moderator in self.reddit.subreddit(subreddit).moderator(m):
                    for perm in moderator.mod_permissions:
                        mp.append(f"• {perm.capitalize()}")
                    mod_perms = "\n".join(mp)
                    modEmbed = discord.Embed(title=f"u/{m.name}", url="https://reddit.com/user/{}".format(m.name),
                                             description=
                                             f"**Permissions**:\n{mod_perms}", colour=reddit_colour)
                    modEmbed.set_author(name=f"r/{sub}", icon_url=sub.icon_img)
                    modEmbed.set_thumbnail(url=m.icon_img)
                    ts = int(moderator.created_utc)
                    
                    modEmbed.set_footer(text='Account created on {}'.format(
                        datetime.datetime.fromtimestamp(ts).strftime('%B %d, %Y')))
                    
                    await message.edit(embed=modEmbed)
            except Exception as err:
                await ctx.send(
                    f"Subreddit not found/Moderator not found/Author not verified. To verify, do `{ctx.prefix}verify [reddit username]`")
        except Exception as err:
            await ctx.send(
                f"Subreddit not found/Moderator not found/Author not verified. To verify, do `{ctx.prefix}verify [reddit username]`")
    
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
        await message.edit(embed=embed) if not submission.over_18 or submission.over_18 and ctx.channel.is_nsfw() else await ctx.send(f"<:warning:727013811571261540> **{ctx.author.name}**, NSFW Channel required!")

    # mod stats

    @commands.command(aliases=['ms'])
    async def modstats(self, ctx, user):
        """Shows you the moderated subreddits of a specific user."""
        reddits = []
        numbas = []
        modstats = []
        try:
            async with aiohttp.ClientSession() as cs:
                async with cs.get(f"https://www.reddit.com/user/{user}/moderated_subreddits/.json") as r:
                    res = await r.json()
                subreddits = res['data']
                for subreddit in subreddits:
                    reddits.append(
                        f"[{subreddit['sr_display_name_prefixed']}](https://reddit.com{subreddit['url']}) • <:member:716339965771907099> **{subreddit['subscribers']:,}**")
                    numbas.append(subreddit['subscribers'])
                msg = "Top 15 Subreddits" if len(reddits) > 15 else "Moderated Subreddits"
                for index, sr in enumerate(reddits[:15], 1):
                    modstats.append(f"{index}. {sr}")
                final_ms = "\n".join(modstats)
                zero_subs = len([item for item in numbas if item == 0])
                one_subs = len([item for item in numbas if item == 1])
                hundred_subs = len([item for item in numbas if item >= 100])
                thousand_subs = len([item for item in numbas if item >= 1000])
                hundred_thousand_subs = len([item for item in numbas if item >= 100_000])
                million = len([item for item in numbas if item >= 1_000_000])
                ten_million = len([item for item in numbas if item >= 10_000_000])
                embed = discord.Embed(
                    description=f"u/{user} mods **{len(reddits):,}** subreddits with **{humanize.intcomma(sum(numbas))}**"
                                f" total readers\n\n*{msg}*\n\n{final_ms}", colour=reddit_colour)
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
        message = await ctx.send(embed=discord.Embed(colour=reddit_colour, title="Loading...").set_image(url=self.loading))
        posts = []
        reddit = self.reddit.subreddit(subreddit)
        sorts = ['new', 'controversial', 'rising', 'top', 'topever', 'hot', 'controversialever']
        reddits = [reddit.new(limit=50), reddit.controversial(limit=50), reddit.rising(limit=50), reddit.top(limit=150), reddit.top(limit=1), reddit.hot(limit=80), reddit.controversial(limit=1)]
        if sort in sorts:
            for x in reddits[sorts.index(sort)]:
                if not x.sticked:
                    posts.append(x)
        else:
            return await ctx.send(f"<:warning:727013811571261540> **{ctx.author.name}**, that isn't a valid sort! Valid sorts include {', '.join(sorts)}.")
        submission = random.choice(posts)
        if submission.is_self:
            embed = discord.Embed(title=submission.title, url=f'https://www.reddit.com{submission.permalink}', colour=reddit_colour, description="{}\n**{:,.0f}** <:upvote:718895913342337036> **{:,.0f}** 💬".format(submission.selftext, submission.score, submission.num_comments))
        else:
            embed = discord.Embed(title=submission.title, url=f'https://www.reddit.com{submission.permalink}', colour=reddit_colour, description="**{:,.0f}** <:upvote:718895913342337036> **{:,.0f}** 💬".format(submission.score, submission.num_comments))
            embed.set_image(url=submission.url)
        ts = int(submission.created_utc)
        embed.set_author(name=f"{submission.author.name}", icon_url=submission.author.icon_img)
        embed.set_footer(text='r/{} • {}'.format(submission.subreddit, datetime.datetime.fromtimestamp(ts).strftime('%B %d, %Y')), icon_url=submission.subreddit.icon_img)
        await message.edit(embed=embed) if not submission.over_18 or submission.over_18 and ctx.channel.is_nsfw() else await ctx.send(f"<:warning:727013811571261540> **{ctx.author.name}**, NSFW Channel required!")
            
def setup(client):
    client.add_cog(Reddit(client))
