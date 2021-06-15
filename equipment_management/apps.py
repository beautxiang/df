from django.apps import AppConfig


class EquipmentManagementConfig(AppConfig):
    name = 'equipment_management'
    # 设置在admin中显示的中文app名字
    verbose_name = '设备管理'
    # verbose_name_plural = verbose_name
