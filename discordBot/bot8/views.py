from rest_framework import generics, response, status
from .models import Task
from .serializers import TaskSerializer
import datetime
from rest_framework.views import APIView
import pytz
from rest_framework.response import Response

# filter by id?
class TaskList(generics.ListCreateAPIView):
    serializer_class = TaskSerializer
    queryset = Task.objects.all()

class DueDate(APIView):
    serializer_class = TaskSerializer
    queryset = Task.objects.all()

    def post(self, request, **kwargs):
        task_id = kwargs.get('pk', -1)
        dueDate = request.data["due_date"]
        dueDateSplit = dueDate.split(", ")
        Year = int(dueDateSplit[0]) 
        Month = int(dueDateSplit[1]) 
        Day = int(dueDateSplit[2]) 
        Hour = int(dueDateSplit[3]) 
        Minute = int(dueDateSplit[4])
        d = datetime.datetime(Year, Month, Day, Hour, Minute, tzinfo= pytz.UTC)
        try:
            task = Task.objects.filter(id=task_id)[0]
        except:
            return Response(data = "A problem occured when trying to add a due date", status =status.HTTP_400_BAD_REQUEST)
        task.due_date=d
        task.save()
        return Response (data="A Due Date has been assigned to the task!", status = status.HTTP_200_OK)
        
    
    def get(self, requests, **kwargs):
        id_given = kwargs.get('pk', -1)
        try:
            task = Task.objects.filter(id=id_given)[0]
            DD = task.due_date
            ND = DD.strftime('%Y-%m-%d %H:%M')
            return Response (data = ND, status = status.HTTP_200_OK)
        except:
            return Response(data=None, status =status.HTTP_400_BAD_REQUEST)
        

