# Generated by Django 4.2.6 on 2023-12-13 05:24

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('MelodyMatrix', '0025_alter_loancart_address'),
    ]

    operations = [
        migrations.RenameField(
            model_name='loancart',
            old_name='name',
            new_name='first_name',
        ),
    ]