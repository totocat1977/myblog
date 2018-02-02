from django.db import models
from django.contrib.auth.models import AbstractUser


# Create your models here.
class User(AbstractUser):
    dept = models.CharField(max_length=100, default='IT')
    desc = models.CharField(max_length=100)
    avatar = models.ImageField(upload_to='photos/%Y/%m/%d', default='photos/default.jpg')

