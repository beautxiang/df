# Generated by Django 3.1.3 on 2021-01-30 11:20

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('inspection_management', '0010_auto_20210130_1120'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='inspectionresult',
            options={'verbose_name_plural': '点检项目_点检任务_点检结果'},
        ),
        migrations.AlterModelTable(
            name='inspectionresult',
            table='点检项目_点检任务_点检结果',
        ),
    ]
