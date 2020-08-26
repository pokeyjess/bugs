from django.contrib.auth.models import AbstractUser
from django.db import models

class MyUser(AbstractUser):
    display_name = models.CharField(blank=True, null=True, max_length=80)
