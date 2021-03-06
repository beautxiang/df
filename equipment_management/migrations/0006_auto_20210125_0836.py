# Generated by Django 3.1.3 on 2021-01-25 08:36

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('equipment_management', '0005_auto_20210116_0743'),
    ]

    operations = [
        migrations.CreateModel(
            name='Department',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('department_name', models.CharField(db_column='部门名', max_length=64, verbose_name='部门名')),
                ('parent_id', models.IntegerField(db_column='父id', max_length=32, verbose_name='父id')),
            ],
        ),
        migrations.AlterField(
            model_name='equipment',
            name='remark',
            field=models.CharField(blank=True, db_column='备注', max_length=512, null=True, verbose_name='备注'),
        ),
        migrations.AlterField(
            model_name='equipment',
            name='department',
            field=models.ForeignKey(blank=True, db_column='所属部门', null=True, on_delete=django.db.models.deletion.CASCADE, to='equipment_management.department', verbose_name='所属部门'),
        ),
    ]
