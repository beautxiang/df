# Generated by Django 3.1.3 on 2021-01-30 09:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('inspection_management', '0008_auto_20210129_1652'),
    ]

    operations = [
        migrations.AddField(
            model_name='inspectiontask',
            name='inspection_projects',
            field=models.ManyToManyField(through='inspection_management.InspectionResult', to='inspection_management.InspectionProject'),
        ),
    ]