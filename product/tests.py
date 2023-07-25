from django.test import TestCase, Client
from rest_framework import status
from .models import Product

class ProductListApiTest(TestCase):
    """
    Test module for ProductListApi view.
    """

    def setUp(self):
        """
        Set up method for the test case. This method runs before each test.
        """
        self.client = Client()
        #todo here

    def test_product_list(self):
        """
        Test to verify the retrieval of product list.
        """
        response = self.client.get('/api/product_list/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue('success' in response.data)
        self.assertTrue('content' in response.data)
        self.assertEqual(response.data['success'], True)
        self.assertEqual(response.data['message'], 'Products retrieved successfully.')

class ProductRetrieveApiTest(TestCase):
    """
    Test module for ProductRetrieveApi view.
    """

    def setUp(self):
        """
        Set up method for the test case. This method runs before each test.
        """
        self.client = Client()
        #todo: to create some instances of Product or other necessary models here
       

    def test_product_retrieve(self):
        """
        Test to verify the retrieval of a single product.
        """
        response = self.client.get(f'/api/product_retrieve/{self.product.id}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue('success' in response.data)
        self.assertTrue('content' in response.data)
        self.assertEqual(response.data['success'], True)
        self.assertEqual(response.data['message'], 'Product retrieved successfully.')
