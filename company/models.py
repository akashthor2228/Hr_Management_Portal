from datetime import timezone, timedelta

from django.conf import settings
from django.db import models
from django.utils import timezone


# Create your models here.
class Company(models.Model):
    STATUS_CHOICES = (
    ('active', 'active'),
    ('inactive', 'inactive'),
    )
    company_name = models.CharField(max_length=255)
    role = models.CharField(max_length=255)
    salary = models.DecimalField(max_digits=10,decimal_places=2)
    tech_stack = models.CharField(max_length=255)
    address = models.TextField()
    year_of_passing = models.PositiveIntegerField()

    added_by = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE,related_name='companies')

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='active')

    def __str__(self):
        return f"{self.company_name}-{self.role}"

    def auto_update_status(self):
        if timezone.now() > self.created_at + timedelta(minutes=55):
            if self.status != 'inactive':
                self.status = 'inactive'
                self.save()