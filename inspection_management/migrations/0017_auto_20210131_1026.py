# Generated by Django 3.1.3 on 2021-01-31 10:26

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('inspection_management', '0016_auto_20210131_1025'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='inspectionresult',
            unique_together={('inspection_project', 'inspection_task')},
        ),
    ]
