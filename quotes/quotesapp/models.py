from django.db import models


# Create your models here.
class Tag(models.Model):
    name = models.CharField(max_length=25, null=False, unique=True)

    def __str__(self):
        return f"{self.name}"

class Author(models.Model):
    fullname = models.CharField(max_length=255, null=False, unique=True)
    born_date = models.CharField(max_length=255, null=True, blank=True)
    born_location = models.TextField(null=True, blank=True)
    description = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.fullname

class Quote(models.Model):
    quote = models.CharField(max_length=500, null=False)
    author=models.ForeignKey(Author, on_delete=models.CASCADE, default=None, null=True)
    tags = models.ManyToManyField(Tag)

    def __str__(self):
        return f"{self.name}"