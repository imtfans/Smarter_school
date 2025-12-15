from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone


# -----------------------------
# CUSTOM USER MODEL
# -----------------------------
class User(AbstractUser):
    ROLE_CHOICES = (
        ('admin', 'Admin'),
        ('teacher', 'Teacher'),
        ('parent', 'Parent'),
    )

    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='parent')
    phone = models.CharField(max_length=20, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    groups = models.ManyToManyField(
        'auth.Group',
        related_name='core_users',
        blank=True,
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='core_users_permissions',
        blank=True,
    )

    def __str__(self):
        return f"{self.username} ({self.role})"


# -----------------------------
# SUBJECT MODEL
# -----------------------------
class Subject(models.Model):
    name = models.CharField(max_length=150, unique=True)

    def __str__(self):
        return self.name


# -----------------------------
# TEACHER MODEL
# -----------------------------
class Teacher(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='teacher_profile',
        limit_choices_to={'role': 'teacher'}
    )
    assigned_subject = models.ForeignKey(
        Subject,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )
    staff_id = models.CharField(max_length=50, unique=True)
    salary = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    def __str__(self):
        return f"Teacher: {self.user.get_full_name()}"


# -----------------------------
# STUDENT MODEL
# -----------------------------
class Student(models.Model):
    CLASS_CHOICES = [
        ('JSS1', 'JSS1'),
        ('JSS2', 'JSS2'),
        ('JSS3', 'JSS3'),
        ('SS1', 'SS1'),
        ('SS2', 'SS2'),
        ('SS3', 'SS3'),
    ]

    first_name = models.CharField(max_length=120)
    last_name = models.CharField(max_length=120)
    admission_no = models.CharField(max_length=50, unique=True)
    current_class = models.CharField(max_length=20, choices=CLASS_CHOICES)
    parent = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        limit_choices_to={'role': 'parent'},
        related_name='children'
    )

    date_of_birth = models.DateField(null=True, blank=True)
    date_joined = models.DateField(default=timezone.now)
    is_graduated = models.BooleanField(default=False)

    def promote(self):
        promotion_map = {
            'JSS1': 'JSS2',
            'JSS2': 'JSS3',
            'JSS3': 'SS1',
            'SS1': 'SS2',
            'SS2': 'SS3',
            'SS3': None,
        }

        next_class = promotion_map.get(self.current_class)

        if next_class:
            self.current_class = next_class
        else:
            self.is_graduated = True

        self.save()

    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.current_class})"


# -----------------------------
# RESULT MODEL
# -----------------------------
class Result(models.Model):
    GRADE_BOUNDARIES = [
        (70, 'A'),
        (60, 'B'),
        (50, 'C'),
        (45, 'D'),
        (40, 'E'),
        (0, 'F'),
    ]

    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='results')
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    session = models.CharField(max_length=20)
    term = models.CharField(max_length=20, default="1st Term")

    ca1 = models.PositiveIntegerField(default=0)
    ca2 = models.PositiveIntegerField(default=0)
    exam = models.PositiveIntegerField(default=0)

    total = models.PositiveIntegerField(blank=True, null=True)
    grade = models.CharField(max_length=2, blank=True)

    class Meta:
        unique_together = ('student', 'subject', 'session', 'term')

    def calculate_grade(self):
        for minimum, grade in self.GRADE_BOUNDARIES:
            if self.total >= minimum:
                return grade
        return 'F'

    def save(self, *args, **kwargs):
        self.total = self.ca1 + self.ca2 + self.exam
        self.grade = self.calculate_grade()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.student} - {self.subject} ({self.session} {self.term})"


# -----------------------------
# ATTENDANCE MODEL
# -----------------------------
class Attendance(models.Model):
    STATUS_CHOICES = (
        ('present', 'Present'),
        ('absent', 'Absent'),
    )

    student = models.ForeignKey(
        Student,
        on_delete=models.CASCADE,
        related_name='attendance_records'
    )
    date = models.DateField(default=timezone.now)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES)

    class Meta:
        unique_together = ('student', 'date')

    def __str__(self):
        return f"{self.student} - {self.status} on {self.date}"
