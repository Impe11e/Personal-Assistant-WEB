# Generated by Django 5.2 on 2025-04-11 13:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pers_assist_app', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='contact',
            name='description',
            field=models.CharField(default='', max_length=500),
        ),
        migrations.AddField(
            model_name='contact',
            name='surname',
            field=models.CharField(default='None', max_length=150),
        ),
    ]
