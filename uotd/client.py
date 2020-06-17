import os
import random
from discord_api import Discord_Api

class Client(Discord_Api):
    def __init__(self):
        super(Client, self).__init__()
        self.all_members = []
        self.prev = None
        self.next = None

    def run(self):
        print('\nbegin\n')
        self.get_all_members()
        print('\ngot users\n')
        self.get_prev_uotd()
        print('\ngot prev user\n')
        self.get_next_uotd()
        print('\ngot next user\n')
        self.finale()        
        print('\nend\n')
        return

    def get_all_members(self):
        m = [] 
        go_agane = True
        while go_agane: # python doesnt have do/while
            last_id = 0 if not len(m) > 0 else m[-1]['user']['id']
            r = self.req_members(after=last_id)
            m += r
            go_agane = len(r) == 1000 # if len is less that 1000, we are done
        print(f'got {len(m)} members')
        self.all_members = m
        return

    def get_prev_uotd(self):
        r = os.getenv('uotd')
        if self.all_members[0].get('roles'):
            p = [u for u in self.all_members if r in u['roles']]
            self.prev = None if len(p) == 0 else p[0]
        else:
            raise Exception('get_prev_uotd ERROR:\nDont have roles property on user')
        return

    def get_next_uotd(self):
        l = self.all_members
        if(self.prev):
            l.remove(self.prev)
        r = os.getenv('active')
        l = [u for u in l if r in u['roles']]
        if len(l) > 0:
            n = random.choice(l)
            self.next = n
        else:
            raise Exception('get_next_uotd ERROR: No eligible users')

    def finale(self):
        if(self.prev):
            self.req_remove_user_role(self.prev)
            self.req_post_msg(self.get_out_msg())
        self.req_add_user_role(self.next)
        self.req_post_msg(self.get_in_msg())
        return

    def get_out_msg(self):
        u = f'<@{self.prev["user"]["id"]}>'
        m = random.choice([
            u + ' is old news',
            u + ' has died from ligma',
            u + ' has been perma-banned',
            u + ' is cancelled'
        ])
        e = random.choice([
            '😔',
            '☠️',
            '😖',
            '🇫',
            '🇱',
        ])
        return f'{e} {m} {e}'

    def get_in_msg(self):
        u = f'<@{self.next["user"]["id"]}>'
        m = random.choice([
            u + ' is mucho more macho',
            u + ' has been chosen by the gamer gods',
            'Please welcome our new gaming overlord, ' + u,
            u + ' has the biggest brain in the server'
        ])
        e = random.choice([
            '👑',
            '😍',
            '😎',
            '😳'
        ])
        return f'{e} {m} {e}'