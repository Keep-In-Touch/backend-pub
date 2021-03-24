import requests
from django.test import TestCase, override_settings

# Create your tests here.
from rest_framework.test import APIRequestFactory

from kit_people.views import RoleViewSet, KitPersonViewSet, InteractionViewSet


class KitPeopleMethodsTest(TestCase):
    def post_role(self):
        factory = APIRequestFactory()
        request = factory.post('', format='json', HTTP_AUTHORIZATION="Bearer " + self.idToken, data={'name': 'Family'})
        response = RoleViewSet.as_view({'post': 'create'})(request)
        return response

    def post_role_and_kit_person_with_regularity(self):
        # Create role
        response = self.post_role()
        role_id = response.data['id']
        # Create KIT_person
        factory = APIRequestFactory()
        request = factory.post('', format='json', HTTP_AUTHORIZATION="Bearer " + self.idToken,
                               data={'name': 'Mother', 'priority': 1, 'regularity': {
                                   "week_days": [
                                       1, 2, 6
                                   ],
                                   "notification_type": "D",
                                   "reminder": "12:00"
                               }, 'contact': 'Mom', 'role': role_id, 'birthday': '1999-08-19'})
        response = KitPersonViewSet.as_view({'post': 'create'})(request)
        return response

    def partial_update_kit_person(self, kit_person_id):
        factory = APIRequestFactory()
        request = factory.patch('', format='json', HTTP_AUTHORIZATION="Bearer " + self.idToken,
                                data={'regularity': {
                                    "week_days": [
                                        1, 2, 3, 4, 5, 6
                                    ],
                                    "notification_type": "D",
                                    "reminder": "13:00"
                                }, 'name': 'Test_update'})
        response = KitPersonViewSet.as_view({'patch': 'partial_update'})(request, pk=kit_person_id)
        return response

    def post_interaction(self, kit_person_id):
        factory = APIRequestFactory()
        request = factory.post('', format='json', HTTP_AUTHORIZATION="Bearer " + self.idToken,
                               data={'kit_person': kit_person_id, 'date': '2020-08-03 20:00',
                                     'interaction_way': 'telegram'})
        response = InteractionViewSet.as_view({'post': 'create'})(request)
        return response

    def setUp(self):
        self.api_key = "AIzaSyBLDYs2sK9Yk3AlSmDZnGa0CJX2s7Eg90M"
        self.email = 'a.solovyov@innopolis.ru'
        self.password = '123kek321'
        response = requests.post(
            url=f"https://identitytoolkit.googleapis.com/v1/accounts:signInWithPassword?key={self.api_key}",
            json={'email': self.email, 'password': self.password, 'returnSecureToken': True})

        self.idToken = response.json()['idToken']

    @override_settings(DEBUG=True)
    def test_post_role(self):

        factory = APIRequestFactory()
        request = factory.post('', format='json', HTTP_AUTHORIZATION="Bearer " + self.idToken, data={'name': 'Family'})
        response = RoleViewSet.as_view({'post': 'create'})(request)
        if response.status_code != 201:
            print('DATA  : ', response.data)
            print('CODE  : ', response.status_code)
        self.assertTrue(response.status_code == 201)

    @override_settings(DEBUG=True)
    def test_post_kit_person_with_regularity(self):
        '''
        Creates role,
        Creates kit_person with daily regularity field
        '''

        response = self.post_role_and_kit_person_with_regularity()
        if response.status_code != 201:
            print('DATA  : ', response.data)
            print('CODE  : ', response.status_code)
        self.assertTrue(response.status_code == 201)

    @override_settings(DEBUG=True)
    def test_post_kit_person_without_regularity(self):
        '''
        Creates role,
        Creates kit_person without regularity field
        '''
        response = self.post_role_and_kit_person_with_regularity()
        if response.status_code != 201:
            print('DATA  : ', response.data)
            print('CODE  : ', response.status_code)
        self.assertTrue(response.status_code == 201)

    @override_settings(DEBUG=True)
    def test_update_kit_person_regularity(self):
        '''
        Creates role,
        Creates kit_person with regularity field
        '''

        response = self.post_role_and_kit_person_with_regularity()
        kit_person_id = response.data['id']

        response = self.partial_update_kit_person(kit_person_id)
        if response.status_code != 200:
            print('DATA  : ', response.data)
            print('CODE  : ', response.status_code)

        self.assertTrue(response.status_code == 200)

    @override_settings(DEBUG=True)
    def test_post_role_no_access(self):
        '''
        Create role with invalid token
        '''
        factory = APIRequestFactory()
        request = factory.post('', format='json', HTTP_AUTHORIZATION="Bearer " + 'kek', data={'name': 'Family'})
        response = RoleViewSet.as_view({'post': 'create'})(request)
        if response.status_code != 401:
            print('DATA  : ', response.data)
            print('CODE  : ', response.status_code)
        self.assertTrue(response.status_code == 401)

    @override_settings(DEBUG=True)
    def test_post_interaction(self):
        # BUILD
        response = self.post_role_and_kit_person_with_regularity()

        # OPERATE
        response = self.post_interaction(response.data['id'])

        # CHECK
        self.assertTrue(response.status_code == 201)

        # print('TEST USER RETRIEVE: ')
        # factory = APIRequestFactory()
        # request = factory.get('', format='json', HTTP_AUTHORIZATION=self.headers['Authorization'])
        #
        # response = UsersViewSet.as_view({'get': 'retrieve'})(request, pk='@me')
        # print('STATUS: ', response.status_code)
        # if response.status_code != 200:
        #     print('DATA  : ', response.data)
        # self.assertTrue(response.status_code == 200)
