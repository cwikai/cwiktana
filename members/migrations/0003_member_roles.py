# Generated by Django 5.2.3 on 2025-06-28 20:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('marshalsync_settings', '0002_permission_role_rolepermission'),
        ('members', '0002_member_profile_picture'),
    ]

    operations = [
        migrations.AddField(
            model_name='member',
            name='roles',
            field=models.ManyToManyField(blank=True, to='marshalsync_settings.role'),
        ),
    ]
