from django.urls import path, include
from rest_framework.routers import SimpleRouter

from kit_people.views import KitPersonViewSet, RoleViewSet, InteractionViewSet

router = SimpleRouter()

router.register(r"roles", RoleViewSet, basename='roles')
router.register(r"kit-people", KitPersonViewSet, basename='kit-people')
router.register(r"interactions", InteractionViewSet, basename='interactions')


urlpatterns = [
    path("", include(router.urls)),
]
