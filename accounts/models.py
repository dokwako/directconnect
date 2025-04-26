from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    ROLE_CHOICES = (
        ('admin', 'Admin'),
        ('employee', 'Employee'),
        ('customer', 'Customer'),
    )
    role = models.CharField(max_length=10, choices=ROLE_CHOICES)

    phone_number = models.CharField(max_length=20, blank=True, null=True)

    # Customer-specific fields
    default_pickup_address = models.CharField(max_length=255, blank=True, null=True)
    default_delivery_address = models.CharField(max_length=255, blank=True, null=True)

    # Employee-specific fields
    employee_id = models.CharField(max_length=50, blank=True, null=True)
    assigned_vehicles = models.CharField(max_length=255, blank=True, null=True)  # Could be a comma-separated list or JSON string

    def __str__(self):
        return self.username
