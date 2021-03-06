import os
import asyncio

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

class Reaction_Service(object):
    def __init__(self, channel, guild):
        self.c = channel
        self.g = guild

    async def handle_add_role(self, payload):
        if payload.message_id not in msg_map.keys():
            return

        _map = msg_map.get(payload.message_id)
        _msg_name = _map.get('_name')

        user, m = await asyncio.gather(
            self.g.fetch_member(payload.user_id),
            self.c.fetch_message(payload.message_id)
        )

        if payload.emoji.name == 'trash': # trash all -> exit
            print(f'trashing {_msg_name} for {user.display_name}')
            reqs = [r.remove(user) for r in m.reactions]
            l = asyncio.get_event_loop()
            l.run_until_complete(asyncio.wait(reqs, return_when=asyncio.ALL_COMPLETED))
            return

        requested_role = _map.get(payload.emoji.name)
        if not requested_role:
            return print(f'<handle_role_add>: role not found with id [{requested_role}]')

        to_add = self.g.get_role(requested_role)
        if not to_add:
            return print(f'<handle_role_add>: No role in server with id = {requested_role}')

        existing = [r for r in user.roles if r.id in _map.values()]
        exist_ids = [r.id for r in existing]
        if requested_role in exist_ids:
            return print(f'<handle_role_add>: {user.display_name} already has role [{to_add.name}]')

        # can only have one region, can have many platforms
        if _msg_name == 'region' and len(existing) > 0: # remove existing reactions & roles -> continue
            r_names = [r.name for r in existing]
            print(f'<handle_role_add>: removing {r_names} from {user.display_name}')
            to_remove = [r for r in m.reactions if r.emoji.name != payload.emoji.name]
            reqs = [r.remove(user) for r in to_remove]
            l = asyncio.get_event_loop()
            l.run_until_complete(asyncio.wait(reqs, return_when=asyncio.ALL_COMPLETED))

        await user.add_roles(to_add)
        return print(f'<handle_role_add>: added [{to_add.name}] to {user.display_name}')

    async def handle_remove_role(self, payload):
        if payload.message_id not in msg_map.keys() or payload.emoji.name == 'trash':
            return

        _map = msg_map.get(payload.message_id)
        _msg_name = _map.get('_name')

        user = await self.g.fetch_member(payload.user_id)
        requested_role = _map.get(payload.emoji.name)

        if not requested_role:
            return print(f'<handle_role_remove>: role not found with id {requested_role}')

        to_remove = self.g.get_role(requested_role)

        if not to_remove:
            return print(f'<handle_role_remove>: No role in server with id = {requested_role}')

        existing = [r for r in user.roles if r.id in _map.values()]
        exist_ids = [r.id for r in existing]        
        if requested_role not in exist_ids:
            return print(f'<handle_role_remove>: {user.display_name} does not have role {to_remove.name}')

        await user.remove_roles(to_remove)
        print(f'<handle_role_remove>: removed [{to_remove.name}] from {user.display_name}')