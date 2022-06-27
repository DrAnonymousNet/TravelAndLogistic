from email import header
import json
from multiprocessing import context
from django.urls import reverse
from requests import request
from rest_framework import status
from rest_framework.test import APITestCase
from ..models import *
from ..serializers import *
from account.models import *
from requests.auth import HTTPBasicAuth


#LOCATION TEST
class CreateNewLocation(APITestCase):
    """ Test module for inserting a new puppy """

    def setUp(self):
        self.user = UserAccount.objects.create_testuser(email="haryourdejijb@gmail.com",password="12345")
    
        self.valid_payload = {
            'state': 'Kwara',
            'city': "ilorin",
            'address':"oke odo"
        }

        self.valid_payload_2 = {
            'state': 'Kwara',
            'city': "ilorin",
            'address':"saw mill"
        }
        self.valid_payload_3 = {
            'state': 'Oyo',
            'city': "ilorin",
            'address':"saw mill"
        }
        self.auth = self.client.post("http://localhost:8000/auth/jwt/create/", data={
            "email":"haryourdejijb@gmail.com",
            "password":"12345"
            }
        )
        

        self.headers = {
            "HTTP_AUTHORIZATION":"JWT " + str(self.auth.data["access"])
        }

        response = self.client.post(
            reverse('location-create-list'),
            data=json.dumps(self.valid_payload_3),
            content_type='application/json', **self.headers
        )
    
        

    def test_create_valid_location(self):
        
        
        response = self.client.post(
            reverse('location-create-list'),
            data=json.dumps(self.valid_payload),
            content_type='application/json', **self.headers
        )
        
        serializer = LocationSerializer(data=self.valid_payload, context = {

        "request":response.wsgi_request})
        #print(response.data)
        serializer.is_valid()
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        #self.assertEqual(response.data, serializer.data)

        response = self.client.post(
            reverse('location-create-list'),
            data=json.dumps(self.valid_payload),
            content_type='application/json' ,**self.headers
        )
        print(response.data)
        serializer = LocationSerializer(data=self.valid_payload)
        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_get_all_location_test(self):
        
        response = self.client.get(reverse('location-create-list'), **self.headers)
        # get data from db
        print(response.data, "jjdij")
        request = response.wsgi_request
        location = Location.objects.all()
        serializer = LocationSerializer(location, many=True, context = {"request":request} )
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_single_location_test(self):
        # get API response
        response = self.client.get(reverse('location-crud', kwargs={"pk":1}))
        # get data from db
        location = Location.objects.get(id=1)
        serializer = LocationSerializer(location, context={"request":response.wsgi_request})
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


    def test_update_single_location_test(self):
        print("Hello")
        location = Location.objects.get(id=1)

        response = self.client.put(
        reverse('location-crud', kwargs={'pk': 1}),
            data=json.dumps(self.valid_payload_2),
            content_type='application/json', **self.headers
        )
        location.refresh_from_db()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(location.address, "Saw Mill")

    def test_delete_single_location(self):
        
        response = self.client.delete(
            reverse('location-crud', kwargs={'pk': 1}), **self.headers)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)


        





