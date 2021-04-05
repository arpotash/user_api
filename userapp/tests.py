from django.test import TestCase
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.test import APIClient
from .models import User
from mixer.backend.django import mixer


class TestAuthUserViewSet(TestCase):

    def setUp(self) -> None:
        self.user = mixer.blend(User)
        user = User.objects.create_superuser('user', 'user@user.ru', 'user123456')
        token, created = Token.objects.get_or_create(user=user)
        self.client = APIClient(HTTP_AUTHORIZATION='Token ' + token.key)

    def test_get_list(self):
        request = self.client.get('/api/v1/users/')
        self.assertEqual(request.status_code, status.HTTP_200_OK)

    def test_create_user(self):
        request = self.client.post('/api/v1/users/',
                                   {'username': 'username',
                                    'first_name': 'user_first_name',
                                    'last_name': 'user_last_name',
                                    'password': 'password12345',
                                    'is_active': True})
        self.assertEqual(request.status_code, status.HTTP_201_CREATED)

    def test_update_user(self):
        request = self.client.put(f'/api/v1/users/{self.user.uuid}/',
                                  {'username': 'new_username',
                                   'first_name': 'new_user_first_name',
                                   'last_name': 'new_user_last_name',
                                   'password': 'pass12345',
                                   'is_active': False})
        self.assertEqual(request.status_code, status.HTTP_200_OK)
        user = User.objects.get(uuid=self.user.uuid)
        self.assertEqual(user.username, 'new_username')
        self.assertEqual(user.first_name, 'new_user_first_name')
        self.assertEqual(user.last_name, 'new_user_last_name')
        self.assertEqual(user.password, 'pass12345')
        self.assertEqual(user.is_active, False)

    def test_patch_user(self):
        request = self.client.patch(f'/api/v1/users/{self.user.uuid}/',
                                    {'username': 'new_username'})
        self.assertEqual(request.status_code, status.HTTP_200_OK)
        user = User.objects.get(uuid=self.user.uuid)
        self.assertEqual(user.username, 'new_username')

    def test_delete_user(self):
        request = self.client.delete(f'/api/v1/users/{self.user.uuid}/')
        self.assertEqual(request.status_code, status.HTTP_204_NO_CONTENT)
        user = User.objects.get(uuid=self.user.uuid)
        self.assertEqual(user.is_active, False)

    def test_get_details_user(self):
        user = mixer.blend(User, username='username_example')
        request = self.client.get(f'/api/v1/users/{user.uuid}/')
        self.assertEqual(request.status_code, status.HTTP_200_OK)
        user = User.objects.get(uuid=user.uuid)
        self.assertEqual(user.username, 'username_example')


class TestGuestUserViewSet(TestCase):

    def setUp(self) -> None:
        self.user = mixer.blend(User)
        self.client = APIClient()

    def test_get_list(self):
        request = self.client.get('/api/v1/users/')
        self.assertEqual(request.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_create_user(self):
        request = self.client.post('/api/v1/users/',
                                   {'username': 'username',
                                    'first_name': 'user_first_name',
                                    'last_name': 'user_last_name',
                                    'password': 'password12345',
                                    'is_active': True})
        self.assertEqual(request.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_put_user(self):
        request = self.client.put(f'/api/v1/users/{self.user.uuid}/',
                                  {'username': 'new_username',
                                   'first_name': 'new_user_first_name',
                                   'last_name': 'new_user_last_name',
                                   'password': 'pass12345',
                                   'is_active': False})
        self.assertEqual(request.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_patch_user(self):
        request = self.client.patch(f'/api/v1/users/{self.user.uuid}/',
                                    {'username': 'new_username'})
        self.assertEqual(request.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_delete_user(self):
        request = self.client.delete(f'/api/v1/users/{self.user.uuid}/')
        self.assertEqual(request.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_get_details_user(self):
        request = self.client.get(f'/api/v1/users/{self.user.uuid}/')
        self.assertEqual(request.status_code, status.HTTP_401_UNAUTHORIZED)

