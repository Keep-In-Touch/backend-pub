import requests
from django.test import TestCase, override_settings

# Create your tests here.
from rest_framework.test import APIRequestFactory

from kit_people.views import RoleViewSet, KitPersonViewSet, InteractionViewSet


class KitPeopleMethodsTest(TestCase):

    def setUp(self):
        self.api_key = "AIzaSyBLDYs2sK9Yk3AlSmDZnGa0CJX2s7Eg90M"
        self.email = 'a.solovyov@innopolis.ru'
        self.password = '123kek321'
        response = requests.post(
            url=f"https://identitytoolkit.googleapis.com/v1/accounts:signInWithPassword?key={self.api_key}",
            json={'email': self.email, 'password': self.password, 'returnSecureToken': True})

        self.idToken = response.json()['idToken']
