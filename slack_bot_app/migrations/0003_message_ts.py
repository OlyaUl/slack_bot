# Generated by Django 2.0 on 2017-12-17 20:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('slack_bot_app', '0002_message_thread'),
    ]

    operations = [
        migrations.AddField(
            model_name='message',
            name='ts',
            field=models.TextField(default='1'),
        ),
    ]
