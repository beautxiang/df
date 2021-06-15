from rest_framework import serializers
from rest_framework.fields import SerializerMethodField

from .models import InspectionTask, InspectionProject, InspectionStandard, InspectionPlan, InspectionResult


class InspectionProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = InspectionProject
        fields = '__all__'


# 为点检标准详情页面提供的序列化器
class InspectionStandardSerializer(serializers.ModelSerializer):
    equipment_name = serializers.ReadOnlyField(source='equipment_number.equipment_name')
    storage_place = serializers.ReadOnlyField(source='equipment_number.storage_place')
    # 反向关联查询需要带上_set
    inspection_project = InspectionProjectSerializer(many=True, read_only=True, source='inspectionproject_set')

    class Meta:
        model = InspectionStandard
        fields = '__all__'


# 为点检标准列表页面提供的序列化器，为了前端能够更有针对性的索要数据
class InspectionStandardListSerializer(serializers.ModelSerializer):
    equipment_name = serializers.ReadOnlyField(source='equipment_number.equipment_name')
    storage_place = serializers.ReadOnlyField(source='equipment_number.storage_place')

    class Meta:
        model = InspectionStandard
        fields = '__all__'


class InspectionPlanSerializer(serializers.ModelSerializer):
    # 若需要全部的内容将inspection_standards = InspectionStandardListSerializer(many=True, read_only=True, source='inspection_standard')
    # 更改为inspection_standards = InspectionStandardSerializer(many=True, read_only=True, source='inspection_standard')
    inspection_standards = InspectionStandardListSerializer(many=True, read_only=True, source='inspection_standard')
    inspection_standard = serializers.PrimaryKeyRelatedField(queryset=InspectionStandard.objects.all(),
                                                             write_only=True, many=True)

    class Meta:
        model = InspectionPlan
        fields = '__all__'


class InspectionPlanListSerializer(serializers.ModelSerializer):
    class Meta:
        model = InspectionPlan
        fields = '__all__'


class InspectionTaskSerializer(serializers.ModelSerializer):
    # 与点检计划相同，若想显示所有数据参考class InspectionPlanSerializer(serializers.ModelSerializer):中的注释
    inspection_standards = InspectionStandardListSerializer(many=True, read_only=True,
                                                        source='belong_plan.inspection_standard')

    # inspection_standard = SerializerMethodField()
    #     # MyCharField(
    #     # source='belong_plan.inspection_standard.all')

    class Meta:
        model = InspectionTask
        # fields = '__all__'
        exclude = ('inspection_projects',)


class InspectionTaskListSerializer(serializers.ModelSerializer):
    class Meta:
        model = InspectionTask
        # fields = '__all__'
        exclude = ('inspection_projects',)


class InspectionResultSerializer(serializers.ModelSerializer):
    part_or_project = serializers.PrimaryKeyRelatedField(read_only=True, source='inspection_project.part_or_project')
    inspection_content = serializers.PrimaryKeyRelatedField(read_only=True,
                                                            source='inspection_project.inspection_content')
    inspection_method = serializers.PrimaryKeyRelatedField(read_only=True,
                                                           source='inspection_project.inspection_method')
    scrutiny_standard = serializers.PrimaryKeyRelatedField(read_only=True,
                                                           source='inspection_project.scrutiny_standard')
    belong_inspection_standard = serializers.PrimaryKeyRelatedField(read_only=True,
                                                                    source='inspection_project.belong_inspection_standard')

    class Meta:
        model = InspectionResult
        fields = '__all__'
