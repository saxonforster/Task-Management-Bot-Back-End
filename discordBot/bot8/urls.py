from django.urls import path
from .views import TaskList, DueDate, assignUsersToTask

urlpatterns = [
    path('Task', TaskList.as_view()),
    path('due_date/<int:pk>', DueDate.as_view()),
    path('assignUsers', assignUsersToTask.as_view()),
]