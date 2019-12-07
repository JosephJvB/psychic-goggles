import os
import requests
import discord
from bot import Bot

class MyClient(discord.Client):
    async def on_ready(self):
        print('Logged on as', self.user)
        self._bot = Bot()
        self.cmds = {
            '!codes': self._bot.cmd_codes
        }
        self.ready = True

    async def on_message(self, message):
        if not self.ready:
            return
        if message.author.bot:
            return
        cmd = message.content.split(' ')[0]
        fn = self.cmds.get(cmd)
        if not fn:
            return
        else:
            await fn(message)


client = MyClient()
client.ready = False

try:
    client.run(os.getenv('token'))
except Exception as e:
    m = {
        'content': f'ERROR:\n{e.args}'
    }
    requests.post(os.getenv('hook'), m)