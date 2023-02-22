
# bot.py
import os
import re
import discord
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

intents = discord.Intents.default()
intents.message_content=True
client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print(f'{client.user} has connected to Discord!')

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    prefix = message.content.split(" ")[0]
    chatter = message.author.id

    if prefix == 'cgs!':
        atk, hp, dfns, er, eff, critC, critD, spd, flatHp, flatAtk, flatDef, brick = 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0
        command = message.content[5:]
        substats = command.split(" ")
        for subs in substats:

            temp = re.compile("([a-zA-Z]+)([0-9]+)")
            res = temp.match(subs).groups()

            stat = res[0]
            statNum = res[1]


            if stat == 'atk':
                atk = int(statNum)
            elif stat == 'def':
                dfns = int(statNum)
            elif stat == 'hp':
                hp = int(statNum)
            elif stat == 'eff':
                eff = int(statNum)
            elif stat == 'er':
                er = int(statNum)
            elif stat == 'cc':
                critC = int(statNum) * 1.6
            elif stat == 'cdmg':
                critD = int(statNum) * 1.1
            elif stat == 'spd':
                spd = int(statNum) * 2
            elif stat == 'fatk':
                flatAtk = int(statNum) * 3.46/39
            elif stat == 'fdef':
                flatDef = int(statNum) * 4.99/31
            elif stat == 'fhp':
                flatHp = int(statNum) * 3.09/174
            else:
                brick=1

        gs = (atk + hp + dfns + er + eff + critC + critD + spd + flatHp + flatAtk + flatDef)
        gs =  "{:.2f}".format(gs)

        if brick==1:
            await message.channel.send(f'<@{chatter}> ' + str(
                stat) + " is not in the expected parameters, type cgsp! for a list of parameters.")
        elif(flatHp != 0 or flatDef != 0 or flatAtk !=0):
            await message.channel.send(f'<@{chatter}> That piece is ' + str(gs) + 'gs. Since it has a flat stat it may be more or less gs depending on the unit.')
        else:
            await message.channel.send(f'<@{chatter}> That piece is ' + str(gs) + 'gs. <:cdomSmile:1077793313823924224>')
    elif prefix == 'cgsp!':
        await message.channel.send(f'<@{chatter}> Accepted substats are: \n-atk\n-hp\n-def\n-eff\n-er\n-cc\n-cdmg'
                                   f'\n-spd\n-fatk (for flat atk)\n-fhp (for flat hp)\n-fdef (for flat def)\n'
                                   f'An example command would be like: cgs! atk17 def15 cc17 spd9')


client.run(TOKEN)
