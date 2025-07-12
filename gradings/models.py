from django.db import models
from members.models import Member 
from django.contrib.auth.models import User # Assuming attendance is tracked per Member

# ✅ Grading session model
class Grading(models.Model):
    STATUS_CHOICES = [
        ('scheduled', 'Scheduled'),
        ('completed', 'Completed'),
        ('canceled', 'Canceled'),
    ]

    class_name = models.CharField(max_length=100)
    instructor = models.CharField(max_length=100)
    examiner = models.CharField(max_length=100, blank=True, null=True)
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
        return f"{self.class_name} by {self.instructor} ({self.start_time.date()})"


# ✅ Grading attendance model
class GradingAttendance(models.Model):
    grading_session = models.ForeignKey(Grading, on_delete=models.CASCADE)
    member = models.ForeignKey(Member, on_delete=models.CASCADE)
    present = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.member} – {self.grading_session} – {'Present' if self.present else 'Absent'}"

# ✅ Grading sheets model

class GradingSheetTemplate(models.Model):
    name = models.CharField(max_length=100)  # e.g., "Line Work"
    created_by = models.ForeignKey(
        User, 
        on_delete=models.CASCADE, 
        related_name='grading_templates_gradings'
    )
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name

class GradingSheet(models.Model):
    grading = models.ForeignKey(Grading, on_delete=models.CASCADE, related_name="grading_sheets")
    template = models.ForeignKey(GradingSheetTemplate, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)  # Optional override or custom label
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(
        User, 
        on_delete=models.CASCADE, 
        related_name='grading_sheets_created'
    )

    def __str__(self):
        return f"{self.title} – {self.grading.class_name}"