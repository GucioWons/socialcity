# Generated by Django 4.0.1 on 2022-01-07 18:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Posts', '0003_alter_post_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='photo',
            field=models.ImageField(null=True, upload_to=''),
        ),
    ]