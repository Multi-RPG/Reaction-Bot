import discord
import configparser
import sys
import random
import collections
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
                                                               "Handshake", "Wave", "Bait"])

    # Emojis formatted into discord syntax
    emoji = Emoji_Reaction("<:blabla:745411421243703438>", "<:worrysquintstare:745481891624255559>",
                           "<:anywaysDude:693637780802109500>", "<:worryshrug2:745484088596627518>",
                           "<:pepeUnsureAbtThatOneChief:680578638499938305>",
                           "<:worrylove:745680240646553682>", "<:pepehandshake:734537325752614933>",
                           "<a:pepeWave:618911376613834752>", "<a:jebaitRod:667530473605562387>")

    # 70% chance to scan a message to react to it
    if 70 >= random.randint(1, 100) >= 1:
        # convert the message into a string uppercase
        message_content = message.content.upper()

        # if they sent a URL or emoji (contains a colon), don't react
        if any([keyword in message_content for keyword in ('HTTP', '/', ':')]):
            return

        # if they said blabla, shut, or stop
        if any([keyword in message_content for keyword in ('BLA BLA', 'BLABLA', 'SHUT', 'STOP')]):
            await message.add_reaction(emoji=emoji.Blabla)
            await message.add_reaction(emoji=emoji.Squint)
        # if they said anyways, whatever, or seriously
        elif any([keyword in message_content for keyword in ('ANYWAY', 'WHATEVER', 'SERIOUSLY')]):
            # if they sent the anyways dude emoji, don't double dip
            if message.content == emoji.Anyways:
                return
            await message.add_reaction(emoji=emoji.Anyways)
        # if they sent a question
        elif any([keyword in message_content for keyword in ('?', 'WHAT', 'WHY', 'HUH')]):
            # this conditional triggers a lot, so lower the odds more with another dice roll
            if 10 >= random.randint(1, 100) >= 1:
                await message.add_reaction(emoji="<:worryshrug2:745484088596627518>")
        # if they said i swear
        elif any([keyword in message_content for keyword in ('SWEAR', 'PROMISE', 'LYING')]):
            await message.add_reaction(emoji=emoji.Unsure)
        # if they said thanks or deal
        elif any([keyword in message_content for keyword in ('THANK', 'DEAL')]):
            await message.add_reaction(emoji=emoji.Handshake)
        # if they said love or miss
        elif any([keyword in message_content for keyword in ('LOVE', 'MISS')]):
            await message.add_reaction(emoji=emoji.Love)
        # if they said cya or later or bye
        elif any([keyword in message_content for keyword in ('CYA', 'LATER', 'BYE', 'LAKE')]):
            await message.add_reaction(emoji=emoji.Wave)
        # if they said sorry
        elif 'SORRY' in message_content:
            await message.add_reaction(emoji=emoji.Squint)
        else:
            if 1 >= random.randint(1, 100) >= 1:
                await message.add_reaction(emoji=emoji.Shrug)

    # need this statement for bot to recognize commands
    await client.process_commands(message)


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
