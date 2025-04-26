from django.db import models

class Vehicle(models.Model):
    TYPE_CHOICES = (
        ('van', 'Van'),
        ('motorcycle', 'Motorcycle'),
        ('e-bike', 'Electric Bicycle'),
        ('pickup', 'Pickup'),
        ('lorry', 'Lorry'),
        ('bike', 'Bike'),
    )
    type = models.CharField(max_length=20, choices=TYPE_CHOICES)
    plate_number = models.CharField(max_length=20)
    in_use = models.BooleanField(default=False)
