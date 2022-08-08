# Generated by Django 4.0 on 2022-02-25 06:07

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0005_remove_profile_person_image'),
        ('place', '0017_alter_place_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='review',
            name='profile',
            field=models.ForeignKey(default='', on_delete=django.db.models.deletion.CASCADE, to='accounts.profile'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='place',
            name='short_info',
            field=models.CharField(max_length=40),
        ),
    ]