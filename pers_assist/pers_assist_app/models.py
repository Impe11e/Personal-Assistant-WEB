from django.db import models
from phonenumber_field.modelfields import PhoneNumberField
from cloudinary_storage.storage import MediaCloudinaryStorage, RawMediaCloudinaryStorage
from django.core.files.uploadedfile import UploadedFile as DjangoUploadedFile


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


class UploadedFile(models.Model):
    CATEGORY_CHOICES = [
        ('image', 'Image'),
        ('video', 'Video'),
        ('document', 'Documents'),
        ('audio', 'Audio'),
        ('other', 'Other'),
    ]

    title = models.CharField(max_length=255)
    file = models.FileField(upload_to='files/')
    uploaded_at = models.DateTimeField(auto_now_add=True)
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES, default='other')
    cloudinary_public_id = models.CharField(max_length=255, blank=True, null=True)

    def save(self, *args, **kwargs):
        if not self.id:  # Если объект новый (еще не сохранен)
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
                # Устанавливаем хранилище в зависимости от категории
                if self.category == 'image':
                    self.file.storage = MediaCloudinaryStorage()
                else:
                    # Для всех остальных типов файлов (включая видео)
                    self.file.storage = RawMediaCloudinaryStorage()

        super().save(*args, **kwargs)

    def __str__(self):
        return self.title
