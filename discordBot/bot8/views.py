from rest_framework import generics
from .models import Todo
from .serializers import TodoSerializer


# filter by id?
class TodoList(generics.ListCreateAPIView):
    serializer_class = TodoSerializer
    queryset = Todo.objects.all()

class TodoDetail(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = TodoSerializer
    queryset = Todo.objects.all()

