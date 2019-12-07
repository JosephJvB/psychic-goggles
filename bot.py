import os

class Bot (object):
    def __init__(self):
        return 

    async def cmd_codes(self, msg):
        if msg.channel.id != int(os.getenv('questions')):
            return

        c = f'**Lucio Surf Codes**\nStandard: {os.getenv("surfcode")}\nGravspeed: {os.getenv("gravcode")}'
        await msg.channel.send(content=c)
        return