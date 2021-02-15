from django.urls import path, include
from rest_framework.routers import SimpleRouter

from habit.views import HabitViewSet, DayPeriodicityViewSet, WeekPeriodicityViewSet, \
    PeriodicityViewSet, DayOfWeekViewSet, GoalViewSet, ProgressViewSet, NoteViewSet

router = SimpleRouter()

router.register(r"habits", HabitViewSet, basename='habits')
router.register(r"day-periodicities", DayPeriodicityViewSet, basename='day-periodicities')
router.register(r"week-periodicities", WeekPeriodicityViewSet, basename='week-periodicities')
router.register(r"periodicities", PeriodicityViewSet, basename='periodicities')
router.register(r"days-of-week", DayOfWeekViewSet, basename='days-of-week')
router.register(r"goals", GoalViewSet, basename='goals')
router.register(r"progresses", ProgressViewSet, basename='progresses')
router.register(r"notes", NoteViewSet, basename='notes')

urlpatterns = [
    path("", include(router.urls)),
]