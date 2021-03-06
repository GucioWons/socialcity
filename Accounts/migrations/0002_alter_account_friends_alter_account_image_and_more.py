# Generated by Django 4.0.1 on 2022-01-13 01:46

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('Accounts', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='account',
            name='friends',
            field=models.ManyToManyField(null=True, related_name='user_friends', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='account',
            name='image',
            field=models.ImageField(default='default.png', null=True, upload_to=''),
        ),
        migrations.AlterField(
            model_name='account',
            name='school',
            field=models.CharField(max_length=500, null=True),
        ),
        migrations.AlterField(
            model_name='account',
            name='town',
            field=models.CharField(max_length=80, null=True),
        ),
    ]
