# Generated by Django 4.2.6 on 2023-10-25 18:16

from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Album',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200, null=True)),
                ('summary', models.TextField(help_text='Enter a brief summary of the album', max_length=2000, null=True)),
                ('duration', models.DurationField(help_text='Enter the duration of the album')),
                ('tracks', models.IntegerField(help_text='Select the number of tracks')),
            ],
        ),
        migrations.CreateModel(
            name='Genre',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(help_text='Enter an album genre (e.g.Country)', max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='Artist',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('artist_name', models.CharField(max_length=100)),
                ('date_of_birth', models.DateField(blank=True, null=True)),
                ('date_of_death', models.DateField(blank=True, null=True, verbose_name='Died')),
                ('summary', models.TextField(help_text='Enter a brief background of the artist', max_length=2000, null=True)),
                ('genre', models.ManyToManyField(help_text='Select a genre for this artist', to='MelodyMatrix.genre')),
            ],
            options={
                'ordering': ['artist_name'],
            },
        ),
        migrations.CreateModel(
            name='AlbumInstance',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, help_text='Unique ID for this particular album across whole library', primary_key=True, serialize=False)),
                ('format', models.CharField(max_length=200)),
                ('due_back', models.DateField(blank=True, null=True)),
                ('return_date', models.DateField(blank=True, null=True)),
                ('status', models.CharField(blank=True, choices=[('a', 'Available'), ('o', 'On loan'), ('r', 'Reserved')], default='a', help_text='Album availability', max_length=1)),
                ('album', models.ForeignKey(null=True, on_delete=django.db.models.deletion.RESTRICT, to='MelodyMatrix.album')),
            ],
            options={
                'ordering': ['due_back'],
            },
        ),
        migrations.AddField(
            model_name='album',
            name='artist',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.RESTRICT, to='MelodyMatrix.artist'),
        ),
        migrations.AddField(
            model_name='album',
            name='genre',
            field=models.ManyToManyField(help_text='Select a genre for this album', to='MelodyMatrix.genre'),
        ),
    ]
