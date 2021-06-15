# Generated by Django 3.1.3 on 2021-01-29 09:40

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('equipment_management', '0011_remove_equipment_parent_number'),
    ]

    operations = [
        migrations.CreateModel(
            name='InspectionStandard',
            fields=[
                ('inspection_standard_number', models.CharField(db_column='点检标准编号', max_length=64, primary_key=True, serialize=False, verbose_name='点检标准编号')),
                ('inspection_standard_name', models.CharField(db_column='点检标准名称', max_length=64, verbose_name='点检标准名称')),
                ('remark', models.CharField(blank=True, db_column='备注', max_length=512, null=True, verbose_name='备注')),
                ('equipment_number', models.ForeignKey(db_column='设备编号', on_delete=django.db.models.deletion.CASCADE, to='equipment_management.equipment', verbose_name='设备编号')),
            ],
            options={
                'verbose_name_plural': '点检标准',
                'db_table': '点检标准',
            },
        ),
        migrations.CreateModel(
            name='InspectionProject',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('part_or_project', models.CharField(db_column='项目或部位', max_length=64, verbose_name='项目或部位')),
                ('inspection_content', models.CharField(blank=True, db_column='点检内容', max_length=128, null=True, verbose_name='点检内容')),
                ('inspection_method', models.CharField(blank=True, db_column='点检方法', max_length=128, null=True, verbose_name='点检方法')),
                ('scrutiny_standard', models.CharField(blank=True, db_column='判断基准', max_length=128, null=True, verbose_name='判断基准')),
                ('reference_inspection_period', models.CharField(blank=True, db_column='参考点检周期', max_length=32, null=True, verbose_name='参考点检周期')),
                ('belong_inspection_standard', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='inspection_management.inspectionstandard', verbose_name='所属点检标准')),
            ],
            options={
                'verbose_name_plural': '点检项目',
                'db_table': '点检项目',
            },
        ),
    ]