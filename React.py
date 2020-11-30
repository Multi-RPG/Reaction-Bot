import discord
import configparser
import sys
import random
import collections
import re
from discord.ext import commands
from pathlib import Path

# Bot's prefix is defaulted to '.'
bot_prefix = "."

client = commands.Bot(command_prefix=[bot_prefix])
print(f"Prefix set to [{bot_prefix}]")

# remove the default help command
client.remove_command("help")


@client.event
async def on_ready():
    print(f"Logged in as {client.user.name}\n{client.user.id}\n---------")
    await client.change_presence(activity=discord.Game(name=".help for commands"))


@client.event
async def on_message(message):
    # Emojis used for reaction
    Emoji_Reaction = collections.namedtuple("Emoji_Reaction", ["Blabla", "Squint", "Anyways",
                                                               "Shrug", "Unsure", "Love",
                                                               "Handshake", "Wave", "Bait",
                                                               "Tired", "Hammer", "Timer",
                                                               "Think", "Teach"])

    # Emojis formatted into discord syntax
    emoji = Emoji_Reaction("<:blabla:745411421243703438>", "<:worrysquintstare:745481891624255559>",
                           "<:anywaysDude:693637780802109500>", "<:worryshrug2:745484088596627518>",
                           "<:pepeUnsureAbtThatOneChief:680578638499938305>",
                           "<:worrylove:745680240646553682>", "<:pepehandshake:734537325752614933>",
                           "<a:lake2:781248856292982825>", "<a:jebaitRod:667530473605562387>",
                           "<:feelsExhaustedWrinklesMan:667532202644602880>", "<a:pepegeHammer:769370156110708766>",
                           "<a:pepeJudy:751230976771883058>", "<:pepethink6:782776439745413140>",
                           "<:pepeTeachChart:782795561987342337>")

    # 70% chance to scan a message to react to it
    if 70 >= random.randint(1, 100) >= 1:
        # convert the message into a string uppercase
        message_content = message.content.upper()

        # if they sent a URL or emoji (contains a colon), don't react
        if search_for_url(message_content):
            print("found link")
            return
        # if they said blabla, shut, or stop
        if search_for_word("BLABLA", "BLA BLA", "SHUT UP", "STOP", string=message_content):
            await message.add_reaction(emoji=emoji.Blabla)
            await message.add_reaction(emoji=emoji.Squint)
        # if they said anyways, whatever, or seriously
        elif search_for_word("ANYWAY", "ANYWAYS", "WHATEVER", "SERIOUSLY", "SRSLY", string=message_content):
            # if they sent the anyways dude emoji, don't double dip
            if message.content == emoji.Anyways:
                return
            await message.add_reaction(emoji=emoji.Anyways)
        # if they said i swear
        elif search_for_word("SWEAR", "PROMISE", "LYING", string=message_content):
            await message.add_reaction(emoji=emoji.Unsure)
        # if they said thanks or deal
        elif search_for_word("THANK", "THANKS", "DEAL", string=message_content):
            await message.add_reaction(emoji=emoji.Handshake)
        # if they said love or miss
        elif search_for_word("MISS", "LOVE", string=message_content):
            await message.add_reaction(emoji=emoji.Love)
        # if they said cya or later or bye
        elif search_for_word("CYA", "LATER", "BYE", "LAKE", string=message_content):
            await message.add_reaction(emoji=emoji.Wave)
        # if they said sorry
        elif search_for_word("SORRY", "SRY", string=message_content):
            await message.add_reaction(emoji=emoji.Squint)
        # if they said tired, exhausted, tedious
        elif search_for_word("TIRED", "EXHAUSTED", "TEDIOUS", string=message_content):
            await message.add_reaction(emoji=emoji.Tired)
        # if they said idiot, mistake, messed
        elif search_for_word("IDIOT", "MISTAKE", "MESSED", string=message_content):
            await message.add_reaction(emoji=emoji.Hammer)
        # if they said wait, hurry, slow, come on
        elif search_for_word("WAIT", "WAITING", "HURRY", "SLOW", "COME ON", string=message_content):
            await message.add_reaction(emoji=emoji.Timer)
        # if they said unsure, thinking, not sure, hmm , or idk
        elif search_for_word("UNSURE", "THINKING", "NOT SURE", "HMM", "IDK", string=message_content):
            await message.add_reaction(emoji=emoji.Think)
        # if they said teach, simple, professor
        elif search_for_word("TEACH", "SIMPLE", "PROFESSOR", string=message_content):
            await message.add_reaction(emoji=emoji.Teach)
        # if they sent a question
        elif any([keyword in message_content for keyword in ('?', 'WHAT', 'WHY', 'HUH')]):
            # this conditional triggers a lot, so lower the odds more with another dice roll
            if 5 >= random.randint(1, 100) >= 1:
                await message.add_reaction(emoji=emoji.Shrug)

    # need this statement for bot to recognize commands
    await client.process_commands(message)


def search_for_word(*args, string):
    if len(args) == 1:
        return re.search(fr'\b({args[0]})\b', string)
    elif len(args) == 2:
        return re.search(fr'\b({args[0]}|{args[1]})\b', string)
    elif len(args) == 3:
        return re.search(fr'\b({args[0]}|{args[1]}|{args[2]})\b', string)
    elif len(args) == 4:
        return re.search(fr'\b({args[0]}|{args[1]}|{args[2]}|{args[3]})\b', string)
    elif len(args) == 5:
        return re.search(fr'\b({args[0]}|{args[1]}|{args[2]}|{args[3]}|{args[4]})\b', string)


def search_for_url(string):
    return re.search(r'[-a-zA-Z0-9@:%._\+~#=]{1,256}\.[a-zA-Z0-9()]{1,6}\b([-a-zA-Z0-9()@:%_\+.~#?&//=]*)', string)

@client.command(
    name="help", description="command information", brief="commands", aliases=["h", "HELP"],
)
async def helper(context):
    # using discord's "ml" language coloring scheme for the encoded help message
    msg = ("<a:jebaitRod:667530473605562387>")

    # Person that invoked this command.
    author = context.author

    try:
        await author.create_dm()
        await author.dm_channel.send(msg)
    except discord.Forbidden as error:
        print(f"{type(error).__name__} {error.text}")
        error_msg = (
            f"I was unable to DM you the help message. "
            f"It is possible that you do not allow DM from server members. "
            f"Please check your privacy settings."
        )
        await context.send(error_msg)

# set up parser to config through our .ini file with our bot's token
config = configparser.ConfigParser()
bot_token_path = Path("tokens/tokenbot.ini")  # use forward slash "/" for path directories
# confirm the token is located in the above path
if bot_token_path.is_file():
    config.read(bot_token_path)
    # we now have the bot's token
    TOKEN = config.get("BOT1", "token")
else:
    print(
        "\n", "Discord bot token not found at: ", bot_token_path, "... Please correct file path in React.py file.",
    )
    sys.exit()

client.run(TOKEN)
