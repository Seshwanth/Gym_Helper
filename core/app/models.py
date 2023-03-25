from django.db import models

# Create your models here.
class Gym(models.Model):

    name = models.CharField(max_length=255)
    description = models.TextField(default='')
    address = models.CharField(max_length=255)
    phone = models.PositiveIntegerField()
    last_update = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)

class Profile(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    phone = models.PositiveBigIntegerField()
    email = models.EmailField()
    last_update = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)
    default = 'T'
    OPTIONS = [
        (default,'trial'),
        ('R','regular')
    ]
    status = models.CharField(max_length=1, choices = OPTIONS, default=default)

class Workout(models.Model):
    time = models.DateTimeField()
    activity = models.ForeignKey('Activity',on_delete=models.SET_NULL, null=True)
    gym = models.ForeignKey('Gym', on_delete=models.CASCADE)
    profile = models.ManyToManyField('Profile')

class Activity(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(default='')