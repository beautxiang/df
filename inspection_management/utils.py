import time

from .models import *
from datetime import timedelta
import datetime

now_time = datetime.datetime.now()


def str2datetime(str_time, fmt):
    t = time.strptime(str_time, fmt)
    year, month, day = t[:3]
    return datetime.date(year, month, day)


def create_task2(start_time, end_time, inspection_plan_number, inspection_period, now, inspection_project_ids):
    """
    生成从start_time到end_time的任务，并且不生成开始时间小于当前时间之前的计划
    :return:
    """
    now_time_str = datetime.datetime.strftime(now_time, '%Y-%m-%d')
    now_time_str_list = now_time_str.split('-')
    year = now_time_str_list[0]
    # 取出inspection_task_number中的数字并将其转换为int类型
    f_out = open('inspection_task_number.txt', 'r+')
    count = int(f_out.read())
    # 若想的end_time往后再生成一次任务就将"<"改为"<=",反之则将"<="改为"<"
    while start_time <= end_time:
        # 判断存储数据的日期是否在当前日期之前，不为在此日期前的的日期生成任务
        if start_time >= now:
            inspection_task_number = 'DJRW' + year + str(count).zfill(5)
            task_start_time = start_time
            task_end_time = start_time + timedelta(days=1)
            belong_plan = InspectionPlan.objects.get(inspection_plan_number=inspection_plan_number)
            inspection_project_count = len(inspection_project_ids)
            a = {'inspection_task_number': inspection_task_number, 'task_start_time': task_start_time,
                 'task_end_time': task_end_time, 'belong_plan': belong_plan,
                 'total_inspection_items': inspection_project_count}
            InspectionTask.objects.create(**a)
            # 以下添加点检任务与点检结果的关联
            inspection_task = InspectionTask.objects.get(inspection_task_number=inspection_task_number)
            create_inspection_result(inspection_task, inspection_project_ids)

            count += 1
        start_time = start_time + timedelta(days=int(inspection_period))
    # 删除文件中原来的数字，将现在的数字写入文件中
    f_out.seek(0)
    f_out.truncate()
    f_out.write(str(count))
    f_out.close()


# 生成与点检任务相关联的点检结果
def create_inspection_result(inspection_task, inspection_project_ids):
    for inspection_project_id in inspection_project_ids:
        inspection_project = InspectionProject.objects.get(id=inspection_project_id)
        InspectionResult.objects.create(inspection_project=inspection_project, inspection_task_number=inspection_task)


# 传入点检标准后返回传入标准下的所有的点检项目
def find_inspection_project(inspection_standard_list=None, inspection_standard_queryset=None):
    """
    :param inspection_standard_list: 传入的是点检标准的列表形式
    :param inspection_standard_queryset: 传入的是点检标准的queryset形式，不可以同时传入
    :return: 传来标准下的全部的点检项目的id，以列表形式返回
    """
    if inspection_standard_list:
        inspection_standard = InspectionStandard.objects.filter(inspection_standard_number__in=inspection_standard_list)
        # 现在任务是取出多个点检标准对应的点检项目
        # 直接从点检项目中查出符合点检标准的queryset
        inspection_project_list = InspectionProject.objects.filter(belong_inspection_standard__in=inspection_standard)
        inspection_project_dict = inspection_project_list.values('id')
        inspection_project_ids = []
        for _ in inspection_project_dict:
            inspection_project_ids.append(_['id'])
        return inspection_project_ids
    else:
        inspection_project_list = InspectionProject.objects.filter(belong_inspection_standard__in=inspection_standard_queryset)
        inspection_project_dict = inspection_project_list.values('id')
        inspection_project_ids = []
        for _ in inspection_project_dict:
            inspection_project_ids.append(_['id'])
        return inspection_project_ids
