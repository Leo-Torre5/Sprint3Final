# Generated by Django 4.2.6 on 2023-11-21 21:13

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('user_management', '0005_userprofile_first_name_userprofile_last_name'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='userprofile',
            name='first_name',
        ),
        migrations.RemoveField(
            model_name='userprofile',
            name='last_name',
        ),
    ]
