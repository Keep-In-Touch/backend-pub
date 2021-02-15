from django.urls import path, include
from rest_framework.routers import SimpleRouter

from firebase_auth.views import FCMTokenViewSet

router = SimpleRouter()

router.register(r"fcm-token", FCMTokenViewSet, basename='roles')



urlpatterns = [
    path("", include(router.urls)),
]
