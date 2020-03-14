# Discord-Facebook-Chat-Bridge

A Discord bot that acts as a chat bridge with Facebook Messenger: messages sent in Discord will be mirrored to Messenger, and vice versa.

How it works:

Each Facebook thread is associated with an ID and each message thread is designated as either a USER or GROUP thread.

When a message is sent in a Discord channel with its name set to be equal to a Facebook thread ID and its topic set to be either USER or GROUP, the message will be mirrored to the appropriate Facebook thread.

When a message is sent in Facebook, if a channel exists in Discord with the correct name and topic, the message will be mirrored to that channel: if not, a new channel is created with name = threadID and topic = the thread type of the message. This channel can then be used to return messages.

Requirements:

Python 3.7.2+

fbchat 1.9.6: https://fbchat.readthedocs.io/en/stable/

discord.py 1.3.2: https://discordpy.readthedocs.io/en/latest/

TODO:

Allow a single instance of bot to operate across multiple guilds: requires a method to search for the desired guild

Implement messaging new Facebook users from Discord: requires some way of searching user ID's from Discord. 

