# Generated by Django 3.1.3 on 2021-01-27 09:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('maintenance_management', '0002_maintenancetask_maintenance_record'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='maintenancetask',
            name='id',
        ),
        migrations.AddField(
            model_name='maintenancetask',
            name='task_number',
            field=models.CharField(db_column='保养任务编号', default=2, max_length=64, primary_key=True, serialize=False, verbose_name='保养任务编号'),
            preserve_default=False,
        ),
    ]
