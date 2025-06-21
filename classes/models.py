from django.db import models
from members.models import Member  # Adjust import if needed

class ClassSession(models.Model):
    STATUS_CHOICES = [
        ('scheduled', 'Scheduled'),
        ('completed', 'Completed'),
        ('canceled', 'Canceled'),
    ]

    class_name = models.CharField(max_length=100)
    instructor = models.CharField(max_length=100)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    location = models.CharField(max_length=200, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    
    status = models.CharField(
        max_length=10,
        choices=STATUS_CHOICES,
        default='scheduled',
    )
    archived = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.class_name} by {self.instructor} from {self.start_time} to {self.end_time}"
class Attendance(models.Model):
    class_session = models.ForeignKey(ClassSession, on_delete=models.CASCADE)
    member = models.ForeignKey(Member, on_delete=models.CASCADE)
    present = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.member} – {self.class_session} – {'Present' if self.present else 'Absent'}"