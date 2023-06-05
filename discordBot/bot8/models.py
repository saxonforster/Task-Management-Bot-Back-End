from django.db import models

# using choices with models
# https://stackoverflow.com/questions/18676156/how-to-properly-use-the-choices-field-option-in-django

# Create your models here.

class Todo(models.Model):
    class Status(models.TextChoices):
        Started = "started", "Started"
        Completed = "completed", "Completed"
        Todo = "todo", "Todo"


    title = models.CharField(max_length=60)
    due_date = models.DateTimeField(null = True)
    status = models.CharField(max_length=10, choices=Status.choices, default=Status.Todo)
    created_at = models.DateTimeField(auto_now_add=True)
    # will need some kind of reminders 
    # will need some kind of participants


    '''
    task_name      -> text
    due_date   -> date time
    status     -> choice
    participants -> list
    reminders     -> some kind of struct
    '''
