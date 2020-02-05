# discord.py

logic for role reactions
- Can react for platform: pc, xbox, ps4, switch
- Can react for region: na, eu, oce, asia

- user clicks reaction to message: pc gamer
    - look up user from reaction.user_id
    - get roleid from reaction.emoji
    - bot checks user roles
    - if user already has a platform role - remove it
    - add requested roleid to user