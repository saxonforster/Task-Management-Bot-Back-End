from django.urls import path
from .views import TodoList

urlpatterns = [
    path('todo', TodoList.as_view()),
]