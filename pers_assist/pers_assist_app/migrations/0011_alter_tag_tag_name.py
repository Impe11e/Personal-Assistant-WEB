# Generated by Django 5.2 on 2025-04-16 14:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pers_assist_app', '0010_tag_note'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tag',
            name='tag_name',
            field=models.CharField(blank=True, max_length=50, unique=True),
        ),
    ]
