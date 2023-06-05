from rest_framework import generics, response, status
from .models import Task, Users
from .serializers import TaskSerializer, UserSerializer
from django.db.models import F
import datetime
from rest_framework.views import APIView
import pytz
from rest_framework.response import Response

# filter by id?
class TaskList(generics.ListCreateAPIView):
    serializer_class = TaskSerializer

    def get_queryset(self):
        user = self.request.query_params.get('user')
        queryset = Task.objects.all().order_by(F('due_date').asc(nulls_last=True))
        if user is not None:
            queryset = queryset.filter(assignees=user)
        return queryset
        
    

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
        

class assignUsersToTask (APIView):
   
   def put(self, request):
        try:
            task_id = request.data['id']
            assignees = request.data.getlist('assignees') # not request.data['assignees']

            task = Task.objects.all().get(id=task_id)
            duplicate_users = task.assignees.filter(pk__in=assignees)

            if len(duplicate_users):
                usernames = [user.username for user in duplicate_users]
                return Response(
                    data = f'User(s) {usernames} are already assigned to this task', 
                    status=status.HTTP_400_BAD_REQUEST)
            
            users = [Users.objects.create(username=assignee) for assignee in assignees]
            task.assignees.add(*users)

            return Response(data="Added User(s)", status=status.HTTP_200_OK)
        
        except:  
            return Response(data='Failed to add user(s)', status=status.HTTP_400_BAD_REQUEST)

class reminder (APIView):
    def put(self,request):
        try:    

            task_id = request.data['id']
            reminder_date = request.data['reminder']
            task = Task.objects.all().get(id = task_id)
            task.reminder = reminder_date
            task.save()

            return Response(data="Reminder has been set", status=status.HTTP_200_OK)
        
        except:
        
            return Response( data= "Reminder was not set or Invalid format", status= status.HTTP_400_BAD_REQUEST)