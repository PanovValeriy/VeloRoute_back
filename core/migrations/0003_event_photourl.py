# Generated by Django 4.2.19 on 2025-03-15 13:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0002_alter_event_route'),
    ]

    operations = [
        migrations.AddField(
            model_name='event',
            name='photoURL',
            field=models.TextField(default=''),
        ),
    ]
