import os
import requests
import discord
from discord import utils
from bot import Bot

# reaction_name : role_id 
platform_map = { # no platform roles atm
    '442691013664833550': '', # switch
    '442691013664833550': '', # pc
    '442691013664833550': '', # playstation
    '442691013664833550': '', # xbox
}
region_map = {
    'na': 331436384349061124, # NA
    'eu': 331436493643972619, # eu
    'oce': 441311109501419541, # oce
    'Asia': 334295825368743936 # asia
}

class MyClient(discord.Client):
    async def on_ready(self):
        print('Logged on as', self.user)
        self._bot = Bot()
        self.msg_cmds = {
            '!codes': self._bot.cmd_codes
        }
        self.ready = True
        self.region_msg = int(os.getenv('regionreactmsg'))
        self.react_channel = int(os.getenv('reactchannel'))
        self.wallride_guild = int(os.getenv('guild'))

    async def on_message(self, message):
        if not self.ready:
            return
        if message.author.bot:
            return
        cmd = message.content.split(' ')[0]
        if not cmd.startswith('!'):
            return
        fn = self.msg_cmds.get(cmd)
        if not fn:
            return
        else:
            print(f'executing command [{cmd}]')
            await fn(message)

    async def on_raw_reaction_add(self, payload):
        if not self.ready:
            return
        if payload.message_id != self.region_msg:
            return

        g = self.get_guild(self.wallride_guild)
        user = g.get_member(payload.user_id)
        existing = [r for r in user.roles if r.id in region_map.values()]

        if payload.emoji.name == 'trash': # trash all -> exit
            print(f'trashing roles for {user.nick}')
            c = self.get_channel(self.react_channel)
            m = await c.fetch_message(self.region_msg)
            for r in m.reactions: # todo: parallel web requests
                await r.remove(user)
            await user.remove_roles(*existing)
            return

        if len(existing) > 0: # remove existing reactions & roles -> continue
            c = self.get_channel(self.react_channel)
            m = await c.fetch_message(self.region_msg)
            r_names = [r.name for r in existing]
            print(f'removing {r_names} from {user.nick}')
            to_remove = [r for r in m.reactions if r.emoji.name != payload.emoji.name]
            for r in to_remove: # todo: parallel web requests
                await r.remove(user)
            await user.remove_roles(*existing)

        requested_role = region_map.get(payload.emoji.name)
        if requested_role: # add requested role
            to_add = g.get_role(requested_role)
            await user.add_roles(to_add)
            print(f'added [{to_add.name}] to {user.nick}')


client = MyClient()
client.ready = False
client.run(os.getenv('token'))