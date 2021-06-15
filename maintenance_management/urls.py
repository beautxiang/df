from rest_framework.routers import DefaultRouter
# from .views import MaintenanceStandardViewSet, MaintenancePlanViewSet
from .views import MaintenanceStandardAPIView, MaintenanceStandardDetailAPIView, MaintenancePlanAPIView, \
    MaintenancePlanDetailAPIView, MaintenanceTaskAPIView, MaintenanceTaskDetailAPIView
from django.urls import path, re_path, include

# router_equipment = DefaultRouter()
# router_equipment.register(r'maintenance_information', MaintenanceStandardViewSet)
# router_equipment.register(r'maintenance_plans', MaintenancePlanViewSet)


urlpatterns = [
    path('maintenance/', MaintenanceStandardAPIView.as_view()),
    re_path('maintenance/(?P<pk>.+)', MaintenanceStandardDetailAPIView.as_view()),
    path('maintenance_plan/', MaintenancePlanAPIView.as_view()),
    re_path('maintenance_plan/(?P<pk>.+)', MaintenancePlanDetailAPIView.as_view()),
    path('maintenance_task/', MaintenanceTaskAPIView.as_view()),
    re_path('maintenance_task/(?P<pk>.+)', MaintenanceTaskDetailAPIView.as_view()),
]
# 添加路由
# urlpatterns += router_equipment.urls
