# Generated by Django 2.0 on 2017-12-17 21:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('slack_bot_app', '0003_message_ts'),
    ]

    operations = [
        migrations.AddField(
            model_name='team',
            name='channel',
            field=models.CharField(default='', max_length=20),
        ),
    ]
