import os
import discord
from discord.ext import commands
from dotenv import load_dotenv
from rest_framework import status
import requests
import json
import asyncio
from datetime import datetime
#from bot8/views.py import *
import re
alert_times = {} #Dictionary of alert times to be checked by the bot every minute Key=id and Value=alert time

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

#channel id in Discord that we want it to respond in
channel_id = 1094031740462436446 # Replace with your channel ID
# Discord bot event for when the bot is ready
@bot.event
async def on_ready():
    print(f"{bot.user} has connected to the server")
    channel = bot.get_channel(channel_id)
    await channel.send("Running") # Send a message to the Discord channel that the bot is Running
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    print('------')
    url = baseurl + "task" 
    response = requests.get(url=url)
    reminders = json.loads(response.text)
    #at start of Discord bot run time, check for any tasks that have a reminder and add them to the alert_times dictionary
    for tasks in reminders:
        DD = tasks["reminder"]
        if DD is not None:
            DD = DD.replace("T", " ")
            DD = DD.replace("Z", "")
            DD = DD.replace(":00", "")
            ND = datetime.strptime(DD,'%Y-%m-%d %H:%M')
            alert_times[tasks["id"]] = ND
    bot.loop.create_task(check_alerts())

@bot.event
async def on_message(message: discord.Message):
    if message.author == bot.user:
        return

    username = str(message.author)
    user_message = str(message.content)
    channel = str(message.channel)

    print(f'{username} said: "{user_message}"  ({channel})') #Prints the message to the console
    await bot.process_commands(message)

@bot.command(name = 'format', help = 'Command to get list of command formats')
async def format(ctx):
    await ctx.send("Command formats are as follows: \n" \
        '!create_task <task name> \n' \
        "!due_date <task id> <due date> \n" \
        "!add_alert <task id> <alert time> \n" \
        "Both due date and alert time must be in the format YYYY-MM-DD HH:MM \n" \
        "!delete_task <task id> \n" \
        "!list_tasks \n" \
        "list_tasks_by_user <user id> \n" \
        "!assign_user <user name> \n" )
        

'''Command for creating a task'''
@bot.command(name = 'create_task', help = '!create_task <task name>   Command for creating a task ')
async def create_task(ctx, title=None):

    if title is None:#if no task name is given
        await ctx.send("No Task Name Given")
    else:
        url = baseurl + f"task"
        data = {"title": title}
        response = requests.post(url=url, data=data)#posting the task to the database
        if response.status_code == status.HTTP_201_CREATED:
            await ctx.send(f"The task {title} has been created!")

        else:
            await ctx.send("A problem occurred when trying to create the task")


'''Command for adding and editing due dates for a task '''
@bot.command(name = 'due_date', help = '!due_date <task id> <YYYY-MM-DD HH:MM>  Command for adding and editing due dates for a task')
async def due_date(ctx, id=None, due_date=None):

    if due_date is None:#no due date given
        url = baseurl + f"due-date/{id}"
        response = requests.get(url)

        if response.status_code == status.HTTP_200_OK:
            await ctx.send(response.text)
        else:
            await ctx.send("No due date found")
    elif id is None:#no id is given
        await ctx.send("No Task ID Given")
    else:#all is good
        url = baseurl + f"due-date/{id}"
        due_date_DT = datetime.strptime(due_date, '%Y-%m-%d %H:%M')#making due date into a datetime object
        data = {"due_date": due_date_DT}
        response = requests.post(url=url, data=data)#posting the due date to the task

        if response.status_code == status.HTTP_200_OK:
            await ctx.send(f"Due date: {due_date} has been assigned to the task!")
        else:
            await ctx.send("A problem occurred when trying to add a due date")


'''Command for adding due date alerts for a task'''
@bot.command(name = 'add_alert', help = '!add_alert <task id> <YYYY-MM-DD HH:MM>  Command for adding due date alerts for a task')
async def add_alert(ctx, id=None, alert=None):

    url = baseurl + f"reminder/{id}"
    
    if alert is None: # no alert given
        response = requests.get(url=url)
        if response.status_code == status.HTTP_200_OK:
            await ctx.send(response.text)
        else:
            await ctx.send(f"No task found with that {id}")
    elif id is None:# no idea is given
        await ctx.send("No Task ID Given")
    else:#all is good
        alert_dt = datetime.strptime(alert, '%Y-%m-%d %H:%M')
        alert_times[id]=alert_dt
        data = {"reminder": alert_dt}
        response = requests.put(url, data=data)

        if response.status_code == status.HTTP_200_OK:
            await ctx.send("Alert has been assigned to the task!")
        else:
            await ctx.send("A problem occurred when trying to add an alert")


'''Command for assigning users to a task'''
@bot.command(name = 'assign_user', help = '!assign_user <user name>  Command for assigning users to a task')
async def assign_user(ctx, id=None, assignees = None):

    if assignees is None: #no assignees given
        print("No assignees given")
        url = baseurl + "assignees/" + f"{id}"
        response = requests.get(url=url)

        if response.status_code == status.HTTP_200_OK:
            await ctx.send(response.text)
        else:
            await ctx.send("No assignees found")
    elif id is None: #no task id given
        await ctx.send("No Task ID Given")
    else:#all is good
        assignees_list = [user for user in assignees.split(',')]
        url = baseurl + "assignees/" + f"{id}"
        data = {"assignees": assignees_list}
        print(f"data: {data}")
        response = requests.put(url=url, data=data)#putting the assignees to the task

        if response.status_code == status.HTTP_200_OK:
            await ctx.send(f"assignees: {assignees} have been assigned to the task!")
        else:
            await ctx.send("A problem occurred when trying to add a assignees")


'''Command for listing all tasks by order of due date'''
@bot.command(name = 'list_tasks', help = '!list_tasks  Command for listing all tasks by order of due date')
async def list_tasks(ctx):
   
    url = baseurl + "task"
    response = requests.get(url=url)

    if response.status_code != status.HTTP_200_OK:
        await ctx.send("No Tasks found")
    else:
        for t in json.loads(response.text):
            dd= t["due_date"]
            if dd is not None:#formatting the due date
                dd = dd.replace("T", " ")
                dd = dd.replace("Z", "")
                dd = dd.replace(":00", "")
            ad = t["reminder"]
            if ad is not None:#formatting the alert
                ad = ad.replace("T", " ")
                ad = ad.replace("Z", "")
                ad = ad.replace(":00", "")
            await ctx.send(f'id: {t["id"]}, {t["title"]}, {t["assignees"]}, {dd}, {ad}')

'''Command for listing all tasks associated with the given user'''
@bot.command(name = 'list_tasks_by_user', help = 'list_tasks_by_user <user id>  Command to list all tasks associated with a given user')
async def list_tasks_by_user(ctx, user=None):

    url = baseurl + "task" + f"?user={user}"
    if user is None:
            await ctx.send("No user given")#if not user is given

    response = requests.get(url=url)

    if response.status_code != status.HTTP_200_OK:
        await ctx.send(f"User {user} not found") #if cant find the user/any tasks associated with the user
    else:
        if json.loads(response.text) == []:
            await ctx.send(f"User {user} has no tasks")
        for t in json.loads(response.text):
            dd= t["due_date"]
            if dd is not None: #formatting the due date
                dd = dd.replace("T", " ")
                dd = dd.replace("Z", "")
                dd = dd.replace(":00", "")
            ad = t["reminder"]
            if ad is not None:#formatting the alert
                ad = ad.replace("T", " ")
                ad = ad.replace("Z", "")
                ad = ad.replace(":00", "")
            await ctx.send(f'id: {t["id"]}, Task Name: {t["title"]}, Assignees: {t["assignees"]}, Due Date: {dd}, Alert Time: {ad}')
    

'''Command for deleting a task'''
@bot.command(name = 'delete_task', help = '!delete_task <task id>  Command for deleting a task')
async def delete_task(ctx, id=None):
   
    url = baseurl + "task/" + f"{id}"
    response = requests.delete(url=url)#delete the task
    if response.status_code == status.HTTP_204_NO_CONTENT:
        await ctx.send(f"Task with id: {id} has been deleted!")
    else:
        await ctx.send(f"A problem occurred when trying to delete the task with id {id}")


#Function to check if current time matches any alert time
async def check_alerts():
    channel = bot.get_channel(channel_id)
    idsToPop = []
    while True:
        current_time = datetime.now()
        for id, alert_time in alert_times.items():
            print("Alert checking")
            print(f"current time: {current_time}, alert time: {alert_time}")
            if current_time >= alert_time:
                print("Alerting")
                await channel.send(f"@everyone An alert for a task with id: {id} has occured!")
                idsToPop.append(id)
        for ID in idsToPop: #Remove all the ids that have been alerted so we dont Alert more then once
            alert_times.pop(ID)
        await asyncio.sleep(60) # Check every minute
 


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