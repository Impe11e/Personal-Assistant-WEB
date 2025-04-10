from django.db import models


# Create your models here.
class Contact(models.Model):
    name = models.CharField(max_length=50, null=False)
    address = models.CharField(max_length=150, null=False)
    phone = models.CharField(max_length=20, unique=True)
    email = models.EmailField(null=False, unique=True)
    birthday = models.DateField(null=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
