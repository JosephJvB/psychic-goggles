import os
import sys
import discord
from discord import utils

# msgid: { reaction_name : role_id }
msg_map = {
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
        int(os.getenv('reactchannel'))
        self.channel = self.get_channel(int(os.getenv('reactchannel')))
        self.guild = self.get_guild(int(os.getenv('guild')))
        await self.restore_roles(int(os.getenv('platformreactmsg')))
        await self.restore_roles(int(os.getenv('regionreactmsg')))

    async def restore_roles(self, msg_id):
        _map = msg_map.get(msg_id)
        m = await self.channel.fetch_message(msg_id)
        to_restore = [r for r in m.reactions if r.emoji.name != 'trash']
        for r in to_restore:
            role_id = _map.get(r.emoji.name)
            u_list = await r.users().flatten()
            print(f'add {r.emoji.name}: {len(u_list)} users')
            role_to_add = self.guild.get_role(role_id)
            restored = 0
            for u in u_list:
                mem = None
                try:
                    mem = await self.guild.fetch_member(u.id)
                except Exception:
                    pass
                if mem != None and role_id not in [r.id for r in mem.roles]:
                    await mem.add_roles(role_to_add)
                    restored += 1
            print(f'restored {restored} / {len(u_list)} {r.emoji.name} roles')
        sys.exit('all reaction roles restored')

client = MyClient()
client.run(os.getenv('token'))