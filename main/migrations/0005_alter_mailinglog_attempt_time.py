# Generated by Django 4.2.5 on 2023-10-03 07:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0004_mailing_recipients'),
    ]

    operations = [
        migrations.AlterField(
            model_name='mailinglog',
            name='attempt_time',
            field=models.DateTimeField(auto_now_add=True),
        ),
    ]
