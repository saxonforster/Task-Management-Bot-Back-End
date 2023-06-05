import os
import discord
from discord.ext import commands
#from bot8/views.py import *

TOKEN = os.getenv('TOKEN') #Put actual discord token in #.env 

#https://realpython.com/how-to
# -make-a-discord-bot-python/
client = discord.Client()
@client.event
async def on_ready():
   
    print(f'{client.user} has connected to Discord')



client.run(TOKEN)

"""
A Client is an object that represents a connection to Discord. A Client handles events, 
tracks state, and generally interacts with Discord APIs.

Here, you’ve created a Client and implemented its on_ready() event handler, 
which handles the event when the Client has established a connection to Discord 
and it has finished preparing the data that Discord has sent, such as login state, 
guild and channel data, and more.

In other words, on_ready() will be called (and your message will be printed) 
once client is ready for further action.
"""