import os
import requests

class Discord_Api(object):
    def __init__(self):
        with requests.Session() as sesh: 
            self.sesh = sesh
            self._base = 'https://discordapp.com/api'
            self._auth = f'Bot {os.getenv("token")}'
            self._guild = os.getenv('guild')
            self._role = os.getenv('uotd')
            self._channel = os.getenv('offtopic')

    def req_members(self, after=0):
        h = { 'Authorization': self._auth }
        u = self._base + f'/guilds/{self._guild)}/members?limit=1000&after={after}'
        r = self.sesh.get(u, headers=h)
        if r.ok:
            return r.json()
        else:
            raise Exception('req_members ERROR:\n'+r.text)

    def req_remove_user_role(self, m):
        h = { 'Authorization': self._auth }
        u = self._base + f'/guilds/{self._guild}/members/{m["user"]["id"]}/roles/{self._role}'
        r = self.sesh.delete(u, headers=h)
        if not r.ok:
            raise Exception('req_remove_user_role ERROR:\n'+r.text)

    def req_add_user_role(self, m):
        h = { 'Authorization': self._auth }
        u = self._base + f'/guilds/{self._guild}/members/{m["user"]["id"]}/roles/{self._role}'
        r = self.sesh.put(u, headers=h)
        if not r.ok:
            raise Exception('req_add_user_role ERROR:\n'+r.text)

    # todo: rich embed
    def req_post_msg(self, c):
        h = { 'Authorization': self._auth }
        u = self._base + f'/channels/{self._channel}/messages'
        d = { 'content': c }
        r = self.sesh.post(u, headers=h, json=d)
        if not r.ok:
            raise Exception('req_post_msg ERROR:\n'+r.text)