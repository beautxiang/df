# Generated by Django 3.1.3 on 2021-01-31 10:12

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('inspection_management', '0011_auto_20210130_1120'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='inspectionproject',
            options={'verbose_name_plural': '2点检项目'},
        ),
        migrations.AlterModelOptions(
            name='inspectionstandard',
            options={'verbose_name_plural': '1点巡检标准'},
        ),
        migrations.AlterModelTable(
            name='inspectionproject',
            table='2点检项目',
        ),
        migrations.AlterModelTable(
            name='inspectionstandard',
            table='1点巡检标准',
        ),
    ]