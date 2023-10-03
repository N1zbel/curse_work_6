from django.conf import settings
from django.db import models

NULLABLE = {'blank': True, 'null': True}


class Client(models.Model):
    email = models.EmailField(unique=True)
    full_name = models.CharField(max_length=150, verbose_name='Имя')
    comment = models.TextField(**NULLABLE, verbose_name='комментарий')
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, **NULLABLE)
    is_active = models.BooleanField(default=True, verbose_name='Активный')

    def __str__(self):
        return self.full_name


class Mailing(models.Model):
    FREQUENCY_CHOICES = [
        ('daily', 'Daily'),
        ('weekly', 'Weekly'),
        ('monthly', 'Monthly'),
    ]
    STATUS_CHOICES = [
        ('created', 'Created'),
        ('running', 'Running'),
        ('completed', 'Completed'),
    ]
    time_to_send = models.DateTimeField()
    end_time = models.DateTimeField(**NULLABLE)
    frequency = models.CharField(max_length=20, choices=FREQUENCY_CHOICES)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES)
    recipients = models.ManyToManyField(Client)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, **NULLABLE)


class Message(models.Model):
    mailing = models.ForeignKey(Mailing, on_delete=models.CASCADE)
    subject = models.CharField(max_length=255)
    body = models.TextField()
    sent_at = models.DateTimeField(auto_now_add=True)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, **NULLABLE)


class MailingLog(models.Model):
    message = models.ForeignKey(Message, on_delete=models.CASCADE)
    attempt_time = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20)
    response = models.TextField(blank=True)
