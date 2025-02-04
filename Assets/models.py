from django.db import models
from django.contrib.auth.models import User

class StaffExtra(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    enrollment = models.CharField(max_length=40)
    department = models.CharField(max_length=40)

    def save(self, *args, **kwargs):
        if not self.user.is_staff:  # Ensure staff flag is set
            self.user.is_staff = True
            self.user.save()
        super().save(*args, **kwargs)

    def __str__(self):
        return self.user.first_name + '[' + str(self.enrollment) + ']'

class Asset(models.Model):
    category_choices = [
        ('hardware', 'Hardware'),
        ('software', 'Software'),
        ('other', 'Other'),
    ]

    condition_choices = [
        ('good condition', 'Good Condition'),
        ('under maintenance', 'Under Maintenance'),
    ]

    name = models.CharField(max_length=30)
    identifier = models.CharField(max_length=30, unique=True)
    description = models.CharField(max_length=100, blank=True)
    category = models.CharField(max_length=30, choices=category_choices, default='other')
    condition = models.CharField(max_length=30, choices=condition_choices, default='good condition')
    available = models.BooleanField(default=True)
    requested_by = models.ForeignKey(User, null=True, blank=True, on_delete=models.SET_NULL)
    requested_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)

    def __str__(self):
        return f"{self.name} [{self.identifier}]"


class IssuedAsset(models.Model):
    enrollment = models.ForeignKey(StaffExtra, on_delete=models.CASCADE, default=None)
    identifier = models.ForeignKey(Asset, on_delete=models.CASCADE, default=None)
    condition = models.CharField(max_length=30, choices=Asset.condition_choices, default='other')

    def __str__(self):
        return f'{self.identifier.name} issued to {self.enrollment.user} '


class CarouselImage(models.Model):
    title = models.CharField(max_length=100, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    image = models.ImageField(upload_to="carousel_images/")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title if self.title else f"Image {self.id}"
