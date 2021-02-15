from django.db import models
from django.utils.translation import gettext_lazy as _

from users.models import User


class FCMToken(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name=_('user'))
    token = models.CharField(max_length=256, verbose_name=_('FCM token'), unique=True)
