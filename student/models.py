from django.conf import settings
from django.db import models

from company.models import Company


# Create your models here.
class Student(models.Model):
   user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
   # first_name = models.CharField(max_length=100)
   qualification = models.CharField(max_length=100)
   tech_stack = models.CharField(max_length=100)
   year_of_passing = models.PositiveIntegerField()
   mobile = models.CharField(max_length=15)


   def __str__(self):
       return self.user.username




class AppliedDrive(models.Model):
   student = models.ForeignKey(Student, on_delete=models.CASCADE)
   company = models.ForeignKey(Company, on_delete=models.CASCADE)
   applied_at = models.DateTimeField(auto_now_add=True)


   class Meta:
       unique_together = ('student', 'company')  # Prevent duplicate applications


   def __str__(self):
       return f"{self.student.user.username} applied to {self.company.company_name}"