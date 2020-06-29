import os
import random
import discord
import yaml
from discord.ext import commands
from dotenv import load_dotenv

from pathlib import Path

load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")
## Runs in Linux via: python3 filename.py
## Requires Python > 3.4
## Bot needs to be given message read and send permissions on the Discord server.
## Need to install the discord.py API wrapper (e.g., via: pip install discord.py)


#sep = ' '
gap = ''

with open("moves.yml",'r') as stream:
    try:
        moves = yaml.safe_load(stream)
    except yaml.YAMLError as exc:
        print(exc)

moveList = [row[0] for row in moves]
dict= {}

def print_help(OutputStream): #it is possible to generalize the Attributes and put it in the yaml file
    OutputStream += "# Usage:\n"
    OutputStream += "!move ? - displays this message\n"
    OutputStream += "!move help - displays this message\n"
    OutputStream += "!move <xxx> - roll to perform Move <xxx>\n"
    OutputStream += "!move <xxx> -1 - roll to perform Move <xxx> with negative modifier -1\n"
    OutputStream += "!move <xxx> +2 - roll to perform Move <xxx> with positive modifier +2\n"
    OutputStream += "# Moves:\n"
    OutputStream += "- Avoid Harm (ah): roll + Reflexes\n"
    OutputStream += "- Endure Injury (ei): roll + Fortitude - Harm (+ Armour)\n"
    OutputStream += "- Keep It Together (kit): roll + Willpower\n"
    OutputStream += "- Act Under Pressure (aup): roll + Coolness\n"
    OutputStream += "- Engage In Combat (eic): roll + Violence\n"
    OutputStream += "- Influence Other - NPC (ion): roll + Charisma\n"
    OutputStream += "- Influence Other - PC (iop): roll + Charisma\n"
    OutputStream += "- See Through the Illusion (sti): roll + Soul\n"
    OutputStream += "- Read A Person (rap): roll + Intuition\n"
    OutputStream += "- Observe A Situation (oas): roll + Perception\n"
    OutputStream += "- Investigate (inv): roll + Reason\n"
    OutputStream += "- Help Or Hinder (hoh): roll + Attribute\n"
    OutputStream += "- Non-standard move (non): roll + Modifier\n"
    return OutputStream

## Get discord connection
client = discord.Client()

## Define an event so that Bot can read messages
@client.event
async def on_message(message):

    ## Respond if user sends "!move"
    if message.content.startswith('!move'):

        ## Split into into "!move", the type of Move to undertake, the modifier (if any), and a comment (if any).
        bits = message.content.split(" ")

        OutputStream = '```md\n'
        if len(bits)==1:
            OutputStream += "Please specify a Move (or use '!move ?' for help)"

        if len(bits)>1:
            if bits[1] in ["?", "help"]: # help
                OutputStream = print_help(OutputStream)

            elif bits[1] not in moveList: # non listed move given
                OutputStream += 'Please specify a Move (or "!move ?" for help)'

            elif bits[1] in moveList: # roll for some move
                roll = [random.randint(1,10), random.randint(1,10)]
                for item,doc in enumerate(moves):
                    if (bits[1] == doc[0]):
                        options = doc

                result = roll[0] + roll[1]
                mod = ''

                if len(bits) > 2:
                    mod = [' ',list(bits[2])[0],' ',list(bits[2])[1],' ']
                    mod = gap.join(mod)
                    if list(bits[2])[0]=="+":
                        result = result + int(list(bits[2])[1])
                    elif list(bits[2])[0]=="-":
                        result = result - int(list(bits[2])[1])

                if result > 14:
                    outcome = options[2]
                elif result > 9:
                    outcome = options[3]
                else:
                    outcome = options[4]

                OutputStream += options[1]
                OutputStream += "\nResult: "
                OutputStream += str(roll[0])
                OutputStream += " + "
                OutputStream += str(roll[1])
                OutputStream += mod
                OutputStream += " = "
                OutputStream += str(result)
                OutputStream += "\nOutcome: "
                OutputStream += outcome
            # end of standard move roll
        OutputStream += '```'

        ## Send message to channel
        #print(OutputStream)
        await message.channel.send(OutputStream)

## Write login details locally (i.e., on linux box where bot code is running)
@client.event
async def on_ready():
    await client.change_presence(activity=discord.Game(name="Kult: !move ? for help"))
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')

## Run Bot on Discord server
client.run(TOKEN)
