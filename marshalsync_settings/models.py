from django.db import models
from django.contrib.auth.models import User

class Settings(models.Model):
    key = models.CharField(max_length=100, unique=True)
    value = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.key}: {self.value}"


class Role(models.Model):
    name = models.CharField(max_length=50, unique=True)
    description = models.TextField(blank=True, null=True)
    is_default = models.BooleanField(default=False)  # e.g., Admin, Instructor

    def __str__(self):
        return self.name


class Permission(models.Model):
    code = models.CharField(max_length=50, unique=True)  # e.g., 'view_attendance'
    description = models.CharField(max_length=255)

    def __str__(self):
        return self.description


class RolePermission(models.Model):
    role = models.ForeignKey(Role, on_delete=models.CASCADE)
    permission = models.ForeignKey(Permission, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('role', 'permission')  # Prevent duplicates

class GradingSheetTemplate(models.Model):
    name = models.CharField(max_length=100)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name
    
class Belt(models.Model):
    grade = models.CharField(max_length=100)
    belt_colour = models.CharField(max_length=100)
    is_active = models.BooleanField(default=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

#class syllabus(models.Model):
    #sylabus_module = models.CharField(max_length=100)
   # syllabus_content = models.TextField()
    #created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    #is_active = models.BooleanField(default=True)

   # def __str__(self):
       # return self.name