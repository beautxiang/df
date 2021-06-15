# Generated by Django 3.1.3 on 2021-01-10 23:52

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('category', models.CharField(db_column='类别', max_length=32, primary_key=True, serialize=False, verbose_name='类别')),
            ],
            options={
                'db_table': '类别',
            },
        ),
        migrations.CreateModel(
            name='Equipment',
            fields=[
                ('equipment_number', models.CharField(db_column='设备编号', help_text='这个字段必须填写，且命名不能重复', max_length=64, primary_key=True, serialize=False, verbose_name='设备编号')),
                ('equipment_name', models.CharField(db_column='设备名称', help_text='这个字段必须填写', max_length=32, verbose_name='设备名称')),
                ('asset_number', models.CharField(blank=True, db_column='资产编号', max_length=32, null=True, verbose_name='资产编号')),
                ('manufacturing_number', models.CharField(blank=True, db_column='出厂编号', max_length=32, null=True, verbose_name='出厂编号')),
                ('units', models.CharField(blank=True, db_column='单位', max_length=16, null=True, verbose_name='单位')),
                ('type', models.CharField(blank=True, db_column='型号', max_length=64, null=True, verbose_name='型号')),
                ('brand', models.CharField(blank=True, db_column='品牌', max_length=64, null=True, verbose_name='品牌')),
                ('supplier', models.CharField(blank=True, db_column='供应商', max_length=64, null=True, verbose_name='供应商')),
                ('purchase_amount', models.FloatField(blank=True, db_column='购置金额', null=True, verbose_name='购置金额')),
                ('purchase_date', models.DateField(blank=True, db_column='购买日期', null=True, verbose_name='购买日期')),
                ('guarantee_period', models.DateField(blank=True, db_column='保修期', null=True, verbose_name='保修期')),
                ('production_time', models.DateField(blank=True, db_column='投产日期', null=True, verbose_name='投产日期')),
                ('estimated_retirement_time', models.DateField(blank=True, db_column='预计报废时间', null=True, verbose_name='预计报废时间')),
                ('person_in_charge', models.CharField(blank=True, db_column='负责人', max_length=32, null=True, verbose_name='负责人')),
                ('department', models.CharField(blank=True, db_column='所属部门', max_length=128, null=True, verbose_name='所属部门')),
                ('storage_place', models.CharField(blank=True, db_column='存放位置', max_length=128, null=True, verbose_name='存放位置')),
                ('relevant_document', models.FileField(blank=True, db_column='相关文件', null=True, upload_to='equipment_relevant_document', verbose_name='相关文件')),
                ('creation_time', models.DateTimeField(auto_now_add=True, db_column='创建时间', verbose_name='创建时间')),
                ('category', models.OneToOneField(blank=True, db_column='类别', null=True, on_delete=django.db.models.deletion.CASCADE, to='equipment_management.category', verbose_name='类别')),
            ],
            options={
                'verbose_name_plural': '设备基本信息表',
                'db_table': '设备基本信息表',
            },
        ),
        migrations.CreateModel(
            name='EquipmentSource',
            fields=[
                ('equipment_source', models.CharField(db_column='设备来源', max_length=32, primary_key=True, serialize=False, verbose_name='设备来源')),
            ],
            options={
                'db_table': '设备来源',
            },
        ),
        migrations.CreateModel(
            name='EquipmentState',
            fields=[
                ('equipment_state', models.CharField(db_column='设备状态', max_length=32, primary_key=True, serialize=False, verbose_name='设备状态')),
            ],
            options={
                'db_table': '设备状态',
            },
        ),
        migrations.CreateModel(
            name='UsageState',
            fields=[
                ('usage_state', models.CharField(db_column='使用状态', max_length=32, primary_key=True, serialize=False, verbose_name='使用状态')),
            ],
            options={
                'db_table': '使用状态',
            },
        ),
        migrations.CreateModel(
            name='Label',
            fields=[
                ('equipment_number', models.OneToOneField(db_column='设备编号', help_text='请选择一个已存在的设备编号', on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to='equipment_management.equipment', verbose_name='设备编号')),
                ('QR_code', models.ImageField(blank=True, db_column='二维码', null=True, upload_to='QR_code', verbose_name='二维码')),
                ('bar_code', models.ImageField(blank=True, db_column='条形码', null=True, upload_to='QR_code', verbose_name='条形码')),
                ('last_printing_time', models.DateTimeField(auto_now=True, db_column='最后打印时间', verbose_name='最后打印时间')),
            ],
            options={
                'db_table': '设备标签信息表',
            },
        ),
        migrations.CreateModel(
            name='OperationRecord',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('record_time', models.DateField(auto_now=True, db_column='记录时间', verbose_name='记录时间')),
                ('boot_time', models.DateTimeField(blank=True, db_column='开机时间', null=True, verbose_name='开机时间')),
                ('off_time', models.DateTimeField(blank=True, db_column='关机时间', null=True, verbose_name='关机时间')),
                ('equipment_number', models.ForeignKey(db_column='设备编号', help_text='请选择一个已存在的设备编号', on_delete=django.db.models.deletion.CASCADE, to='equipment_management.equipment', verbose_name='设备编号')),
            ],
            options={
                'db_table': '设备运行记录信息表',
            },
        ),
        migrations.AddField(
            model_name='equipment',
            name='equipment_source',
            field=models.OneToOneField(blank=True, db_column='设备来源', null=True, on_delete=django.db.models.deletion.CASCADE, to='equipment_management.equipmentsource', verbose_name='设备来源'),
        ),
        migrations.AddField(
            model_name='equipment',
            name='equipment_state',
            field=models.OneToOneField(blank=True, db_column='设备状态', null=True, on_delete=django.db.models.deletion.CASCADE, to='equipment_management.equipmentstate', verbose_name='设备状态'),
        ),
        migrations.AddField(
            model_name='equipment',
            name='usage_state',
            field=models.OneToOneField(blank=True, db_column='使用状态', null=True, on_delete=django.db.models.deletion.CASCADE, to='equipment_management.usagestate', verbose_name='使用状态'),
        ),
    ]
