# Generated by Django 4.2.6 on 2023-12-12 19:26

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('MelodyMatrix', '0021_alter_genre_image'),
    ]

    operations = [
        migrations.CreateModel(
            name='LoanCart',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('last_name', models.CharField(max_length=255)),
                ('email', models.EmailField(max_length=254)),
                ('address', models.TextField()),
                ('zip_code', models.CharField(max_length=10)),
                ('state', models.CharField(max_length=100)),
                ('albums', models.ManyToManyField(to='MelodyMatrix.album')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
