import os
import requests

class User_History_Service(object):
    def __init__(self):
      self.save_url = 'https://qos3ykxv4d.execute-api.us-west-2.amazonaws.com/Prod/save'

    def handle_member_update(self, before, after):
      registered_users = os.getenv('registered_users', '').split(',')
      if str(before.id) in registered_users:
        self.handle_diff(
          before.id,
          before.avatar_url,
          before.nick,
          after.avatar_url,
          after.nick
        )
    def handle_user_update(self, before, after):
      registered_users = os.getenv('registered_users', '').split(',')
      if str(before.id) in registered_users:
        self.handle_diff(
          before.id,
          before.avatar_url,
          before.display_name,
          after.avatar_url,
          after.display_name
        )
      
    def handle_diff(self, id, before_avi, before_name, after_avi, after_name):
      ba = str(before_avi)
      aa = str(after_avi)
      if ba != aa or before_name != after_name:
          print(f'updating user history: {id}')
          jason = {
            'user': {
              'id': id,
              'avatar': aa,
              'nickname': after_name
            }
          }
          print(jason)
          requests.post(self.save_url, json=jason)


# if __name__ == '__main__':
#   class M:
#     def __init__(self, d):
#       self.id = 'pythontest'
#       self.avatar_url = 'pythontest' + d
#       self.nick = 'pythontest' + d
#   u = User_History_Service()
#   b = M('-before')
#   a = M('-after')
#   u.handle_user_update(b, a)