from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    USER_TYPES = (
        ("TEACHER", "Teacher"),
        ("STUDENT", "Student"),
    )
    GENDER_CHOICES = (
        ('M', 'Male'),
        ('F', 'Female'),
    )
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)
    user_type = models.CharField(max_length=100, choices=USER_TYPES)
    date_of_birth = models.DateField()
    REQUIRED_FIELDS = ['date_of_birth']

class Course(models.Model):
    STATUS = (
        (0, 'Inactive'),
        (1, 'Active'),
    )
    name = models.CharField(max_length=100)
    start_date = models.DateField()
    end_date = models.DateField()
    active = models.IntegerField(default=0, choices=STATUS)
    users = models.ManyToManyField(User, related_name='enrolled')
    search_fields = ('name')
    
