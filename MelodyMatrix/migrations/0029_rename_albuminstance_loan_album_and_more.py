# Generated by Django 4.2.6 on 2023-12-13 07:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('MelodyMatrix', '0028_rename_album_loan_albuminstance'),
    ]

    operations = [
        migrations.RenameField(
            model_name='loan',
            old_name='AlbumInstance',
            new_name='album',
        ),
        migrations.RemoveField(
            model_name='loancart',
            name='AlbumInstance',
        ),
        migrations.AddField(
            model_name='loancart',
            name='albums',
            field=models.ManyToManyField(to='MelodyMatrix.album'),
        ),
    ]