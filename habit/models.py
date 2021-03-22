import django
from django.db import models
from django.utils.timezone import now
from django.utils.translation import gettext_lazy as _
from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation
from django.contrib.contenttypes.models import ContentType

from users.models import User


class Habit(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name=_('user'))
    name = models.CharField(_('name'), max_length=512)
    description = models.CharField(_('description'), max_length=4096)
    periodicity = models.OneToOneField('Periodicity', on_delete=models.DO_NOTHING,
                                       verbose_name=_('periodicity'))
    goal = models.OneToOneField('Goal', on_delete=models.DO_NOTHING, verbose_name=_('goal'), related_name=_('habit'))
    start_day = models.DateField(default=django.utils.timezone.now, blank=True)
    is_good = models.BooleanField()

    # day_periodicity = models.OneToOneField('DayPeriodicity', on_delete=models.DO_NOTHING,
    #                                        verbose_name=_('periodicity'))
    # week_periodicity = models.OneToOneField('WeekPeriodicity', on_delete=models.DO_NOTHING,
    #                                         verbose_name=_('periodicity'))

    # content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    # object_id = models.PositiveIntegerField()
    # periodicity = GenericForeignKey('content_type', 'object_id')

    def __str__(self):
        return f"%{self.name}. %{self.description}"


class GoalUnit(models.TextChoices):
    COUNT = 'COUNT', _('Count')
    SECONDS = 'SEC', _('Seconds')
    METERS = 'MET', _('Meters')
    PAGES = 'PAGES', _('Pages')


class Goal (models.Model):
    unit = models.CharField(_('unit'), choices=GoalUnit.choices, max_length=16)
    value = models.IntegerField()

    def __str__(self):
        return f"{self.value} {self.unit}/day"


class Progress (models.Model):
    habit = models.ForeignKey('Habit', on_delete=models.CASCADE, verbose_name=_('habit'), related_name=_('progress'))
    date = models.DateField()
    completed = models.IntegerField()
    out_of = models.IntegerField()
    unit = models.CharField(_('unit'), choices=GoalUnit.choices, max_length=16)

    def __str__(self):
        return f"{self.completed} / {self.out_of} {self.unit}"


class Periodicity(models.Model):
    # class Meta:
    #     abstract = True
    pass


class DayOfWeek(models.Model):
    class Day(models.TextChoices):
        MONDAY = 'MON', _('Monday')
        TUESDAY = 'TUE', _('Tuesday')
        WEDNESDAY = 'WED', _('Wednesday')
        THURSDAY = 'THU', _('Thursday')
        FRIDAY = 'FRI', _('Friday')
        SATURDAY = 'SAT', _('Saturday')
        SUNDAY = 'SUN', _('Sunday')

    day = models.CharField(_('day'), choices=Day.choices, max_length=16, unique=True)

    def __str__(self):
        return self.day


class DayPeriodicity(Periodicity):
    times = models.IntegerField()
    days = models.IntegerField()

    def __str__(self):
        return f" {self.times} times in {self.days} days"


class WeekPeriodicity(Periodicity):
    days_of_week = models.ManyToManyField('DayOfWeek', verbose_name='week periodicity', related_name='week_periodicity')

    def __str__(self):
        def days_to_str(days):
            return f"%{days[0]} {days_to_str(days[1:])}" if len(days) > 0 else ""

        return f"{days_to_str(self.days_of_week.all())}"


class Note(models.Model):
    habit = models.ForeignKey(Habit, on_delete=models.CASCADE, verbose_name=_('habit'))
    text = models.TextField()
    datetime = models.DateTimeField(auto_now_add=True)
