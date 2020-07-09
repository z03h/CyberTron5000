"""

For JSON lists.

"""

import discord

STAT_NAMES = {
    "speed": "SPEED",
    "attack": "ATTACK",
    "special-attack": "SPECIAL ATTACK",
    "special-defense": "SPECIAL DEFENSE",
    "defense": "DEFENSE",
    "hp": "HP"
    
}

ALPHABET_NUMBER = {
    "A": 1,
    "B": 2,
    "C": 3,
    "D": 4,
    "E": 5,
    "F": 6,
    "G": 7,
    "H": 8,
    "I": 9,
    "J": 10,
    "K": 11,
    "L": 12,
    "M": 13,
    "N": 14,
    "O": 15,
    "P": 16,
    "Q": 17,
    "R": 18,
    "S": 19,
    "T": 20,
    "U": 21,
    "V": 22,
    "W": 23,
    "X": 24,
    "Y": 25,
    "Z": 26
}
NUMBER_ALPHABET = {value: key for (key, value) in ALPHABET_NUMBER.items()}

TYPES = {
    "normal": "<:normal:715628305541496915>",
    "fighting": "<:fighting:715628306015191220>",
    "fire": "<:fire:715626721402945567>",
    "water": "<:water:715629330621005915>",
    "grass": "<:grass:715629330830721104>",
    "ground": "<:ground:715626721772175472>",
    "rock": "<:rock:715626723126804532>",
    "steel": "<:steel:715629330637520988>",
    "fairy": "<:fairy:715629865071542328>",
    "ghost": "<:ghost:715630366769021038>",
    "dark": "<:dark:715630366651711549>",
    "poison": "<:poison:715628305671389285>",
    "dragon": " <:dragon:715630390597124177>",
    "electric": "<:electric:715626721399013489>",
    "ice": "<:ice:715630367687573774>",
    "flying": "<:flying:715631197140811847>",
    "bug": "<:bug:715627787427381319>",
    "psychic": "<:psychic:715628305763663923>"
}

REGIONS = {
    "europe": "Europe",
    "us-east": "US East",
    "india": "India",
    "brazil": "Brazil",
    "japan": "Japan",
    "russia": "Russia",
    "singapore": "Singapore",
    "southafrica": "South Africa",
    "sydney": "Sydney",
    "hongkong": "Hong Kong",
    "us-central": "US Central",
    "us-south": "US South",
    "us-west": "US West"
}

INDICATOR_LETTERS = {'1': '1️⃣', '2': '2️⃣', '3': '3️⃣',
                     '4': '4️⃣', '5': '5️⃣', '6': '6️⃣',
                     '7': '7️⃣', '8': '8️⃣', '9': '9️⃣'}

sl = {
    discord.Status.online: "<:online:726127263401246832>",
    discord.Status.offline: "<:offline:726127263203983440>",
    discord.Status.idle: "<:idle:726127192165187594>",
    discord.Status.dnd: "<:dnd:726127192001478746>"
}

mlsl = {"online": "<:mobile:730843223102193744>",
        "offline": "\u200b",
        "idle": "<:mobile:730843223102193744>",
        "dnd": "<:mobile:730843223102193744>"}

wlsl = {"online": "🌐",
        "offline": "\u200b",
        "idle": "🌐",
        "dnd": "🌐"}
# 🌐

dlsl = {"online": ":desktop:",
        "offline": "\u200b",
        "idle": ":desktop:",
        "dnd": ":desktop:"}

emotes = {
    'eight-year club': '<:eightyearclub:702188391961198683>',
    'alpha tester': '<:alpha_user:702188392154267715>',
    'best comment': '<:bestcomment:702188392175370240>',
    'combocommenter': '<:combocommenter:702188392183758910>',
    'bellwether': '<:bellwether:702188392192147546>',
    'combolinker': '<:combolinker:702188392196341940>',
    'best link': '<:bestlink:702188392221507654>',
    'eleven-year club': '<:elevenyearclub:702188392384954459>',
    'four-year club': '<:fouryearclub:702188392489943251>',
    'extra life': '<:extralife:702188392506458212>',
    'gilding iii': '<:gildingiii:702188392590344264>',
    'gilding vii': '<:gildingvii:702188392607383564>',
    'gilding v': '<:gildingv:702188392645001277>',
    'gilding ii': '<:gildingii:702188392657715312>',
    'five-year club': '<:fiveyearclub:702188392779087942>',
    'gilding iv': '<:gildingiv:702188392808448080>',
    'gilding vi': '<:gildingvi:702188392842133505>',
    'gilding i': '<:gildingi:702188392842133545>',
    'gilding ix': '<:gildingix:702188392867430480>',
    'gilding viii': '<:gildingviii:702188392917630986>',
    'gilding x': '<:gildingx:702188394108682241>',
    'rpan viewer': '<:rpanviewer:702188394226384997>',
    'inciteful link': '<:incitefullink:702188394373185666>',
    'one-year club': '<:oneyearclub:702188394398220290>',
    'not_forgotten': '<:not_forgotten:702188394402283541>',
    'new user': '<:newuser:702188394423386263>',
    'gilding xi': '<:gildingxi:702188394427580427>',
    'inciteful comment': '<:incitefulcomment:702188394440163378>',
    'nine-year club': '<:nineyearclub:702188394490363945>',
    'open sorcerer': '<:opensorcerer:702188394490626150>',
    'two-year club': '<:twoyearclub:702188394519986248>',
    'reddit_gold': '<:reddit_gold:702188394616193125>',
    'undead | lich': '<:undeadlich:702188394624843887>',
    'undead | zombie': '<:undeadzombie:702188394649878561>',
    'sequence | editor': '<:sequence_editor:702188394729570364>',
    'sequence | screenwriter': '<:sequence_text:702188394851074500>',
    'seven-year club': '<:sevenyearclub:702188394851205200>',
    'six-year club': '<:sixyearclub:702188394863656960>',
    'three-year club': '<:threeyearclub:702188394872176680>',
    'ten-year club': '<:tenyearclub:702188394914119720>',
    'shutterbug': '<:shutterbug:702188394918445166>',
    'verified email': '<:verifiedemailaddress:702188394930765835>',
    'xboxl live': '<:xboxlive:702188394930765845>',
    'thirteen-year club': '<:thirteenyearclub:702188394947543060>',
    'rpan broadcaster': '<:rpanbroadcaster:702188394947674213>',
    'twelve-year club': '<:twelveyearclub:702188394956062740>',
    'undead | necromancer': '<:undeadnecromancer:702188395111383130>',
    'well-rounded': '<:wellrounded:702188395136548874>',
    'spared': '<:thanos_spared:702219317021769759>',
    'secret santa': '<:ss:702219316938014750>',
    'redditgifts elf': '<:elf:702219316694745110>',
    'not forgotten': '<:not_forgotten:702219317143404675>',
    'reddit premium': '<:reddit_gold:702219317051129906>',
    'redditgifts exchanges': '<:rgexchange:702219316875231273>'
}

status_mapping = {
    discord.ActivityType.listening: "Listening to",
    discord.ActivityType.watching: "Watching",
    discord.ActivityType.playing: "Playing",
    discord.ActivityType.streaming: "Streaming",
    discord.ActivityType.custom: "\u200b"
}

