# Discord-Facebook-Chat-Bridge

A Discord bot that acts as a chat bridge with Facebook Messenger: messages sent in Discord will be mirrored to Messenger, and vice versa.

How it works:

Each Facebook user is associated with an ID and each message thread is designated as either a USER or GROUP thread.

When a message is sent in a Discord channel with its name set to be equal to a Facebook users ID and its topic set to be either USER or GROUP, the message will be mirrored to the appropriate Facebook thread.


When a message is sent in Facebook, if a channel exists in Discord with the correct name and topic, the message will be mirrored to that channel: if not, a new channel is created with name = sender ID and topic = the thread type of the message. 

TODO:

Extend functionality across different guilds: requires a method to search for the desired guild

Implement messaging new users from Discord: requires some way of searching user ID's from Discord. 
