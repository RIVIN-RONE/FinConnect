# Generated by Django 5.0.6 on 2024-10-08 09:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('finance_app', '0006_request_notes_alter_vendor_vendor_account_number'),
    ]

    operations = [
        migrations.AddField(
            model_name='request',
            name='invoice',
            field=models.FileField(blank=True, null=True, upload_to='attachments/'),
        ),
    ]
