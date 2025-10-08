from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings

class User(AbstractUser):
    ROLE_CHOICES = (
        ('admin', 'Admin'),
        ('teacher', 'Teacher'),
        ('student', 'Student'),
        ('parent', 'Parent'),
    ) 
    
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='student')
    matric_no = models.CharField(max_length=20, blank=True, null=True, unique=True)
    staff_id = models.CharField(max_length=20, blank=True, null=True, unique=True)

    def __str__(self):
        return f"{self.username} ({self.role})"


class Department(models.Model):
    name = models.CharField(max_length=100, unique=True)
    code = models.CharField(max_length=10, unique=True)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.code} - {self.name}"


class Course(models.Model):
    department = models.ForeignKey(Department, on_delete=models.CASCADE, related_name="courses")
    code = models.CharField(max_length=10, unique=True)
    title = models.CharField(max_length=200)
    unit = models.PositiveIntegerField(default=3)
    lecturer = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True, blank=True,
        limit_choices_to={'role': 'teacher'}
    )

    def __str__(self):
        return f"{self.code} - {self.title}"


class Enrollment(models.Model):
    SEMESTER_CHOICES = (
        ('first', 'First'),
        ('second', 'Second'),
    )

    student = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="enrollments",
        limit_choices_to={'role': 'student'}
    )
    course = models.ForeignKey('Course', on_delete=models.CASCADE)
    semester = models.CharField(max_length=20, choices=SEMESTER_CHOICES)
    session = models.CharField(max_length=9, help_text="e.g., 2025/2026")
    date_enrolled = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('student', 'course', 'semester', 'session')
        verbose_name_plural = "Enrollments"

    def __str__(self):
        return f"{self.student.username} - {self.course.code} ({self.session}, {self.semester})"


class Grade(models.Model):
    enrollment = models.OneToOneField(Enrollment, on_delete=models.CASCADE)
    score = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    grade = models.CharField(max_length=2, blank=True, null=True)

    def save(self, *args, **kwargs):
        if self.score is not None:
            if self.score >= 70:
                self.grade = "A"
            elif self.score >= 60:
                self.grade = "B"
            elif self.score >= 50:
                self.grade = "C"
            elif self.score >= 45:
                self.grade = "D"
            elif self.score >= 40:
                self.grade = "E"
            else:
                self.grade = "F"
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.enrollment.student.username} - {self.enrollment.course.code}: {self.grade}"


class Announcement(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    date_created = models.ForeignKey(User, on_delete=models.CASCADE)
    target_role = models.CharField(
        max_length=20,
        choices=[('student', 'Student'), ('teacher', 'Teacher'), ('all', 'All')],
        default='all'
    )
    date_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
