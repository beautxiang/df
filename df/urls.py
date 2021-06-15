from django.contrib import admin
from rest_framework.documentation import include_docs_urls
from django.conf.urls import url
from django.urls import path, re_path, include
from django.views.static import serve
import equipment_management.urls
import maintenance_management.urls
import inspection_management.urls
from df.settings import MEDIA_ROOT
from django.conf.urls.static import static
from django.conf import settings
# 引入此库为了使用TokenAuthentication自带的生成token值的视图
from rest_framework.authtoken import views
from equipment_management.models import Department, Equipment
from equipment_management.serializers import DepartmentSerializer, EquipmentSerializer
from django.http import HttpResponse
from maintenance_management.models import MaintenanceStandard, MaintenancePlan
from maintenance_management.serializers import MaintenanceStandardSerializer, MaintenancePlanSerializer
from inspection_management.models import *
from inspection_management.serializers import *
from rest_framework.response import Response
from rest_framework.views import APIView


class test(APIView):
    def get(self, request):
        inspection_task = InspectionTask.objects.filter(belong_plan='DJJH-0013')
        print(InspectionResult.objects.filter(inspection_task_number__in=inspection_task).delete())

        return Response('ok')


urlpatterns = [
    path('admin/', admin.site.urls),
    # 配置此项才能在admin中访问图片
    # re_path(r'^media/(?P<path>.*)$', serve, {"document_root": MEDIA_ROOT}),
    path('api.equipment_management/', include(equipment_management.urls)),
    # path('api-auth/', include('rest_framework.urls')),  # 用户登录页面
    path('api.maintenance_management/', include(maintenance_management.urls)),
    path('api.inspection_management/', include(inspection_management.urls)),
    path('test/', test.as_view()),
    url(r'docs/', include_docs_urls(title='接口文档')),
]
# 配置此项才可以访问图片
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
