from django.shortcuts import render

from rest_framework import viewsets, permissions

from habit.serializers import *


class HabitViewSet(viewsets.ModelViewSet):
    serializer_class = HabitSerializer
    # permission_classes = [permissions.IsAuthenticated]
    queryset = Habit.objects.all()

    # def get_queryset(self):
    #     if self.request.user.is_superuser:
    #         return self.queryset
    #     else:
    #         return self.queryset.objects.filter(user=self.request.user)


class PeriodicityViewSet(viewsets.ModelViewSet):
    serializer_class = PeriodicitySerializer
    # permission_classes = [permissions.IsAuthenticated]
    queryset = Periodicity.objects.all()
    # queryset = DayPeriodicity.objects.all().union(
    #     WeekPeriodicity.objects.all(),
    #     MonthPeriodicity.objects.all()
    # )

    # def get_queryset(self):
    #     if self.request.user.is_superuser:
    #         return self.queryset
    #     else:
    #         return self.queryset.objects.filter(user=self.request.user)


class DayPeriodicityViewSet(viewsets.ModelViewSet):
    serializer_class = DayPeriodicitySerializer
    # permission_classes = [permissions.IsAuthenticated]
    queryset = DayPeriodicity.objects.all()

    # def get_queryset(self):
    #     if self.request.user.is_superuser:
    #         return self.queryset
    #     else:
    #         return self.queryset.objects.filter(user=self.request.user)


class WeekPeriodicityViewSet(viewsets.ModelViewSet):
    serializer_class = WeekPeriodicitySerializer
    # permission_classes = [permissions.IsAuthenticated]
    queryset = WeekPeriodicity.objects.all()

    # def get_queryset(self):
    #     if self.request.user.is_superuser:
    #         return self.queryset
    #     else:
    #         return self.queryset.objects.filter(user=self.request.user)


class DayOfWeekViewSet(viewsets.ModelViewSet):
    serializer_class = DayOfWeekSerializer
    # permission_classes = [permissions.IsAuthenticated]
    queryset = DayOfWeek.objects.all()

    # def get_queryset(self):
    #     if self.request.user.is_superuser:
    #         return self.queryset
    #     else:
    #         return self.queryset.objects.filter(user=self.request.user)


class GoalViewSet(viewsets.ModelViewSet):
    serializer_class = GoalSerializer
    # permission_classes = [permissions.IsAuthenticated]
    queryset = Goal.objects.all()

    # def get_queryset(self):
    #     if self.request.user.is_superuser:
    #         return self.queryset
    #     else:
    #         return self.queryset.objects.filter(user=self.request.user)


class ProgressViewSet(viewsets.ModelViewSet):
    serializer_class = ProgressSerializer
    # permission_classes = [permissions.IsAuthenticated]
    queryset = Progress.objects.all()

    # def get_queryset(self):
    #     if self.request.user.is_superuser:
    #         return self.queryset
    #     else:
    #         return self.queryset.objects.filter(user=self.request.user)


class NoteViewSet(viewsets.ModelViewSet):
    serializer_class = NoteSerializer
    # permission_classes = [permissions.IsAuthenticated]
    queryset = Note.objects.all()

    # def get_queryset(self):
    #     if self.request.user.is_superuser:
    #         return self.queryset
    #     else:
    #         return self.queryset.objects.filter(user=self.request.user)
