from django.shortcuts import render
from rest_framework import viewsets, mixins, permissions

from firebase_auth.models import FCMToken
from firebase_auth.serializers import FCMTokenSerializer


class FCMTokenViewSet(viewsets.ModelViewSet):
    serializer_class = FCMTokenSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_serializer_context(self):
        return {'request': self.request}

    def get_queryset(self):
        if self.request.user.is_superuser:
            return FCMToken.objects.all()
        else:
            return FCMToken.objects.filter(user=self.request.user)
