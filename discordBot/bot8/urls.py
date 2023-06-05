from django.urls import path
from .views import TaskList, DueDate

urlpatterns = [
    path('Task', TaskList.as_view()),
    path('due_date/<int:pk>', DueDate.as_view())
]