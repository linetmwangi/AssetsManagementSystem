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
    condition = [
        ('good condition', 'Good Condition'),
        ('under maintenance', 'Under Maintenance'),
    ]
    name = models.CharField(max_length=30)
    identifier = models.CharField(max_length=30, unique=True)
    description = models.CharField(max_length=100, blank=True)
    category = models.CharField(max_length=30, choices=category_choices, default='other')
    condition = models.CharField(max_length=30, choices=condition, default='good condition')

    def __str__(self):
        return str(self.name) + '[' + str(self.identifier) + ']'
from django.db import models

class IssuedAsset(models.Model):
    category_choices = [
        ('hardware', 'Hardware'),
        ('software', 'Software'),
        ('other', 'Other'),
    ]
    enrollment = models.ForeignKey(StaffExtra, on_delete=models.CASCADE, default=None)
    identifier = models.ForeignKey(Asset, on_delete=models.CASCADE, default=None)
    category = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.identifier.name} issued to {self.enrollment.name}"
class CarouselImage(models.Model):
    title = models.CharField(max_length=100, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    image = models.ImageField(upload_to="carousel_images/")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title if self.title else f"Image {self.id}"