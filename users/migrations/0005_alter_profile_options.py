# Generated by Django 5.0.1 on 2024-02-12 11:03

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0004_profile_location_skill'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='profile',
            options={'ordering': ['created_at']},
        ),
    ]
