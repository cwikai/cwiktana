# Generated by Django 5.2.3 on 2025-07-12 17:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('marshalsync_settings', '0006_belt'),
    ]

    operations = [
        migrations.AddField(
            model_name='belt',
            name='is_active',
            field=models.BooleanField(default=True),
        ),
    ]
