from django.urls import path
from .views import TaskList, DueDate, assignUsersToTask, reminder, TaskDetail

urlpatterns = [
    path('Task', TaskList.as_view()),
    path('Task/<int:pk>', TaskDetail.as_view()),
    path('due_date/<int:pk>', DueDate.as_view()),
    path('assignUsers', assignUsersToTask.as_view()),
    path('reminder',reminder.as_view()),
]