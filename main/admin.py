from django.contrib import admin

from main.models import Client, Mailing, Message, MailingLog

admin.site.register(Client)
admin.site.register(Mailing)
admin.site.register(Message)
admin.site.register(MailingLog)
