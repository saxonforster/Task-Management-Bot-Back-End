from django.test import TestCase
import sys
import os 
import requests
import unittest
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from bot8.models import Task
import datetime
import json
# Create your tests here.

class US1Tests(APITestCase):
    # run tests with "python .\manage.py test"
    # all tests must start with test to run
    # based off https://github.com/bobby-didcoding/drf_course/blob/main/steps/module_4.md

    def setUp(self):
        self.data = {
            "title" : "newTest"
        }
        self.url = "/Task"
        
    
    def testTaskCreationResponeIn(self):
       
        response = self.client.post(self.url, data=self.data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
    
    def testTaskCreationActuallyAddedCount(self):
        
        self.assertEqual(Task.objects.count(), 0)
        response = self.client.post(self.url, data=self.data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Task.objects.count(), 1)

    def testTaskCreationTitleThere(self):
        
        self.assertEqual(Task.objects.count(), 0)
        response = self.client.post(self.url, data=self.data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Task.objects.count(), 1)
        get_response = self.client.get(self.url)
        responseOne = get_response.json()[0]
        self.assertEqual(responseOne["title"], self.data["title"])

class US2Tests(APITestCase):

    def setUp(self):
        # create a task in database
        # endpoint needs existing task
        Task.objects.create(title = 'newTask')

        self.data = {
            "id" : 1,
            "assignees": ["Amann#4989","Jack#7654"]
        }
        self.url = "/assignUsers"
   
    def testTaskAssignment(self):
        """
        When a task is created, users should be able to be assigned to it
        by providing a list of users and an id of a task
        """
        response = self.client.put(path=self.url, data=self.data)

        self.assertEqual(response.status_code,status.HTTP_200_OK)
        tasks = Task.objects.all()
        self.assertEqual(1, len(tasks))
        assignees = tasks[0].assignees.all()
        self.assertEqual(2, len(assignees))
        self.assertEqual(self.data['assignees'][0], assignees[0].username)
        self.assertEqual(self.data['assignees'][1], assignees[1].username)

    def testAssigningDuplicateUser(self):
        '''
        Assigning a user to a task that they are already assigned
        to should return an error status code
        '''
        self.client.put(path=self.url, data=self.data)
        # remove first assignee from data
        self.data['assignees'].pop(0)
        # put request with single duplicate user
        response = self.client.put(path=self.url, data=self.data)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        expected_message = f'User(s) {self.data["assignees"]} are already assigned to this task'
        self.assertEqual(response.data, expected_message)
    
    def testAddingUserToTaskWithUser(self):
        '''
        Adding a user to a task when the task already has a user assigned
        should not clear the existing user
        '''
        self.client.put(path=self.url, data={"id":1, "assignees":["User#2345"]})
        self.assertEqual(1, len(Task.objects.get(id=1).assignees.all()))
        self.client.put(path=self.url, data={"id":1, "assignees":["Another#1115"]})
        self.assertEqual(2, len(Task.objects.get(id=1).assignees.all()))

        
class US4Tests(APITestCase):
    def setUp(self):
        self.data = {
            "title" : "newTest"
        }
        self.url = "/due_date/1"
        self.dd = '2023-10-25 14:30'
        self.due_dateAndID = {"id": 1,"due_date":'2023, 10, 25, 14, 30'}
        self.new_dd = '2023-11-24 14:30'
        self.ID = {"id": 1}
        self.response = self.client.post("/Task", data=self.data)

    def testNoDueDate(self):
        """
        testing to see if there is no due date when first making a task
        """
        get_response = self.client.get(self.url)
        self.assertIsNone(get_response.data)

    def testAddDueDate(self):
        """
        testing to see if you can add a due date and it then exists
        """
        self.response = self.client.post(self.url, data=self.due_dateAndID)
        get_response = self.client.get(self.url)
        self.assertEqual(get_response.data, self.dd)

    def testChangeDueDate(self):
        """
        testing to see if you can change the duedate after it is created
        """
        self.response = self.client.post(self.url, data=self.due_dateAndID)
        self.due_dateAndID = {"due_date":'2023, 11, 24, 14, 30'}
        self.response = self.client.post(self.url, data=self.due_dateAndID)
        get_response = self.client.get(self.url)
        self.assertEqual(get_response.data, self.new_dd)

    def testDifferentDueDateFormats(self):
        """
        Should test multiple ways users can input the duedate to see if it can handle it properly
        as well as send an error if incorrect format is used
        """
        

