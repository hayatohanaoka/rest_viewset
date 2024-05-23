from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth.models import User
from parameterized import parameterized

class UserViewSetTestCase(APITestCase):
    username = 'test'
    password = '123456'

    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_user(
            username=cls.username,
            password=cls.password
        )
    
    def test_regist(self):
        url = '/api/user/regist/'
        data = {'username': 'newuser', 'password': 'newpassword'}
        res = self.client.post(url, data)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        self.assertTrue(User.objects.get(username=self.username))

    @parameterized.expand([
        ('', ''),
        ('testuser', ''),
        ('', 'testpassword'),
        (username, password)
    ])
    def test_regist_failed(self, username, password):
        url = '/api/user/regist/'
        data = {'username': username, 'password': password}
        res = self.client.post(url, data)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertTrue(User.objects.count(), 1)
    
    def test_login(self):
        url = '/api/user/login/'
        data = {'username': self.username, 'password': self.password}
        res = self.client.post(url, data)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
    
    @parameterized.expand([
        ('', ''),
        ('testuser', ''),
        ('', 'testpassword'),
        ('testuser', 'testpassword'),
    ])
    def test_login_failed(self, username, password):
        url = '/api/user/login/'
        data = {'username': username, 'password': password}
        res = self.client.post(url, data)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

