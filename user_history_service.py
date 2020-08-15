import os
import requests

class User_History_Service(object):
    def __init__(self):
      self.save_url = 'https://qos3ykxv4d.execute-api.us-west-2.amazonaws.com/Prod/save'

    def handle_user_update(self, before, after):
      registered_users = os.getenv('registered_users', '').split(',')
      if str(before.id) in registered_users:
        change_avi = before.avatar_url != after.avatar_url
        change_nick = before.nick != after.nick
        if change_avi or change_nick:
          print(f'updating user history: {before.id}')
          requests.post(self.save_url, json={
            'user': {
              'id': after.id,
              'avatar': after.avatar_url,
              'nickname': after.nick
            }
          })

# if __name__ == '__main__':
  # class M:
  #   def __init__(self, d):
  #     self.id = 'pythontest'
  #     self.avatar_url = 'pythontest' + d
  #     self.nick = 'pythontest' + d
  # u = User_History_Service()
  # b = M('-before')
  # a = M('-after')
  # u.handle_user_update(b, a)