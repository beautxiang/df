from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from django.db.models import Q
from .models import MaintenancePlan, MaintenanceStandard, MaintenanceType, MaintenanceTask
from .serializers import MaintenancePlanSerializer, MaintenanceStandardSerializer, MaintenanceTaskSerializer

import null as null
from django.http import HttpResponse
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework import status
from rest_framework.generics import GenericAPIView, CreateAPIView, ListAPIView, RetrieveAPIView, DestroyAPIView, \
    UpdateAPIView, ListCreateAPIView, RetrieveUpdateAPIView, RetrieveDestroyAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.mixins import CreateModelMixin, ListModelMixin, RetrieveModelMixin, UpdateModelMixin, \
    DestroyModelMixin
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet, ViewSet
from rest_framework.generics import CreateAPIView
from rest_framework.decorators import action
from rest_framework import status
import time, datetime
from datetime import timedelta
from .utils import str2datetime, create_task1


class MaintenanceStandardAPIView(APIView):
    def get(self, request):
        maintenance_list = MaintenanceStandard.objects.all()
        ser = MaintenanceStandardSerializer(maintenance_list, many=True)
        return Response(ser.data)

    def post(self, request):
        iser = MaintenanceStandardSerializer(data=request.data)
        if iser.is_valid():
            iser.save()  # 生成记录
            return Response(iser.data)
        else:
            return Response(iser.errors)


class MaintenanceStandardDetailAPIView(APIView):
    def get(self, request, pk):
        maintenance_obj = MaintenanceStandard.objects.filter(pk=pk).first()
        if maintenance_obj is not None:
            ser = MaintenanceStandardSerializer(maintenance_obj, many=False)
            return Response(ser.data)
        return Response({'msg': '没有此id的保养标准'}, status=status.HTTP_404_NOT_FOUND)

    def put(self, request, pk):
        maintenance_obj = MaintenanceStandard.objects.filter(pk=pk).first()

        iser = MaintenanceStandardSerializer(data=request.data, instance=maintenance_obj)
        if iser.is_valid():
            iser.save()  # update
            return Response(iser.data)
        else:
            return Response(iser.errors)

    def delete(self, request, pk):
        MaintenanceStandard.objects.filter(pk=pk).delete()
        return Response({'msg': 'id为' + str(pk) + '的保养标准已删除'}, status.HTTP_204_NO_CONTENT)


class MaintenancePlanAPIView(APIView):
    def get(self, request):
        # 在取数据之前对数据的plan_status进行校验
        time_now = time.strftime('%Y-%m-%d', time.localtime(time.time()))
        maintenance_plan_list = MaintenancePlan.objects.filter(start_time__gt=time_now).update(plan_status=0)
        maintenance_plan_list = MaintenancePlan.objects.filter(start_time__lte=time_now).update(plan_status=1)
        maintenance_plan_list = MaintenancePlan.objects.filter(end_time__lt=time_now).update(plan_status=2)

        maintenance_plan_list = MaintenancePlan.objects.all()
        ser = MaintenancePlanSerializer(maintenance_plan_list, many=True)
        return Response(ser.data)

    def post(self, request):
        time_now = time.strftime('%Y-%m-%d', time.localtime(time.time()))
        # 转换字符串到datetime格式
        now = datetime.date.fromisoformat(time_now)
        iser = MaintenancePlanSerializer(data=request.data)
        # 转换数据格式为datetime以便于生成保养任务
        fmt = '%Y-%m-%d'
        start_time = str2datetime(request.data['start_time'], fmt)
        end_time = str2datetime(request.data['end_time'], fmt)
        maintenance_plan_number = request.data['maintenance_plan_number']
        maintenance_time_point = request.data['maintenance_time_point']

        if iser.is_valid():
            # 生成记录后为自动为计划创建任务根据的是maintenance_time_point提供的时间点来创建的
            iser.save()  # 生成记录
            create_task1(start_time, end_time, maintenance_plan_number, maintenance_time_point, now)
            return Response(iser.data)
        else:
            return Response(iser.errors)


class MaintenancePlanDetailAPIView(APIView):
    def get(self, request, pk):
        # 在取数据之前对数据的plan_status进行校验
        time_now = time.strftime('%Y-%m-%d', time.localtime(time.time()))
        maintenance_plan_list = MaintenancePlan.objects.filter(start_time__gt=time_now).update(plan_status=0)
        maintenance_plan_list = MaintenancePlan.objects.filter(start_time__lte=time_now).update(plan_status=1)
        maintenance_plan_list = MaintenancePlan.objects.filter(end_time__lt=time_now).update(plan_status=2)

        maintenance_plan_obj = MaintenancePlan.objects.filter(pk=pk).first()
        if maintenance_plan_obj is not None:
            ser = MaintenancePlanSerializer(maintenance_plan_obj, many=False)
            return Response(ser.data)
        return Response({'msg': '没有此id的保养计划'}, status=status.HTTP_404_NOT_FOUND)

    def put(self, request, pk):
        # 尝试着用get_or_create()来解决所需要的需求
        maintenance_plan_obj = MaintenancePlan.objects.filter(pk=pk).first()
        # 转换字符串到datetime格式
        fmt = '%Y-%m-%d'
        # 得到当前时间
        time_now = time.strftime('%Y-%m-%d', time.localtime(time.time()))
        now = datetime.date.fromisoformat(time_now)

        # 得到了修改前修改后开始结束时间
        start_time_after = str2datetime(request.data['start_time'], fmt)
        end_time_after = str2datetime(request.data['end_time'], fmt)
        start_time_before = maintenance_plan_obj.start_time
        end_time_before = maintenance_plan_obj.end_time

        # 获取未修改前的计划状态，下面会用到计划状态来进行判断
        plan_status = maintenance_plan_obj.plan_status

        # 获取循环周期
        maintenance_time_point = maintenance_plan_obj.maintenance_time_point

        # 获取计划编号
        maintenance_plan_number = maintenance_plan_obj.maintenance_plan_number

        # 当计划的状态为已完成时，不允许对其进行修改
        if plan_status == 2:
            return Response({'msg': '不允许对已完成的计划进行操作'})
        # 当计划状态为未开始时，对其进行修改的方式就是重建一个
        if plan_status == 0:
            MaintenancePlan.objects.filter(pk=pk).delete()
            iser = MaintenancePlanSerializer(data=request.data)
            if iser.is_valid():
                # .save()方法执行的update方法如果需要重写则需要在serializers.py中找到相应的序列化器进行重写
                iser.save()  # update
                create_task1(start_time_after, end_time_after, maintenance_plan_number, maintenance_time_point, now)
                return Response(iser.data)
            else:
                return Response(iser.errors)
        # 当计划在进行中的时候，不允许对开始时间进行修改，但是对结束时间可以有相应的修改
        if plan_status == 1:
            iser = MaintenancePlanSerializer(data=request.data, instance=maintenance_plan_obj)
            # 如果结束时间提前
            if end_time_after < end_time_before:
                # 当结束时间大于现在时刻的时间
                if end_time_after >= now:
                    # 筛选出原任务结束时间大于当前任务结束时间的所有任务，将其进行删除
                    MaintenanceTask.objects.filter(belong_plan=maintenance_plan_number).filter(
                        task_end_time__gt=end_time_after).delete()
                    if iser.is_valid():
                        # .save()方法执行的update方法如果需要重写则需要在serializers.py中找到相应的序列化器进行重写
                        iser.save()  # update
                        return Response(iser.data)
                    else:
                        return Response(iser.errors)
                if end_time_after < now:
                    MaintenanceTask.objects.filter(belong_plan=maintenance_plan_number).filter(
                        task_end_time__gte=now).delete()
                    if iser.is_valid():
                        # .save()方法执行的update方法如果需要重写则需要在serializers.py中找到相应的序列化器进行重写
                        iser.save()  # update
                        return Response(iser.data)
                    else:
                        return Response(iser.errors)
            # 如果结束时间未变化，则不对其进行操作
            if end_time_after == end_time_before:
                iser = MaintenancePlanSerializer(data=request.data, instance=maintenance_plan_obj)
                if iser.is_valid():
                    # .save()方法执行的update方法如果需要重写则需要在serializers.py中找到相应的序列化器进行重写
                    iser.save()  # update
                    return Response(iser.data)
                else:
                    return Response(iser.errors)
            # 当结束时间大于原结束时间，则新增从原结束时间开始到当前结束时间的任务
            if end_time_after > end_time_before:
                iser = MaintenancePlanSerializer(data=request.data, instance=maintenance_plan_obj)
                if iser.is_valid():
                    iser.save()  # update
                    create_task1(end_time_before, end_time_after, maintenance_plan_number, maintenance_time_point, now)
                    return Response(iser.data)
                else:
                    return Response(iser.errors)

    def delete(self, request, pk):
        MaintenancePlan.objects.filter(pk=pk).delete()
        return Response({'msg': 'id为' + str(pk) + '的保养计划已删除'}, status.HTTP_204_NO_CONTENT)


class MaintenanceTaskAPIView(APIView):
    def get(self, request):
        time_now = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
        # 任务开始时间大于当前时间则会对task_status置0
        MaintenanceTask.objects.filter(task_start_time__gt=time_now).update(task_status=0)
        # 任务开始时间小于等于当前时间会对task_status置1
        MaintenanceTask.objects.filter(task_start_time__lte=time_now).update(task_status=1)
        # 任务结束时间小于当前时间会对task_status置2
        MaintenanceTask.objects.filter(task_end_time__lt=time_now).update(task_status=2)
        # 任务结束时间小于当前时间且保养记录未填写会对task_status置3
        # 这段代码的意思是对于当前时间大于任务结束时间并且保养内容为null或者空字符串就将任务状态置为3（未完成）
        MaintenanceTask.objects.filter(
            Q(task_end_time__lt=time_now) & (Q(maintenance_record=None) | Q(maintenance_record=''))).update(
            task_status=3)

        maintenance_task_list = MaintenanceTask.objects.all()
        ser = MaintenanceTaskSerializer(maintenance_task_list, many=True)
        return Response(ser.data)


class MaintenanceTaskDetailAPIView(APIView):
    def get(self, request, pk):
        maintenance_task_obj = MaintenanceTask.objects.filter(pk=pk).first()
        if maintenance_task_obj is not None:
            ser = MaintenanceTaskSerializer(maintenance_task_obj, many=False)
            return Response(ser.data)
        return Response({'msg': '没有此编号的的保养任务'}, status=status.HTTP_404_NOT_FOUND)

    # 等做完权限管理再来到这里写一些负责人，验收人相关的权限控制，或者对负责人与验收人不再公用一套put方法（可能并不好），再或者让前端去检验
    def put(self, request, pk):
        maintenance_task_obj = MaintenanceStandard.objects.filter(pk=pk).first()
        task_status = maintenance_task_obj.task_status

        # 任务未开始，已完成，未完成，均不再允许对其进行操作
        if task_status == 0 or 2 or 3:
            return Response({'msg': '当前时间不允许对对其进行编辑'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)
        # 任务进行中，允许对其进行操作。
        if task_status == 1:
            iser = MaintenanceTaskSerializer(data=request.data, instance=maintenance_task_obj)
            if iser.is_valid():
                iser.save()  # update
                return Response(iser.data)
            else:
                return Response(iser.errors)

    # 这个功能是为有权限的人定制的，一般人没有删除的权限
    def delete(self, request, pk):
        MaintenanceStandard.objects.filter(pk=pk).delete()
        return Response({'msg': 'id为' + str(pk) + '的保养任务已删除'}, status.HTTP_204_NO_CONTENT)
