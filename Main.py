import discord
import configparser
import sys
import random
from discord.ext import commands
from pathlib import Path

# Bot's prefix is defaulted to '='.
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
    # if message.author.id == 141393326871019521:
    #     if 25 >= random.randint(1, 100) >= 1:
    #         await message.add_reaction(emoji="<:worryshrug2:745484088596627518>")
    #         await message.add_reaction(emoji="<:blabla:745411421243703438>")
    #         await message.add_reaction(emoji="<:antSquintStare2:740945924402053131>")
    #         await message.add_reaction(emoji="<:worrysquintstare:745481891624255559>")

    # 70% chance to scan a message to react to it
    if 70 >= random.randint(1, 100) >= 1:
        # convert the message into a string uppercase
        message_content = message.content.upper()

        # if they said blabla, shut, or stop
        if any([keyword in message_content for keyword in ('BLA BLA','BLABLA', 'SHUT', 'STOP')]):
                await message.add_reaction(emoji="<:blabla:745411421243703438>")
                await message.add_reaction(emoji="<:worrysquintstare:745481891624255559>")
        # if they said anyways, whatever, or seriously
        elif any([keyword in message_content for keyword in ('ANYWAY', 'WHATEVER', 'SERIOUSLY')]):
            # if they sent the anyways dude emoji, don't double dip
            if message.content == '<:anywaysDude:693637780802109500>':
                return
            await message.add_reaction(emoji="<:anywaysDude:693637780802109500>")
        # if they sent a question
        elif any([keyword in message_content for keyword in ('?', 'WHAT')]):
            # don't react to it if it was a URL
            if any([keyword in message_content for keyword in ('HTTPS','HTTP')]):
                return
            await message.add_reaction(emoji="<:worryshrug2:745484088596627518>")
        # if they said i swear
        elif any([keyword in message_content for keyword in ('SWEAR', 'PROMISE', 'LYING')]):
            await message.add_reaction(emoji="<:pepeUnsureAbtThatOneChief:680578638499938305>")
        # if they said thanks or deal
        elif any([keyword in message_content for keyword in ('THANK', 'DEAL')]):
            await message.add_reaction(emoji="<:pepehandshake:734537325752614933>")
        # if they said love or miss
        elif any([keyword in message_content for keyword in ('LOVE', 'MISS')]):
            await message.add_reaction(emoji="<:worrylove:745680240646553682>")
        # if they said cya or later or bye
        elif any([keyword in message_content for keyword in ('CYA', 'LATER', 'BYE')]):
            await message.add_reaction(emoji="<a:pepeWave:618911376613834752>")
        # if they said sorry
        elif 'SORRY' in message_content:
            await message.add_reaction(emoji="<:worrysquintstare:745481891624255559>")

        else:
            if 5 >= random.randint(1, 100) >= 1:
                #await message.add_reaction(emoji="<:blabla:745411421243703438>")
                #await message.add_reaction(emoji="<:worryrope:745417899103092886>")
                await message.add_reaction(emoji="<:worryshrug2:745484088596627518>")
                #await message.add_reaction(emoji="<:antSquintStare2:740945924402053131>")
                #await message.add_reaction(emoji="<:worrysquintstare:745481891624255559>")

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
        "\n", "Discord bot token not found at: ", bot_token_path, "... Please correct file path in Main.py file.",
    )
    sys.exit()

client.run(TOKEN)
