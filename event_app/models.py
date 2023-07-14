from django.db import models
from django.contrib.auth.models import User


class Event(models.Model):
    creator = models.ForeignKey(User, related_name='events', on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    description = models.TextField()
    date = models.DateTimeField()
    type = models.CharField(max_length=100)
    status = models.CharField(max_length=100)
    capacity = models.IntegerField()
    attendees = models.ManyToManyField(User, related_name='attending', blank=True)
