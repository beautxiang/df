import django_filters

from equipment_management.models import Equipment


class EquipmentFilter(django_filters.FilterSet):
    """
    商品的过滤类
    """
    # 对创建时间进行过滤
    min_creation_time = django_filters.DateTimeFilter(field_name="creation_time", lookup_expr='gte')
    max_creation_time = django_filters.DateTimeFilter(field_name="creation_time", lookup_expr='lte')
    equipment_name = django_filters.CharFilter(field_name='equipment_name', lookup_expr='icontains')
    equipment_number = django_filters.CharFilter(field_name='equipment_number',
                                                 lookup_expr='icontains')  # icontains，包含且忽略大小写
    type = django_filters.CharFilter(field_name='type', lookup_expr='icontains')  # icontains，包含且忽略大小写
    storage_place = django_filters.CharFilter(field_name='storage_place', lookup_expr='icontains')  # icontains，包含且忽略大小写
    supplier = django_filters.CharFilter(field_name='supplier', lookup_expr='icontains')  # icontains，包含且忽略大小写
    category = django_filters.CharFilter(field_name='category')
    equipment_state = django_filters.CharFilter(field_name='equipment_state')
    equipment_source = django_filters.CharFilter(field_name='equipment_source')
    usage_state = django_filters.CharFilter(field_name='usage_state')

    class Meta:
        model = Equipment
        fields = ['min_creation_time', 'max_creation_time', 'equipment_name', 'equipment_number', 'type',
                  'storage_place', 'supplier', 'category', 'equipment_state', 'equipment_source', 'usage_state']
