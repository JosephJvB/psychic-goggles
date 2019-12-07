import os
import discord

class Bot (object):
    def __init__(self):
        return 

    async def cmd_codes(self, msg):
        if msg.channel.id != int(os.getenv('questions')):
            return

        e1 = discord.Embed(title='Rollout Workshop Codes', colour=0x7175ed)
        e1.add_field(name='Standard', value=os.getenv('standardrolloutcode'))
        e1.add_field(name='Advanced', value=os.getenv('advrolloutcode'))

        e2 = discord.Embed(title='Surf Workshop Codes', colour=0x7175ed)
        n = '1\n2\n3'
        s = '\n'.join(os.getenv('standardsurfcodes').split(','))
        g = '\n'.join(os.getenv('gravsurfcodes').split(','))
        e2.add_field(name='Season No.', value=n)
        e2.add_field(name='Standard', value=s)
        e2.add_field(name='Gravspeed', value=g)

        await msg.channel.send(embed=e1)
        await msg.channel.send(embed=e2)
        return