# Generated by Django 4.0.1 on 2022-01-10 21:22

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('Accounts', '0009_alter_notification_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='notification',
            name='date',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
    ]