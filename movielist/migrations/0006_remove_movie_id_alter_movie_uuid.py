# Generated by Django 4.1.1 on 2022-10-05 07:29

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('movielist', '0005_rename_genre_movie_genres'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='movie',
            name='id',
        ),
        migrations.AlterField(
            model_name='movie',
            name='uuid',
            field=models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False),
        ),
    ]
