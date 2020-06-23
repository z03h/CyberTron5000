"""Vibe School is the best Discord Server. Join today!"""


import discord
from discord.ext import commands

from .utils.funcs import check_guild_and_channel, check_guild, check_guild_and_admin

colour = 0x00dcff


# ≫

class VibeSchool(commands.Cog):
    """The best Discord Server. Join today!"""
    def __init__(self, client):
        self.client = client
    
    vibe = 687814997841150016
    
    @commands.command(help="For report card templates in <#695340515088007249>")
    @check_guild_and_channel(channel=695340515088007249)
    async def rct(self, ctx):
        await ctx.send("```Mentor:[], Mentee:[]\nMentee Level: []\nGrade: []\n[]```")
    
    @commands.command(help="info about Vibe School.")
    @check_guild(guild=vibe)
    async def vinfo(self, ctx):
        infoEmbed = discord.Embed(title="Vibe School Info", color=ctx.message.author.color)
        infoEmbed.add_field(name="Visitors",
                            value="People who are visiting, but not official vibers or young. Must take a short quiz before officially starting their journeys.",
                            inline=False)
        infoEmbed.add_field(name="The Young",
                            value="New vibers, hoping to qualify into the vibe program and complete their vibe training",
                            inline=False)
        infoEmbed.add_field(name="Vibe Apprentice",
                            value="Passed their first vibe checks, allowed to prove themselves. Assigned a Vibe Mentor.",
                            inline=False)
        infoEmbed.add_field(name="Vibe", value="Realized their potential, completed the vibe program.")
        infoEmbed.add_field(name="Alumni",
                            value="After being granted the Vibe role, you are granted the Alumni role. Unlike Vibe, Alumni is temporary and only stays with you for as long as you're an alumni/don't have any other advanced roles.",
                            inline=False)
        infoEmbed.add_field(name="Vibe Mentor",
                            value="The teachers of new vibers, here to pass their knowledge and allow new vibers to succeed in the cruel vibe world",
                            inline=False)
        infoEmbed.add_field(name="The Council",
                            value="performs every vibe check, including on the mentors. Bosses of you.", inline=False)
        infoEmbed.add_field(name="Sensei",
                            value="Don't mess with these guys. The mentors of the mentors of the mentors. They know their shit and their vibe.",
                            inline=False)
        infoEmbed.add_field(name="Vibe Adults",
                            value="trust-able and responsible vibers on their way to moving up. Gained after successfully making it through vibe school and finding a post-vibe career path.",
                            inline=False)
        infoEmbed.add_field(name="Seito",
                            value=" Pupils of the Sensei and engage in many special projects. Generally very trustworthy.",
                            inline=False)
        infoEmbed.add_field(name="HEAD COUNCIL",
                            value="Finally, Head Council. This is the most powerful role in the whole establishment, and this person (currently YeetVegetabales) is your boss, on everything. (They are the senate)",
                            inline=False)
        infoEmbed.add_field(name="Moderator", value="Moderator", inline=False)
        infoEmbed.add_field(name="Subreddit Manager", value="Subreddit Moderator", inline=False)
        infoEmbed.add_field(name="Failures", value="Failures", inline=False)
        await ctx.send(embed=infoEmbed)
    
    @commands.command(help="rules for Vibe School")
    @check_guild(guild=vibe)
    async def rules(self, ctx):
        rulesEmbed = discord.Embed(color=ctx.message.author.color, title="Vibe School Rules")
        rulesEmbed.add_field(name="No Cheating",
                             value="Cheating for others will be treated harshly for all parties involved, so do not do it. Vibe School is meant to be fun and competitive, and cheating ruins the purpose of it.")
        rulesEmbed.add_field(name="Don't be a jerk",
                             value="Vibe School is difficult, there is no time to be mean to people",
                             inline=False)
        rulesEmbed.add_field(name="No Slurs",
                             value="We want Vibe School to be a safe and supportive place for everyone, so please- no slurs. A slur will at minimum get you a 14 day ban from this sub and a mute from the discord server. Now you may ask, what is a slur? If you are thinking of a word, and do not know if it is a slur or not, then do not say it. That simple.",
                             inline=False)
        rulesEmbed.add_field(name="Do not incite violence",
                             value="The Vibe School is no place to be violent, you will receive a ban for doing so",
                             inline=False)
        rulesEmbed.add_field(name="No Horny-ness",
                             value="Sheesh bro, take your hormones somewhere else. We do not allow horns or the act of being horny. You could get struck by the horny police.",
                             inline=False)
        rulesEmbed.add_field(name="Have fun and Vibe!",
                             value="Vibe School is meant to be fun, so just be yourself, have fun, and most importantly, VIBE.",
                             inline=False)
        await ctx.send(embed=rulesEmbed)
    
    @commands.command(help="MEE6 commands for Vibe School")
    @check_guild(guild=vibe)
    async def cmds(self, ctx):
        await ctx.send(embed=discord.Embed(title="MEE6 Commands",
                                           description="`!niz`- alerts Sensei Niz\n`!yv` - Alerts YeetVegetabales."
                                                       "\n`!vibecheck` - Checks your vibe\n`!rank` - Check your level.",
                                           color=ctx.message.author.color))
    
    @commands.command(
        help="Fetch a link and some info about your next quiz. `ty = The Young`, `va = Vibe Apprentice`, `ad = Vibe Adult`")
    @check_guild(guild=vibe)
    async def quiz(self, ctx, quiz=None):
        if quiz is None:
            await ctx.send(embed=discord.Embed(title=f"QUIZ INBOX", description="**It is __imperative__ that you use "
                                                                                "<#694316034110390343> to submit your "
                                                                                "quizzes.**\n_Here's how to do "
                                                                                "that._\n "
                                                                                "\n**1)** You take a test [The Young, "
                                                                                "Vibe Apprentice, Vibe Adult] "
                                                                                "\n**2)** If you are taking The Young or Vibe Adult quiz: remember your score, go to <#694316034110390343>, and format a message like so:\n"
                                                                                f"\n`{ctx.prefix}quizs [the quiz you took][your score]`\n"
                                                                                "\nFor example, if I got 4/6 on my Young Quiz, I would format it like so:"
                                                                                f"\n`{ctx.prefix}quizs TY 4/6`"
                                                                                f"\nIf I had submitted my apprentice quiz, I would format the command like this."
                                                                                f"\n`{ctx.prefix}quizs VA submitted`\n"
                                                                                f"\nThat's it.",
                                               color=ctx.message.author.color))
        elif quiz == "ty":
            youngEmbed = discord.Embed(color=0x00c78a, title="The Young",
                                       description=f"[Here's a link, good luck!](https://docs.google.com/forms/d/e/1FAIpQLScvdoivkqYXBjh-o3pnoYvPryQiFELmRwTVad9an1V8CnwX5w/viewform)")
            youngEmbed.add_field(name="**Info**",
                                 value=f"**Level Required**: 0\n**Study**: `{ctx.prefix}vinfo`, `{ctx.prefix}rules`, `{ctx.prefix}cmds`\n**Upgrade after passing**: Acquire <@&687817754798981227> role")
            await ctx.send(embed=youngEmbed)
        elif quiz == "va":
            youngEmbed = discord.Embed(color=0x00ffe3, title="Vibe Apprentice",
                                       description=f"[Here's a link, good luck!](https://docs.google.com/forms/d/e/1FAIpQLSe4PBF0M5KcWVcuaEmVsiXf4Q7YDVQ8mqj7n-tFcHPzOaAPNA/viewform)")
            youngEmbed.add_field(name="**Info**",
                                 value=f"**Level Required**: 2\n**Study**: Don't study; just take it.\n**Upgrade after passing**: Acquire <@&687817437214670868> role")
            await ctx.send(embed=youngEmbed)
        elif quiz == "ad":
            youngEmbed = discord.Embed(color=0xa30533, title="Vibe Adulthood",
                                       description=f"[Here's a link, good luck!](https://docs.google.com/forms/d/e/1FAIpQLSemcwfhuliBEy2y1fYVtgBDhdZpYBGQWtN00H_O06kxBBhbUw/viewform)")
            youngEmbed.add_field(name="**Info**",
                                 value=f"**Level Required**: 7\n**Study**: `{ctx.prefix}adinfo`.\n**Upgrade after passing**: Graduate to Vibe Adulthood and choose a Junior Vibe role.")
            await ctx.send(embed=youngEmbed)
    
    @commands.command(help="Gets you info about Vibe Adulthood")
    @check_guild(guild=vibe)
    async def adinfo(self, ctx):
        adEmbed = discord.Embed(color=0xa30533, title="Job Info")
        adEmbed.add_field(name="Vibe Mentor",
                          value="As the server has no pattern to its growth, Vibe Mentor will always be an open role. You perform the same vibe checks as your mentor did to you, but you DON'T MOVE ANYONE UP. That's The Council's job. You can become Vibe Mentor simply by asking, however usually your own Vibe Mentor or a Councilperson will recommend it for you. Nice blue colour too. This role is the bottom of the post-school job hierarchy.",
                          inline=False)
        adEmbed.add_field(name="Queue Manager",
                          value="A pink role and obligation to post as much as possible on the subreddit. Ignore your morals ;).")
        adEmbed.add_field(name="Subreddit Manager",
                          value="Alongside a nice orangey colour - These guys are the moderators of r/VibeSchool and are in charge of frequently posting, promoting the subreddit, approving posts in new, and answering questions.",
                          inline=False)
        adEmbed.add_field(name="BotStyle",
                          value="A role given to you if you if you have added a bot to the server.",
                          inline=False)
        adEmbed.add_field(name="\n*The roles from now on are Senior Viber roles. The roles before have been Junior.*",
                          value="--------------------------------------------------------------------------------------------",
                          inline=False)
        adEmbed.add_field(name="Management Staff",
                          value="these guys deal with the Vibe School meta - such as how to deal with specific users, big ideas, and new moderators. you can also apply for this one > [here](https://docs.google.com/forms/d/e/1FAIpQLScW5N51sTUpQexDOlxIm3XPS9BPWBJGvM8TxbGXvOytU4yYdg/viewform)",
                          inline=False)
        
        adEmbed.add_field(name="Moderator",
                          value="These guys have a sangria red colour, and a responsibility to use CyberTron5000 to mute, kick and ban people, create new channels, add new features to the server, and make announcements. ",
                          inline=False)
        adEmbed.add_field(name="Bot Dictator",
                          value="Whereas BotStyle is simply for users who add bots, Bot Dicator is for users who's bots have made a meaningful, practical contribution to VibeSchool.",
                          inline=False)
        adEmbed.add_field(name="Head Moderator",
                          value="moderator except more trusted with stuff.",
                          inline=False)
        adEmbed.add_field(name="The Council",
                          value="These guys are the real big shots of the server. They decide on every vibe check beneath them, and vote on very important rules for the subreddit and Discord. Councilpeople usually have many or all of the roles beneath them on the job hierarchy. ",
                          inline=False)
        adEmbed.add_field(name="Overseer",
                          value="Boss of management staff. Closed.",
                          inline=False)
        adEmbed.add_field(name="Subreddit Boss",
                          value="Technically a closed role held by YeetVegetabales. This one person is the boss of the Subreddit managers and takes extra care of the Subreddit. Teal colour.",
                          inline=False)
        adEmbed.add_field(name="HEAD COUNCIL",
                          value="While not a closed role necessarily, only becomes open once the current HEAD COUNCIL resigns. When that happens, a way to organize the next one will be made, but for now, know that this guy is the boss of The Council, and also gets final say on pretty much everything. Currently, it is YeetVegetabales.",
                          inline=False)
        await ctx.send(embed=adEmbed)
    
    @commands.command(help="the eppicest server in the land")
    async def vibeschool(self, ctx):
        embed = discord.Embed(
            colour=colour,
            title="join now", url="https://discord.gg/E85ZHkt"
        )
        await ctx.send(embed=embed)
    
    @commands.command(help="Submit your quizzes in #quiz-inbox")
    @check_guild_and_channel(channel=694316034110390343)
    async def quizs(self, ctx, *, quiz):
        niz = self.client.get_user(id=350349365937700864)
        await niz.send(f"Hey, {ctx.message.author.display_name} just submitted a quiz:\n```{quiz}```")
        await ctx.message.add_reaction(emoji=":GreenTick:707950252434653184")
    
    @commands.command(help="Submit your report cards in #report-cards")
    @check_guild_and_channel(channel=695340515088007249)
    async def rcsend(self, ctx, *, report):
        niz = self.client.get_user(id=350349365937700864)
        await niz.send(f"Hey, {ctx.message.author.display_name} just submitted a report card:\n```{report}```")
        await ctx.message.add_reaction(emoji=":GreenTick:707950252434653184")
    
    @commands.command(help="Vote when it's voting time")
    @check_guild(guild=687814997841150016)
    async def votev(self, ctx, person, *, reason):
        niz = self.client.get_user(id=350349365937700864)
        await niz.send(f"Hey, {ctx.message.author.display_name} just voted for {person}. Reason:\n```{reason}```")
        await ctx.message.add_reaction(emoji=":GreenTick:707950252434653184")
    
    @commands.group(invoke_without_command=True,
                    help="contact management if there's anything you want to say to them")
    @check_guild(guild=vibe)
    async def management(self, ctx, *, message):
        channel = self.client.get_channel(id=688812777653141711)
        await channel.send(
            f"Hey, {ctx.message.author} contacted you <@&689613285170872575>\n```{message}```")
        await ctx.message.add_reaction(emoji=":GreenTick:707950252434653184")
    
    @management.command(invoke_without_command=True, help="reply to someone contacting management")
    @check_guild_and_admin(guild=687814997841150016)
    async def reply(self, ctx, member: discord.Member, *, message):
        try:
            user = self.client.get_user(id=member.id)
            await user.send(f"Hey, Management got back to you for {ctx.guild}.\n```{message}```")
            await ctx.message.add_reaction(emoji=":GreenTick:707950252434653184")
        except Exception as error:
            await ctx.send(error)
    
    @commands.command(help="ascend someone")
    @check_guild_and_admin(guild=687814997841150016)
    async def ascend(self, ctx, member: discord.Member):
        roles = [role for role in member.roles]
        message = "<@&712341913575096430>"
        embed = discord.Embed(title=f"A new member is ready to ascend!", color=0xff0000,
                              description=f"**Name: {member.display_name}\n\n**USER NEEDS 5 VOTES TO ASCEND!")
        embed.set_thumbnail(url=member.avatar_url)
        embed.set_author(name=f"Ascension initiated by {ctx.message.author}", icon_url=ctx.message.author.avatar_url)
        embed.add_field(name=f"**Roles ({len(roles) - 1})**",
                        value=" • ".join([role.mention for role in roles[::-1][:10] if role.id != ctx.guild.id]),
                        inline=False)
        embed.add_field(name="**Joined Guild**", value=f"{member.joined_at.strftime('%B %d, %Y')} ", inline=False)
        message = await ctx.send(message, embed=embed)
        for r in [':upvote:718895913342337036', ':downvote:718895842404335668']:
            await message.add_reaction(r)


def setup(client):
    client.add_cog(VibeSchool(client))
