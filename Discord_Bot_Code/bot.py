import os
import discord
from discord.ext import commands
from dotenv import load_dotenv

#from bot8/views.py import *

TOKEN = os.getenv('TOKEN') #Put actual discord token in #.env 

#https://realpython.com/how-to
# -make-a-discord-bot-python/
client = discord.Client()
@client.event
async def on_ready():
    '''Stop telling me to put doscstring'''
    guild = discord.utils.get(client.guilds, name=GUILD)
    print(f'{client.user} has connected to the following guild:\n'
          f'{guild.name}(id: {guild.id})')

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

class TaskCreation(commands.Cog):
    '''View for creating a task'''

class DueDate(commands.Cog):
    ''' View for adding, editing and getting due dates for a task '''

    @commands.command()
    async def due_date(self, ctx, id, due_date=None):
        if ctx.message.author == bot.user:
            return

        if ctx.message.author.bot:
            return

        if due_date is None:
            url = f"http://127.0.0.1:8000/due-date/{id}"
            response = requests.get(url)

            if response.status_code == 200:
                await ctx.send(response.text)
            else:
                await ctx.send("No due date found")

        else:
            url = f"http://127.0.0.1:8000/due-date/{id}"
            data = {"due_date": due_date}
            response = requests.post(url, data=data)

            if response.status_code == 200:
                await ctx.send("Due date has been assigned to the task!")
            else:
                await ctx.send("A problem occurred when trying to add a due date")

class DueDateAlert(commands.Cog):
    '''View for adding and getting due date alerts for a task'''

class TaskAssignment(commands.Cog):
    '''View for assigning users to a task'''

class TaskListByDueDates(commands.Cog):
    '''View for listing all tasks by order of due date'''

class TaskListByUser(commands.Cog):
    '''View for listing all tasks associated with the given user'''

class TaskDelete(commands.Cog):
    '''View for deleting a task'''



def setup(bot):
    bot.add_cog(DueDate(bot))
    bot.add_cog(DueDateAlert(bot))
    bot.add_cog(TaskAssignment(bot))
    bot.add_cog(TaskCreation(bot))
    bot.add_cog(TaskListByDueDates(bot))
    bot.add_cog(TaskListByUser(bot))
    bot.add_cog(TaskDelete(bot))

bot.run('your-bot-token')
"""
This code sets up a new Discord bot using the commands.Bot class and sets the command prefix to "!". It also creates a new cog called DueDate which handles the !due_date command.

The !due_date command takes two arguments: the task ID and an optional due date. If a due date is not provided, it sends a GET request to the Django view to get the due date for the task ID. If a due date is provided, it sends a POST request to the Django view to add the due date to the task ID.

Note that you will need to replace the http://127.0.0.1:8000 URL with the URL of your Django app.

To run the Discord bot, you'll need to replace your-bot-token with your actual bot token and run the discordbot.py file: python discordbot.py
"""