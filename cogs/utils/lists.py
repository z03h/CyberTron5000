"""

For JSON lists.

"""

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
    "us-east": "US-East",
    "india": "India",
    "brazil": "Brazil",
    "japan": "Japan",
    "russia": "Russia",
    "singapore": "Singapore",
    "southafrica": "South Africa",
    "sydney": "Sydney",
    "hongkong": "Hong Kong",
    "us-central": "US-Central",
    "us-south": "US-South",
    "us-west": "US-West"
}

INDICATOR_LETTERS = {'1': '1️⃣', '2': '2️⃣', '3': '3️⃣',
                     '4': '4️⃣', '5': '5️⃣', '6': '6️⃣',
                     '7': '7️⃣', '8': '8️⃣', '9': '9️⃣'}

sl = {
    "online": "<:online:703903072824459265>",
    "offline": "<:offline:703918395518746735>",
    "idle": "<:idle:703903072836911105>",
    "dnd": "<:dnd:703903073315192832>"
}

mlsl = {"online": "<:whiteiphone:703726679377575996>",
      "offline": "\u200b",
      "idle": "<:whiteiphone:703726679377575996>",
      "dnd": "<:whiteiphone:703726679377575996>"}

wlsl = {"online": "🌐",
      "offline": "\u200b",
      "idle": "🌐",
      "dnd": "🌐"}
 # 🌐
 
dlsl = {"online": ":desktop:",
      "offline": "\u200b",
      "idle": ":desktop:",
      "dnd": ":desktop:"}