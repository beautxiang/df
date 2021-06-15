import time
from rest_framework import serializers
from .models import MaintenancePlan, MaintenanceStandard, MaintenanceTask
from equipment_management.models import Equipment
from equipment_management.serializers import EquipmentSerializer


class MaintenanceStandardSerializer(serializers.ModelSerializer):
    equipment_name = serializers.ReadOnlyField(source='equipment_number.equipment_name')
    # 像这样写就无法得到设备信息的数据，因为在未命名的情况下，判断的是equipment_number，而现在指定的是equipment，不在其中。
    # equipment = EquipmentSerializer(read_only=True)
    # 这样写才可以
    # equipment = EquipmentSerializer(read_only=True, source='equipment_number')

    class Meta:
        model = MaintenanceStandard
        fields = '__all__'


class MaintenancePlanSerializer(serializers.ModelSerializer):
    # maintenancestandards = MaintenanceStandardSerializer(source='', many=True, read_only=True)
    # 这一句写了一下午，要牢记啊
    # 这种方法可以向前端传出所有的数据，但是在post操作的时候，相应地前端也需要传来所有数据才可以
    # 不管是序列化还是反序列化当有多个数据时候都必须加上many=True
    maintenancestandard = MaintenanceStandardSerializer(many=True, read_only=True, source='maintenance_information')
    # maintenance_information = MaintenanceStandardSerializer(many=True)
    # maintenance_information = MaintenanceStandardSerializer(many=True, write_only=True)
    # 所有的外键类型都被映射为PrimaryRelatedField的类型
    # 用这种方法写的前端只需传来MaintenanceStandard的id号，而不用传来一整个字典就可以对数据进行post操作
    maintenance_information = serializers.PrimaryKeyRelatedField(queryset=MaintenanceStandard.objects.all(),
                                                                 write_only=True, many=True)
    id = serializers.IntegerField(required=False)

    class Meta:
        model = MaintenancePlan
        fields = '__all__'

        # 这里记得加上一个write_only为maintenance_information

    # def to_representation(self, instance):
    #     """序列化前最后一步，转换json给前端，用于自定义显示给用户"""
    #     # instance序列化原始数据
    #     # print(instance)
    #     instance.maintenance_information = instance.maintenance_information.all()
    #     ret = super(MaintenancePlanSerializer, self).to_representation(instance)
    #     # ret['maintenance_information'] = {track['id']: track for track in ret['maintenance_information']}
    #     return ret

    def to_internal_value(self, data):
        """反序列化第一步，拿到的是前端提交过来的原始QueryDict"""
        """如有些字段不需要用户传入，自己这里处理，添加字段"""
        # 判断计划的开始时间决定是否启用计划
        if data['start_time'] > time.strftime('%Y-%m-%d', time.localtime(time.time())):
            # print(time.strftime('%Y-%m-%d', time.localtime(time.time())))
            data['plan_status'] = 0
        else:
            data['plan_status'] = 1
        return super(MaintenancePlanSerializer, self).to_internal_value(data)
    # 覆盖原有的to_internal_value方法，拿到前端穿过来的最原始的数据，可以对其及进行一些操作


class MaintenanceTaskSerializer(serializers.ModelSerializer):

    class Meta:
        model = MaintenanceTask
        fields = '__all__'

