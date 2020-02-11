import os
import requests
import discord
from discord import utils
from bot import Bot

# msgid: { reaction_name : role_id }
msg_map = {
    # no platform roles atm
    int(os.getenv('platformreactmsg')): {
        '_name': 'platform',
        'ntswitch': 676896417297465389,
        'bnet': 676896041437495306,
        'ps4': 676896298669965376,
        'xbox': 676896289836892160,
    },
    int(os.getenv('regionreactmsg')): {
        '_name': 'region',
        'na': 331436384349061124,
        'eu': 331436493643972619,
        'oce': 441311109501419541,
        'Asia': 334295825368743936,
    }
}

class MyClient(discord.Client):
    async def on_ready(self):
        print('Logged on as', self.user)
        self._bot = Bot()
        self.msg_cmds = {
            '!codes': self._bot.cmd_codes
        }
        self.ready = True
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
        if payload.message_id in msg_map.keys():
            await self.handle_reaction_roles(payload)
        else:
            return

    async def handle_reaction_roles(self, payload):
        _map = msg_map.get(payload.message_id)
        _msg_name = _map.get('_name')

        g = self.get_guild(self.wallride_guild)
        user = g.get_member(payload.user_id)
        c = self.get_channel(self.react_channel)
        m = await c.fetch_message(payload.message_id)
        existing = [r for r in user.roles if r.id in _map.values()]

        if payload.emoji.name == 'trash': # trash all -> exit
            print(f'trashing {_msg_name} for {user.display_name}')
            for r in m.reactions: # todo: parallel web requests
                await r.remove(user)
            await user.remove_roles(*existing)
            return

        if len(existing) > 0: # remove existing reactions & roles -> continue
            r_names = [r.name for r in existing]
            print(f'removing {r_names} from {user.display_name}')
            to_remove = [r for r in m.reactions if r.emoji.name != payload.emoji.name]
            for r in to_remove: # todo: parallel web requests
                await r.remove(user)
            await user.remove_roles(*existing)

        requested_role = _map.get(payload.emoji.name)
        if requested_role: # add requested role
            to_add = g.get_role(requested_role)
            await user.add_roles(to_add)
            print(f'added [{to_add.name}] to {user.display_name}')
        else:
            print(f'No role found for emojiname={payload.emoji.name}, msg={_msg_name}')

client = MyClient()
client.ready = False
client.run(os.getenv('token'))