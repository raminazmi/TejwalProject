# Generated by Django 4.0 on 2022-02-19 14:50

import country.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('country', '0009_alter_city_image_alter_city_slug'),
    ]

    operations = [
        migrations.AlterField(
            model_name='city',
            name='image',
            field=models.ImageField(upload_to=country.models.ImageUploadCity),
        ),
    ]