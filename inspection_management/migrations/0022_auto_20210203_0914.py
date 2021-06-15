# Generated by Django 3.1.3 on 2021-02-03 09:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('inspection_management', '0021_auto_20210202_0856'),
    ]

    operations = [
        migrations.AddField(
            model_name='inspectiontask',
            name='checked_the_number',
            field=models.IntegerField(blank=True, db_column='已检数', null=True, verbose_name='已检数'),
        ),
        migrations.AddField(
            model_name='inspectiontask',
            name='total_inspection_items',
            field=models.IntegerField(blank=True, db_column='总巡检项个数', null=True, verbose_name='总巡检项个数'),
        ),
    ]
