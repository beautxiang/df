# Generated by Django 3.1.3 on 2021-02-02 08:56

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('inspection_management', '0020_inspectiontask_inspection_projects'),
    ]

    operations = [
        migrations.RenameField(
            model_name='inspectionresult',
            old_name='inspection_task',
            new_name='inspection_task_number',
        ),
        migrations.AlterUniqueTogether(
            name='inspectionresult',
            unique_together={('inspection_project', 'inspection_task_number')},
        ),
    ]
