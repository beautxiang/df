from django.db import models
from equipment_management.models import Equipment


class InspectionStandard(models.Model):
    inspection_standard_number = models.CharField(primary_key=True, verbose_name='点巡检标准编号', db_column='点巡检标准编号',
                                                  max_length=64)
    equipment_number = models.ForeignKey(Equipment, on_delete=models.CASCADE, to_field='equipment_number',
                                         verbose_name='设备编号', db_column='设备编号')
    inspection_standard_name = models.CharField(verbose_name='点巡检标准名称', db_column='点巡检标准名称', max_length=64)
    reference_inspection_period = models.CharField(verbose_name='参考点巡检周期', db_column='参考点巡检周期', max_length=32,
                                                   blank=True,
                                                   null=True)
    remark = models.CharField(verbose_name='备注', max_length=512, db_column='备注', blank=True, null=True)

    class Meta:
        # 设置表的名字
        db_table = '32点巡检标准'
        # 设置admin中表的名字
        verbose_name_plural = '32点巡检标准'


class InspectionProject(models.Model):
    part_or_project = models.CharField(verbose_name='项目或部位', db_column='项目或部位', max_length=64)
    inspection_content = models.CharField(verbose_name='点检内容', db_column='点检内容', max_length=128, blank=True, null=True)
    inspection_method = models.CharField(verbose_name='点检方法', db_column='点检方法', max_length=128, blank=True, null=True)
    scrutiny_standard = models.CharField(verbose_name='判断基准', db_column='判断基准', max_length=128, blank=True, null=True)
    belong_inspection_standard = models.ForeignKey(InspectionStandard, on_delete=models.CASCADE,
                                                   to_field='inspection_standard_number', verbose_name='所属点检标准')

    class Meta:
        # 设置表的名字
        db_table = '31点检项目'
        # 设置admin中表的名字
        verbose_name_plural = '31点检项目'


class InspectionPlan(models.Model):
    inspection_plan_number = models.CharField(verbose_name='点检计划编号', db_column='点检计划编号', max_length=64,
                                              primary_key=True)
    inspection_plan_name = models.CharField(verbose_name='点检计划名称', db_column='点检计划名称', max_length=64)
    creator = models.CharField(verbose_name='创建人', db_column='创建人', max_length=64, blank=True, null=True)
    principal = models.CharField(verbose_name='负责人', db_column='负责人', max_length=64, blank=True, null=True)
    start_time = models.DateField(auto_now_add=False, verbose_name='开始时间', db_column='开始时间', blank=True, null=True)
    end_time = models.DateField(auto_now_add=False, verbose_name='结束时间', db_column='结束时间', blank=True, null=True)
    plan_status = models.IntegerField(choices=((0, '未开始'), (1, '进行中'), (2, '已结束')), verbose_name='计划状态',
                                      db_column='计划状态', default=0)
    inspection_period = models.CharField(verbose_name='点检周期(天)', max_length=32, db_column='点检周期(天)')
    remark = models.CharField(verbose_name='备注', max_length=512, db_column='备注', blank=True, null=True)
    inspection_standard = models.ManyToManyField(to='InspectionStandard', verbose_name='点检标准')

    class Meta:
        # 设置表的名字
        db_table = '33点检计划'
        # 设置admin中表的名字
        verbose_name_plural = '33点检计划'


class InspectionTask(models.Model):
    inspection_task_number = models.CharField(verbose_name='点检任务编号', db_column='点检任务编号', max_length=64,
                                              primary_key=True)
    task_start_time = models.DateTimeField(auto_now_add=False, verbose_name='任务开始时间')
    task_end_time = models.DateTimeField(auto_now_add=False, verbose_name='任务结束时间')
    belong_plan = models.ForeignKey(to=InspectionPlan, on_delete=models.CASCADE, to_field='inspection_plan_number',
                                    verbose_name='所属计划')
    task_status = models.IntegerField(choices=((0, '未开始'), (1, '进行中'), (2, '已完成'), (3, '未完成')), default=0)
    inspection_projects = models.ManyToManyField(to=InspectionProject, through='InspectionResult')
    total_inspection_items = models.IntegerField(verbose_name='总巡检项个数', db_column='总巡检项个数', null=True, blank=True)
    checked_the_number = models.IntegerField(verbose_name='已检数', db_column='已检数', null=True, blank=True)

    class Meta:
        # 设置表的名字
        db_table = '34点检任务'
        # 设置admin中表的名字
        verbose_name_plural = '34点检任务'


class InspectionResult(models.Model):
    inspection_value = models.CharField(verbose_name='巡检值', db_column='巡检值', max_length=64, null=True, blank=True)
    is_unusual = models.IntegerField(choices=((0, '否'), (1, '是')), verbose_name='是否异常', db_column='是否异常', null=True, blank=True)
    inspection_project = models.ForeignKey(InspectionProject, on_delete=models.CASCADE, verbose_name='点检项目')
    inspection_task_number = models.ForeignKey(InspectionTask, on_delete=models.CASCADE, verbose_name='点检任务')

    class Meta:
        # 设置表的名字
        db_table = '35点检项目_点检任务_点检结果'
        # 设置admin中表的名字
        verbose_name_plural = '35点检项目_点检任务_点检结果'
        unique_together = (("inspection_project", "inspection_task_number"),)
