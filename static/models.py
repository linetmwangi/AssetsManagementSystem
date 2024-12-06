from django.db import models
from django.contrib.auth.models import User

class StaffExtra(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    enrollment = models.CharField(max_length=40)
    department = models.CharField(max_length=40)

    def __str__(self):
        return self.user.first_name + '[' + str(self.enrollment) + ']'

    @property
    def get_name(self):
        return self.user.first_name

    @property
    def getuserid(self):
        return self.user.id

class Asset(models.Model):
    category_choices = [
        ('hardware', 'Hardware'),
        ('software', 'Software'),
        ('other', 'Other'),
    ]
    name = models.CharField(max_length=30)
    identifier = models.CharField(max_length=30, unique=True)  # Replacing ISBN
    description = models.CharField(max_length=100, blank=True)
    category = models.CharField(max_length=30, choices=category_choices, default='other')

    def __str__(self):
        return str(self.name) + '[' + str(self.identifier) + ']'

class IssuedAsset(models.Model):
    category_choices = [
        ('hardware', 'Hardware'),
        ('software', 'Software'),
        ('other', 'Other'),
    ]
    enrollment = models.CharField(max_length=30)
    asset_identifier = models.CharField(max_length=30)  # Replacing ISBN
    issuedate = models.DateField(auto_now=True)
    category =  category = models.CharField(max_length=30, choices=category_choices, default='other')
    issuedate = models.DateField(auto_now=True)


    def __str__(self):
        return f"{self.enrollment} - {self.asset_identifier}"

