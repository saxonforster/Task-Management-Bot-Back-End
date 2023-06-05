from django.db import models

#After editing python .\manage.py makemigrations then python .\manage.py migrate
class Task(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=60)
    due_date = models.DateTimeField(null=True)

'''
    task_name      -> text
    due_date   -> date time
    status     -> choice
    participants -> list
    reminders     -> some kind of struct
    '''
