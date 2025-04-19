from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Note, Tag


@receiver(post_save, sender=Note)
def add_default_tags_to_note(sender, instance, created, **kwargs):
    if created:
        default_tag_names = ['New', 'In Work', 'Done']
        tags = []
        for name in default_tag_names:
            tag, _ = Tag.objects.get_or_create(tag_name=name)
            tags.append(tag)
        instance.tags.set(tags)
