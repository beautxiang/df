# Generated by Django 3.1.3 on 2021-01-29 16:52

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('inspection_management', '0007_auto_20210129_1629'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='inspectiontask',
            name='inspected_number',
        ),
        migrations.RemoveField(
            model_name='inspectiontask',
            name='inspection_project_count',
        ),
    ]
