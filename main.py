import os
import requests
import discord
from discord import utils
from reaction_service import Reaction_Service

class MyClient(discord.Client):
    async def on_ready(self):
        print('Logged on as', self.user)
        self.msg_cmds = {}
        self.ready = True
        self.c = self.get_channel(int(os.getenv('reactchannel')))
        self.g = self.get_guild(int(os.getenv('guild')))
        self.reaction_service = Reaction_Service()

    async def on_message(self, message):
        legal = self.ready and !message.author.bot and message.startswith('!')
        if not legal:
            return
        cmd = message.content.split(' ')[0]
        fn = self.msg_cmds.get(cmd)
        if not fn:
            return
        else:
            print(f'executing command [{cmd}]')
            await fn(message)

    async def on_raw_reaction_add(self, payload):
        if not self.ready:
            return
        if payload.message_id in msg_map.keys():
            await self.reaction_service.handle_add_role(payload)
        else:
            return

    async def on_raw_reaction_remove(self, payload):
        if not self.ready:
            return
        if payload.message_id in msg_map.keys() and payload.emoji.name != 'trash':
            await self.reaction_service.handle_remove_role(payload)
        else:
            return


client = MyClient()
client.ready = False
client.run(os.getenv('token'))