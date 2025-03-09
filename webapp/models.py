from django.db import models
from django.contrib.auth.models import User  # Import the User model

class Record(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)# Link to the User model
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.CharField(max_length=255)
    phone = models.CharField(max_length=20)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"