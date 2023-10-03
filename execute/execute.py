import datetime

from django.conf import settings
from django.core.mail import send_mail
from datetime import timedelta, datetime
from main.models import Mailing, MailingLog


def send_mailings():
    current_datetime = datetime.now()
    for mailing in Mailing.objects.filter(status='created'):
        is_mailing = False
        emails = [client.email for client in mailing.recipients.all()]
        month_start = mailing.time_to_send.month
        day_start = mailing.time_to_send.day
        hour_start = mailing.time_to_send.hour
        minute_start = mailing.time_to_send.minute
        attempt_status = 'Выполнено'
        server_response = 'Успешно доставлена'
        messages = mailing.message_set.all()

        if mailing.frequency == 'daily' and day_start == current_datetime.day \
                and current_datetime.hour == hour_start and current_datetime.minute == minute_start:
            mailing.time_to_send = mailing.time_to_send + timedelta(days=1)
            is_mailing = True

        elif mailing.frequency == 'weekly' and day_start == current_datetime.day \
                and current_datetime.hour == hour_start and current_datetime.minute == minute_start:
            mailing.time_to_send = mailing.time_to_send + timedelta(days=7)
            is_mailing = True

        elif mailing.frequency == 'monthly' and month_start == current_datetime.month \
                and day_start == current_datetime.day \
                and current_datetime.hour == hour_start and current_datetime.minute == minute_start:
            mailing.time_to_send = mailing.time_to_send + timedelta(days=30)
            is_mailing = True

        if is_mailing:
            mailing.save()
            for message in messages:
                try:

                    send_mail(
                        subject=message.subject,
                        message=message.body,
                        from_email=settings.EMAIL_HOST_USER,
                        recipient_list=emails
                    )

                except Exception as e:

                    attempt_status = 'error'
                    server_response = str(e)

                finally:
                    pass
                    MailingLog.objects.create(message=message,
                                              status=attempt_status,
                                              response=server_response)
