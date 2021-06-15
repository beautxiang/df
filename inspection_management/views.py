from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet, ViewSet
from rest_framework.generics import CreateAPIView
from rest_framework.decorators import action
from rest_framework import status
from .models import InspectionTask, InspectionProject, InspectionStandard, InspectionPlan, InspectionResult
from .serializers import *
import time, datetime
from datetime import timedelta
from .utils import create_task2, str2datetime, find_inspection_project, create_inspection_result
from django.db.models import Q, F


# 接受的url形式为http://127.0.0.1:8000/api.inspection_management/inspection_standard/
class InspectionStandardListAPIView(APIView):
    """
    get请求发送url：返回点检标准列表页面填写所需的信息
    post请求发送url：新增一个点检标准，只有在数据库中建立好点检标准之后才可以在标准中添加点检项目
    """

    # 返回所有的点检标准
    def get(self, request):
        inspection_standard_list = InspectionStandard.objects.all()
        ser = InspectionStandardListSerializer(inspection_standard_list, many=True)
        return Response(ser.data)

    # 新增一个点检标准
    def post(self, request):
        iser = InspectionStandardSerializer(data=request.data)
        if iser.is_valid():
            iser.save()  # 生成记录
            return Response(iser.data)
        else:
            return Response(iser.errors)


# 接受的url形式为http://127.0.0.1:8000/api.inspection_management/inspection_standard/标准编号
class InspectionStandardDetailAPIView(APIView):
    """
    get请求发送url：返回该标准的内容以及该标准下所有的点检项目
    put请求发送url：只能修改点检标准，不能够对点检项目中的数据进行修改，若要修改点检项目中的数据，需要对点检项目发送响应的url
    delete请求发送url：删除响应点检标准及以下全部的点检项目
    """

    # 返回单个的点检标准，若数据库中没有此条信息则返回msg：没有此id的点检标准
    def get(self, request, pk):
        inspection_standard_obj = InspectionStandard.objects.filter(pk=pk).first()
        if inspection_standard_obj is not None:
            ser = InspectionStandardSerializer(inspection_standard_obj, many=False)
            return Response(ser.data)
        return Response({'msg': '没有此id的点检标准'}, status=status.HTTP_404_NOT_FOUND)

    # 修改一条点检标准
    def put(self, request, pk):
        inspection_standard_obj = InspectionStandard.objects.filter(pk=pk).first()

        iser = InspectionStandardSerializer(data=request.data, instance=inspection_standard_obj)
        if iser.is_valid():
            iser.save()  # update
            return Response(iser.data)
        else:
            return Response(iser.errors)

    # 删除一条点检标准，连同此标准下的点检项全部删除
    def delete(self, request, pk):
        InspectionStandard.objects.filter(pk=pk).delete()
        return Response({'msg': 'id为' + str(pk) + '的点检标准已删除'}, status.HTTP_204_NO_CONTENT)


# 接受的url形式为http://127.0.0.1:8000/api.inspection_management/inspection_project/
class InspectionProjectListAPIView(APIView):
    """
    post请求发送url：需要传入该点检项目对应的点检计划，这样就将二者关联起来了
    """

    # 新增一个点检项目，点检项目无需查看，因为在点检标准中已经全部给出了
    def post(self, request):
        iser = InspectionProjectSerializer(data=request.data)
        if iser.is_valid():
            iser.save()  # 生成记录
            return Response(iser.data)
        else:
            return Response(iser.errors)


# 接受的url形式为http://127.0.0.1:8000/api.inspection_management/inspection_project/点检项目id
class InspectionProjectDetailAPIView(APIView):
    """
    put请求发送url：更改这个id的点检项目的信息
    delete请求发送url：删除这个id的点检项目的信息（不会连带点检标准一起删除）
    """

    # 修改一个点检项目
    def put(self, request, pk):
        inspection_project_obj = InspectionProject.objects.filter(pk=pk).first()

        iser = InspectionProjectSerializer(data=request.data, instance=inspection_project_obj)
        if iser.is_valid():
            iser.save()  # update
            return Response(iser.data)
        else:
            return Response(iser.errors)

    # 删除一个点检项目
    def delete(self, request, pk):
        InspectionProject.objects.filter(pk=pk).delete()
        return Response({'msg': 'id为' + str(pk) + '的点检项目已删除'}, status.HTTP_204_NO_CONTENT)


# 接受的url形式为http://127.0.0.1:8000/api.inspection_management/inspection_plan/
class InspectionPlanListAPIView(APIView):
    """
    get请求发送url：取出点检计划列表形式的数据传给前端
    post请求发送url：接受前端传来的生成点检计划的参数，并且按照周期切分自动生成相应数量的点检任务
    """

    def get(self, request):
        # 在取数据之前对InspectionPlan进行校验，判断计划的状态
        time_now = time.strftime('%Y-%m-%d', time.localtime(time.time()))
        InspectionPlan.objects.filter(start_time__gt=time_now).update(plan_status=0)
        InspectionPlan.objects.filter(start_time__lte=time_now).update(plan_status=1)
        InspectionPlan.objects.filter(end_time__lt=time_now).update(plan_status=2)

        inspection_plan_list = InspectionPlan.objects.all()
        ser = InspectionPlanListSerializer(inspection_plan_list, many=True)
        return Response(ser.data)

    # 这里实现了点检任务的生成和点检结果的生成
    def post(self, request):
        time_now = time.strftime('%Y-%m-%d', time.localtime(time.time()))
        # 转换字符串到datetime格式
        now = datetime.date.fromisoformat(time_now)
        # 转换数据格式为datetime以便于生成保养任务
        fmt = '%Y-%m-%d'
        start_time = str2datetime(request.data['start_time'], fmt)
        end_time = str2datetime(request.data['end_time'], fmt)
        inspection_plan_number = request.data['inspection_plan_number']
        inspection_period = request.data['inspection_period']
        inspection_standard = request.data['inspection_standard']

        # 得到点检标准下的所有点检项目的id
        inspection_project_ids = find_inspection_project(inspection_standard)
        # 以上实现了得到符合点检标准的全部点检项目的id

        # 点检结果的关联(已经在create_task2中完成关联)
        iser = InspectionPlanSerializer(data=request.data)
        if iser.is_valid():
            # 生成记录后为自动为计划创建任务根据的是maintenance_time_point提供的时间点来创建的
            iser.save()  # 生成记录
            create_task2(start_time, end_time, inspection_plan_number, inspection_period, now, inspection_project_ids)
            return Response(iser.data)
        else:
            return Response(iser.errors)


# 接受的url形式为http://127.0.0.1:8000/api.inspection_management/inspection_plan/点检标准编号
class InspectionPlanDetailAPIView(APIView):
    """
    get请求发送url：得到一个点检计划的详情内容
    put请求发送url：修改这个计划的内容
    delete请求发送url：删除掉这个计划，但不会删除关联的点检标准
    """

    def get(self, request, pk):
        inspection_plan_obj = InspectionPlan.objects.filter(pk=pk).first()
        if inspection_plan_obj is not None:
            ser = InspectionPlanSerializer(inspection_plan_obj, many=False)
            return Response(ser.data)
        return Response({'msg': '没有此id的点检计划'}, status=status.HTTP_404_NOT_FOUND)

    # 这里是一个大块，需要理清所需要的逻辑
    # 下午将new note（2）中的逻辑用代码来实现
    def put(self, request, pk):
        inspection_plan_obj = InspectionPlan.objects.filter(pk=pk).first()

        # 转换字符串到datetime格式
        fmt = '%Y-%m-%d'
        # 得到当前时间
        time_now = time.strftime('%Y-%m-%d', time.localtime(time.time()))
        now = datetime.date.fromisoformat(time_now)

        # 得到了修改前修改后开始结束时间
        start_time_after = str2datetime(request.data['start_time'], fmt)
        end_time_after = str2datetime(request.data['end_time'], fmt)
        start_time_before = inspection_plan_obj.start_time
        end_time_before = inspection_plan_obj.end_time

        # 获取未修改前的计划状态，下面会用到计划状态来进行判断
        plan_status = inspection_plan_obj.plan_status

        # 获取循环周期
        inspection_period = inspection_plan_obj.inspection_period

        # 获取计划编号
        inspection_plan_number = inspection_plan_obj.inspection_plan_number

        # 得到前端传来的点检标准
        inspection_standard = request.data['inspection_standard']
        inspection_project_ids_after = find_inspection_project(inspection_standard_list=inspection_standard)

        # 得到原来的计划中的点检标准
        inspection_standard_before = inspection_plan_obj.inspection_standard.all()
        inspection_project_ids_before = find_inspection_project(inspection_standard_queryset=inspection_standard_before)

        # 当计划的状态为已完成时，不允许对其进行修改
        if plan_status == 2:
            return Response({'msg': '不允许对已完成的计划进行操作'})
        # 当计划未开始的时候，允许对其进行修改，并且可以修改巡检项
        if plan_status == 0:
            # 取出与点检标准相关的点检项目的id
            InspectionPlan.objects.filter(pk=pk).delete()
            inspection_project_ids = find_inspection_project(inspection_standard)

            iser = InspectionPlanSerializer(data=request.data)
            if iser.is_valid():
                # 生成记录后为自动为计划创建任务根据的是maintenance_time_point提供的时间点来创建的
                iser.save()  # 生成记录
                create_task2(start_time_after, end_time_after, inspection_plan_number, inspection_period, now, inspection_project_ids)
                return Response(iser.data)
            else:
                return Response(iser.errors)
        # 当计划在进行中的时候，不允许对开始时间进行修改，但是对结束时间可以有相应的修改
        # 计划进行的时候可以对巡检项进行相应的修改，修改对以前的任务没有影响，但是对未来还没有做的任务有影响
        # 影响就是未来的任务需要加上修改后的巡检项，以前的则不需要加上
        if plan_status == 1:
            iser = InspectionPlanSerializer(data=request.data, instance=inspection_plan_obj)
            # 结束时间提前且巡检项有所变化
            if (end_time_after < end_time_before) and (inspection_project_ids_after != inspection_project_ids_before):
                # 如果结束时间提前到当前时间之前（前端会对此进行限制，但这里还是做出了约束），返回如下信息
                if end_time_after < now:
                    return Response({'msg': '不能提前计划在当前时间之前'})
                # 若不会提前到当前时间之前
                else:
                    # 删除掉在时间大于当前时间的点检任务，相应的点检项会跟着删除
                    InspectionTask.objects.filter(belong_plan=inspection_plan_number).filter(task_end_time__gt=end_time_after+timedelta(days=1)).delete()
                    # 筛选出当前剩余的开始时间大于当前时间的任务
                    inspection_tasks = InspectionTask.objects.filter(belong_plan=inspection_plan_number).filter(task_start_time__gt=now)
                    # 将它们对应的点检结果全部删除
                    InspectionResult.objects.filter(inspection_task_number__in=inspection_tasks).delete()
                    # 按照新的点检项生成点检结果表
                    for inspection_task in inspection_tasks:
                        create_inspection_result(inspection_task, inspection_project_ids_after)
                    if iser.is_valid():
                        # .save()方法执行的update方法如果需要重写则需要在serializers.py中找到相应的序列化器进行重写
                        iser.save()  # update
                        return Response(iser.data)
                    else:
                        return Response(iser.errors)

            # 结束时间提前且巡检项没有变化
            elif (end_time_after < end_time_before) and (inspection_project_ids_after == inspection_project_ids_before):
                if end_time_after < now:
                    return Response({'msg': '不能提前计划在当前时间之前'})
                else:
                    InspectionTask.objects.filter(belong_plan=inspection_plan_number).filter(
                        task_end_time__gt=end_time_after + timedelta(days=1)).delete()
                    if iser.is_valid():
                        # .save()方法执行的update方法如果需要重写则需要在serializers.py中找到相应的序列化器进行重写
                        iser.save()  # update
                        return Response(iser.data)
                    else:
                        return Response(iser.errors)
            # 结束时间不变且巡检项有所变化
            elif (end_time_after == end_time_before) and (inspection_project_ids_after != inspection_project_ids_before):
                # 筛选出当前剩余的开始时间大于当前时间的任务
                inspection_tasks = InspectionTask.objects.filter(belong_plan=inspection_plan_number).filter(
                    task_start_time__gt=now)
                # 将它们对应的点检结果全部删除
                InspectionResult.objects.filter(inspection_task_number__in=inspection_tasks).delete()
                # 按照新的点检项生成点检结果表
                for inspection_task in inspection_tasks:
                    create_inspection_result(inspection_task, inspection_project_ids_after)
                if iser.is_valid():
                    # .save()方法执行的update方法如果需要重写则需要在serializers.py中找到相应的序列化器进行重写
                    iser.save()  # update
                    return Response(iser.data)
                else:
                    return Response(iser.errors)
            # 结束时间不变且巡检项没有变化
            elif (end_time_after == end_time_before) and (inspection_project_ids_after == inspection_project_ids_before):
                if iser.is_valid():
                    # .save()方法执行的update方法如果需要重写则需要在serializers.py中找到相应的序列化器进行重写
                    iser.save()  # update
                    return Response(iser.data)
                else:
                    return Response(iser.errors)
            # 结束时间推后且巡检项有所变化
            elif (end_time_after > end_time_before) and (inspection_project_ids_after != inspection_project_ids_before):
                create_task2(end_time_before + timedelta(days=1), end_time_after, inspection_plan_number, inspection_period, now, inspection_project_ids_after)
                # 筛选出当前剩余的开始时间大于当前时间的任务
                inspection_tasks = InspectionTask.objects.filter(belong_plan=inspection_plan_number).filter(
                    task_start_time__gt=now)
                # 将它们对应的点检结果全部删除
                InspectionResult.objects.filter(inspection_task_number__in=inspection_tasks).delete()
                # 按照新的点检项生成点检结果表
                for inspection_task in inspection_tasks:
                    create_inspection_result(inspection_task, inspection_project_ids_after)
                if iser.is_valid():
                    # .save()方法执行的update方法如果需要重写则需要在serializers.py中找到相应的序列化器进行重写
                    iser.save()  # update
                    return Response(iser.data)
                else:
                    return Response(iser.errors)
            # 结束时间推后且巡检项没有变化
            elif (end_time_after > end_time_before) and (inspection_project_ids_after == inspection_project_ids_before):
                create_task2(end_time_before + timedelta(days=1), end_time_after, inspection_plan_number, inspection_period, now, inspection_project_ids_after)
                if iser.is_valid():
                    # .save()方法执行的update方法如果需要重写则需要在serializers.py中找到相应的序列化器进行重写
                    iser.save()  # update
                    return Response(iser.data)
                else:
                    return Response(iser.errors)


    # 删除点检计划后，相应的点检任务以及点检结果都会被删除，所以一般不能随便使用
    def delete(self, request, pk):
        InspectionPlan.objects.filter(pk=pk).delete()
        return Response({'msg': 'id为' + str(pk) + '的点检计划已删除'}, status.HTTP_204_NO_CONTENT)


# 接受的url形式为：http://127.0.0.1:8000/api.inspection_management/inspection_task/
class InspectionTaskListAPIView(APIView):
    """
    get请求发送url：返回所有的点检任务给前端
    """

    def get(self, request):
        time_now = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
        # 任务开始时间大于当前时间则会对task_status置0(未开始)
        InspectionTask.objects.filter(task_start_time__gt=time_now).update(task_status=0)
        # 任务开始时间小于等于当前时间会对task_status置1(进行中)
        InspectionTask.objects.filter(task_start_time__lte=time_now).update(task_status=1)
        # 任务结束时间小于当前时间会对task_status置3(未完成)
        InspectionTask.objects.filter(task_end_time__lt=time_now).update(task_status=3)
        # 任务结束时间小于当前时间且保养记录未填写会对task_status置2
        # 这段代码的意思是对于当前时间大于任务结束时间并且已检项等于总点检项时就将任务状态置为2（未完成）
        InspectionTask.objects.filter(
            Q(task_end_time__lt=time_now) & (Q(checked_the_number=F('total_inspection_items')))).update(
            task_status=2)

        inspection_task_list = InspectionTask.objects.all()
        ser = InspectionTaskListSerializer(inspection_task_list, many=True)
        return Response(ser.data)


# 接受的url形式为：http://127.0.0.1:8000/api.inspection_management/inspection_task/点检任务编号
class InspectionTaskDetailAPIView(APIView):
    """
    get请求发送url：返回相应点检任务的详情页面
    delete请求发送url：只能由有相应权限的角色才能使用此功能，删除一个点检任务
    """

    # 增加了统计任务的已检数的个数
    def get(self, request, pk):
        inspection_task_obj = InspectionTask.objects.filter(pk=pk).first()
        # 统计了某一点检任务下的已检项的个数
        inspection_result_list = InspectionResult.objects.filter(inspection_task_number=inspection_task_obj)
        checked_the_number = 0
        for inspection_result_obj in inspection_result_list:
            if inspection_result_obj.inspection_value and inspection_result_obj.is_unusual:
                checked_the_number += 1

        if inspection_task_obj is not None:
            # 改变取得点检任务的点检项的值
            inspection_task_obj.checked_the_number = checked_the_number
            inspection_task_obj.save()
            ser = InspectionTaskSerializer(inspection_task_obj, many=False)
            return Response(ser.data)
        return Response({'msg': '没有此编号的的点检任务'}, status=status.HTTP_404_NOT_FOUND)

    # 这个功能是为有权限的人定制的，一般人没有删除的权限
    def delete(self, request, pk):
        InspectionTask.objects.filter(pk=pk).delete()
        return Response({'msg': 'id为' + str(pk) + '的点检任务已删除'}, status.HTTP_204_NO_CONTENT)


# 接受的url形式：http://127.0.0.1:8000/api.inspection_management/inspection_result/?inspection_standard_number=DJBZ-0001&inspection_task_number=DJRW-0001
class InspectionResultAPIView(APIView):
    """
    get请求发送url：需要前端传入相应的inspection_standard_number，inspection_task_number，即可返回对应的点检结果和点检项目给前端
    put请求发送url：前端将点检结果和是否异常填入，若为批量发送需要遵循json格式，以点检结果的id为主键，去数据库中修改相应的值
    """

    # 返回一个点检任务下对应的点检标准中点检项的值
    # 需要的参数是点检任务编号，点检标准编号
    def get(self, request):
        # 得到前端传来的查询参数，分别是点检标准编号和点检任务编号
        inspection_standard_number = request.query_params['inspection_standard_number']
        inspection_task_number = request.query_params['inspection_task_number']
        # 得到该点检标准下的点检标准编号为inspection_standard_number的点检标准
        inspection_standard_obj = InspectionStandard.objects.filter(
            inspection_standard_number=inspection_standard_number).first()
        # 从点检任务中筛选出所有点检编号为inspection_task_number的点检任务
        inspection_result_list = InspectionResult.objects.filter(inspection_task_number=inspection_task_number)
        # 取到了id，下一步就是去得到相应的任务即可。
        print(inspection_standard_obj.inspectionproject_set.values_list('id'))
        inspection_project_id = inspection_standard_obj.inspectionproject_set.values('id')

        # 取出点检标准中对应的点检项目
        id_list = []
        for i in inspection_project_id:
            id_list.append(i['id'])

        # 取出点检结果中与其对应的结果
        inspection_result_list = inspection_result_list.filter(inspection_project__in=id_list)
        ser = InspectionResultSerializer(inspection_result_list, many=True)
        return Response(ser.data)

    def put(self, request):
        # 批量修改接口完成，下一步在测试的过程中添加异常处理机制
        # try:
        for result in request.data:
            InspectionResult.objects.filter(id=result['id']).update(inspection_value=result['inspection_value'],
                                                                    is_unusual=result['is_unusual'])
        return Response({'msg': '数据已修改'})
        # except:
        #     return Response({'msg': '未知错误'})
