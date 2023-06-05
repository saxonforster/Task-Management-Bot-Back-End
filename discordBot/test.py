from django.test import TestCase
import sys
import os 
import requests
import unittest
from rest_framework.test import APITestCase
from rest_framework import status
from bot8.models import Todo
# Create your tests here.

class Bot8Tests(APITestCase):
    # run tests with "python .\manage.py test"
    # all tests must start with test to run
    # based off https://github.com/bobby-didcoding/drf_course/blob/main/steps/module_4.md
    
    def testTaskCreationResponeIn(self):
        self.data = {
            "title" : "newTest"
        }
        self.url = "/todo"
        response = self.client.post(self.url, data=self.data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
    
    def testTaskCreationActuallyAddedCount(self):
        self.data = {
            "title" : "newTest"
        }
        self.url = "/todo"
        self.assertEqual(Todo.objects.count(), 0)
        response = self.client.post(self.url, data=self.data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Todo.objects.count(), 1)

    def testTaskCreationTitleThere(self):
        self.data = {
            "title" : "newTest"
        }
        self.url = "/todo"
        self.assertEqual(Todo.objects.count(), 0)
        response = self.client.post(self.url, data=self.data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Todo.objects.count(), 1)
        get_response = self.client.get(self.url) 
        responseOne = get_response.json()[0]
        self.assertEqual(responseOne["title"], self.data["title"])
        
