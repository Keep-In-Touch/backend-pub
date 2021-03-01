from random import randrange

from celery import shared_task
import datetime

from pyfcm import FCMNotification

from backend.settings import FCM_API_KEY
from firebase_auth.models import FCMToken
from kit_people.models import Regularity, KitPerson, Interaction

import logging

logger = logging.getLogger("backend.custom")

push_service = FCMNotification(api_key=FCM_API_KEY)


def send_notification(regularity_id):
    regularity = Regularity.objects.get(id=regularity_id)
    fcm_tokens = FCMToken.objects.filter(user=regularity.kit_person.user_id)
    for token in fcm_tokens:
        logger.info(
            push_service.notify_single_device(
                token.token,
                f"Remember to contact {regularity.kit_person.name}",
                "Stay in touch",
                badge=1,
            )
        )


def send_in_reminder_time_or_by_default(regularity_id, reminder_hour, reminder_minute):
    if reminder_hour is not None:
        if reminder_time_is_now(reminder_hour, reminder_minute):
            send_notification(regularity_id)
    else:
        if datetime.datetime.now().hour == 17 and datetime.datetime.now().minute == 0:
            send_notification(regularity_id)


def reminder_time_is_now(hour, minutes):
    if (
            datetime.datetime.now().hour == hour
            and datetime.datetime.now().minute == minutes
    ):
        return True
    return False


def reminder_time_around_10_minutes(reminder):
    if datetime.datetime.now().hour - reminder.hour == 1:
        if datetime.datetime.now().minute == 0 and reminder.minute >= 50:
            return True
    if datetime.datetime.now().hour - reminder.hour == 0:
        if datetime.datetime.now().minute - reminder.minute <= 10:
            return True
    if datetime.datetime.now().hour == 0 and reminder.hour == 23:
        if datetime.datetime.now().minute == 0 and reminder.minute >= 50:
            return True
    return False


def push_notification_daily():
    for regularity in Regularity.objects.filter(notification_type="D"):
        if str(datetime.datetime.now().weekday()) in regularity.week_days:
            send_in_reminder_time_or_by_default(
                regularity.id, regularity.reminder.hour, regularity.reminder.minute
            )


def push_notification_weekly():
    for regularity in Regularity.objects.filter(notification_type="W"):
        if datetime.datetime.now().weekday() == 0:
            if 4 <= regularity.times_a_week <= 6:
                send_in_reminder_time_or_by_default(
                    regularity.id, regularity.reminder.hour, regularity.reminder.minute
                )
        elif datetime.datetime.now().weekday() == 1:
            if regularity.times_a_week == 3 or regularity.times_a_week == 6:
                send_in_reminder_time_or_by_default(
                    regularity.id, regularity.reminder.hour, regularity.reminder.minute
                )
        elif datetime.datetime.now().weekday() == 2:
            if (
                    regularity.times_a_week == 2
                    or regularity.times_a_week == 4
                    or regularity.times_a_week == 5
            ):
                send_in_reminder_time_or_by_default(
                    regularity.id, regularity.reminder.hour, regularity.reminder.minute
                )
        elif datetime.datetime.now().weekday() == 3:
            if regularity.times_a_week == 3 or regularity.times_a_week == 6:
                send_in_reminder_time_or_by_default(
                    regularity.id, regularity.reminder.hour, regularity.reminder.minute
                )
        elif datetime.datetime.now().weekday() == 4:
            if 4 <= regularity.times_a_week <= 6:
                send_in_reminder_time_or_by_default(
                    regularity.id, regularity.reminder.hour, regularity.reminder.minute
                )
        elif datetime.datetime.now().weekday() == 5:
            if 1 <= regularity.times_a_week <= 2 or 5 <= regularity.times_a_week <= 6:
                send_in_reminder_time_or_by_default(
                    regularity.id, regularity.reminder.hour, regularity.reminder.minute
                )
        elif datetime.datetime.now().weekday() == 6:
            if 3 <= regularity.times_a_week <= 6:
                send_in_reminder_time_or_by_default(
                    regularity.id, regularity.reminder.hour, regularity.reminder.minute
                )


def push_notification_monthly():
    for regularity in Regularity.objects.filter(notification_type="W", times_a_week=7):
        if datetime.datetime.now().day == 1 or datetime.datetime.now().day == 15:
            send_in_reminder_time_or_by_default(
                regularity.id, regularity.reminder.hour, regularity.reminder.minute
            )
    for regularity in Regularity.objects.filter(notification_type="M"):
        if datetime.datetime.now().day == 1 and regularity.time_of_month == "BE":
            send_in_reminder_time_or_by_default(
                regularity.id, regularity.reminder.hour, regularity.reminder.minute
            )
        if datetime.datetime.now().day == 15 and regularity.time_of_month == "MI":
            send_in_reminder_time_or_by_default(
                regularity.id, regularity.reminder.hour, regularity.reminder.minute
            )
        if datetime.datetime.now().day == 28 and regularity.time_of_month == "EN":
            send_in_reminder_time_or_by_default(
                regularity.id, regularity.reminder.hour, regularity.reminder.minute
            )
        if datetime.datetime.now().day == 15 and regularity.time_of_month == "AN":
            send_in_reminder_time_or_by_default(
                regularity.id, regularity.reminder.hour, regularity.reminder.minute
            )


def new_send_in_reminder_time_or_by_default(
        regularity_id, reminder_hour, reminder_minute, user_id, user_reminders
):
    if reminder_hour is not None:
        if reminder_time_is_now(reminder_hour, reminder_minute):
            if user_reminders.get(user_id) is None:
                user_reminders[user_id] = [
                    regularity_id,
                ]
            else:
                user_reminders[user_id].append(regularity_id)
    elif datetime.datetime.now().hour == 17 and datetime.datetime.now().minute == 0:
        if user_reminders.get(user_id) is None:
            user_reminders[user_id] = [
                regularity_id,
            ]
        else:
            user_reminders[user_id].append(regularity_id)


def new_push_notification_daily():
    user_reminders = {}
    for regularity in Regularity.objects.filter(notification_type="D"):
        if str(datetime.datetime.now().weekday()) in regularity.week_days:
            new_send_in_reminder_time_or_by_default(
                regularity.id,
                regularity.reminder.hour,
                regularity.reminder.minute,
                regularity.kit_person.user_id,
                user_reminders,
            )
    return user_reminders


def new_push_notification_weekly():
    user_reminders = {}
    for regularity in Regularity.objects.filter(notification_type="W"):
        if check_time_for_weekly(regularity.id):
            new_send_in_reminder_time_or_by_default(
                regularity.id,
                regularity.reminder.hour,
                regularity.reminder.minute,
                regularity.kit_person.user_id,
                user_reminders,
            )
    return user_reminders


def check_time_for_weekly(regularity_id):
    regularity = Regularity.objects.get(id=regularity_id)
    if datetime.datetime.now().weekday() == 0:
        if 4 <= regularity.times_a_week <= 6:
            return True
    elif datetime.datetime.now().weekday() == 1:
        if regularity.times_a_week == 3 or regularity.times_a_week == 6:
            return True
    elif datetime.datetime.now().weekday() == 2:
        if (
                regularity.times_a_week == 2
                or regularity.times_a_week == 4
                or regularity.times_a_week == 5
        ):
            return True
    elif datetime.datetime.now().weekday() == 3:
        if regularity.times_a_week == 3 or regularity.times_a_week == 6:
            return True
    elif datetime.datetime.now().weekday() == 4:
        if 4 <= regularity.times_a_week <= 6:
            return True
    elif datetime.datetime.now().weekday() == 5:
        if 1 <= regularity.times_a_week <= 2 or 5 <= regularity.times_a_week <= 6:
            return True
    elif datetime.datetime.now().weekday() == 6:
        if 3 <= regularity.times_a_week <= 6:
            return True
    return False


def new_push_notification_monthly():
    user_reminders = {}
    for regularity in Regularity.objects.filter(notification_type="W", times_a_week=7):
        if datetime.datetime.now().day == 1 or datetime.datetime.now().day == 15:
            new_send_in_reminder_time_or_by_default(
                regularity.id,
                regularity.reminder.hour,
                regularity.reminder.minute,
                regularity.kit_person.user_id,
                user_reminders,
            )
    for regularity in Regularity.objects.filter(notification_type="M"):
        if check_time_for_monthly(regularity.id):
            new_send_in_reminder_time_or_by_default(
                regularity.id,
                regularity.reminder.hour,
                regularity.reminder.minute,
                regularity.kit_person.user_id,
                user_reminders,
            )
    return user_reminders


def check_time_for_monthly(regularity_id):
    regularity = Regularity.objects.get(id=regularity_id)
    if datetime.datetime.now().day == 1 and regularity.time_of_month == "BE":
        return True
    if datetime.datetime.now().day == 15 and regularity.time_of_month == "MI":
        return True
    if datetime.datetime.now().day == 28 and regularity.time_of_month == "EN":
        return True
    if datetime.datetime.now().day == 15 and regularity.time_of_month == "AN":
        return True
    return False


def send_notifications_to_users_from_dict(user_reminders):
    for user_id in user_reminders.keys():
        kit_persons = []
        for regularity_id in user_reminders[user_id]:
            kit_person = KitPerson.objects.get(regularity=regularity_id)
            if not is_contacted_today(kit_person.id):
                kit_persons.append(KitPerson.objects.get(regularity=regularity_id))
        others = ""
        if len(kit_persons) > 3:
            kit_persons = kit_persons[0:3]
            others = " and the others"
        kp_names = ", ".join([str(kp.name) for kp in kit_persons])
        fcm_tokens = FCMToken.objects.filter(user=user_id)
        message = create_message(kp_names)
        for token in fcm_tokens:
            logger.info(
                push_service.notify_single_device(
                    token.token,
                    f"{message}{others}",
                    "Stay in touch",
                    badge=1,
                )
            )


def create_message(kp_names):
    messages = ["Remember to contact", "Reach out to", "Stay in touch with", "Keep your connections warm. Contact"]
    rand_message_index = randrange(len(messages))
    result_message = f"{messages[rand_message_index]} {kp_names}"
    return result_message


def is_contacted_today(kit_person_id):
    if Interaction.objects.filter(kit_person=kit_person_id, date=datetime.datetime.now().date()).exists():
        return True
    return False


def mergeDict(dict1, dict2):
    """ Merge dictionaries and concat lists of common keys in list"""
    dict3 = {**dict1, **dict2}
    for key, value in dict3.items():
        if key in dict1 and key in dict2:
            dict3[key] = value + dict1[key]
    return dict3


@shared_task
def push_notifications():
    dict_daily = new_push_notification_daily()
    dict_weekly = new_push_notification_weekly()
    dict_monthly = new_push_notification_monthly()
    result_dict_user_reminders = mergeDict(dict_daily, dict_weekly)
    result_dict_user_reminders = mergeDict(result_dict_user_reminders, dict_monthly)
    send_notifications_to_users_from_dict(result_dict_user_reminders)
