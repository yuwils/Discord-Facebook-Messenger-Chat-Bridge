import discord
import asyncio

import fbchat
from fbchat import Client
from fbchat import models

import threading
from threading import Thread

global fb_message
global fb_thread_id
global fb_message_name
global fb_thread_type

#Facebook messenger data is saved as global variables to be used by the Discord client
fb_message = []
fb_thread_id = []
fb_message_name = []
fb_thread_type = []

class CustomClient(Client):

    """Inherits from fbchat module's Client object. Handles behaviour when a message is sent from a Facebook user."""

    def onMessage(self, author_id, message_object, thread_id, thread_type, **kwargs):

        """Updates message text, threadID, author name and thread type to be used by Discord client

           Parameters:
            author_id (string): Unique ID of the message sender
            message_object(fbchat.Client.Message): Object representing Facebook message sent
            thread_id(string): Unique ID of the thread message was sent in
            thread_type(aenum): Enumeration representing the type of thread message was sent in
        """

        global fb_message
        global fb_thread_id
        global fb_message_name
        global fb_thread_type

        if message_object.author == self.uid:   
            return

        fb_thread_id.append(thread_id)
    
        fb_message.append(message_object.text)
        
        #retrieves name from dictionary accessed using fetchUserInfo
        fb_message_name.append(self.fetchUserInfo(message_object.author)[message_object.author].name)

        fb_thread_type.append(str(thread_type)[11:])
        
class MyClient(discord.Client):
    """An class representing the Discord client that handles behaviour when a message is sent or received from Discord."""
    def __init__(self, *args, **kwargs):
        """Inherits from discord.py's Client object, and initialises background task"""       
        super().__init__(*args, **kwargs)

        self.bg_task = self.loop.create_task(self.my_background_task())

    async def on_ready(self):
        """Asynchronous method that prints a notification on successful Discord bot activation"""
        print ('Logged on successfully')

    async def my_background_task(self):
        """Background task that sends message sent from Facebook to an appropriate Discord channel
        when global Facebook messenge data is updated"""
        await self.wait_until_ready()
        while not self.is_closed():
            global fb_message
            global fb_thread_id
            global fb_message_name
            global fb_thread_type
            
            if fb_thread_type:
                
                #Current functionality only for one guild
                guild = self.guilds[0]

                for i in range(0, len(fb_thread_type), 1):

                    chans = discord.utils.get(guild.text_channels, name=fb_thread_id[i])

                    if chans:
                        pass
                    else:
                        #Creates a new channel if no appropriate channel exists
                        await guild.create_text_channel(fb_thread_id[i], topic = fb_thread_type[i])

                        #Sends message to channel with name equal to the sender's ID, and topic
                        #equal to the thread type
                        chans = discord.utils.get(guild.text_channels, name=fb_thread_id[i])

                    channel = self.get_channel(chans.id)
                    
                    msg = fb_message_name[i] + ': ' + fb_message[i]
                    await channel.send(msg)

                fb_message = []
                fb_thread_id = []
                fb_message_name = []
                fb_thread_type = []
                
            else:
                await asyncio.sleep(1)

    async def on_message(client, message):

        """Sends message to appropriate Facebook thread when message is sent in Discord.

        Parameters:
            client (MyClient): Instance of custom Discord client
            message (discord.Message): Message object sent in Discord
        """

        if message.author == client.user:   
            return

        channel = message.channel

        message_type_str = channel.topic
        if message_type_str == 'USER':
            message_type = fbchat.ThreadType.USER
        elif message_type_str == 'GROUP':
            message_type = fbchat.ThreadType.GROUP
        else:
            return

        latest_message = message.content

        #Determines ID of thread from channel name and recipient type from channel topic
        fbclient.send(fbchat.Message(text=latest_message), thread_id=channel.name, thread_type=message_type)

if __name__ == "__main__":

    import sys
    print(sys.version)
    
    token = input('Enter your Discord bot token: \n')
    email = input('Enter your Facebook email: \n')
    password = input('Enter your Facebook password: \n')

    #Initialises Facebook and Discord client objects
    fbclient = CustomClient(email, password, None, 1)
    client = MyClient()

    #Initialises Facebook listening loop and Discord bot on seperate threads
    threading.Thread(target = lambda: fbclient.listen()).start()
    threading.Thread(target = lambda: client.run(token)).start()
