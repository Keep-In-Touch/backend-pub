from rest_framework import serializers
from rest_framework.fields import IntegerField

from learn.models import Section, Lesson, LessonLike


class SectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Section
        fields = '__all__'


class LessonSerializer(serializers.ModelSerializer):
    section = SectionSerializer()
    likes_total = IntegerField()

    class Meta:
        model = Lesson
        fields = '__all__'


class ImageLessonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lesson
        fields = ['image']


class LessonLikeSerializer(serializers.ModelSerializer):

    def create(self, validated_data):
        validated_data['user'] = self.context['request'].user
        return super(LessonLikeSerializer, self).create(validated_data)

    class Meta:
        model = LessonLike
        fields = '__all__'
        extra_kwargs = {"user": {"read_only": True}}
