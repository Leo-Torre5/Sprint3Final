# Generated by Django 4.2.6 on 2023-11-15 06:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('MelodyMatrix', '0012_alter_userprofile_address_alter_userprofile_city_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='address',
            field=models.CharField(max_length=400, null=True),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='city',
            field=models.CharField(max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='first_name',
            field=models.CharField(max_length=250, null=True),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='last_name',
            field=models.CharField(max_length=250, null=True),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='state',
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='zip',
            field=models.IntegerField(null=True),
        ),
    ]
