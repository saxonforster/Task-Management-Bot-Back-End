from django.db import models

#After editing python .\manage.py makemigrations then python .\manage.py migrate

class Users(models.Model):

    username = models.CharField(primary_key=True, max_length=60)
    servername = models.CharField(null=True, max_length=100)

    def __str__(self):
        return self.username
    
class Task(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=60)
    due_date = models.DateTimeField(null=True)
    assignees = models.ManyToManyField(Users, blank=True, related_name='task')
    reminder = models.DateTimeField(null=True)


    

    
    
'''
    task_name      -> text
    due_date   -> date time
    status     -> choice
    participants -> list
    reminders     -> some kind of struct
'''





