# Generated by Django 3.1.3 on 2021-01-29 11:03

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('inspection_management', '0004_inspectionresult_inspectiontask'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='inspectionresult',
            options={'verbose_name_plural': '点检结果'},
        ),
        migrations.AlterModelOptions(
            name='inspectiontask',
            options={'verbose_name_plural': '点检任务'},
        ),
        migrations.AlterModelTable(
            name='inspectionresult',
            table='点检结果',
        ),
        migrations.AlterModelTable(
            name='inspectiontask',
            table='点检任务',
        ),
    ]
