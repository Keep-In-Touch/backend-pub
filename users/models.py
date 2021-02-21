from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _


class User(AbstractUser):
    email = models.EmailField(_('email address'), unique=True, null=True, blank=True)

    def __str__(self):
        return f'{self.id} {self.email} {self.username}'
