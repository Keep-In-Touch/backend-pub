from django.utils import timezone
from firebase_admin import auth
from rest_framework import authentication

from firebase_auth.exceptions import NoAuthToken, InvalidAuthToken, FirebaseError
from users.models import User


class FirebaseAuthentication(authentication.BaseAuthentication):

    def authenticate_header(self, request):
        return 'Bearer'

    def authenticate(self, request):
        auth_header = request.META.get("HTTP_AUTHORIZATION")

        if not auth_header:
            return None
            # raise NoAuthToken("No auth token provided")

        id_token = auth_header.split(" ").pop()
        decoded_token = None
        try:
            decoded_token = auth.verify_id_token(id_token)
        except Exception:
            raise InvalidAuthToken("Invalid auth token")

        if not id_token or not decoded_token:
            return None

        try:
            uid = decoded_token.get("uid")
        except Exception:
            raise FirebaseError()
        firebase_user = auth.get_user(uid)
        email = firebase_user.email
        if email is not None:
            user, created = User.objects.get_or_create(username=uid, email=email)
        else:
            user, created = User.objects.get_or_create(username=uid)

        return (user, None)