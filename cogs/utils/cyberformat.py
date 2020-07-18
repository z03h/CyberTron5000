"""
bruh
"""

import discord
import random


def shorten(s: str):
    if len(s) >= 2000:
        return s[:-3] + "..."
    else:
        return s


def minimalize(string):
    final = ''
    final += string[0:1].lower() + string[1:] if string else ''
    return final


def listify(list: list, char='\n', limit: int = None):
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


def hyper_replace(text, old: list, new: list):
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


def bool_help(value: bool, true: str = None, false: str = None):
    """Returns a custom bool message without you having to write a pesky if/else.
    :param true:
    :param false:
    :return:
    """
    if value:
        return true
    else:
        return false


def bar(stat: int, max: int, filled: str, empty: str, show_stat: bool = False):
    percent = round((stat / max) * 100, 1)
    if percent > 100:
        bar = f"{percent}% {filled * 10} 100.0%" if not show_stat else f"{stat} {filled * 10} {max:,}"
        return bar
    elif percent <= 0:
        bar = f"{percent}% {empty * 10} 100.0%" if not show_stat else f"{stat} {empty * 10} {max:,}"
        return bar
    elif 0 < percent < 5:
        return f"{str(percent)}% {filled * 1}{empty * 9} 100.0%" if not show_stat else f"{str(stat)} {filled * 1}{empty * 9} {max:,}"
    else:
        total_filled = round(percent / 10)
        total_empty = 10 - (round(percent / 10))
        return f"{str(percent)}% {filled * total_filled}{empty * total_empty} 100.0%" if not show_stat else f"{str(stat)} {filled * total_filled}{empty * total_empty} {max:,}"


def fieldify(embed: discord.Embed, names: list, values: list, inline: bool = True, limit: int = None):
    """Easy embed fieldification
        :returns embed:
        """
    embed = embed
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


def codeblock(body):
    if str(body).startswith("```py") and str(body).endswith("```"):
        py, c = str(body).split("```py")
        return c[:-3]
    else:
        return body


def to_emoji(c):
    base = 0x1f1e6
    return chr(base + c)


async def better_random_char(s: str, c: str = None):
    string = ''
    for i in s:
        if i == " ":
            string += i
        elif s.index(i) % 2 == 0:
            if c:
                string += c
            else:
                string += i.upper()
        else:
            string += i
    return string
