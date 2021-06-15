from django.db import models
from equipment_management.models import Equipment


class MaintenanceType(models.Model):
    maintenance_type = models.CharField(verbose_name='保养类型', db_column='保养类型', max_length=32, primary_key=True)

    class Meta:
        # 设置表的名字
        db_table = '22保养类型'
        # 设置admin中表的名字
        verbose_name_plural = '22保养类型'


class MaintenanceStandard(models.Model):
    maintenance_standard_number = models.CharField(verbose_name='保养标准编号', db_column='保养标准编号', max_length=64,
                                                   primary_key=True)
    equipment_number = models.ForeignKey(to=Equipment, on_delete=models.CASCADE, to_field='equipment_number',
                                         verbose_name='设备编号', db_column='设备编号')
    maintenance_type = models.ForeignKey(to=MaintenanceType, on_delete=models.CASCADE, verbose_name='保养类型',
                                         blank=False, null=False, to_field='maintenance_type', db_column='保养类型')
    maintenance_content = models.TextField(verbose_name='保养内容', db_column='保养内容')
    remark = models.CharField(verbose_name='备注', max_length=512, db_column='备注', blank=True, null=True)

    class Meta:
        # 设置表的名字
        db_table = '21保养标准'
        # 设置admin中表的名字
        verbose_name_plural = '21保养标准'
        unique_together = (("equipment_number", "maintenance_type"),)


class MaintenancePlan(models.Model):
    maintenance_plan_number = models.CharField(verbose_name='保养计划编号', db_column='保养计划编号', max_length=64,
                                               primary_key=True)
    plan_name = models.CharField(verbose_name='计划名称', db_column='计划名称', max_length=64)
    creator = models.CharField(verbose_name='创建人', db_column='创建人', max_length=64, blank=True, null=True)
    principal = models.CharField(verbose_name='负责人', db_column='负责人', max_length=64, blank=True, null=True)
    acceptor = models.CharField(verbose_name='验收人', db_column='验收人', max_length=64, blank=True, null=True)
    start_time = models.DateField(auto_now_add=False, verbose_name='开始时间', db_column='开始时间', blank=True, null=True)
    end_time = models.DateField(auto_now_add=False, verbose_name='结束时间', db_column='结束时间', blank=True, null=True)
    plan_status = models.IntegerField(choices=((0, '未开始'), (1, '进行中'), (2, '已结束')), verbose_name='计划状态',
                                      db_column='计划状态', default=0)
    remark = models.CharField(verbose_name='备注', max_length=512, db_column='备注', blank=True, null=True)
    maintenance_time_point = models.CharField(verbose_name='保养周期(天)', max_length=128, db_column='保养周期(天)', blank=True,
                                              null=True)
    maintenance_information = models.ManyToManyField(to='MaintenanceStandard', verbose_name='保养信息')

    class Meta:
        # 设置表的名字
        db_table = '23保养计划'
        # 设置admin中表的名字
        verbose_name_plural = '23保养计划'


class MaintenanceTask(models.Model):
    task_status = models.IntegerField(choices=((0, '未开始'), (1, '进行中'), (2, '已完成'), (3, '未完成')), default=0)
    task_number = models.CharField(verbose_name='保养任务编号', db_column='保养任务编号', max_length=64, primary_key=True)
    task_start_time = models.DateTimeField(auto_now_add=False, verbose_name='任务开始时间')
    task_end_time = models.DateTimeField(auto_now_add=False, verbose_name='任务结束时间')
    belong_plan = models.ForeignKey(to=MaintenancePlan, on_delete=models.CASCADE, to_field='maintenance_plan_number',
                                    verbose_name='所属计划')
    acceptance_phase = models.IntegerField(choices=((0, '未验收'), (1, '验收通过'), (2, '验收不通过')), verbose_name='验收状态',
                                           db_column='验收状态', default=0)
    acceptance_descriptions = models.CharField(verbose_name='验收说明', max_length=512, db_column='验收说明', blank=True,
                                               null=True)
    maintenance_record = models.CharField(verbose_name='保养记录', max_length=512, db_column='保养记录', blank=True, null=True)

    class Meta:
        # 设置表的名字
        db_table = '24保养任务'
        # 设置admin中表的名字
        verbose_name_plural = '24保养任务'
