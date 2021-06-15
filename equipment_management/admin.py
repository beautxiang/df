from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from import_export.admin import ImportExportModelAdmin, ImportMixin, ExportActionModelAdmin, \
    ImportExportActionModelAdmin, ExportActionMixin
from .models import Equipment, UsageState, Category, EquipmentState, EquipmentSource, Label, OperationRecord
from import_export import resources
from .models import Equipment
from import_export import fields, widgets

# Register your models here.
# admin.site.register(Equipment)

admin.site.site_title = '东研工业云管理系统'
admin.site.site_header = '东研工业云超级管理员系统'
admin.site.index_title = '东研工业云'


@admin.register(UsageState)
class UsageStateAdmin(admin.ModelAdmin):
    # 设置在列表中显示的字段
    list_display = ('usage_state',)
    # 设置每页显示多少条数据
    list_per_page = 20


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    # 设置在列表中显示的字段
    list_display = ('category',)
    # 设置每页显示多少条数据
    list_per_page = 20


@admin.register(EquipmentState)
class EquipmentStateAdmin(admin.ModelAdmin):
    # 设置在列表中显示的字段
    list_display = ('equipment_state',)
    # 设置每页显示多少条数据
    list_per_page = 20


@admin.register(EquipmentSource)
class EquipmentSourceAdmin(admin.ModelAdmin):
    # 设置在列表中显示的字段
    list_display = ('equipment_source',)
    # 设置每页显示多少条数据
    list_per_page = 20


@admin.register(Label)
class LabelAdmin(admin.ModelAdmin):
    # 设置在列表中显示的字段
    list_display = ('equipment_number', 'QR_code', 'bar_code', 'last_printing_time')
    # 设置每页显示多少条数据
    list_per_page = 20


@admin.register(OperationRecord)
class OperationRecordAdmin(admin.ModelAdmin):
    # 设置在列表中显示的字段
    list_display = ('equipment_number', 'record_time', 'boot_time', 'off_time')
    # 设置每页显示多少条数据
    list_per_page = 20


# 这部分代码实现了admin中完整的导入导出功能以及勾选后导出的功能
class EquipmentResource(resources.ModelResource):
    equipment_name = fields.Field(attribute='equipment_name', column_name=u'设备名称')
    equipment_number = fields.Field(attribute='equipment_number', column_name=u'设备编号')
    asset_number = fields.Field(attribute='asset_number', column_name=u'资产编号')
    manufacturing_number = fields.Field(attribute='manufacturing_number', column_name=u'出厂编号')
    units = fields.Field(attribute='units', column_name=u'单位')
    type = fields.Field(attribute='type', column_name=u'型号')
    brand = fields.Field(attribute='brand', column_name=u'品牌')
    supplier = fields.Field(attribute='supplier', column_name=u'供应商')
    # 这些项中设置widget属性则会在字符串为空的情况下默认为数据库写入一个None即为数据库中的null
    purchase_amount = fields.Field(attribute='purchase_amount', column_name=u'购置金额', widget=widgets.FloatWidget())
    purchase_date = fields.Field(attribute='purchase_date', column_name=u'购买日期', widget=widgets.DateWidget())
    guarantee_period = fields.Field(attribute='guarantee_period', column_name=u'保修期', widget=widgets.DateWidget())
    production_time = fields.Field(attribute='production_time', column_name=u'投产日期', widget=widgets.DateWidget())
    estimated_retirement_time = fields.Field(attribute='estimated_retirement_time', column_name=u'预计报废时间',
                                             widget=widgets.DateWidget())
    person_in_charge = fields.Field(attribute='person_in_charge', column_name=u'负责人')
    department = fields.Field(attribute='department', column_name=u'所属部门')
    storage_place = fields.Field(attribute='storage_place', column_name=u'存放位置')
    remark = fields.Field(attribute='remark', column_name=u'备注')
    usage_state = fields.Field(attribute='usage_state', column_name=u'使用状态',
                               widget=widgets.ForeignKeyWidget(UsageState, 'usage_state'))
    category = fields.Field(attribute='category', column_name=u'类别',
                            widget=widgets.ForeignKeyWidget(Category, 'category'))
    equipment_state = fields.Field(attribute='equipment_state', column_name=u'设备状态',
                                   widget=widgets.ForeignKeyWidget(EquipmentState, 'equipment_state'))
    equipment_source = fields.Field(attribute='equipment_source', column_name=u'设备来源',
                                    widget=widgets.ForeignKeyWidget(EquipmentSource, 'equipment_source'))
    # 以下在设置时间格式的情况下设置了只读
    creation_time = fields.Field(attribute='creation_time', column_name=u'创建时间', readonly=True,
                                 widget=widgets.DateTimeWidget(format='%Y-%m-%d %H:%M:%S'))

    class Meta:
        model = Equipment
        exclude = ('relevant_document',)
        # # 当导入数据无改变的时候，选择跳过此条数据
        skip_unchanged = True
        # 是否报告跳过的数据
        report_skipped = True
        # 未懂是什么意思
        import_id_fields = ('equipment_number',)


# 以下的设置使得可以在admin界面实现数据的导入与导出功能
@admin.register(Equipment)
class EquipmentAdmin(ImportExportModelAdmin, ImportExportActionModelAdmin):
    # 导出数据的resource数据源
    resource_class = EquipmentResource
    # 设置在列表中显示的字段
    list_display = (
        'equipment_name', 'equipment_number', 'usage_state', 'category', 'equipment_state', 'equipment_source',
        'creation_time')
    # 设置每页显示多少条数据
    list_per_page = 20
    # 设置排序的字段
    ordering = ('-creation_time',)
    # 设置哪些字段可以点击进入编辑界面
    list_display_links = ('equipment_number',)

    # 设置列表页面可以直接编辑的字段
    list_editable = ('usage_state', 'category', 'equipment_state', 'equipment_source')

    # 筛选器
    list_filter = ('equipment_number',)  # 过滤器
    search_fields = ('equipment_name',)  # 搜索字段
    date_hierarchy = 'creation_time'  # 详细时间分层筛选　
    readonly_fields = ('creation_time',)