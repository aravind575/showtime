# Generated by Django 4.1.1 on 2022-10-04 23:48

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('movielist', '0004_movie_username'),
    ]

    operations = [
        migrations.RenameField(
            model_name='movie',
            old_name='genre',
            new_name='genres',
        ),
    ]