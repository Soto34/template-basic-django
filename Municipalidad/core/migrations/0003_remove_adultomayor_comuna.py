# Generated by Django 5.1.3 on 2024-11-21 05:34

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0002_comuna_alter_adultomayor_telefono_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='adultomayor',
            name='comuna',
        ),
    ]
