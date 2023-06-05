from django.db import models
#After editing python .\manage.py makemigrations then python .\manage.py migrate
class Todo(models.Model):
    title = models.CharField(max_length=60)

'''
    task_name      -> text
    due_date   -> date time
    status     -> choice
    participants -> list
    reminders     -> some kind of struct
    '''
