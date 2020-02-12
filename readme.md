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

Wanna make: gif vault of rollouts and trickjumps.

User in channel can request gifs for examples of rollouts

submissions process: can message bot, bot posts to channel restricted to #big-boys
if post gets ticks then somehow save image + tags which it can be queried by..? need to think more


dan wants to add roles to all users who have already reacted: should be doable