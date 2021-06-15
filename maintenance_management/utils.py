import time

from maintenance_management.models import MaintenancePlan, MaintenanceTask
from datetime import timedelta
import datetime

now_time = datetime.datetime.now()


def str2datetime(str_time, fmt):
    t = time.strptime(str_time, fmt)
    year, month, day = t[:3]
    return datetime.date(year, month, day)


def create_task1(start_time, end_time, maintenance_plan_number, maintenance_time_point, now):
    """
    生成从start_time到end_time的任务，并且不生成开始时间小于当前时间之前的计划
    :return:
    """
    now_time_str = datetime.datetime.strftime(now_time, '%Y-%m-%d')
    now_time_str_list = now_time_str.split('-')
    year = now_time_str_list[0]
    # 取出task_number中的数字并将其转换为int类型
    f_out = open('maintenance_task_number.txt', 'r+')
    count = int(f_out.read())
    # 若想的end_time往后再生成一次任务就将"<"改为"<=",反之则将"<="改为"<"
    while start_time <= end_time:
        # 判断存储数据的日期是否在当前日期之前，不为在此日期前的的日期生成计划
        if start_time >= now:
            task_number = 'BYRW' + year + str(count).zfill(5)
            task_start_time = start_time
            task_end_time = start_time + timedelta(days=1)
            belong_plan = MaintenancePlan.objects.get(maintenance_plan_number=maintenance_plan_number)
            a = {'task_number': task_number, 'task_start_time': task_start_time, 'task_end_time': task_end_time, 'belong_plan': belong_plan}
            MaintenanceTask.objects.create(**a)
            count += 1
        start_time = start_time + timedelta(days=int(maintenance_time_point))
    # 删除文件中原来的数字，将现在的数字写入文件中
    f_out.seek(0)
    f_out.truncate()
    f_out.write(str(count))
    f_out.close()