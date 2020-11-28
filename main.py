import os
import requests
import discord
from discord import utils
from reaction_service import Reaction_Service
from user_history_service import User_History_Service

class MyClient(discord.Client):
    async def on_ready(self):
        print('Logged on as', self.user)
        self.msg_cmds = {}
        self.ready = True
        self.reaction_service = Reaction_Service(
            self.get_channel(int(os.getenv('reactchannel'))),
            self.get_guild(int(os.getenv('guild')))
        )
        self.user_history_service = User_History_Service()

    async def on_message(self, message):
        legal = self.ready and not message.author.bot and message.content.startswith('!')
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
        if self.ready:
            await self.reaction_service.handle_add_role(payload)

    async def on_raw_reaction_remove(self, payload):
        if self.ready:
            await self.reaction_service.handle_remove_role(payload)

    # async def on_member_update(self, before, after):
    #     if self.ready:
    #         self.user_history_service.handle_user_update(before, after)


client = MyClient()
client.ready = False
client.run(os.getenv('token'))