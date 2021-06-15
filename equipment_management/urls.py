# from .views import LabelViewSet, OperationRecordViewSet, EquipmentViewSet
from rest_framework.routers import DefaultRouter
from django.urls import path, re_path, include
from .views import EquipmentListAPIView, EquipmentDetailAPIView

# router_equipment = DefaultRouter()
# router_equipment.register(r'labels', LabelViewSet)
# router_equipment.register(r'operations', OperationRecordViewSet)
# router_equipment.register(r'equipments', EquipmentViewSet)

urlpatterns = [
    path('equipments/', EquipmentListAPIView.as_view()),
    re_path('equipments/(?P<pk>.+)', EquipmentDetailAPIView.as_view()),
]
# 添加路由
# urlpatterns += router_equipment.urls
