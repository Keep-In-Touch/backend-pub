from django.db import models
from django.utils.translation import gettext_lazy as _
from multiselectfield import MultiSelectField
# Create your models here.
from users.models import User


# class RoleCategory(models.Model):
#     name = models.CharField(_('name'), max_length=256)
#
#     def __str__(self):
#         return self.name


class Role(models.Model):
    name = models.CharField(_('name'), max_length=256)
    user = models.ForeignKey(User, models.CASCADE, verbose_name=_('user'))

    # category = models.ForeignKey(RoleCategory, models.PROTECT, verbose_name=_('role category'))

    def __str__(self):
        return self.name


# TODO Date without year
class KitPerson(models.Model):
    class Priority(models.TextChoices):
        TOP = 'T', _('Top')
        HIGH = 'H', _('High')
        OTHER = 'O', _('Other')

    role = models.ForeignKey(Role, models.SET_NULL, verbose_name=_('role'), null=True, blank=True)
    name = models.CharField(_('name'), max_length=256)
    # priority = models.CharField(_('priority'), max_length=2, choices=Priority.choices)
    priority = models.IntegerField(verbose_name=_('priority'))
    contact = models.CharField(_('contact'), max_length=256, blank=True, null=True)
    user = models.ForeignKey(User, models.CASCADE, verbose_name=_('user'))
    birthday = models.DateField(_('birthday'), blank=True, null=True)
    chatApp = models.IntegerField(verbose_name=_('chat app'), default=0)

    def __str__(self):
        return self.name


WEEK_DAYS = ((0, 'Monday'),
             (1, 'Tuesday'),
             (2, 'Wednesday'),
             (3, 'Thursday'),
             (4, 'Friday'),
             (5, 'Saturday'),
             (6, 'Sunday'))


class Regularity(models.Model):
    class Meta:
        verbose_name_plural = _('Regularities')

    class NotificationType(models.TextChoices):
        DAILY = 'D', _('Daily')
        WEEKLY = 'W', _('Weekly')
        MONTHLY = 'M', _('Monthly')

    notification_type = models.CharField(_('notification type'), max_length=2, choices=NotificationType.choices)
    week_days = MultiSelectField(choices=WEEK_DAYS, max_choices=7, blank=True, verbose_name=_('week days'), null=True)

    class TimesAWeek(models.IntegerChoices):
        ONE = 1, _('One')
        TWO = 2, _('Two')
        THREE = 3, _('Three')
        FOUR = 4, _('Four')
        FIVE = 5, _('Five')
        SIX = 6, _('Six')
        ONCE_EVERY_TWO_WEEKS = 7, _('Once every 2 weeks')

    times_a_week = models.SmallIntegerField(null=True, blank=True, verbose_name=_('times a week'),
                                            choices=TimesAWeek.choices)

    class MonthTime(models.TextChoices):
        BEGINNING = 'BE', _('Beginning')
        MIDDLE = 'MI', _('Middle')
        END = 'EN', _('End')
        ANY = 'AN', _('Any time')

    time_of_month = models.CharField(_('time of month'), max_length=2, choices=MonthTime.choices, blank=True, null=True)
    reminder = models.TimeField(_('reminder time'), blank=True, null=True)
    kit_person = models.OneToOneField(KitPerson, on_delete=models.CASCADE, verbose_name=_('kit person'), default=None,
                                      null=True, blank=True)


class Interaction(models.Model):
    user = models.ForeignKey(User, models.CASCADE, verbose_name=_('user'))
    kit_person = models.ForeignKey(KitPerson, models.CASCADE, verbose_name=_('kit person'))
    date = models.DateTimeField(_('date'))
    interaction_way = models.CharField(_('interaction way'), max_length=128)

    def __str__(self):
        return self.user.get_full_name() + self.kit_person.name + str(self.date)
