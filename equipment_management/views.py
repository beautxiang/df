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
from .models import Equipment, Label, OperationRecord, Department
from .serializers import EquipmentSerializer, LabelSerializer, OperationRecordSerializer, DepartmentSerializer

import pandas as pd

from .filter import EquipmentFilter
from equipment_management.admin import EquipmentResource


# # 定义分页器的一些基本设置
# class StandardPageNumberPagination(PageNumberPagination):
#     page_size = 5
#     page_query_param = 'page'
#     page_size_query_param = 'page_size'
#     max_page_size = 50
#
#
# class LabelViewSet(ModelViewSet):
#     queryset = Label.objects.all()
#     serializer_class = LabelSerializer
#
#
# class OperationRecordViewSet(ModelViewSet):
#     queryset = OperationRecord.objects.all()
#     serializer_class = OperationRecordSerializer
#
#
# class EquipmentViewSet(ModelViewSet):
#     queryset = Equipment.objects.all()
#     serializer_class = EquipmentSerializer
#     pagination_class = StandardPageNumberPagination
#     filter_backends = (DjangoFilterBackend, SearchFilter, OrderingFilter)
#     filterset_class = EquipmentFilter  # 这里面写的是要过滤的字段
#     # 设置搜索的filter，以设备名称和设备编号进行模糊查找
#     search_fields = ('equipment_number', 'equipment_name')
#     lookup_field = 'equipment_number'
#
#     # 写一个可以导出数据的方法，发送的url地址为http://127.0.0.1:8000/api.equipment_management/equipments/batch_export/
#     @action(methods=['get'], detail=False)
#     def batch_export(self, request):
#         # 获取查询参数并将其转换为字典类型
#         params = request.query_params
#         params = dict(params)
#         # 创建一个新字典，用来转换params的格式
#         new_dict = {}
#         for i, j in params.items():
#             j = ''.join(j)
#             new_dict[i] = j
#         # 消除掉字典中为空字符串''的查询条件
#         dict_key = list(new_dict.keys())
#         for i in dict_key:
#             if new_dict[i] == '':
#                 new_dict.pop(i)
#         # 进行过滤
#         equipment_resource = EquipmentResource()
#         equipments = self.get_queryset()
#         equipments = equipments.filter(**new_dict)
#
#         # 返回过滤后的excel表格
#         dataset = equipment_resource.export(equipments)
#         response = HttpResponse(dataset.xls, content_type='application/vnd.ms-excel')
#         response['Content-Disposition'] = 'attachment; filename="equipments.xls"'
#         return response

class EquipmentListAPIView(APIView):
    def get(self, request):
        equipment_list = Equipment.objects.all()
        ser = EquipmentSerializer(equipment_list, many=True)
        return Response(ser.data)

    def post(self, request):
        iser = EquipmentSerializer(data=request.data)
        if iser.is_valid():
            iser.save()  # 生成记录
            return Response(iser.data)
        else:
            return Response(iser.errors)


class EquipmentDetailAPIView(APIView):
    def get(self, request, pk):
        equipment_obj = Equipment.objects.filter(pk=pk).first()
        if equipment_obj is not None:
            ser = EquipmentSerializer(equipment_obj, many=False)
            return Response(ser.data)
        return Response({'msg': '无此编号的设备信息'}, status=status.HTTP_404_NOT_FOUND)

    def put(self, request, pk):
        equipment_obj = Equipment.objects.filter(pk=pk).first()

        iser = EquipmentSerializer(data=request.data, instance=equipment_obj)
        if iser.is_valid():
            iser.save()  # update
            return Response(iser.data)
        else:
            return Response(iser.errors)

    def delete(self, request, pk):
        Equipment.objects.filter(pk=pk).delete()
        return Response({'msg': '设备编号为' + str(pk) + '的设备信息已删除'})


class DepartmentAPIView(APIView):
    def get(self, request):
        pass

    def post(self, request):
        pass

    def put(self, request):
        pass

    def delete(self, request):
        pass

