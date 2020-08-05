from django.db import models




class dept(models.Model):
    """
    部门信息表
    :return:
    """
    name = models.CharField(max_length=255, null=False)
    pid = models.IntegerField(null=False, default=-1)
    enable = models.PositiveSmallIntegerField(null=False, default=1)
    path = models.CharField(max_length=64, null=False, default="/")
    position = models.PositiveSmallIntegerField(null=False, default=32767)
    register = models.DateTimeField(null=False, auto_now_add=True)


class user_info(models.Model):
    """
    用户信息表
    :return:
    """
    login = models.CharField(max_length=64, unique=True, null=False)
    password = models.CharField(max_length=64, null=False)
    nickname = models.CharField(max_length=64, null=False)
    dept = models.IntegerField(blank=False)
    role = models.PositiveSmallIntegerField(null=False, default=9)
    level = models.PositiveSmallIntegerField(null=False, default=5)
    phone = models.CharField(max_length=20, null=True)
    mobile = models.CharField(max_length=20, null=True)
    email = models.EmailField(max_length=256, null=True)
    longitude = models.DecimalField(max_digits=11, decimal_places=5, default=1)
    latitude = models.DecimalField(max_digits=11, decimal_places=5, default=1)
    height = models.DecimalField(max_digits=11, decimal_places=5, default=0)
    locate = models.CharField(max_length=256, null=True)
    enable = models.PositiveSmallIntegerField(null=False, default=1)
    position = models.PositiveSmallIntegerField(null=False, default=32767)
    register = models.DateTimeField(auto_now_add=True)


class rtsp_info(models.Model):
    """
    Rtsp信息表
    :return:
    """
    name = models.CharField(max_length=64, null=False)
    dept = models.IntegerField(null=False, default=0)
    type = models.PositiveSmallIntegerField(null=False, default=1)
    server = models.IntegerField(null=False, default=0)
    channel = models.CharField(max_length=64, null=False,default=0)
    longitude = models.DecimalField(max_digits=11, decimal_places=5, null=True)
    latitude = models.DecimalField(max_digits=11, decimal_places=5, null=True)
    height = models.DecimalField(max_digits=11, decimal_places=5, null=True)
    locate = models.CharField(max_length=256, null=True)
    enable = models.PositiveSmallIntegerField(null=False, default=1)
    manufacturer_type=models.IntegerField(null=False, default=1)
    permissions_info=models.IntegerField(null=False, default=1)
    channel_type=models.IntegerField(null=False, default=1)
    inter_code_SN=models.IntegerField(null=False,default=0)
    multicast_ip=models.CharField(max_length=64, null=True)
    multicast_port=models.IntegerField(null=True)
    position = models.PositiveSmallIntegerField(null=False, default=32767)

class rtsp_server(models.Model):
    """
    Rtsp设备信息表
    :return:
    """
    name = models.CharField(max_length=64, unique=True, null=False)
    ip = models.CharField(max_length=48, null=True)
    port = models.IntegerField(null=True, default=37777)
    user = models.CharField(max_length=64, null=False)
    password = models.CharField(max_length=64, null=False)
    channels = models.PositiveSmallIntegerField(null=False, default=1)
    type = models.PositiveSmallIntegerField(null=False, default=1)
    enable = models.PositiveSmallIntegerField(null=False, default=1)


class rtsp_rolling(models.Model):
    """
    Rtsp设备轮询信息表
    :return:
    """
    ipc = models.CharField(max_length=64, null=False,default=0)
    user = models.IntegerField(null=False, default=0)
    enable = models.PositiveSmallIntegerField(null=False, default=1)


class rtsp_record(models.Model):
    """
    Rtsp设备录像信息表
    :return:
    """
    ipc = models.CharField(max_length=64, null=False,default=0)
    user = models.IntegerField(null=False, default=0)
    record_code = models.CharField(max_length=64, null=False)
    type = models.PositiveSmallIntegerField(null=False, default=1)
    time = models.DateTimeField(auto_now_add=True)

class ai_rtsp_record(models.Model):
    """
     AI Rtsp设备录像信息表
    :return:
    """
    ipc = models.CharField(max_length=64, null=False,default=0)
    user = models.IntegerField(null=False, default=3)
    record_code = models.CharField(max_length=64, null=False)
    start_time = models.CharField(max_length=64, null=False,default=0)
    end_time=models.CharField(max_length=64, null=False,default=0)


class operation_log(models.Model):
    """
    Rtsp设备信息表
    :return:
    """
    user = models.CharField(max_length=64, null=False)
    type = models.CharField(max_length=64, null=False)
    result = models.CharField(max_length=64, null=False)
    note = models.CharField(max_length=64, null=False)
    time = models.DateTimeField(auto_now_add=True)


class option_sys(models.Model):
    """
    系统配置信息表
    :return:
    """
    opt_name = models.CharField(max_length=64, null=False)
    opt_key = models.CharField(max_length=64, unique=True,  null=False)
    opt_value = models.CharField(max_length=256, null=False)
    opt_modify = models.PositiveSmallIntegerField(null=False, default=1)


class generic_plan(models.Model):
    """
    iot设备预案信息表
    """
    name = models.CharField(max_length=64, null=False)
    user = models.IntegerField(null=False, default=0)
    content = models.CharField(max_length=256, null=False)
    type = models.PositiveSmallIntegerField(null=False, default=1)
    time = models.DateTimeField(auto_now_add=True)



class iot_device(models.Model):
    """
    iot设备信息表
    """
    name = models.CharField(max_length=64, null=False)
    dept = models.IntegerField(null=False, default=0)
    code = models.CharField(max_length=64, null=False,default=0)
    gateway_server_id=models.IntegerField(null=False,default=0)
    gateway_server=models.CharField(max_length=64, null=False)
    device_type=models.CharField(max_length=64, null=False,default=0)
    iot_device_code=models.CharField(max_length=64, null=False)
    device_type_name=models.CharField(max_length=64, null=False,default=0)
    device_brand_name=models.CharField(max_length=64, null=False,default=0)
    time = models.DateTimeField(auto_now_add=True)
    flag = models.BooleanField(null=False, default=False)
    ipc = models.CharField(max_length=64, null=False,default=0)
    generic_plan = models.IntegerField(null=False, default=0)
    sms_level_1 = models.IntegerField(null=False, default=0)
    sms_level_2 = models.IntegerField(null=False, default=0)
    longitude = models.DecimalField(max_digits=14, decimal_places=11, null=True)
    latitude = models.DecimalField(max_digits=14, decimal_places=11, null=True)
    height = models.DecimalField(max_digits=14, decimal_places=11, null=True)
    iot_address = models.CharField(max_length=256, null=False,default=0)
    enable = models.PositiveSmallIntegerField(null=False, default=1)
    tp_threshold_level_1 = models.CharField(max_length=64,null=True)
    hd_threshold_level_1 = models.CharField(max_length=64,null=True)
    tp_threshold_level_2 = models.CharField(max_length=64,null=True)
    hd_threshold_level_2 = models.CharField(max_length=64,null=True)
    cd_threshold_level_1 = models.CharField(max_length=64,null=True)
    cd_threshold_level_2 = models.CharField(max_length=64,null=True)


class iot_device_info(models.Model):
    """
    iot设备数据表
    """
    dept = models.IntegerField(null=False, default=39)
    adapter_code = models.CharField(max_length=64, null=False)
    adapter_type=models.CharField(max_length=64, null=False)
    gw_code=models.CharField(max_length=64, null=False)
    gw_type=models.CharField(max_length=64, null=False)
    iot_code=models.CharField(max_length=64, null=False)
    iot_type=models.CharField(max_length=64, null=False)
    loRaSNR=models.DecimalField(max_digits=3, decimal_places=1, null=False,default=0)
    rssi=models.IntegerField(null=False,default=0)
    time = models.DateTimeField(auto_now_add=True)
    fCnt=models.IntegerField(null=False, default=0)
    iot_device_code=models.CharField(max_length=64, null=False)
    status=models.IntegerField(null=False, default=0)


class iot_device_values(models.Model):
    """
    iot设备实时数据表
    """
    iot_device=models.ForeignKey(iot_device_info,on_delete=models.CASCADE)
    attribute=models.CharField(max_length=64, null=False)
    value=models.CharField(max_length=64, null=False)

class iot_device_warn(models.Model):
    """
    iot设备告警实时数据表
    """
    iot_device=models.ForeignKey(iot_device_info,on_delete=models.CASCADE)
    warn_data=models.CharField(max_length=256, null=False,default=0)
    warn_type=models.CharField(max_length=64, null=False,default=0)
    warn_cause=models.CharField(max_length=64, null=False,default=0)


class ai_device_warn(models.Model):
    """
        ai设备告警数据表
        """

    warn_data = models.CharField(max_length=256, null=False, default=0)
    warn_type = models.CharField(max_length=64, null=False, default=0)
    warn_cause = models.CharField(max_length=64, null=False, default=0)
    time = models.DateTimeField(auto_now_add=True)
    name = models.CharField(max_length=64, null=False)
    code = models.CharField(max_length=64, null=False)
    locate = models.CharField(max_length=256, null=False, default=0)


class iot_gas(models.Model):
    """
    气体感应器信息表
    """
    code = models.CharField(max_length=64, null=False)
    code_sub = models.CharField(max_length=64, null=False)
    brand = models.CharField(max_length=64, null=False)
    type = models.PositiveSmallIntegerField(null=False, default=1)
    type_name = models.CharField(max_length=64)
    threshold_level_1 = models.DecimalField(max_digits=11, decimal_places=5, null=True)
    threshold_level_2 = models.DecimalField(max_digits=11, decimal_places=5, null=True)
    signal_strength = models.PositiveSmallIntegerField(null=True, default=1)
    gas_strength = models.DecimalField(max_digits=11, decimal_places=5, null=True)
    air_temp = models.DecimalField(max_digits=11, decimal_places=5, null=True)
    air_humidity = models.DecimalField(max_digits=11, decimal_places=5, null=True)
    status = models.IntegerField(null=False, default=1)
    time = models.DateTimeField(auto_now_add=True)


class info_hazards(models.Model):
    """
    重大危险源信息表
    """
    unit_name = models.CharField(max_length=128, null=False)
    address = models.CharField(max_length=128, null=False)
    region = models.CharField(max_length=128, null=False)
    contact = models.CharField(max_length=128, null=False)
    phone = models.CharField(max_length=16, null=False)
    type = models.CharField(max_length=64, null=False)
    name = models.CharField(max_length=64, null=False)
    level = models.CharField(max_length=16, null=False)


class info_admin_license(models.Model):
    """
    安全生产许可信息表
    """
    type = models.CharField(max_length=128, null=False)
    name = models.CharField(max_length=128, null=False)
    code = models.CharField(max_length=128, null=False)
    result = models.CharField(max_length=128, null=False)
    organization = models.CharField(max_length=16, null=False)
    time = models.DateField(null=False)
    validity = models.DateField(null=False)


class info_enterprise(models.Model):
    """
    企业基本信息表
    """
    name = models.CharField(max_length=128, null=False)
    type = models.CharField(max_length=128, null=False)
    address = models.CharField(max_length=128, null=False)
    corporate_name = models.CharField(max_length=32, null=False)
    corporate_job = models.CharField(max_length=32, null=False)
    corporate_phone = models.CharField(max_length=16, null=False)
    safety_name = models.CharField(max_length=32, null=False)
    safety_job = models.CharField(max_length=32, null=False)
    safety_phone = models.CharField(max_length=16, null=False)


class info_plan(models.Model):
    """
    应急预案信息表
    """
    plan_name = models.CharField(max_length=128, null=False)
    plan_time = models.DateTimeField(null=False)
    scheme_name = models.CharField(max_length=128, null=False)
    scheme_time = models.DateTimeField(null=False)
    commanding_organization = models.PositiveSmallIntegerField(null=False, default=1)
    risk_assessment = models.PositiveSmallIntegerField(null=False, default=1)
    commander_name = models.CharField(max_length=32, null=False)
    commander_phone = models.CharField(max_length=16, null=False)
    resource_investigation = models.PositiveSmallIntegerField(null=False, default=1)
    plan_record = models.PositiveSmallIntegerField(null=False, default=1)


class info_trouble(models.Model):
    """
    事故隐患信息表
    """
    code = models.CharField(max_length=64, null=False)
    source = models.CharField(max_length=32, null=False)
    type = models.CharField(max_length=16, null=False)
    describe = models.CharField(max_length=128, null=False)
    level = models.CharField(max_length=16, null=False)
    status = models.CharField(max_length=16, null=False)
    dept = models.CharField(max_length=32, null=False)
    enterprise = models.CharField(max_length=64, null=False)
    reporter = models.CharField(max_length=32, null=False)
    time = models.DateTimeField(null=False)


class info_check_log(models.Model):
    """
    行政执法记录信息表
    """
    code = models.CharField(max_length=64, null=False)
    enterprise = models.CharField(max_length=64, null=False)
    address = models.CharField(max_length=128, null=False)
    corporate_name = models.CharField(max_length=32, null=False)
    corporate_job = models.CharField(max_length=32, null=False)
    corporate_phone = models.CharField(max_length=16, null=False)
    place = models.CharField(max_length=128, null=False)
    begin_time = models.DateTimeField(null=False)
    end_time = models.DateTimeField(null=False)
    dept = models.CharField(max_length=32, null=False)


class info_check_checker(models.Model):
    """
    执法人员信息表
    """
    log_id = models.CharField(max_length=64, null=False)
    checker_name = models.CharField(max_length=32, null=False)
    checker_id = models.CharField(max_length=32, null=False)


class info_template(models.Model):
    """
    执法人员信息表
    """
    user = models.IntegerField(null=False, default=0)
    name = models.CharField(max_length=32, null=False)
    content = models.CharField(max_length=256, null=False)
    type = models.PositiveSmallIntegerField(null=False, default=1)
    time = models.DateTimeField(auto_now_add=True)


class sms_log(models.Model):
    """
    短信发送记录信息表
    """
    user_id = models.IntegerField(null=False, default=0)
    name = models.CharField(max_length=32, null=True)
    phone = models.CharField(max_length=16, null=False)
    content = models.CharField(max_length=256, null=False)
    type = models.PositiveSmallIntegerField(null=False, default=1)
    time = models.DateTimeField(auto_now_add=True)

class ai_device(models.Model):
    """
    ai 分析仪设备信息表
    """

    name = models.CharField(max_length=64, null=False)
    dept = models.IntegerField(null=False, default=0)
    code=models.CharField(max_length=64, null=False)
    time = models.DateTimeField(auto_now_add=True)
    generic_plan = models.IntegerField(null=False, default=0)
    sms_level_1 = models.IntegerField(null=False, default=0)
    sms_level_2 = models.IntegerField(null=False, default=0)
    longitude = models.DecimalField(max_digits=14, decimal_places=11, null=True)
    latitude = models.DecimalField(max_digits=14, decimal_places=11, null=True)
    height = models.DecimalField(max_digits=14, decimal_places=11, null=True)
    locate = models.CharField(max_length=256, null=False, default=0)
    enable = models.PositiveSmallIntegerField(null=False, default=1)


class video_monitor(models.Model):
    """
    Ai 视频监控设备信息表
    """
    ai_device = models.ForeignKey(ai_device, on_delete=models.CASCADE)
    dept = models.IntegerField(null=False, default=0)
    name = models.CharField(max_length=64, null=False)
    code=models.CharField(max_length=64, null=False)
    channel = models.CharField(max_length=64, null=False,default=0)
    longitude = models.DecimalField(max_digits=14, decimal_places=11, null=True)
    latitude = models.DecimalField(max_digits=14, decimal_places=11, null=True)
    height = models.DecimalField(max_digits=14, decimal_places=11, null=True)
    locate = models.CharField(max_length=256, null=False, default=0)
    enable = models.PositiveSmallIntegerField(null=False, default=1)


class administration_punish_info(models.Model):
    """
    行政处罚信息表
    """
    administration_name=models.CharField(max_length=64, null=False) #行政相对人名称(必填)
    administration_type=models.CharField(max_length=64, null=False) #行政相对人类别(必填)
    administration_code_1=models.CharField(max_length=64, null=True) #行政相对人代码_1(统一社会信用代码)
    administration_code_2=models.CharField(max_length=64, null=True) #行政相对人代码_2(工商注册号)
    administration_code_3=models.CharField(max_length=64, null=True) #行政相对人代码_3(组织机构代码)
    administration_code_4=models.CharField(max_length=64, null=True) #行政相对人代码_4(税务登记码)
    administration_code_5=models.CharField(max_length=64, null=True) #行政相对人代码_5(事业单位证书号)
    administration_code_6=models.CharField(max_length=64, null=True) #行政相对人代码_6(社会组织登记证号)
    legal_representative=models.CharField(max_length=64, null=True) #法定代表人
    certificates_type=models.CharField(max_length=64, null=True) #证件类型
    certificates_number=models.CharField(max_length=64, null=True) #证件号码
    administration_punish_number=models.CharField(max_length=64, null=False)  #行政处罚决定书文号(必填)
    lllegal_type=models.CharField(max_length=128, null=False) #违法行为类型(必填)
    lllegal_fact=models.CharField(max_length=128, null=False) #违法事实(必填)
    punishment_basis=models.CharField(max_length=256, null=False) #处罚依据(必填)
    punishment_type=models.CharField(max_length=64, null=False) #处罚类别(必填)
    punishment_content=models.CharField(max_length=64, null=False) #处罚内容(必填)
    fine_money=models.DecimalField(max_digits=7, decimal_places=6, null=True) #罚款金额（万元）
    confiscate_money=models.DecimalField(max_digits=7, decimal_places=6, null=True) #没收违法所得、没收非法财物的金额（万元）
    Revocation_licence=models.CharField(max_length=64, null=True) #暂扣或吊销证照名称及编号
    punish_date=models.CharField(max_length=64, null=False)  #处罚决定日期(必填)
    punish_valid_date=models.CharField(max_length=64, null=False)  #处罚有效期(必填)
    deadline_publicity=models.CharField(max_length=64, null=True) #公示截止期
    penalty_authorities=models.CharField(max_length=64, null=False) #处罚机关(必填)
    penalty_authorities_code=models.CharField(max_length=128, null=False) #处罚机关统一社会信用代码(必填)
    data_source=models.CharField(max_length=64, null=False) #数据来源单位(必填)
    data_source_code=models.CharField(max_length=128, null=False) #数据来源单位统一社会信用代码(必填)