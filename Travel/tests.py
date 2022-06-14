'''
import json
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from .models import Task
from .serializers import *


#LOCATION TEST
class CreateNewTaskTest(APITestCase):
    """ Test module for inserting a new puppy """

    def setUp(self):
        self.valid_payload = {
            'title': 'Book',
            'state': "draft",
        }

        self.invalid_payload_1 = {
            'title': 'Book 1',
            'state': 'active',
        }

        self.invalid_payload_2 = {
            'title': 'Book 2',
            'state': 'done',
        }

        self.invalid_payload_3= {
            'title': 'Book 3',
            'state': 'achieved',
        }
        

    def test_create_valid_task(self):
        response = self.client.post(
            reverse('task-create-list'),
            data=json.dumps(self.valid_payload),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_invalid_task_1(self):
        response = self.client.post(
            reverse('task-create-list'),
            data=json.dumps(self.invalid_payload_1),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_invalid_task_2(self):
        response = self.client.post(
            reverse('task-create-list'),
            data=json.dumps(self.invalid_payload_2),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_invalid_task_3(self):
        response = self.client.post(
            reverse('task-create-list'),
            data=json.dumps(self.invalid_payload_3),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class GetAllTask(APITestCase):
    """ Test module for GET all Task API """

    def setUp(self):
        Task.objects.create(title="BOOK 5")
        Task.objects.create(title="BOOK 5")

    def test_get_all_puppies(self):
        # get API response
        response = self.client.get(reverse('task-create-list'))
        # get data from db
        task = Task.objects.all()
        serializer = TaskSerializer(task, many=True)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class GetSingleTask(APITestCase):
    """ Test module for GET all Task API """

    def setUp(self):
        self.book = Task.objects.create(title="BOOK 6")

    def test_single_task(self):
        # get API response
        response = self.client.get(reverse('task-crud', kwargs={"pk":self.book.pk}))
        # get data from db
        task = Task.objects.get(id=self.book.pk)
        serializer = TaskSerializer(task)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)



class UpdateSingleTaskTest(APITestCase):
    """ Test module for updating an existing puppy record """

    def setUp(self):
        self.book_6 = Task.objects.create(title="BOOK 6", state ="draft")
        self.book_7= Task.objects.create(title="BOOK 7", state= "active")
        self.book_8= Task.objects.create(title="BOOK 8", state= "done")
        self.book_9= Task.objects.create(title="BOOK 9", state= "achieved")
      
        self.payload_1 = {
            "title":"Book 6",
           "state":"draft"
        }      
        self.payload_2 = {
            "title":"Book 7",
            "state":"active"
        }
        self.payload_3 = {
            "title":"Book 8",
           "state":"done"
        }
        self.payload_4 = {
            "title":"Book 9",
           "state":"achieved"
        }
      

    def test_valid_update_task_1(self):
        response = self.client.put(
            reverse('task-crud', kwargs={'pk': self.book_6.pk}),
            data=json.dumps(self.payload_2),
            content_type='application/json'
        )
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        

        response = self.client.put(
            reverse('task-crud', kwargs={'pk': self.book_6.pk}),
            data=json.dumps(self.payload_3),
            content_type='application/json'
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
       

        response = self.client.put(
            reverse('task-crud', kwargs={'pk': self.book_6.pk}),
            data=json.dumps(self.payload_4),
            content_type='application/json'
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        

        

    def test_invalid_update_task_1(self):
        response = self.client.put(
            reverse('task-crud', kwargs={'pk': self.book_7.pk}),
            data=json.dumps(self.payload_1),
            content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        response = self.client.put(
            reverse('task-crud', kwargs={'pk': self.book_8.pk}),
            data=json.dumps(self.payload_1),
            content_type='application/json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        response = self.client.put(
            reverse('task-crud', kwargs={'pk': self.book_9.pk}),
            data=json.dumps(self.payload_3),
            content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        response = self.client.put(
            reverse('task-crud', kwargs={'pk': self.book_9.pk}),
            data=json.dumps(self.payload_2),
            content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        response = self.client.put(
            reverse('task-crud', kwargs={'pk': self.book_9.pk}),
            data=json.dumps(self.payload_1),
            content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)



class DeleteSingleTaskTest(APITestCase):
    """ Test module for deleting an existing puppy record """

    def setUp(self):
        self.task_1 = Task.objects.create(title = "Task 1")
        

    def test_valid_delete_task(self):
        response = self.client.delete(
            reverse('task-crud', kwargs={'pk': self.task_1.pk}))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_invalid_delete_task(self):
        response = self.client.delete(
            reverse('task-crud', kwargs={'pk': 30}))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
'''