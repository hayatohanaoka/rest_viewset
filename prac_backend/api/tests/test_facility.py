from django.test import TestCase
from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.test import APITestCase
from parameterized import parameterized

from ..models import Facility
from ..serializers import FacilitySerializer

# Create your tests here.
class FacilityViewSetTestCase(APITestCase):
    username = 'test'
    password = '1234567'

    @classmethod
    def setUpTestData(cls):
        cls.facility_one = Facility.objects.create(
            name='Facility1',
            detail='Detail1'
        )
        cls.facility_two = Facility.objects.create(
            name='Facility2',
            detail='Detail2'
        )
        cls.user = User.objects.create_user(
            username=cls.username,
            password=cls.password
        )
    
    def login(self):
        self.client.login(username=self.username, password=self.password)
    
    def test_list(self):
        url = '/api/facility/'
        res = self.client.get(url)
    
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, FacilitySerializer([self.facility_one, self.facility_two], many=True).data)

    def test_retrieve(self):
        url_one = f'/api/facility/{self.facility_one.id}/'
        url_two = f'/api/facility/{self.facility_two.id}/'
    
        res_one = self.client.get(url_one)
        res_two = self.client.get(url_two)
    
        self.assertEqual(res_one.status_code, status.HTTP_200_OK)
        self.assertEqual(res_one.data, FacilitySerializer(self.facility_one).data)
        self.assertEqual(res_two.status_code, status.HTTP_200_OK)
        self.assertEqual(res_two.data, FacilitySerializer(self.facility_two).data)
    
    def testy_retrieve_non_exist_facility(self):
        url = f'/api/facility/999999/'
        res = self.client.get(url)
        self.assertEqual(res.status_code, status.HTTP_404_NOT_FOUND)

    def test_filter_list(self):
        url = '/api/facility/filter_list/'
        res = self.client.get(url, {'name': 'Facility1'})
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, FacilitySerializer([self.facility_one], many=True).data)
    
    def test_create_without_login(self):
        url = '/api/facility/'
        data = {'name': 'new Facility', 'detail': 'new Detail'}
        res = self.client.post(url, data)
        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(Facility.objects.count(), 2)

    @parameterized.expand([  # 複数パラメータを用いたテスト
        ('new Facility', 'new Detail'),
        ('1'*100, 'new Detail'),
    ])
    def test_create(self, name, detail):
        url = '/api/facility/'
        data = {'name': name, 'detail': detail}

        self.login()
        res = self.client.post(url, data)
        inserted_facility = Facility.objects.get(id=res.data['id'])

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Facility.objects.count(), 3)
        self.assertEqual(inserted_facility.name, data['name'])
        self.assertEqual(inserted_facility.detail, data['detail'])

    @parameterized.expand([  # 複数パラメータを用いたテスト
        ('1'*101, 'over 100 chars'),
        ('', 'name is empty'),
        ('detail empty facility', ''),
    ])
    def test_create_invalid_data(self, name, detail):
        url = '/api/facility/'
        data = {'name': name, 'detail': detail}

        self.login()
        res = self.client.post(url, data)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Facility.objects.count(), 2)
