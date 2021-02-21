from django.shortcuts import render

# Create your views here.
from rest_framework import viewsets, permissions

from kit_people.models import Role, KitPerson, Interaction
from kit_people.serializers import RoleSerializer, KitPersonSerializer, InteractionSerializer


class RoleViewSet(viewsets.ModelViewSet):
    serializer_class = RoleSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_serializer_context(self):
        return {'request': self.request}

    def get_queryset(self):
        if self.request.user.is_anonymous:
            # for documentation only
            return Role.objects.none()
        if self.request.user.is_superuser:
            return Role.objects.all()
        else:
            return Role.objects.filter(user=self.request.user)


class KitPersonViewSet(viewsets.ModelViewSet):
    serializer_class = KitPersonSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_serializer_context(self):
        return {'request': self.request}

    def get_queryset(self):
        if self.request.user.is_anonymous:
            # for documentation only
            return KitPerson.objects.none()
        if self.request.user.is_superuser:
            return KitPerson.objects.all()
        else:
            return KitPerson.objects.filter(user=self.request.user)


class InteractionViewSet(viewsets.ModelViewSet):
    serializer_class = InteractionSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_serializer_context(self):
        return {'request': self.request}

    def get_queryset(self):
        if self.request.user.is_anonymous:
            # for documentation only
            return Interaction.objects.none()
        if self.request.user.is_superuser:
            return Interaction.objects.all()
        else:
            return Interaction.objects.filter(user=self.request.user)
