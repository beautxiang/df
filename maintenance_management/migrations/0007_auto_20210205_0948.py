# Generated by Django 3.1.3 on 2021-02-05 09:48

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('maintenance_management', '0006_auto_20210129_0956'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='maintenanceplan',
            options={'verbose_name_plural': '23保养计划'},
        ),
        migrations.AlterModelOptions(
            name='maintenancestandard',
            options={'verbose_name_plural': '21保养标准'},
        ),
        migrations.AlterModelOptions(
            name='maintenancetask',
            options={'verbose_name_plural': '24保养计划'},
        ),
        migrations.AlterModelOptions(
            name='maintenancetype',
            options={'verbose_name_plural': '22保养类型'},
        ),
        migrations.AlterModelTable(
            name='maintenanceplan',
            table='23保养计划',
        ),
        migrations.AlterModelTable(
            name='maintenancestandard',
            table='21保养标准',
        ),
        migrations.AlterModelTable(
            name='maintenancetask',
            table='24保养计划',
        ),
        migrations.AlterModelTable(
            name='maintenancetype',
            table='22保养类型',
        ),
    ]
