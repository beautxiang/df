from django.db import models


class Equipment(models.Model):
    equipment_number = models.CharField(verbose_name='设备编号', max_length=64, primary_key=True,
                                        db_column='设备编号', help_text='这个字段必须填写，且命名不能重复')  # 此项max_length参数分根据提供的格式更改
    equipment_name = models.CharField(verbose_name='设备名称', max_length=32, blank=False, null=False, db_column='设备名称',
                                      help_text='这个字段必须填写')
    asset_number = models.CharField(verbose_name='资产编号', max_length=32, blank=True, null=True, db_column='资产编号')
    manufacturing_number = models.CharField(verbose_name='出厂编号', max_length=32, blank=True, null=True, db_column='出厂编号')
    units = models.CharField(verbose_name='单位', max_length=16, blank=True, null=True, db_column='单位')
    type = models.CharField(verbose_name='型号', max_length=64, blank=True, null=True, db_column='型号')
    brand = models.CharField(verbose_name='品牌', max_length=64, blank=True, null=True, db_column='品牌')
    supplier = models.CharField(verbose_name='供应商', max_length=64, blank=True, null=True, db_column='供应商')
    purchase_amount = models.FloatField(verbose_name='购置金额', blank=True, null=True, db_column='购置金额')
    purchase_date = models.DateField(verbose_name='购买日期', blank=True, null=True, db_column='购买日期')
    guarantee_period = models.DateField(verbose_name='保修期', blank=True, null=True, db_column='保修期')
    production_time = models.DateField(verbose_name='投产日期', blank=True, null=True, db_column='投产日期')
    estimated_retirement_time = models.DateField(verbose_name='预计报废时间', blank=True, null=True, db_column='预计报废时间')
    person_in_charge = models.CharField(verbose_name='负责人', max_length=32, blank=True, null=True, db_column='负责人')
    department = models.ForeignKey(to='Department', on_delete=models.CASCADE, verbose_name='所属部门', blank=True,
                                   null=True, db_column='所属部门')
    storage_place = models.ForeignKey(to='StoragePlace', on_delete=models.CASCADE, verbose_name='存放位置', blank=True,
                                      null=True, db_column='存放位置')
    usage_state = models.ForeignKey(to='UsageState', on_delete=models.CASCADE, verbose_name='使用状态', blank=True,
                                    null=True, to_field='usage_state', db_column='使用状态')
    category = models.ForeignKey(to='Category', on_delete=models.CASCADE, verbose_name='类别', blank=True, null=True,
                                 to_field='category', db_column='类别')
    equipment_state = models.ForeignKey(to='EquipmentState', on_delete=models.CASCADE, verbose_name='设备状态',
                                        blank=True, null=True, to_field='equipment_state', db_column='设备状态')
    equipment_source = models.ForeignKey(to='EquipmentSource', on_delete=models.CASCADE, verbose_name='设备来源',
                                         blank=True, null=True, to_field='equipment_source', db_column='设备来源')
    remark = models.CharField(verbose_name='备注', max_length=512, blank=True, null=True, db_column='备注')
    creation_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间', db_column='创建时间')

    class Meta:
        # 设置表的名字
        db_table = '00设备基本信息表'
        # 设置admin中表的名字
        verbose_name_plural = '00设备基本信息表'
        ordering = ('-creation_time',)


class EquipmentFile(models.Model):
    equipment = models.ForeignKey(to='Equipment', on_delete=models.CASCADE, verbose_name='设备编号',
                                  to_field='equipment_number', db_column='设备编号')
    relevant_document = models.FileField(verbose_name='相关文件', upload_to='equipment_relevant_document', blank=True,
                                         null=True, db_column='相关文件')

    class Meta:
        # 设置表的名字
        db_table = '01设备文件'
        # 设置admin中表的名字
        verbose_name_plural = '01设备文件'


class StoragePlace(models.Model):
    storage_place_name = models.CharField(verbose_name='存放位置', max_length=64, db_column='存放位置')
    parent_id = models.ForeignKey(to='self', on_delete=models.CASCADE, verbose_name='父id',
                                  blank=True, null=True, db_column='父id')

    class Meta:
        db_table = '02存放位置'
        verbose_name_plural = '02存放位置'


class Department(models.Model):
    department_name = models.CharField(verbose_name='部门名', max_length=64, db_column='部门名')
    parent_id = models.ForeignKey(to='self', on_delete=models.CASCADE, verbose_name='父id',
                                  blank=True, null=True, db_column='父id')

    class Meta:
        db_table = '03部门'
        verbose_name_plural = '03部门'


class UsageState(models.Model):
    usage_state = models.CharField(verbose_name='使用状态', db_column='使用状态', max_length=32, primary_key=True)

    class Meta:
        db_table = '04使用状态'
        verbose_name_plural = '04使用状态'


class Category(models.Model):
    category = models.CharField(verbose_name='类别', db_column='类别', max_length=32, primary_key=True)

    class Meta:
        db_table = '05类别'
        verbose_name_plural = '05类别'


class EquipmentState(models.Model):
    equipment_state = models.CharField(verbose_name='设备状态', db_column='设备状态', max_length=32, primary_key=True)

    class Meta:
        db_table = '06设备状态'
        verbose_name_plural = '06设备状态'


class EquipmentSource(models.Model):
    equipment_source = models.CharField(verbose_name='设备来源', db_column='设备来源', max_length=32, primary_key=True)

    class Meta:
        db_table = '07设备来源'
        verbose_name_plural = '07设备来源'


class Label(models.Model):
    equipment_number = models.OneToOneField(to=Equipment, on_delete=models.CASCADE, verbose_name='设备编号',
                                            primary_key=True, to_field='equipment_number', db_column='设备编号',
                                            help_text='请选择一个已存在的设备编号')
    QR_code = models.ImageField(upload_to='QR_code/%Y/%m/%d/', verbose_name='二维码', blank=True, null=True,
                                db_column='二维码')
    bar_code = models.ImageField(upload_to='bar_code/%Y/%m/%d/', verbose_name='条形码', blank=True, null=True,
                                 db_column='条形码')
    last_printing_time = models.DateTimeField(auto_now=True, verbose_name='最后打印时间', db_column='最后打印时间')

    class Meta:
        db_table = '08设备标签信息表'
        verbose_name_plural = '08设备标签信息表'


class OperationRecord(models.Model):
    equipment_number = models.ForeignKey(to=Equipment, on_delete=models.CASCADE, verbose_name='设备编号',
                                         to_field='equipment_number', db_column='设备编号', help_text='请选择一个已存在的设备编号')
    record_time = models.DateField(auto_now=True, verbose_name='记录时间', db_column='记录时间')
    boot_time = models.DateTimeField(blank=True, null=True, verbose_name='开机时间', db_column='开机时间')
    off_time = models.DateTimeField(blank=True, null=True, verbose_name='关机时间', db_column='关机时间')

    class Meta:
        db_table = '09设备运行记录信息表'
        verbose_name_plural = '09设备运行记录信息表'
