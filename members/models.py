from django.db import models
from marshalsync_settings.models import Role  # Adjust if your Role model lives elsewhere

class Member(models.Model):
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=20, blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    join_date = models.DateField(auto_now_add=True)
    profile_picture = models.ImageField(upload_to='profile_pics/', blank=True, null=True)

    roles = models.ManyToManyField(Role, blank=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.email})"
