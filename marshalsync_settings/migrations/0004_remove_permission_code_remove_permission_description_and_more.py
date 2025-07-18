# Generated by Django 5.2.3 on 2025-07-05 23:06

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('marshalsync_settings', '0003_role_description_and_more'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.RemoveField(
            model_name='permission',
            name='code',
        ),
        migrations.RemoveField(
            model_name='permission',
            name='description',
        ),
        migrations.RemoveField(
            model_name='role',
            name='description',
        ),
        migrations.RemoveField(
            model_name='role',
            name='is_default',
        ),
        migrations.AddField(
            model_name='permission',
            name='name',
            field=models.CharField(default='Unnamed Permission', max_length=100, unique=True),
        ),
        migrations.AddField(
            model_name='role',
            name='permissions',
            field=models.ManyToManyField(blank=True, to='marshalsync_settings.permission'),
        ),
        migrations.AddField(
            model_name='role',
            name='users',
            field=models.ManyToManyField(blank=True, related_name='roles', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='role',
            name='name',
            field=models.CharField(max_length=100, unique=True),
        ),
        migrations.DeleteModel(
            name='RolePermission',
        ),
    ]
