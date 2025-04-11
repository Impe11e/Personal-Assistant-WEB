from django.db import models
from phonenumber_field.modelfields import PhoneNumberField


# Create your models here.
class Contact(models.Model):
    name = models.CharField(max_length=50, null=False)
    surname = models.CharField(max_length=150, blank=True, null=True)
    address = models.CharField(max_length=150, blank=True, null=True)
    phone = PhoneNumberField(max_length=20, unique=True)
    email = models.EmailField(blank=True, null=True, unique=False)
    birthday = models.DateField(blank=True, null=True)
    description = models.CharField(max_length=500, default="")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
