from django.urls import path, re_path, include
from .views import InspectionPlanListAPIView, InspectionStandardListAPIView, InspectionPlanDetailAPIView,\
    InspectionResultAPIView, InspectionProjectDetailAPIView, \
    InspectionStandardDetailAPIView, InspectionTaskDetailAPIView, InspectionTaskListAPIView,\
    InspectionProjectListAPIView

urlpatterns = [
    path('inspection_standard/', InspectionStandardListAPIView.as_view()),
    re_path('inspection_standard/(?P<pk>.+)', InspectionStandardDetailAPIView.as_view()),
    path('inspection_project/', InspectionProjectListAPIView.as_view()),
    re_path('inspection_project/(?P<pk>.+)', InspectionProjectDetailAPIView.as_view()),
    path('inspection_plan/', InspectionPlanListAPIView.as_view()),
    re_path('inspection_plan/(?P<pk>.+)', InspectionPlanDetailAPIView.as_view()),
    path('inspection_task/', InspectionTaskListAPIView.as_view()),
    re_path('inspection_task/(?P<pk>.+)', InspectionTaskDetailAPIView.as_view()),
    path('inspection_result/', InspectionResultAPIView.as_view()),
]
