# Generated by Django 4.0.1 on 2022-01-10 19:43

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Accounts', '0005_request_notification'),
    ]

    operations = [
        migrations.AlterField(
            model_name='request',
            name='notification',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, to='Accounts.notification'),
        ),
    ]
