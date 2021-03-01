from django.db.models import Sum, Count
from django.http import Http404
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from rest_framework import permissions, viewsets, mixins, status

from rest_framework.authentication import SessionAuthentication
from rest_framework.decorators import action
from rest_framework.parsers import MultiPartParser
from rest_framework.permissions import SAFE_METHODS
from rest_framework.response import Response

from firebase_auth.authentication import FirebaseAuthentication
from learn.models import Section, Lesson, LessonLike
from learn.serializers import SectionSerializer, LessonSerializer, ImageLessonSerializer, LessonLikeSerializer

import logging

logger = logging.getLogger('backend.custom')


class ReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.method in SAFE_METHODS


class SectionViewSet(viewsets.ModelViewSet):
    queryset = Section.objects.all()
    serializer_class = SectionSerializer
    permission_classes = [permissions.IsAdminUser | ReadOnly]


class LessonViewSet(viewsets.ModelViewSet):
    serializer_class = LessonSerializer
    permission_classes = [permissions.IsAdminUser | ReadOnly]
    authentication_classes = [FirebaseAuthentication, SessionAuthentication]

    def get_queryset(self):
        if self.action in ('list', 'retrieve'):
            return Lesson.objects.all().select_related('section').prefetch_related('likes').annotate(
                likes_total=Count('likes'))
        else:
            return Lesson.objects.all()

    @method_decorator(cache_page(60))
    def list(self, request, *args, **kwargs):
        return super(LessonViewSet, self).list(request, *args, **kwargs)

    @action(methods=['PUT'], detail=True, parser_classes=[MultiPartParser], serializer_class=ImageLessonSerializer)
    def image(self, request, *args, **kwargs):
        return super(LessonViewSet, self).update(request, request, *args, **kwargs)

    @action(methods=['get'], detail=True, permission_classes=[permissions.IsAuthenticated], url_path='like')
    def get_like(self, request, *args, **kwargs):
        lesson = self.get_object()
        if LessonLike.objects.filter(lesson=lesson, user=self.request.user).exists():
            like = LessonLike.objects.get(lesson=lesson, user=self.request.user)
            serializer = LessonLikeSerializer(like)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(status=status.HTTP_404_NOT_FOUND, data={"detail": "Like doesn't exist"})

    @action(methods=['post'], detail=True, permission_classes=[permissions.IsAuthenticated], url_path='set-like')
    def set_like(self, request, pk=None):
        try:
            lesson = self.get_object()
            if not LessonLike.objects.filter(lesson=lesson, user=self.request.user).exists():
                lesson_like = LessonLike.objects.create(lesson=lesson, user=self.request.user)
                serializer = LessonLikeSerializer(lesson_like)
                lesson_like.save()
            else:
                return Response(status=status.HTTP_400_BAD_REQUEST, data={"detail": "Like already exist"})
        except Http404:
            return Response(status=status.HTTP_404_NOT_FOUND)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @action(methods=['delete'], detail=True, permission_classes=[permissions.IsAuthenticated], url_path='delete-like')
    def delete_like(self, request, pk=None):
        try:
            lesson = self.get_object()
            if LessonLike.objects.filter(lesson=lesson, user=self.request.user).exists():
                like = LessonLike.objects.get(lesson=lesson, user=self.request.user)
                serializer = LessonLikeSerializer(like)
                like.delete()
            else:
                return Response(status=status.HTTP_404_NOT_FOUND, data={"detail": "Like doesn't exist"})
        except Http404:
            return Response(status=status.HTTP_404_NOT_FOUND)
        return Response(serializer.data, status=status.HTTP_204_NO_CONTENT)

    @action(methods=['get'], detail=False, permission_classes=[permissions.IsAuthenticated], url_path='liked-lessons')
    def liked_lessons(self, request, *args, **kwargs):
        liked_lessons = Lesson.objects.filter(likes__user=self.request.user).select_related('section').prefetch_related(
            'likes').annotate(likes_total=Count('likes'))
        serializer = LessonSerializer(liked_lessons, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
