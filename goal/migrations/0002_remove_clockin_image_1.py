# Generated by Django 3.1.7 on 2021-04-07 14:32

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('goal', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='clockin',
            name='image_1',
        ),
    ]