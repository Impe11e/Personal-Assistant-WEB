from django.contrib import admin
from .models import Contact, Note, Tag, UploadedFile

# Register your models here.
admin.site.register(Contact)
admin.site.register(Note)
admin.site.register(Tag)
admin.site.register(UploadedFile)