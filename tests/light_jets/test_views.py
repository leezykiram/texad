# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.authtoken.models import Token
# Create your tests here.
from rest_framework.test import APIClient, APIRequestFactory, APITestCase

from light_jets.models import Product


class ProductTest(APITestCase):
    
    def setUp(self):
        self.username = "yellove"
        self.email = "mcarthy@gmail.com"
        self.password = "howsimpleitis"

        self.user = User.objects.create_user(
            self.username, self.email, self.password
        )

    def test_anonymous_user_create_product(self):
        """
        Ensure user has to be logged in we can create a new product object.
        """
        url = reverse('product-list')
        data = {
            "product_id": 74,
            "description": "Primex Jet 3"
        }
        # without logging in
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
    
    def test_wrong_user_creds_create_product(self):
        """
        Ensure user has to provide expected credentials.
        """
        url = reverse('product-list')
        data = {
            "product_id": 74,
            "description": "Primex Jet 3"
        }
        # without logging in
        self.client.login(username=self.username, password="Iforgotthepassword")
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_create_product(self):
        """
        Ensure we can create a new product object.
        """
        url = reverse('product-list')
        data = {
            "product_id": 74,
            "description": "Primex Jet 3"
        }

        self.client.login(username=self.username, password=self.password)
        response = self.client.get(url)
        self.assertEqual(response.status_code,status.HTTP_200_OK)
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Product.objects.count(), 1)
        self.assertEqual(Product.objects.get().product_id, 74)
        self.assertEqual(Product.objects.get().description,"Primex Jet 3")
