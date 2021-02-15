from rest_framework import serializers

from habit.models import *


class HabitSerializer(serializers.ModelSerializer):
    class Meta:
        model = Habit
        fields = ['id', 'user', 'name', 'description', 'periodicity', 'goal', 'is_good', 'start_day']
        read_only_fields = ['start_day']
        # fields = '__all__'


class PeriodicitySerializer(serializers.ModelSerializer):
    class Meta:
        model = Periodicity
        fields = '__all__'


class DayPeriodicitySerializer(PeriodicitySerializer):
    class Meta:
        model = DayPeriodicity
        fields = '__all__'


class WeekPeriodicitySerializer(PeriodicitySerializer):
    class Meta:
        model = WeekPeriodicity
        fields = ['id', 'days_of_week']


class DayOfWeekSerializer(serializers.ModelSerializer):
    class Meta:
        model = DayOfWeek
        fields = '__all__'


class GoalSerializer(serializers.ModelSerializer):
    class Meta:
        model = Goal
        fields = ['id', 'unit', 'value', 'habit']
        read_only_fields = ['habit']


class ProgressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Progress
        fields = '__all__'


class NoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Note
        fields = '__all__'
