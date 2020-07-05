"""

A python package made to make Python formatting easier for us all.
Technically useless, aesthetically pleasing.

Made by nizcomix
Contact on discord ♿niztg#7532 (350349365937700864) for questions

"""

import discord


class NativePython(object):
    """For functions that can help using Native Python"""
    
    def __init__(self):
        pass
    
    def listify(self, list: list, char='\n', limit: int = None):
        """
        Puts everything in a pretty list for you.

        :param list:
        :param char:
        :param limit:
        :return:
        """
        if not limit:
            return f"{char}".join(list)
        else:
            return f"{char}".join(list[:limit])
    
    def hyper_replace(self, text, old: list, new: list):
        """
        Allows you to replace everything you need in one function using two lists.
        :param text:
        :param old:
        :param new:
        :return:
        """
        msg = str(text)
        for x, y in zip(old, new):
            msg = str(msg).replace(x, y)
        return msg
    
    def bool_help(self, value: bool, true: str = None, false: str = None):
        """Returns a custom bool message without you having to write a pesky if/else.
        :param true:
        :param false:
        :return:
        """
        if value:
            return true
        else:
            return false
    
    def bar(self, stat: int, max: int, filled: str, empty: str, show_stat: bool = False):
        percent = round((stat / max) * 100, 1)
        if percent > 100:
            bar = f"{percent}% {filled * 10} 100.0%" if not show_stat else f"{stat} {filled * 10} {max}"
            return bar
        elif percent <= 0:
            bar = f"{percent}% {empty * 10} 100.0%" if not show_stat else f"{stat} {empty * 10} {max}"
            return bar
        else:
            total_filled = round(percent / 10)
            total_empty = 10 - (round(percent / 10))
            return f"{str(percent)}% {filled * total_filled}{empty * total_empty} {max}%" if not show_stat else f"{str(stat)} {filled * total_filled}{empty * total_empty} {max}"


class Discord(object):
    def __init__(self, bot_user_id):
        self.bot_user_id = bot_user_id
    
    async def fieldify(self, names: list, values: list, inline: bool, limit: int = None):
        """Easy embed fieldification
        :returns embed:
        """
        embed = discord.Embed()
        if not limit:
            for name, val in zip(names, values):
                embed.add_field(name=name, value=val, inline=inline)

        elif limit:
            counter = 0
            for name, val in zip(names, values):
                embed.add_field(name=name, value=val, inline=inline)
                counter += 1
                if counter >= limit:
                    return embed
                else:
                    continue

        return embed
    
    def codeblock(self, body):
        if str(body).startswith("```py") and str(body).endswith("```"):
            py, c = str(body).split("```py")
            return c[:-3]
        else:
            return body
