# Generated by Django 4.2.6 on 2023-11-30 02:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user_management', '0007_delete_customuser'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='image',
            field=models.ImageField(default='media/default_image/Defaut.png', upload_to='profile_pics'),
        ),
    ]
