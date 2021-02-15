from django.urls import path, include
from rest_framework.routers import SimpleRouter

from kit_people.views import KitPersonViewSet
from learn.views import SectionViewSet, LessonViewSet

router = SimpleRouter()

router.register(r"sections", SectionViewSet)
router.register(r"lessons", LessonViewSet, 'lessons')


urlpatterns = [
    path("", include(router.urls)),
]
