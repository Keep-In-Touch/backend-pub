import requests
from django.test import TestCase, override_settings

# Create your tests here.
from rest_framework.test import APIRequestFactory

from firebase_auth.views import FCMTokenViewSet


class FCMMethodsTest(TestCase):

    def setUp(self):
        self.api_key = "AIzaSyBLDYs2sK9Yk3AlSmDZnGa0CJX2s7Eg90M"
        self.email = 'a.solovyov@innopolis.ru'
        self.password = '123kek321'
        response = requests.post(
            url=f"https://identitytoolkit.googleapis.com/v1/accounts:signInWithPassword?key={self.api_key}",
            json={'email': self.email, 'password': self.password, 'returnSecureToken': True})

        self.idToken = response.json()['idToken']

    @override_settings(DEBUG=True)
    def test_post_fcm_token(self):

        factory = APIRequestFactory()
        request = factory.post('', format='json', HTTP_AUTHORIZATION="Bearer " + self.idToken,
                               data={'token': 'TokenExample123'})
        response = FCMTokenViewSet.as_view({'post': 'create'})(request)
        if response.status_code != 201:
            print('DATA  : ', response.data)
            print('CODE  : ', response.status_code)
        self.assertTrue(response.status_code == 201)

    @override_settings(DEBUG=True)
    def test_post_fcm_token_not_authenticated(self):

        factory = APIRequestFactory()
        request = factory.post('', format='json', HTTP_AUTHORIZATION="Bearer " + "kek",
                               data={'token': 'TokenExample123'})
        response = FCMTokenViewSet.as_view({'post': 'create'})(request)
        if response.status_code != 401:
            print('DATA  : ', response.data)
            print('CODE  : ', response.status_code)
        self.assertTrue(response.status_code == 401)
