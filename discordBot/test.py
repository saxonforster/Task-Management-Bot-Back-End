from django.test import TestCase
import sys
import os 
import requests
import unittest
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from bot8.models import Task
import datetime
# Create your tests here.

class US1Tests(APITestCase):
    # run tests with "python .\manage.py test"
    # all tests must start with test to run
    # based off https://github.com/bobby-didcoding/drf_course/blob/main/steps/module_4.md
    
    def testTaskCreationResponeIn(self):
        self.data = {
            "title" : "newTest"
        }
        self.url = "/Task"
        response = self.client.post(self.url, data=self.data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
    
    def testTaskCreationActuallyAddedCount(self):
        self.data = {
            "title" : "newTest"
        }
        self.url = "/Task"
        self.assertEqual(Task.objects.count(), 0)
        response = self.client.post(self.url, data=self.data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Task.objects.count(), 1)

    def testTaskCreationTitleThere(self):
        self.data = {
            "title" : "newTest"
        }
        self.url = "/Task"
        self.assertEqual(Task.objects.count(), 0)
        response = self.client.post(self.url, data=self.data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Task.objects.count(), 1)
        get_response = self.client.get(self.url) 
        responseOne = get_response.json()[0]
        self.assertEqual(responseOne["title"], self.data["title"])
        
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
        

