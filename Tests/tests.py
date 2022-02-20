from django.urls import reverse
from rest_framework.test import APITestCase, APIClient
from django.contrib.auth.models import User
from rest_framework import status
import json

# Create your tests here.

class TradeApiTest(APITestCase):
    def setUp(self):
        self.test_user = User.objects.create_user('testuser1', 'testuser1@example.com', 'testpassword1', is_staff=False)

        self.test_user2 = User.objects.create_user('testuser2', 'testuser2@example.com', 'testpassword2', is_staff=False)

        self.customclient = APIClient()

        self.create_url = reverse('api_trade')

    def test_create_trade_user1(self):
        data = {
            'type': 'buy',
            'user_id': '1',
            'symbol': 'ABX',
            'shares': '30',
            'price': '134'
        }

        response = self.customclient.post(self.create_url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(1, response.data['user_id'])

    def test_create_trade_user2(self):
        data = {
            'type': 'buy',
            'user_id': '2',
            'symbol': 'ABX',
            'shares': '30',
            'price': '134'
        }

        response = self.customclient.post(self.create_url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(2, response.data['user_id'])


    def test_create_trade_wrong_share(self):
        data = {
            'type': 'buy',
            'user_id': '1',
            'symbol': 'ABX',
            'shares': '400',
            'price': '134'
        }

        response = self.customclient.post(self.create_url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_trade_wrong_type(self):
        data = {
            'type': 'dance',
            'user_id': '1',
            'symbol': 'ABX',
            'shares': '80',
            'price': '134'
        }

        response = self.customclient.post(self.create_url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_get_trades(self):
        self.test_create_trade_user1()
        self.test_create_trade_user2()

        response = self.customclient.get(self.create_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_trade_id(self):
        self.test_create_trade_user1()

        response = self.customclient.get('http://127.0.0.1:8000/api/trades/1')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_trade_queryset(self):
        self.test_create_trade_user2()

        response = self.customclient.get('http://127.0.0.1:8000/api/trades/?type=buy&user_id=2')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_trade_queryset_wrong(self):
        self.test_create_trade_user2()

        response = self.customclient.get('http://127.0.0.1:8000/api/trades/?type=car&user_id=2')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_delete_trade(self):
        self.test_create_trade_user1()

        response = self.customclient.delete('http://127.0.0.1:8000/api/trades/1')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

class TestInvalidOperations(APITestCase):

    def setUp(self):
        self.customclient = APIClient()
        self.create_url = reverse('api_trade')
        self.test_user = User.objects.create_user('testuser1', 'testuser1@example.com', 'testpassword1',
                                                  is_staff=False)
        TradeApiTest.test_create_trade_user1(self)

    def test_put_not_allowed(self):
        data = {
            'type': 'sell',
            'user_id': '2',
            'symbol': 'ABX',
            'shares': '30',
            'price': '134'
        }
        response = self.customclient.put('http://127.0.0.1:8000/api/trades/1', data)
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_patch_not_allowed(self):
        data = {
            'type': 'sell',
        }
        response = self.customclient.patch('http://127.0.0.1:8000/api/trades/1', data)
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)



