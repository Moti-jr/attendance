from django.db import models
from django.contrib.auth.models import User as AuthUser
from django.utils import timezone

class User(models.Model):
    SEX_CHOICES = [
        ('M', 'Male'),
        ('F', 'Female'),
        ('O', 'Other'),
    ]
    auth_user = models.ForeignKey(AuthUser, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    id_number = models.CharField(max_length=20, unique=True)
    personal_number = models.CharField(max_length=20, unique=True)
    mda=models.CharField(max_length=20, null=True)
    phone = models.CharField(max_length=20)
    sex = models.CharField(max_length=1, choices=SEX_CHOICES)
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

class Attendance(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateField(auto_now_add=True)
    check_in_time = models.DateTimeField(null=True, blank=True)
    check_out_time = models.DateTimeField(null=True, blank=True)
    checked_out_by = models.CharField(max_length=50, blank=True, null=True)

    class Meta:
        unique_together = ('user', 'date')

    def __str__(self):
        return f"{self.user.auth_user.username} - {self.date}"
2
