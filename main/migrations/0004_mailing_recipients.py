# Generated by Django 4.2.5 on 2023-10-03 06:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0003_mailing_end_time'),
    ]

    operations = [
        migrations.AddField(
            model_name='mailing',
            name='recipients',
            field=models.ManyToManyField(to='main.client'),
        ),
    ]