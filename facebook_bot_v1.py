import discord
import asyncio

import fbchat
from fbchat import Client
from fbchat import models

import threading
from threading import Thread

global fb_message
global fb_message_author
global fb_message_name
global fb_thread_type

#Facebook messenger data is saved as global variables to be used by the Discord client
fb_message = []
fb_message_author = ""
fb_message_name = ""
fb_thread_type = ""

class CustomClient(Client):

    """Inherits from fbchat module's Client object. Handles behaviour when a message is sent from a Facebook user."""

    def onMessage(self, author_id, message_object, thread_id, thread_type, **kwargs):

        """Updates message text, authorID, author name and thread type to be used by Discord client

           Parameters:
            author_id (string): Unique ID of the message sender
            message_object(fbchat.Client.Message): Object representing Facebook message sent
            thread_id(string): Unique ID of the thread message was sent in
            thread_type(aenum): Enumeration representing the type of thread message was sent in
        """

        global fb_message
        global fb_message_author
        global fb_message_name
        global fb_thread_type

        if message_object.author == self.uid:   
            return

        fb_message_author = message_object.author
    
        fb_message.append(message_object.text)
        
        #retrieves name from dictionary accessed using fetchUserInfo
        fb_message_name = self.fetchUserInfo(fb_message_author)[fb_message_author].name

        fb_thread_type = str(thread_type)[11:15]
        
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
            global fb_message_author
            global fb_message_name
            global fb_thread_type
            
            if fb_thread_type:

                #Current functionality only for one guild
                guild = self.guilds[0] 

                chans = discord.utils.get(guild.text_channels, name=fb_message_author)

                if chans:
                    pass
                else:
                    #Creates a new channel if no appropriate channel exists
                    await guild.create_text_channel(fb_message_author, topic = fb_thread_type)

                    #Sends message to channel with name equal to the sender's ID, and topic
                    #equal to the thread type
                    chans = discord.utils.get(guild.text_channels, name=fb_message_author) 

                channel = self.get_channel(chans.id)

                for i in fb_message:
                    msg = fb_message_name + ': ' + i 
                    await channel.send(msg)

                fb_message = []
                fb_message_author = ""
                fb_message_name = ""
                fb_thread_type = ""
                
            else:
                await asyncio.sleep(1)

    async def on_message(client, message):

        """Sends message to appropriate Facebook user when message is sent in Discord.

        Parameters:
            client (MyClient): Instance of custom Discord client
            message (discord.Message): Message object sent in Discord
        """

        latest_message = message.content

        if message.author == client.user:   
            return

        server = message.channel

        message_type_str = server.topic
        if message_type_str == 'USER':
            message_type = fbchat.ThreadType.USER
        elif message_type_str == 'GROUP':
            message_type = fbchat.ThreadType.GROUP
        else:
            print('Channel topic is missing recipient type')
            return

        #Determines ID of recepient from channel name and recipient type from channel topic
        fbclient.send(fbchat.Message(text=latest_message), thread_id=server.name, thread_type=message_type)

if __name__ == "__main__":
    token = input('Enter your Discord bot token: \n')
    email = input('Enter your Facebook email: \n')
    password = input('Enter your Facebook password: \n')

    #Initialises Facebook and Discord client objects
    fbclient = CustomClient(email, password, None, 1)
    client = MyClient()

    #Initialises Facebook listening loop and Discord bot on seperate threads
    threading.Thread(target = lambda: fbclient.listen()).start()
    threading.Thread(target = lambda: client.run(token)).start()
