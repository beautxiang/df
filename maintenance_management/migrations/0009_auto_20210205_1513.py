# Generated by Django 3.1.3 on 2021-02-05 15:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('maintenance_management', '0008_auto_20210205_0948'),
    ]

    operations = [
        migrations.AlterField(
            model_name='maintenancestandard',
            name='maintenance_standard_number',
            field=models.CharField(db_column='保养标准编号', max_length=64, primary_key=True, serialize=False, verbose_name='保养标准编号'),
        ),
    ]
