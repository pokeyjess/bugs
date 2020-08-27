from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone



class MyUser(AbstractUser):
    display_name = models.CharField(blank=True, null=True, max_length=80)

class Ticket(models.Model):
    OPTIONS = (('N', 'New'), ('P', 'In Progress'), ('D', 'Done'), ('I', 'Invalid'))
    status = models.CharField(max_length=1, choices=OPTIONS)
    title = models.CharField(max_length=80)
    time_created = models.DateTimeField(default=timezone.now)
    description = models.TextField()
    creator = models.ForeignKey(MyUser, null=True, unique=False, related_name="creator", on_delete=models.SET_NULL)
    owner = models.ForeignKey(MyUser, null=True, unique=False, related_name="owner", on_delete=models.SET_NULL)
    last_owner = models.ForeignKey(MyUser, null=True, unique=False, related_name="last_owner", on_delete=models.SET_NULL)

'''
Some resources used here:
# https://docs.djangoproject.com/en/3.0/ref/models/fields/#choices
# https://stackoverflow.com/questions/38388423/what-does-on-delete-do-on-django-models
# https://books.agiliq.com/projects/django-admin-cookbook/en/latest/current_user.html
# https://stackoverflow.com/questions/9051328/django-assigning-instance-of-a-model-to-a-user  
# https://stackoverflow.com/questions/4670783/make-the-user-in-a-model-default-to-the-current-user
    
'''