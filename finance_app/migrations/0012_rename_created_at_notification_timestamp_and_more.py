# Generated by Django 5.1.2 on 2024-10-18 06:45

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('finance_app', '0011_notification_request'),
    ]

    operations = [
        migrations.RenameField(
            model_name='notification',
            old_name='created_at',
            new_name='timestamp',
        ),
        migrations.RemoveField(
            model_name='notification',
            name='request',
        ),
    ]
