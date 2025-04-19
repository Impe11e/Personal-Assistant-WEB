from django.contrib.auth.models import User
from django.db import models
from django.db.models import CharField, TextField
from django.utils.text import slugify
from phonenumber_field.modelfields import PhoneNumberField
from cloudinary_storage.storage import MediaCloudinaryStorage, RawMediaCloudinaryStorage


# TODO: try without null, just blank
class Contact(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='contacts', null=True)
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
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notes', null=True)
    title = CharField(max_length=100, blank=True, null=False)
    text = TextField(blank=True, null=True)  # like just for reminders, where we dont need more text than title

    color = CharField(blank=True, null=True)
    tags = models.ManyToManyField('Tag')

    # owner = ForeignKey(User, on_delete=CASCADE)

    def __str__(self):
        tags = ', '.join([tag.tag_name for tag in self.tags.all()])
        return f'{self.title} | {tags or "No Tags"}'


class Tag(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='tags', null=True)
    tag_name = CharField(max_length=50, blank=True, null=False, unique=True)
    slug = models.SlugField(unique=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.tag_name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.tag_name


class UploadedFile(models.Model):
    CATEGORY_CHOICES = [
        ('image', 'Image'),
        ('video', 'Video'),
        ('document', 'Documents'),
        ('audio', 'Audio'),
        ('other', 'Other'),
    ]

    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='documents', null=True)
    title = models.CharField(max_length=255)
    file = models.FileField(upload_to='files/')
    uploaded_at = models.DateTimeField(auto_now_add=True)
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES, default='other')
    cloudinary_public_id = models.CharField(max_length=255, blank=True, null=True)

    def save(self, *args, **kwargs):
        if not self.id:
            if not self.category or self.category == 'other':
                extension = self.file.name.split('.')[-1].lower()
                if extension in ['jpg', 'jpeg', 'png', 'gif', 'bmp', 'svg']:
                    self.category = 'image'
                    self.file.storage = MediaCloudinaryStorage()
                elif extension in ['mp4', 'avi', 'mov', 'wmv', 'flv', 'mkv']:
                    self.category = 'video'
                    self.file.storage = RawMediaCloudinaryStorage()
                elif extension in ['doc', 'docx', 'pdf', 'txt', 'xls', 'xlsx', 'ppt', 'pptx']:
                    self.category = 'document'
                    self.file.storage = RawMediaCloudinaryStorage()
                elif extension in ['mp3', 'wav', 'ogg', 'flac', 'aac']:
                    self.category = 'audio'
                    self.file.storage = RawMediaCloudinaryStorage()
                else:
                    self.category = 'other'
                    self.file.storage = RawMediaCloudinaryStorage()
            else:
                if self.category == 'image':
                    self.file.storage = MediaCloudinaryStorage()
                else:
                    self.file.storage = RawMediaCloudinaryStorage()

        super().save(*args, **kwargs)

    def __str__(self):
        return self.title
