# Generated by Django 3.1.3 on 2021-01-31 10:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('inspection_management', '0015_auto_20210131_1023'),
    ]

    operations = [
        migrations.AlterField(
            model_name='inspectionresult',
            name='is_unusual',
            field=models.IntegerField(blank=True, choices=[(0, '否'), (1, '是')], db_column='是否异常', null=True, verbose_name='是否异常'),
        ),
    ]
