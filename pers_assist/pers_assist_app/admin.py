from django.contrib import admin
from .models import Contact, Note, Tag

# Register your models here.
admin.site.register(Contact)
admin.site.register(Note)
admin.site.register(Tag)
