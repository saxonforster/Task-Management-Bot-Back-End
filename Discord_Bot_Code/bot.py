import os
import discord
from discord.ext import commands
from dotenv import load_dotenv
from rest_framework import status
import requests
import json
#from bot8/views.py import *

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN') #Put actual discord token in #.env 
#GUILD = os.getenv('DISCORD_GUILD') #Put actual guild name in #.env
#https://realpython.com/how-to-make-a-discord-bot-python/


class TestableBot(commands.Bot):
    async def process_commands(self, message: discord.Message, /) -> None:
        ctx = await self.get_context(message)
        await self.invoke(ctx)

baseurl = 'http://127.0.0.1:8000/'
bot = TestableBot(intents=discord.Intents.all(), command_prefix='!')

@bot.event
async def on_ready():
    print(f"{bot.user} has connected to the server")
    channel = bot.get_channel(1090771155163549796)
    await channel.send("Running")

@bot.event
async def on_message(message: discord.Message):
    if message.author == bot.user:
        return

    username = str(message.author)
    user_message = str(message.content)
    channel = str(message.channel)

    print(f'{username} said: "{user_message}"  ({channel})')
    await bot.process_commands(message)


'''View for creating a task'''
@bot.command(name = 'create_task', help = 'Creates a task')
async def task_creation(ctx, title):

    if title is None:
        await ctx.send("No Task Name Given")
    else:
        url = baseurl + f"task"
        data = {"title": title}
        response = requests.post(url=url, data=data)
        if response.status_code == status.HTTP_201_CREATED:
            await ctx.send(f"The task {title} has been created!")

        else:
            await ctx.send("A problem occurred when trying to create the task")


''' View for adding, editing and getting due dates for a task '''
@bot.command(name = 'due_date')
async def due_date(ctx, id, due_date=None):
    if ctx.message.author == bot.user:
        return

    if ctx.message.author.bot:
        return

    if due_date is None:
        url = baseurl + f"due-date/{id}"
        response = requests.get(url)

        if response.status_code == status.HTTP_200_OK:
            await ctx.send(response.text)
        else:
            await ctx.send("No due date found")

    else:
        url = baseurl + f"{id}"
        data = {"due_date": due_date}
        response = requests.post(url=url, data=data)

        if response.status_code == status.HTTP_200_OK:
            await ctx.send(f"Due date: {due_date} has been assigned to the task!")
        else:
            await ctx.send("A problem occurred when trying to add a due date")


'''View for adding and getting due date alerts for a task'''
@bot.command(name = 'add_alert')
async def add_alert(ctx, id, alert=None):

    url = baseurl + f"reminder/{id}"

    if alert is None:
        response = requests.get(url=url)
        if response.status_code == status.HTTP_200_OK:
            await ctx.send(response.text)
        else:
            await ctx.send(f"No task found with that {id}")
    else:
        #Finish later
        data = {"reminder": alert}
        response = requests.post(url, data=data)

        if response.status_code == status.HTTP_200_OK:
            await ctx.send("Alert has been assigned to the task!")
        else:
            await ctx.send("A problem occurred when trying to add an alert")


'''View for assigning users to a task'''
@bot.command(name = 'task_assignment')
async def task_assignment(ctx, id, assignees = []):

    if not assignees:
        url = baseurl + "assignees/" + f"{id}"
        response = requests.get(url=url)

        if response.status_code == status.HTTP_200_OK:
            await ctx.send(response.text)
        else:
            await ctx.send("No assignees found")
    else:
        url = baseurl + "assignees/" + f"{id}"
        data = {"assignees": assignees}
        response = requests.post(url=url, data=data)

        if response.status_code == status.HTTP_200_OK:
            await ctx.send(f"assignees: {assignees} have been assigned to the task!")
        else:
            await ctx.send("A problem occurred when trying to add a assignees")


'''View for listing all tasks by order of due date'''
@bot.command(name = 'list_tasks')
async def list_tasks(ctx):
   
    url = baseurl + "task"
    response = requests.get(url=url)

    if response.status_code != status.HTTP_200_OK:
        await ctx.send("No Tasks found")
    else:
        for t in json.loads(response.text):
            await ctx.send(f'{t["id"]}, {t["title"]}, {t["assignees"]}, {t["due_date"]}, {t["reminder"]}')


'''View for listing all tasks associated with the given user'''
@bot.command(name = 'list_tasks_by_user')
async def list_tasks_by_user(ctx, user):

    url = baseurl + "task" + f"?user=<{user}>"
    if user is None:
            await ctx.send("No user given")

    response = requests.get(url=url)

    if response.status_code != status.HTTP_200_OK:
        await ctx.send(f"User {user} not found")
    else:
        for t in json.loads(response.text):
            await ctx.send(f'{t["id"]}, {t["title"]}, {t["assignees"]}, {t["due_date"]}, {t["reminder"]}')
    

'''View for deleting a task'''
@bot.command(name = 'delete_task')
async def delete_task(ctx, id):
   
    url = baseurl + "task/" + f"{id}"
    response = requests.delete(url=url)
    if response.status_code == status.HTTP_204_NO_CONTENT:
        await ctx.send(f"Task with id: {id} has been deleted!")
    else:
        await ctx.send(f"A problem occurred when trying to delete the task with id {id}")
'''
def setup(bot):
    bot.add_cog(DueDate(bot))
    bot.add_cog(DueDateAlert(bot))
    bot.add_cog(TaskAssignment(bot))
    bot.add_cog(TaskCreation(bot))
    bot.add_cog(TaskListByDueDates(bot))
    bot.add_cog(TaskListByUser(bot))
    bot.add_cog(TaskDelete(bot))'''

bot.run(TOKEN)
"""
This code sets up a new Discord bot using the commands.Bot class and sets the command prefix to "!". 
It also creates a new cog called DueDate which handles the !due_date command.

The !due_date command takes two arguments: the task ID and an optional due date. 
If a due date is not provided, it sends a GET request to the Django view to get the due date for the task ID. 
If a due date is provided, it sends a POST request to the Django view to add the due date to the task ID.

Note that you will need to replace the http://127.0.0.1:8000 URL with the URL of your Django app.

To run the Discord bot, you'll need to replace your-bot-token with your actual bot token and run the discordbot.py file: python discordbot.py
"""