import uuid
from django.db import models
from django.contrib.auth.models import AbstractUser
import threading


# Create your models here.
class User(AbstractUser):
    username = models.CharField(unique=True, max_length=255)
    password = models.CharField(max_length=255)


class Movie(models.Model):
    title = models.CharField(max_length=255)
    description = models.CharField(max_length=255)
    genres = models.CharField(max_length=255)
    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    collection_uuid = models.CharField(max_length=255)
    username = models.CharField(max_length=255)


class Collection(models.Model):
    title = models.CharField(max_length=255)
    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    description = models.CharField(max_length=255)
    username = models.CharField(max_length=255)

