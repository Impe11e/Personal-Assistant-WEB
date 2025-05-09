# Generated by Django 5.2 on 2025-04-17 15:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pers_assist_app', '0012_eng_docs_ext'),
    ]

    operations = [
        migrations.AddField(
            model_name='uploadedfile',
            name='cloudinary_public_id',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='uploadedfile',
            name='file',
            field=models.FileField(upload_to='files/'),
        ),
    ]
