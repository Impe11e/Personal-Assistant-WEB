from django.db import models
from django.db.models import CharField, TextField, JSONField, ForeignKey, CASCADE
from django.utils.text import slugify
from phonenumber_field.modelfields import PhoneNumberField


# TODO: try without null, just blank
class Contact(models.Model):
    name = models.CharField(max_length=50, null=False)
    surname = models.CharField(max_length=150, blank=True, null=True)
    address = models.CharField(max_length=150, blank=True, null=True)
    phone = PhoneNumberField(unique=True)
    email = models.EmailField(blank=True, null=True, unique=False)
    birthday = models.DateField(blank=True, null=True)
    description = models.CharField(max_length=500, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


# NOTES
class Note(models.Model):
    title = CharField(max_length=100, blank=True, null=False)
    text = TextField(blank=True, null=True)  # like just for reminders, where we dont need more text than title

    color = CharField(blank=True, null=True)
    tags = models.ManyToManyField('Tag')

    # owner = ForeignKey(User, on_delete=CASCADE)

    def __str__(self):
        tags = ', '.join([tag.tag_name for tag in self.tags.all()])
        return f'{self.title} | {tags or "No Tags"}'


class Tag(models.Model):
    tag_name = CharField(max_length=50, blank=True, null=False, unique=True)
    slug = models.SlugField(unique=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.tag_name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.tag_name
