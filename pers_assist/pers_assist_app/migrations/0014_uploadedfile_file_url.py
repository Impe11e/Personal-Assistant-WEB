# Generated by Django 5.2 on 2025-04-19 09:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pers_assist_app', '0013_uploadedfile_cloudinary_public_id_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='uploadedfile',
            name='file_url',
            field=models.URLField(blank=True, max_length=500, null=True),
        ),
    ]
