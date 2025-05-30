# Generated by Django 5.2 on 2025-04-11 14:23

import phonenumber_field.modelfields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pers_assist_app', '0004_fix_email_fiels'),
    ]

    operations = [
        migrations.AlterField(
            model_name='contact',
            name='address',
            field=models.CharField(blank=True, max_length=150, null=True),
        ),
        migrations.AlterField(
            model_name='contact',
            name='birthday',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='contact',
            name='email',
            field=models.EmailField(blank=True, max_length=254, null=True),
        ),
        migrations.AlterField(
            model_name='contact',
            name='phone',
            field=phonenumber_field.modelfields.PhoneNumberField(max_length=20, region=None, unique=True),
        ),
        migrations.AlterField(
            model_name='contact',
            name='surname',
            field=models.CharField(blank=True, default='None', max_length=150, null=True),
        ),
    ]
