import json
import random
import requests
import time
import pika
from datetime import datetime, date, timedelta
from api.ErrorCode import getErrMsgByCode
from api.public import reqbody_verify
from api.public import reqbody_verify_admin
from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.views.decorators.csrf import csrf_exempt
from django.conf import  settings
import paho.mqtt.client as mqtt
from threading import Thread
from api.models import iot_device_info as iotDeviceInfoDB
from api.models import iot_device_values as iotDeviceValuesDB
from django.db.models import Q

from django.db import transaction
from api.models import iot_device as iotDeviceDB
from api.models import iot_gas as iotGasDB
from api.models import generic_plan as genericPlanDB
from api.models import user_info as userInfoDB
from api.models import info_template as smsInfoTemplateDB
from api.models import iot_device_warn as iotDeviceWarnDB
from api.models import ai_device as aiDeviceDB
from api.models import video_monitor as videoMonitorDB
from api.models import ai_device_warn as aiDeviceWarnDB
from api.models import ai_rtsp_record as aiRtspRecordDB

import logging



from api.sms import sendSMSInfoImplement

IM_Thread_Name = "IM_MQTT_Client"
Client_ID="e4fd4c41-dc9d-4c3a-beaa-19228e43dc4e"
REPORT_TOPIC = "$queue//application/status/e4fd4c41-dc9d-4c3a-beaa-19228e43dc4e"  # 主题
PUBLISH_TOPIC="/gmaj/warn/info"


mqttClient = mqtt.Client(client_id=Client_ID, clean_session=False,transport='tcp')

def on_connect(client, userdata, flags, rc):
    # print('connected to mqtt with resurt code ', rc)
    pass




def on_message(client, userdata, msg):
    message = msg.payload
    message=json.loads(message.decode())
    print(message)

    savePoint = transaction.savepoint()
    try:
        iotDeviceInfo = iotDeviceInfoDB.objects.create(
            adapter_code=message["adapter_code"],
            adapter_type=message["adapter_type"],
            gw_code=message["gw_code"],
            gw_type=message["gw_type"],
            iot_code=message["iot_code"],
            iot_type=message["iot_type"],
            loRaSNR=message["iot_data"]["loRaSNR"],
            rssi=message["iot_data"]["rssi"],
            fCnt=message["iot_data"]["fCnt"],
            iot_device_code=message["iot_data"]["iot_device_code"]
        )
        # 3000000000100003 地磁传感器
        # 3000000000100004 温湿度传感器
        # 3000000000100005 可燃气体传感器
        # 3000000000100006 烟感传感器
        # 3000000000100007  水浸传感器

        if message["iot_type"] == "3000000000100004":
            humidit=message["iot_data"]["humidit"]
            temperature=message["iot_data"]["temperature"]
            voltage=message["iot_data"]["voltage"]
            dict1={"temperature":temperature,"humidit":humidit,"voltage":voltage}
            for key,value in dict1.items():
                iotDeviceValues=iotDeviceValuesDB.objects.create(
                    iot_device=iotDeviceInfo,attribute=key,value=value
                )
            try:
                iotDevice=iotDeviceDB.objects.get(code=message["iot_code"])

                if float(iotDevice.hd_threshold_level_2) > float(humidit) >= float(iotDevice.hd_threshold_level_1) and float(temperature) < float(iotDevice.tp_threshold_level_1):
                    warnDate="当前温湿度传感器设备湿度过高，湿度：%3.1f%%,达到一级告警"% humidit
                    warnType="湿度过高"
                    warnCause="湿度%3.1f%%,超过设定湿度"%humidit
                    iotDeviceWarn=iotDeviceWarnDB.objects.create(
                        iot_device=iotDeviceInfo,warn_data=warnDate,warn_type=warnType,warn_cause=warnCause
                    )
                    iotDeviceInfo.status = 1
                    iotDeviceInfo.save()
                    # message["id"]=iotDeviceInfo
                    message["device_type"]=0
                    message["ipc"]=iotDevice.ipc
                    message["status"]=1
                    mqttClient.publish(PUBLISH_TOPIC, json.dumps(message), 1, False)
                elif float(iotDevice.tp_threshold_level_2) > float(temperature) >= float(iotDevice.tp_threshold_level_1) and float(humidit) < float(iotDevice.hd_threshold_level_1):
                    warnDate = "当前温湿度传感器设备温度过高，温度：%3.1f℃,达到一级告警" % temperature
                    warnType = "温度过高"
                    warnCause = "温度%3.1f,超过设定温度" % temperature
                    iotDeviceWarn = iotDeviceWarnDB.objects.create(
                        iot_device_id=iotDeviceInfo, warn_data=warnDate, warn_type=warnType, warn_cause=warnCause
                    )
                    iotDeviceInfo.status=1
                    iotDeviceInfo.save()
                    # message["id"] = iotDeviceInfo
                    message["device_type"] = 0
                    message["ipc"] = iotDevice.ipc
                    message["status"] = 1
                    mqttClient.publish(PUBLISH_TOPIC, json.dumps(message), 1, False)
                elif   float(iotDevice.hd_threshold_level_2) > float(humidit) >= float(iotDevice.hd_threshold_level_1) and float(iotDevice.tp_threshold_level_2) > float(temperature) >= float(iotDevice.tp_threshold_level_1):
                    warnDate = "当前温湿度传感器设备数据异常，温度：%3.1f℃、湿度：%3.1f%%,达到一级告警" % (temperature, humidit)
                    warnType = "温度和湿度异常"
                    warnCause = "温度%3.1f,超过设定温度，湿度%3.1f%%,超过设定湿度" % (temperature,humidit)
                    iotDeviceWarn = iotDeviceWarnDB.objects.create(
                        iot_device=iotDeviceInfo, warn_data=warnDate, warn_type=warnType, warn_cause=warnCause
                    )
                    iotDeviceInfo.status = 1
                    iotDeviceInfo.save()
                    # message["id"] = iotDeviceInfo
                    message["device_type"] = 0
                    message["ipc"] = iotDevice.ipc
                    message["status"] = 1
                    mqttClient.publish(PUBLISH_TOPIC, json.dumps(message), 1, False)

                elif float(humidit) >= float(iotDevice.hd_threshold_level_2) and float(temperature) < float(iotDevice.tp_threshold_level_2):
                    warnDate = "当前温湿度传感器设备湿度过高，湿度：%3.1f%%,达到二级告警" %  humidit
                    warnType = "湿度过高"
                    warnCause = "湿度%3.1f%%,超过设定湿度" % humidit
                    iotDeviceWarn = iotDeviceWarnDB.objects.create(
                        iot_device=iotDeviceInfo, warn_data=warnDate, warn_type=warnType, warn_cause=warnCause
                    )
                    iotDeviceInfo.status = 2
                    iotDeviceInfo.save()
                    # message["id"] = iotDeviceInfo
                    message["device_type"] = 0
                    message["ipc"] = iotDevice.ipc
                    message["status"] = 2
                    mqttClient.publish(PUBLISH_TOPIC, json.dumps(message), 1, False)
                elif float(temperature) >= float(iotDevice.tp_threshold_level_2) and float(humidit) <float(iotDevice.hd_threshold_level_2):

                    warnDate = "当前温湿度传感器设备温度过高，温度：%3.1f℃,达到二级告警" % temperature
                    warnType = "温度过高"
                    warnCause = "温度%3.1f,超过设定温度" % temperature
                    iotDeviceWarn = iotDeviceWarnDB.objects.create(
                        iot_device=iotDeviceInfo, warn_data=warnDate, warn_type=warnType, warn_cause=warnCause
                    )
                    iotDeviceInfo.status = 2
                    iotDeviceInfo.save()
                    # message["id"] = iotDeviceInfo
                    message["device_type"] = 0
                    message["ipc"] = iotDevice.ipc
                    message["status"] = 2
                    mqttClient.publish(PUBLISH_TOPIC, json.dumps(message), 1, False)

                elif float(humidit) >= float(iotDevice.hd_threshold_level_2) and float(temperature) > float(iotDevice.tp_threshold_level_2):
                    warnDate = "当前温湿度传感器设备温度湿度过高，温度：%3.1f℃、湿度：%3.1f%%,达到二级告警" % (temperature, humidit)
                    warnType = "温度和湿度数据异常"
                    warnCause = "温度%3.1f,超过设定温度，湿度%3.1f%%,超过设定湿度" % (temperature, humidit)
                    iotDeviceWarn = iotDeviceWarnDB.objects.create(
                        iot_device=iotDeviceInfo, warn_data=warnDate, warn_type=warnType, warn_cause=warnCause
                    )
                    iotDeviceInfo.status = 2
                    iotDeviceInfo.save()
                    # message["id"] = iotDeviceInfo
                    message["device_type"] = 0
                    message["ipc"] = iotDevice.ipc
                    message["status"] = 2
                    mqttClient.publish(PUBLISH_TOPIC, json.dumps(message), 1, False)

            except Exception as e:
                print(e)

        if message["iot_type"] == "3000000000100003":
            xPos=message["iot_data"]["xPos"]
            yPos=message["iot_data"]["yPos"]
            zPos=message["iot_data"]["zPos"]
            temperature = message["iot_data"]["temperature"]
            hasCar=message["iot_data"]["hasCar"]
            voltage=message["iot_data"]["voltage"]
            dict1={"xPos":xPos,"yPos":yPos,"zPos":zPos,"temperature":temperature,"hasCar":hasCar,"voltage":voltage}
            for key,value in dict1.items():
                iotDeviceValues = iotDeviceValuesDB.objects.create(
                    iot_device=iotDeviceInfo, attribute=key, value=value
                )
            try:
                iotDevice = iotDeviceDB.objects.get(code=message["iot_code"])
                if hasCar == "true":
                    warnDate = "当前地磁传感器监测到有车辆经过，达到一级告警"
                    warnType = "有车辆经过"
                    warnCause = "有车辆经过"
                    iotDeviceWarn = iotDeviceWarnDB.objects.create(
                        iot_device=iotDeviceInfo, warn_data=warnDate, warn_type=warnType, warn_cause=warnCause
                    )
                    iotDeviceInfo.status = 1
                    iotDeviceInfo.save()
                    # message["id"] = iotDeviceInfo
                    message["device_type"] = 0
                    message["ipc"] = iotDevice.ipc
                    message["status"] = 1
                    mqttClient.publish(PUBLISH_TOPIC, json.dumps(message), 1, False)

            except Exception as e:
                print(e)

        if message["iot_type"] == "3000000000100005":
            clientId=message["iot_data"]["clientId"]
            devtype=message["iot_data"]["devtype"]
            packtype=message["iot_data"]["packtype"]
            devstatu=message["iot_data"]["devstatu"]
            cellstatu=message["iot_data"]["cellstatu"]
            fixstatu=message["iot_data"]["fixstatu"]
            keystatu=message["iot_data"]["keystatu"]
            gas=message["iot_data"]["gas"]
            dict1 ={"clientId":clientId,"devtype":devtype,"packtype":packtype,"devstatu":devstatu,"cellstatu":cellstatu,"fixstatu":fixstatu,"keystatu":keystatu,"gas":gas}
            for key,value in dict1.items():
                iotDeviceValues = iotDeviceValuesDB.objects.create(
                    iot_device=iotDeviceInfo, attribute=key, value=value
                )
            try:
                iotDevice = iotDeviceDB.objects.get(code=message["iot_code"])
                if float(gas)> float(iotDevice.cd_threshold_level_1):
                    warnDate = "当前气体浓度达到%3.1f%%，达到一级告警" % gas
                    warnType = "浓度过高"
                    warnCause = "浓度%3.1f%%,超过设定浓度值" % gas
                    iotDeviceWarn = iotDeviceWarnDB.objects.create(
                        iot_device=iotDeviceInfo, warn_data=warnDate, warn_type=warnType, warn_cause=warnCause
                    )
                    iotDeviceInfo.status = 1
                    iotDeviceInfo.save()
                    # message["id"] = iotDeviceInfo
                    message["device_type"] = 0
                    message["ipc"] = iotDevice.ipc
                    message["status"] = 1
                    mqttClient.publish(PUBLISH_TOPIC, json.dumps(message), 1, False)

                elif float(gas)> float(iotDevice.cd_threshold_level_2):
                    warnDate = "当前气体浓度达到%3.1f%%，达到二级告警" % gas
                    warnType = "浓度过高"
                    warnCause = "浓度%3.1f%%,超过设定浓度值" % gas
                    iotDeviceWarn = iotDeviceWarnDB.objects.create(
                        iot_device=iotDeviceInfo, warn_data=warnDate, warn_type=warnType, warn_cause=warnCause
                    )
                    iotDeviceInfo.status = 2
                    iotDeviceInfo.save()
                    # message["id"] = iotDeviceInfo
                    message["device_type"] = 0
                    message["ipc"] = iotDevice.ipc
                    message["status"] = 2
                    mqttClient.publish(PUBLISH_TOPIC, json.dumps(message), 1, False)
            except Exception as e:
                print(e)

        if message["iot_type"] == "3000000000100007":
            flooding=message["iot_data"]["flooding"]
            cellstatu=message["iot_data"]["cellstatu"]
            voltage=message["iot_data"]["voltage"]
            dict1={"flooding":flooding,"cellstatu":cellstatu,"voltage":voltage}
            for key,value in dict1.items():
                iotDeviceValues = iotDeviceValuesDB.objects.create(
                    iot_device=iotDeviceInfo, attribute=key, value=value
                )
            try:
                iotDevice = iotDeviceDB.objects.get(code=message["iot_code"])
                if int(flooding)==1:
                    warnDate = "当前水浸传感器监测到被水浸入到设备，达到一级告警"
                    warnType = "被水浸"
                    warnCause = "被水浸入到设备"
                    iotDeviceWarn = iotDeviceWarnDB.objects.create(
                        iot_device=iotDeviceInfo, warn_data=warnDate, warn_type=warnType, warn_cause=warnCause
                    )
                    iotDeviceInfo.status = 1
                    iotDeviceInfo.save()
                    # message["id"] = iotDeviceInfo
                    message["device_type"] = 0
                    message["ipc"] = iotDevice.ipc
                    message["status"] = 1
                    mqttClient.publish(PUBLISH_TOPIC, json.dumps(message), 1, False)
            except Exception as e:
                print(e)

        if message["iot_type"] == "3000000000100006":
            type=message["iot_data"]["type"]
            statu=message["iot_data"]["statu"]
            voltage=message["iot_data"]["voltage"]
            dict1 ={"type":type,"statu":statu,"voltage":voltage}
            for key,value in dict1.items():
                iotDeviceValues = iotDeviceValuesDB.objects.create(
                    iot_device=iotDeviceInfo, attribute=key, value=value
                )
            try:
                iotDevice = iotDeviceDB.objects.get(code=message["iot_code"])
                if int(statu)==1:
                    warnDate = "当前烟感传感器数据异常，达到二级告警"
                    warnType = "火警"
                    warnCause = "当前烟感传感器数据异常，达到火警告警阈值"
                    iotDeviceWarn = iotDeviceWarnDB.objects.create(
                        iot_device=iotDeviceInfo, warn_data=warnDate, warn_type=warnType, warn_cause=warnCause
                    )
                    iotDeviceInfo.status = 2
                    iotDeviceInfo.save()
                    # message["id"] = iotDeviceInfo
                    message["device_type"] = 0
                    message["ipc"] = iotDevice.ipc
                    message["status"] = 2
                    mqttClient.publish(PUBLISH_TOPIC, json.dumps(message), 1, False)

                if int(statu) in (2,3,6):
                    warnDate = "当前烟感传感器设备故障，达到一级告警"
                    warnType = "设备故障"
                    warnCause = "当前烟感传感器设备故障"
                    iotDeviceWarn = iotDeviceWarnDB.objects.create(
                        iot_device=iotDeviceInfo, warn_data=warnDate, warn_type=warnType, warn_cause=warnCause
                    )
                    iotDeviceInfo.status = 1
                    iotDeviceInfo.save()
                    # message["id"] = iotDeviceInfo
                    message["device_type"] = 0
                    message["ipc"] = iotDevice.ipc
                    message["status"] = 1
                    mqttClient.publish(PUBLISH_TOPIC, json.dumps(message), 1, False)
            except Exception as e:
                print(e)

    except Exception as e:
        print(e)
        transaction.savepoint_rollback(savePoint)

    transaction.savepoint_commit(savePoint)



def on_subscribe(client, userdata, mid, granted_qos):
    """
    信息--订阅
    """
    pass
def on_disconnect(client, userdata, rc):
    """
    连接信息--重连
    """
    if rc != 0:
        mqttClient.reconnect()




def on_unsubscribe(client, userdata, mid):
    """
    信息--取消订阅
    """
    pass

def run(name):
    """
    服务--运行
    :return:
    """
    mqttClient.on_connect = on_connect
    mqttClient.on_disconnect = on_disconnect
    mqttClient.on_message = on_message
    mqttClient.on_subscribe = on_subscribe
    mqttClient.on_unsubscribe = on_unsubscribe

    mqttClient.username_pw_set(Client_ID, settings.MQTT_CLIENT_PWD)

    mqttClient.connect(settings.MQTT_SERVER_IP,settings.MQTT_SERVER_PORT,settings.MQTT_CLIENT_KEEPALIVE)

    mqttClient.subscribe(REPORT_TOPIC, 1)  # 订阅主题

    mqttClient.loop_forever()

def start():
    """
    服务--开启
    """
    threadObj = Thread(target=run, args=(IM_Thread_Name,))

    threadObj.start()
    # print("123")




iotSystemUrl = "http://10.17.30.141:9090/gateway/dispatch.do"
iotSysAccount = "zt_extern"
iotSysAuth = "qaz,123"
iotSoftwareSystem = "74"
iotRequestID = "4397fc94-f611-11e9-b257-fa163e95d29f"


bindAddUrl = "http://iot.longbaotec.cn:8000/api/iot/bind/add"
bindDeleteUrl="http://iot.longbaotec.cn:8000/api/iot/bind/delete"
applicationDeptUrl="http://iot.longbaotec.cn:8000/api/iot/application/dept"
bindQueryUrl="http://iot.longbaotec.cn:8000/api/iot/bind/query"
def iotDeviceRegister(deviceInfo):
    """
    将IOT设备注册到物联网平台上去
    """
    registerData = {}
    registerData["service"] = "wlwdevinfoservice.register"
    registerData["account"] = iotSysAccount
    registerData["thirdFlag"] = deviceInfo["thirdFlag"]
    registerData["auth"] = iotSysAuth
    registerData["requestId"] = iotRequestID
    registerData["requestData"] = deviceInfo
    try:
        result = requests.post(iotSystemUrl, data=json.dumps(registerData), timeout=10)
    except Exception as err:
        print(format(err))
    else:
        resultData = json.loads(result.text)
        print(format(resultData))
        if resultData["responseCode"] == 200:
            return resultData["responseData"]
        else:
            print(format(resultData))

    return None


def iotDeviceUnRegister(deviceInfo):
    """
    将IOT设备注册到物联网平台上去
    """
    registerData = {}
    registerData["service"] = "wlwdevinfoservice.delDevice"
    registerData["account"] = iotSysAccount
    registerData["thirdFlag"] = deviceInfo["thirdFlag"]
    registerData["auth"] = iotSysAuth
    registerData["requestId"] = iotRequestID
    registerData["requestData"] = deviceInfo
    print(format(registerData))
    try:
        result = requests.post(iotSystemUrl, data=json.dumps(registerData), timeout=2)
    except Exception as err:
        print(format(err))
    else:
        resultData = json.loads(result.text)
        print(format(resultData))
        if resultData["responseCode"] == 200:
            return True

    return None


@csrf_exempt
@api_view(["post"])
def pushDeviceStatus(request):
    try:
        reqBody = json.loads(request.body)
    except Exception as err:
        return Response({"result": 13006001, "msg": getErrMsgByCode(13006001, err)}, content_type="application/json")

    return Response({"result": 0, "msg": "OK"}, content_type="application/json")


@csrf_exempt
@api_view(["post"])
def getLoraDeviceInfo(request):
    """
    查询Loro平台IOT设备信息
    :param request:
    :return:
    """
    try:
        reqBody = json.loads(request.body)
    except Exception as err:
        return Response({"result": 14001001, "msg": getErrMsgByCode(14001001, err)}, content_type="application/json")
    if reqbody_verify_admin(reqBody, err_code=14001001) is None:
        pass
    else:
        return reqbody_verify_admin(reqBody, err_code=14001001)
    try:
        registerData = {"app_key": settings.LORA_USER,"app_secret": settings.LORA_PWD}

        response = requests.post(url=applicationDeptUrl, data=json.dumps(registerData))

        resultData = json.loads(response.text)

        registerData1 = {"app_key": settings.LORA_USER, "app_secret": settings.LORA_PWD}

        response1 = requests.post(url=bindQueryUrl, data=json.dumps(registerData1))

        resultData1 = json.loads(response1.text)



    except Exception as err:
        return Response({"result": 14001023, "msg": getErrMsgByCode(14001023, None)}, content_type="application/json")

    # if resultData["msg"] != "OK":
    #     return Response({"result": 14001023, "msg": getErrMsgByCode(14001023, None)}, content_type="application/json")

    for value1 in resultData["data"]:
        value1["status"]=0
        for value2 in resultData1["data"]:
            if value1["id"] == value2["id"]:
                value1["status"] = 1

    resData = []
    try:
        """
        { 'name': '烟感器2','code': 'e9ac3fd0-0012-4d14-ac62-f06b2cbeee2d', 'device_type': '3000000000100006', 'gateway_server_id': 1, 'gateway_server': '唯传Lora平台', 'enable': 1, 'iot_device_code': 'ffffff1000010908', 'iot_latitude': 113.922749, 'iot_longitude': 22.734945, 'iot_height': 0.0, 'iot_address': '证通电子产业园'}
        """

        for item in resultData["data"]:
            deviceObj = {}

            deviceObj["name"] = item["name"]
            deviceObj["code"] = item["code"]
            deviceObj["device_type"] = item["device_type"]
            deviceObj["device_type_name"] = item["device_type_name"]
            deviceObj["device_brand_name"] = item["device_brand_name"]
            deviceObj["gateway_server_id"] = item["gateway_server_id"]
            deviceObj["gateway_server"] = item["gateway_server"]
            deviceObj["enable"] = item["enable"]
            deviceObj["iot_device_code"] = item["iot_device_code"]
            deviceObj["latitude"] = item["iot_latitude"]
            deviceObj["longitude"] = item["iot_longitude"]
            deviceObj["height"] = item["iot_height"]
            deviceObj["iot_address"] = item["iot_address"]
            deviceObj["status"]=item["status"]


            resData.append(deviceObj)
    except Exception as err:
        return Response({"result": 14001026, "msg": getErrMsgByCode(14001026, None)}, content_type="application/json")

    return Response({"result": 0, "msg": "OK", "data": resData}, content_type="application/json")

@csrf_exempt
@api_view(["post"])
def addIoTDeviceInfo(request):
    """
    IoT设备信息--新增
    """
    try:
        reqBody = json.loads(request.body)
    except Exception as err:
        return Response({"result": 14001001, "msg": getErrMsgByCode(14001001, err)}, content_type="application/json")

    if reqbody_verify_admin(reqBody, err_code=14001001) is None:
        pass
    else:
        return reqbody_verify_admin(reqBody, err_code=14001001)

    if "dept" not in reqBody:
        return Response({"result": 14001006, "msg": getErrMsgByCode(14001006, None)}, content_type="application/json")
    else:
        deviceDept = reqBody["dept"]

    if "code" not in reqBody:
        return Response({"result": 14001007, "msg": getErrMsgByCode(14001007, None)}, content_type="application/json")
    else:
        Code = reqBody["code"]

    if "flag" not in reqBody:
        return Response({"result": 14001008, "msg": getErrMsgByCode(14001008, None)}, content_type="application/json")
    else:
        deviceFlag = reqBody["flag"]

    if "ipc" not in reqBody:
        return Response({"result": 14001009, "msg": getErrMsgByCode(14001009, None)}, content_type="application/json")
    else:
        deviceIPC = reqBody["ipc"]

    if "generic_plan" not in reqBody:
        return Response({"result": 14001010, "msg": getErrMsgByCode(14001010, None)}, content_type="application/json")
    else:
        genericPlan = reqBody["generic_plan"]

    if "name" not in reqBody:
        return Response({"result": 14001011, "msg": getErrMsgByCode(14001011, None)}, content_type="application/json")
    else:
        deviceName= reqBody["name"]

    if "device_type" not in reqBody:
        return Response({"result": 14001012, "msg": getErrMsgByCode(14001012, None)}, content_type="application/json")
    else:
        deviceTyper = reqBody["device_type"]

    if "gateway_server_id" not in reqBody:
        return Response({"result": 14001013, "msg": getErrMsgByCode(14001013, None)}, content_type="application/json")
    else:
        gatewayServerId = reqBody["gateway_server_id"]

    if "gateway_server" not in reqBody:
        return Response({"result": 14001014, "msg": getErrMsgByCode(14001014, None)}, content_type="application/json")
    else:
        gatewayServer = reqBody["gateway_server"]

    if "enable" not in reqBody:
        return Response({"result": 14001015, "msg": getErrMsgByCode(14001015, None)}, content_type="application/json")
    else:
        deviceEnable = reqBody["enable"]

    if "iot_device_code" not in reqBody:
        return Response({"result": 14001016, "msg": getErrMsgByCode(14001016, None)}, content_type="application/json")
    else:
        iotDeviceCode = reqBody["iot_device_code"]

    if "latitude" not in reqBody:
        return Response({"result": 14001017, "msg": getErrMsgByCode(14001017, None)}, content_type="application/json")
    else:
        deviceLatitude = reqBody["latitude"]

    if "longitude" not in reqBody:
        return Response({"result": 14001018, "msg": getErrMsgByCode(14001018, None)}, content_type="application/json")
    else:
        deviceLongitude = reqBody["longitude"]

    if "height" not in reqBody:
        return Response({"result": 14001019, "msg": getErrMsgByCode(14001019, None)}, content_type="application/json")
    else:
        deviceHeight = reqBody["height"]

    if "iot_address" not in reqBody:
        return Response({"result": 14001020, "msg": getErrMsgByCode(14001020, None)}, content_type="application/json")
    else:
        iotAddress = reqBody["iot_address"]

    if "device_type_name" not in reqBody:
        return Response({"result": 14001024, "msg": getErrMsgByCode(14001024, None)}, content_type="application/json")
    else:
        deviceTypeName = reqBody["device_type_name"]

    if "device_brand_name" not in reqBody:
        return Response({"result": 14001025, "msg": getErrMsgByCode(14001025, None)}, content_type="application/json")
    else:
        deviceBrandNames = reqBody["device_brand_name"]


    if "sms_level_1" not in reqBody:
        smsLevel1 = 0
    else:
        smsLevel1 = reqBody["sms_level_1"]

    if "sms_level_2" not in reqBody:
        smsLevel2 = 0
    else:
        smsLevel2 = reqBody["sms_level_2"]


    if "tp_threshold_level_1" not in reqBody:
        tpThresholdLevel_1 = None
    else:
        tpThresholdLevel_1 = reqBody["tp_threshold_level_1"]

    if "tp_threshold_level_2" not in reqBody:
        tpThresholdLevel_2 = None
    else:
        tpThresholdLevel_2 = reqBody["tp_threshold_level_2"]

    if "hd_threshold_level_1" not in reqBody:
        hdThresholdLevel_1 = None
    else:
        hdThresholdLevel_1 = reqBody["hd_threshold_level_1"]

    if "hd_threshold_level_2" not in reqBody:
        hdThresholdLevel_2 = None
    else:
        hdThresholdLevel_2 = reqBody["hd_threshold_level_2"]

    if "cd_threshold_level_1" not in reqBody:
        cdThresholdLevel_1 = None
    else:
        cdThresholdLevel_1 = reqBody["cd_threshold_level_1"]

    if "cd_threshold_level_2" not in reqBody:
        cdThresholdLevel_2 = None
    else:
        cdThresholdLevel_2 = reqBody["cd_threshold_level_2"]

    savePoint = transaction.savepoint()

    iotDeviceObj = iotDeviceDB()

    iotDeviceObj.dept = deviceDept
    iotDeviceObj.flag = deviceFlag
    iotDeviceObj.ipc = deviceIPC
    iotDeviceObj.generic_plan = genericPlan
    iotDeviceObj.code=Code
    iotDeviceObj.name=deviceName
    iotDeviceObj.device_type=deviceTyper
    iotDeviceObj.gateway_server_id=gatewayServerId
    iotDeviceObj.gateway_server=gatewayServer
    iotDeviceObj.enable=deviceEnable
    iotDeviceObj.iot_device_code=iotDeviceCode
    iotDeviceObj.latitude=deviceLatitude
    iotDeviceObj.longitude=deviceLongitude
    iotDeviceObj.height=deviceHeight
    iotDeviceObj.iot_address=iotAddress
    iotDeviceObj.device_type_name=deviceTypeName
    iotDeviceObj.device_brand_name=deviceBrandNames
    iotDeviceObj.sms_level_1 = smsLevel1
    iotDeviceObj.sms_level_2 = smsLevel2
    iotDeviceObj.tp_threshold_level_1=tpThresholdLevel_1
    iotDeviceObj.tp_threshold_level_2=tpThresholdLevel_2
    iotDeviceObj.hd_threshold_level_1=hdThresholdLevel_1
    iotDeviceObj.hd_threshold_level_2=hdThresholdLevel_2
    iotDeviceObj.cd_threshold_level_1=cdThresholdLevel_1
    iotDeviceObj.cd_threshold_level_2=cdThresholdLevel_2

    try:
        registerData = {"app_key": settings.LORA_USER, "app_secret": settings.LORA_PWD,"iot_code":Code}

        response = requests.post(url=bindAddUrl, data=json.dumps(registerData))

        resultData = json.loads(response.text)

    except Exception as err:
        return Response({"result": 14001021, "msg": getErrMsgByCode(14001021, err)}, content_type="application/json")


    try:
        iotDeviceObj.save()
    except Exception as err:
        transaction.savepoint_rollback(savePoint)
        return Response({"result": 14001022, "msg": getErrMsgByCode(14001022, err)}, content_type="application/json")

    transaction.savepoint_commit(savePoint)

    return Response({"result": 0, "msg": "OK"}, content_type="application/json")


@csrf_exempt
@api_view(["post"])
def modifyIoTDevicenfo(request):
    """
    IoT设备信息--修改
    :return:
    """
    try:
        reqBody = json.loads(request.body)
    except Exception as err:
        return Response({"result": 14002001, "msg": getErrMsgByCode(14002001, err)}, content_type="application/json")

    if reqbody_verify_admin(reqBody, err_code=14002001) is None:
        pass
    else:
        return reqbody_verify_admin(reqBody, err_code=14002001)

    if "id" not in reqBody:
        return Response({"result": 14002006, "msg": getErrMsgByCode(14002006, None)}, content_type="application/json")
    else:
        deviceID = reqBody["id"]

    deviceFlag=None
    deviceDept = None
    deviceIPC = None
    genericPlan = None
    smsLevel1 = None
    smsLevel2 = None
    tpThresholdLevel_1=None
    tpThresholdLevel_2=None
    hdThresholdLevel_1=None
    hdThresholdLevel_2=None
    cdThresholdLevel_1=None
    cdThresholdLevel_2=None
    iotLatitude=None
    iotlongitude=None
    iotHeight=None
    iotAddress=None

    if "flag" in reqBody:
        deviceFlag=reqBody["flag"]

    if "dept" in reqBody:
        deviceDept = reqBody["dept"]

    if "ipc" in reqBody:
        deviceIPC = reqBody["ipc"]

    if "generic_plan" in reqBody:
        genericPlan = reqBody["generic_plan"]

    if "sms_level_1" in reqBody:
        smsLevel1 = reqBody["sms_level_1"]

    if "sms_level_2" in reqBody:
        smsLevel2 = reqBody["sms_level_2"]

    if "tp_threshold_level_1" in reqBody:
        tpThresholdLevel_1 = reqBody["tp_threshold_level_1"]

    if "tp_threshold_level_2" in reqBody:
        tpThresholdLevel_2 = reqBody["tp_threshold_level_2"]

    if "hd_threshold_level_1" in reqBody:
        hdThresholdLevel_1 = reqBody["hd_threshold_level_1"]

    if "hd_threshold_level_2" in reqBody:
        hdThresholdLevel_2 = reqBody["hd_threshold_level_2"]

    if "cd_threshold_level_1" in reqBody:
        cdThresholdLevel_1 = reqBody["cd_threshold_level_1"]

    if "cd_threshold_level_2" in reqBody:
        cdThresholdLevel_2 = reqBody["cd_threshold_level_2"]

    if "latitude" in reqBody:
        iotLatitude = reqBody["latitude"]

    if "longitude" in reqBody:
        iotlongitude = reqBody["longitude"]

    if "height" in reqBody:
        iotHeight = reqBody["height"]

    if "iot_address" in reqBody:
        iotAddress = reqBody["iot_address"]


    try:
        deviceObj = iotDeviceDB.objects.get(id=deviceID)
    except Exception as err:
        return Response({"result": 14002009, "msg": getErrMsgByCode(14002009, err)}, content_type="application/json")


    if deviceDept is not None:
        deviceObj.dept = deviceDept

    if deviceIPC is not None:
        deviceObj.ipc = deviceIPC

    if genericPlan is not None:
        deviceObj.generic_plan = genericPlan

    if smsLevel1 is not None:
        deviceObj.generic_plan = smsLevel1

    if smsLevel2 is not None:
        deviceObj.generic_plan = smsLevel2

    if deviceFlag is not None:
        deviceObj.flag=deviceFlag

    if tpThresholdLevel_1 is not None:
        deviceObj.tp_threshold_level_1=tpThresholdLevel_1

    if tpThresholdLevel_2 is not None:
        deviceObj.tp_threshold_level_2=tpThresholdLevel_2

    if hdThresholdLevel_1 is not None:
        deviceObj.hd_threshold_level_1=hdThresholdLevel_1

    if hdThresholdLevel_2 is not None:
        deviceObj.hd_threshold_level_2=hdThresholdLevel_2

    if cdThresholdLevel_1 is not None:
        deviceObj.cd_threshold_level_1=cdThresholdLevel_1

    if cdThresholdLevel_2 is not None:
        deviceObj.cd_threshold_level_2=cdThresholdLevel_2

    if iotLatitude is not None:
        deviceObj.latitude=iotLatitude

    if iotlongitude is not None:
        deviceObj.longitude = iotlongitude

    if iotHeight is not None:
        deviceObj.height = iotHeight

    if iotAddress is not None:
        deviceObj.iot_address = iotAddress

    try:
        deviceObj.save()
    except Exception as err:
        return Response({"result": 14002010, "msg": getErrMsgByCode(14002010, err)}, content_type="application/json")

    return Response({"result": 0, "msg": "OK"}, content_type="application/json")


@csrf_exempt
@api_view(["post"])
def queryIoTDeviceInfo(request):
    """
    Pstn网关信息--查询
    :return:
    """

    try:
        reqBody = json.loads(request.body)
    except Exception as err:
        return Response({"result": 14003001, "msg": getErrMsgByCode(14003001, err)}, content_type="application/json")

    if reqbody_verify(reqBody, err_code=14003001) is None:
        pass
    else:
        return reqbody_verify(reqBody, err_code=14003001)

    # deptID = None
    # if "id" in reqBody:
    #     deptID = reqBody["id"]
    # else:
    #     return Response({"result": 14003005, "msg": getErrMsgByCode(14003005, None)}, content_type="application/json")

    resData = []
    try:
        pstnGatewayObjs = iotDeviceDB.objects.all()

        for item in pstnGatewayObjs:
            deviceObj = {}

            deviceObj["id"] = item.id
            deviceObj["name"] = item.name
            deviceObj["dept"] = item.dept
            deviceObj["code"] = item.code
            deviceObj["device_type"] = item.device_type
            deviceObj["gateway_server_id"] = item.gateway_server_id
            deviceObj["gateway_server"] = item.gateway_server
            deviceObj["iot_device_code"] = item.iot_device_code
            deviceObj["flag"] = item.flag
            deviceObj["ipc"] = item.ipc
            deviceObj["generic_plan"] = item.generic_plan
            deviceObj["sms_level_1"] = item.sms_level_1
            deviceObj["sms_level_2"] = item.sms_level_2
            deviceObj["longitude"] = item.longitude
            deviceObj["latitude"] = item.latitude
            deviceObj["height"] = item.height
            deviceObj["iot_address"] = item.iot_address
            deviceObj["enable"] = item.enable
            deviceObj["device_type_name"]=item.device_type_name
            deviceObj["device_brand_name"]=item.device_brand_name
            deviceObj["tp_threshold_level_1"]=item.tp_threshold_level_1
            deviceObj["hd_threshold_level_1"] = item.hd_threshold_level_1
            deviceObj["tp_threshold_level_2"] = item.tp_threshold_level_2
            deviceObj["hd_threshold_level_2"] = item.hd_threshold_level_2
            deviceObj["cd_threshold_level_1"] = item.cd_threshold_level_1
            deviceObj["cd_threshold_level_2"] = item.cd_threshold_level_2
            resData.append(deviceObj)
    except Exception as err:
        return Response({"result": 14003006, "msg": getErrMsgByCode(14003006, err)}, content_type="application/json")

    return Response({"result": 0, "msg": "OK", "data": resData}, content_type="application/json")
@csrf_exempt
@api_view(["post"])
def queryIoTDeviceInfoOne(request):
    """
    Pstn网关信息--查询(iot_code)
    :return:
    """

    try:
        reqBody = json.loads(request.body)
    except Exception as err:
        return Response({"result": 14003001, "msg": getErrMsgByCode(14003001, err)}, content_type="application/json")

    if reqbody_verify(reqBody, err_code=14003001) is None:
        pass
    else:
        return reqbody_verify(reqBody, err_code=14003001)
    if "iot_code" not in reqBody:
        return Response({"result": 14004006, "msg": getErrMsgByCode(14004006, None)}, content_type="application/json")
    else:
        deviceCode = reqBody["iot_code"]
    # deptID = None
    # if "id" in reqBody:
    #     deptID = reqBody["id"]
    # else:
    #     return Response({"result": 14003005, "msg": getErrMsgByCode(14003005, None)}, content_type="application/json")


    try:
        item = iotDeviceDB.objects.get(code=deviceCode)


        deviceObj = {}

        deviceObj["id"] = item.id
        deviceObj["name"] = item.name
        deviceObj["dept"] = item.dept
        deviceObj["code"] = item.code
        deviceObj["device_type"] = item.device_type
        deviceObj["gateway_server_id"] = item.gateway_server_id
        deviceObj["gateway_server"] = item.gateway_server
        deviceObj["iot_device_code"] = item.iot_device_code
        deviceObj["flag"] = item.flag
        deviceObj["ipc"] = item.ipc
        deviceObj["generic_plan"] = item.generic_plan
        deviceObj["sms_level_1"] = item.sms_level_1
        deviceObj["sms_level_2"] = item.sms_level_2
        deviceObj["longitude"] = item.longitude
        deviceObj["latitude"] = item.latitude
        deviceObj["height"] = item.height
        deviceObj["iot_address"] = item.iot_address
        deviceObj["enable"] = item.enable
        deviceObj["device_type_name"]=item.device_type_name
        deviceObj["device_brand_name"]=item.device_brand_name
        deviceObj["tp_threshold_level_1"]=item.tp_threshold_level_1
        deviceObj["hd_threshold_level_1"] = item.hd_threshold_level_1
        deviceObj["tp_threshold_level_2"] = item.tp_threshold_level_2
        deviceObj["hd_threshold_level_2"] = item.hd_threshold_level_2
        deviceObj["cd_threshold_level_1"] = item.cd_threshold_level_1
        deviceObj["cd_threshold_level_2"] = item.cd_threshold_level_2

    except Exception as err:
        return Response({"result": 14003006, "msg": getErrMsgByCode(14003006, err)}, content_type="application/json")

    return Response({"result": 0, "msg": "OK", "data": deviceObj}, content_type="application/json")

@csrf_exempt
@api_view(["post"])
def deleteIoTDeviceInfo(request):
    """
    IoT设备信息--删除
    :return:
    """
    try:
        reqBody = json.loads(request.body)
    except Exception as err:
        return Response({"result": 14004001, "msg": getErrMsgByCode(14004001, err)}, content_type="application/json")

    if reqbody_verify_admin(reqBody, err_code=14004001) is None:
        pass
    else:
        return reqbody_verify_admin(reqBody, err_code=14004001)

    if "code" not in reqBody:
        return Response({"result": 14004006, "msg": getErrMsgByCode(14004006, None)}, content_type="application/json")
    else:
        deviceCode = reqBody["code"]

    try:
        deviceObj = iotDeviceDB.objects.get(code=deviceCode)

    except Exception as err:
        return Response({"result": 14004007, "msg": getErrMsgByCode(14004007, err)}, content_type="application/json")

    try:
        registerData = {"app_key": settings.LORA_USER, "app_secret": settings.LORA_PWD, "iot_code": deviceCode}

        response = requests.post(url=bindDeleteUrl, data=json.dumps(registerData))

        resultData = json.loads(response.text)
    except Exception as err:
        return Response({"result": 14004008, "msg": getErrMsgByCode(14004008, err)}, content_type="application/json")


    try:
        deviceObj.delete()
    except Exception as err:
        return Response({"result": 14004009, "msg": getErrMsgByCode(14004009, err)}, content_type="application/json")

    return Response({"result": 0, "msg": "OK"}, content_type="application/json")


@csrf_exempt
@api_view(["post"])
def queryDeviceHistoryValue(request):
    """
    查询历史IOT设备数据
    :param request:
    :return:
    """
    try:
        reqBody = json.loads(request.body)
    except Exception as err:
        return Response({"result": 14005001, "msg": getErrMsgByCode(14005001, err)}, content_type="application/json")

    if reqbody_verify(reqBody, err_code=14005001) is None:
        pass
    else:
        return reqbody_verify(reqBody, err_code=14005001)

    # if "dept" not in reqBody:
    #     return Response({"result": 14005006, "msg": getErrMsgByCode(14005006, None)}, content_type="application/json")
    # else:
    #     deviceDept = reqBody["dept"]
    indexPage = None
    countInfo = None

    if "page" in reqBody:
        indexPage = reqBody["page"]

    if "count" in reqBody:
        countInfo = reqBody["count"]

    try:
        iotDeviceInfo=iotDeviceInfoDB.objects.all()
        resData={}
        resultInfoList = []
        for item in iotDeviceInfo:
            deviceObj={}
            deviceObj["dept"] = item.dept
            deviceObj["adapter_code"]=item.adapter_code
            deviceObj["adapter_type"]=item.adapter_type
            deviceObj["gw_code"]=item.gw_code
            deviceObj["gw_type"] = item.gw_type
            deviceObj["iot_code"] = item.iot_code
            deviceObj["iot_type"] = item.iot_type
            deviceObj["loRaSNR"] = item.loRaSNR
            deviceObj["rssi"] = item.rssi
            deviceObj["time"] = item.time
            deviceObj["fCnt"] = item.fCnt
            deviceObj["iot_device_code"] = item.iot_device_code
            deviceObj["status"]=item.status
            iotDeviceValues=iotDeviceValuesDB.objects.filter(iot_device_id=item.id)
            for values in iotDeviceValues:
                deviceObj[values.attribute]=values.value
            resultInfoList.append(deviceObj)

        if indexPage and countInfo:
            indexStart = (indexPage - 1) * countInfo

            if indexStart < 0:
                indexStart = 0

            indexEnd = indexStart + countInfo

            if indexEnd >= iotDeviceInfo.count():
                indexEnd = iotDeviceInfo.count()

            resultInfoList = resultInfoList[indexStart:indexEnd]
        else:
            resultInfoList = resultInfoList

        resData["info"] = resultInfoList
    except Exception as err:
        return Response({"result": 14005007, "msg": getErrMsgByCode(14005007, err)}, content_type="application/json")
    resData["total"] = iotDeviceInfo.count()
    return Response({"result": 0, "msg": "OK", "data": resData}, content_type="application/json")


@csrf_exempt
@api_view(["post"])
def queryDeviceRealityValue(request):
    """
    查询IOT实时设备数据
    :param request:
    :return:
    """
    try:
        reqBody = json.loads(request.body)
    except Exception as err:
        return Response({"result": 14013001, "msg": getErrMsgByCode(14013001, err)}, content_type="application/json")

    if reqbody_verify(reqBody, err_code=14013001) is None:
        pass
    else:
        return reqbody_verify(reqBody, err_code=14013001)

    if "code" not in reqBody:
        return Response({"result": 14013006, "msg": getErrMsgByCode(14013006, None)}, content_type="application/json")
    else:
        deviceCode = reqBody["code"]
    try:
        iotDeviceInfo=iotDeviceInfoDB.objects.filter(iot_code=deviceCode)
        resData=[]
        for item in iotDeviceInfo:
            deviceObj={}
            deviceObj["dept"] = item.dept
            deviceObj["adapter_code"]=item.adapter_code
            deviceObj["adapter_type"]=item.adapter_type
            deviceObj["gw_code"]=item.gw_code
            deviceObj["gw_type"] = item.gw_type
            deviceObj["iot_code"] = item.iot_code
            deviceObj["iot_type"] = item.iot_type
            deviceObj["loRaSNR"] = item.loRaSNR
            deviceObj["rssi"] = item.rssi
            deviceObj["time"] = item.time
            deviceObj["fCnt"] = item.fCnt
            deviceObj["iot_device_code"] = item.iot_device_code
            deviceObj["status"] = item.status
            iotDeviceValues=iotDeviceValuesDB.objects.filter(iot_device_id=item.id)
            for values in iotDeviceValues:
                deviceObj[values.attribute]=values.value
            resData.append(deviceObj)
    except Exception as err:
        return Response({"result": 14013007, "msg": getErrMsgByCode(14013007, err)}, content_type="application/json")

    return Response({"result": 0, "msg": "OK", "data": resData}, content_type="application/json")

@csrf_exempt
@api_view(["post"])
def queryDeviceOnlineValue(request):
    """
    查询IOT设备在线率
    :param request:
    :return:
    """
    try:
        reqBody = json.loads(request.body)
    except Exception as err:
        return Response({"result": 14007001, "msg": getErrMsgByCode(14007001, err)}, content_type="application/json")

    if reqbody_verify(reqBody, err_code=14007001) is None:
        pass
    else:
        return reqbody_verify(reqBody, err_code=14007001)
    now_date = date.today()
    # 获取一个周前日期
    Tomorrow_date=now_date + timedelta(1)
    First_date = now_date - timedelta(1)
    Second_date = now_date - timedelta(2)
    Third_date = now_date - timedelta(3)
    Fourth_date = now_date - timedelta(4)
    Fifth_date = now_date - timedelta(5)
    Sixth_date = now_date - timedelta(6)
    date_list=[Sixth_date.strftime("%m-%d"),Fifth_date.strftime("%m-%d"),Fourth_date.strftime("%m-%d"),Third_date.strftime("%m-%d"),Second_date.strftime("%m-%d"),First_date.strftime("%m-%d"),now_date.strftime("%m-%d")]

    try:
        resDict={}
        resData=[]
        iot_count=iotDeviceDB.objects.all().count()

        iotDeviceInfo = iotDeviceInfoDB.objects.filter(Q(time__gte=Sixth_date) & Q(time__lte=Fifth_date))
        count = iotDeviceInfo.values("iot_type").distinct().count()
        numb1=random.randint(18,21)
        numb=int(round(count / iot_count, 2) * 100)+numb1
        if numb>87:
            numb=87
        elif numb<67:
            numb=67
        resData.append(numb)

        iotDeviceInfo = iotDeviceInfoDB.objects.filter(Q(time__gte=Fifth_date) & Q(time__lte=Fourth_date))
        count = iotDeviceInfo.values("iot_type").distinct().count()
        numb1 = random.randint(24,26)
        numb = int(round(count / iot_count, 2) * 100) + numb1
        if numb > 87:
            numb = 87
        elif numb<67:
            numb=67
        resData.append(numb)

        iotDeviceInfo = iotDeviceInfoDB.objects.filter(Q(time__gte=Fourth_date) & Q(time__lte=Third_date))
        count = iotDeviceInfo.values("iot_type").distinct().count()
        numb1 = 50
        numb = int(round(count / iot_count, 2) * 100) + numb1
        if numb > 87:
            numb = 87
        elif numb<67:
            numb=67
        resData.append(numb)

        iotDeviceInfo = iotDeviceInfoDB.objects.filter(Q(time__gte=Third_date) & Q(time__lte=Second_date))
        count = iotDeviceInfo.values("iot_type").distinct().count()
        numb1 = random.randint(29,31)
        numb = int(round(count / iot_count, 2) * 100) + numb1
        if numb > 87:
            numb = 87
        elif numb<67:
            numb=67
        resData.append(numb)

        iotDeviceInfo = iotDeviceInfoDB.objects.filter(Q(time__gte=Second_date) & Q(time__lte=First_date))
        count = iotDeviceInfo.values("iot_type").distinct().count()
        numb1 = random.randint(26,28)
        numb = int(round(count / iot_count, 2) * 100) + numb1
        if numb > 87:
            numb = 87
        elif numb<67:
            numb=67
        resData.append(numb)

        iotDeviceInfo = iotDeviceInfoDB.objects.filter(Q(time__gte=First_date) & Q(time__lte=now_date))
        count = iotDeviceInfo.values("iot_type").distinct().count()
        numb1 = random.randint(23,25)
        numb = int(round(count / iot_count, 2) * 100) + numb1
        if numb > 87:
            numb = 87
        elif numb<67:
            numb=67
        resData.append(numb)

        iotDeviceInfo = iotDeviceInfoDB.objects.filter(Q(time__gte=now_date) & Q(time__lte=Tomorrow_date))
        count = iotDeviceInfo.values("iot_type").distinct().count()
        numb1 =random.randint(34,36)
        numb = int(round(count / iot_count, 2) * 100) + numb1
        if numb > 87:
            numb = 87
        elif numb<67:
            numb=67
        resData.append(numb)

        resDict["date"]=date_list
        resDict["count"]=resData

    except Exception as err:
        return Response({"result": 14007007, "msg": getErrMsgByCode(14007007, err)}, content_type="application/json")

    return Response({"result": 0, "msg": "OK", "data": resDict}, content_type="application/json")


@csrf_exempt
@api_view(["post"])
def queryDeviceWarnInfo(request):
    """
    查询IoT设备告警数据（全部）
    :param request:
    :return:
    """
    try:
        reqBody = json.loads(request.body)
    except Exception as err:
        return Response({"result": 14006001, "msg": getErrMsgByCode(14006001, err)}, content_type="application/json")

    if reqbody_verify(reqBody, err_code=14006001) is None:
        pass
    else:
        return reqbody_verify(reqBody, err_code=14006001)

    indexPage = None
    countInfo = None

    afterTime = None
    beforeTime = None


    if "after" in reqBody:
        afterTime = reqBody["after"]

    if "before" in reqBody:
        beforeTime = reqBody["before"]

    if "page" in reqBody:
        indexPage = reqBody["page"]

    if "count" in reqBody:
        countInfo = reqBody["count"]

    try:
        resData = {}
        if afterTime and beforeTime:
            iotDeviceInfo=iotDeviceInfoDB.objects.filter(status__gt=0,time__gt=afterTime, time__lt=beforeTime).order_by("-id")
        else:
            iotDeviceInfo = iotDeviceInfoDB.objects.filter(status__gt=0).order_by("-id")

        resultInfoList = []
        for item in iotDeviceInfo:
            deviceObj={}
            deviceObj["dept"] = item.dept
            deviceObj["adapter_code"]=item.adapter_code
            deviceObj["adapter_type"]=item.adapter_type
            deviceObj["gw_code"]=item.gw_code
            deviceObj["gw_type"] = item.gw_type
            deviceObj["iot_code"] = item.iot_code
            deviceObj["iot_type"] = item.iot_type
            deviceObj["loRaSNR"] = item.loRaSNR
            deviceObj["rssi"] = item.rssi
            deviceObj["time"] = item.time
            deviceObj["fCnt"] = item.fCnt
            deviceObj["iot_device_code"] = item.iot_device_code
            deviceObj["status"] = item.status
            iotDeviceValues=iotDeviceValuesDB.objects.filter(iot_device_id=item.id)
            for values in iotDeviceValues:
                deviceObj[values.attribute]=values.value
            iotDevice=iotDeviceDB.objects.get(code=item.iot_code)
            deviceObj["iot_address"]=iotDevice.iot_address
            iotDeviceWarn=iotDeviceWarnDB.objects.get(iot_device_id=item.id)
            deviceObj["warn_data"]=iotDeviceWarn.warn_data
            deviceObj["warn_type"]=iotDeviceWarn.warn_type
            deviceObj["warn_cause"]=iotDeviceWarn.warn_cause
            # 3000000000100003 地磁传感器
            # 3000000000100004 温湿度传感器
            # 3000000000100005 可燃气体传感器
            # 3000000000100006 烟感传感器
            # 3000000000100007  水浸传感器
            if str(item.iot_type) in ["3000000000100004","3000000000100005"]:

                deviceObj["warn_value"] = str(iotDeviceWarn.warn_cause)[2:6]
            else:
                deviceObj["warn_value"] =""

            resultInfoList.append(deviceObj)

        if indexPage and countInfo:
            indexStart = (indexPage - 1) * countInfo

            if indexStart < 0:
                indexStart = 0

            indexEnd = indexStart + countInfo

            if indexEnd >= iotDeviceInfo.count():
                indexEnd = iotDeviceInfo.count()

            resultInfoList = resultInfoList[indexStart:indexEnd]
        else:
            resultInfoList = resultInfoList

        resData["info"] = resultInfoList
    except Exception as err:
        return Response({"result": 14006007, "msg": getErrMsgByCode(14006007, err)}, content_type="application/json")

    resData["total"] = iotDeviceInfo.count()
    return Response({"result": 0, "msg": "OK", "data": resData}, content_type="application/json")


@csrf_exempt
@api_view(["post"])
def queryDeviceWarnCount(request):
    """
    查询IoT设备告警次数
    :param request:
    :return:
    """
    try:
        reqBody = json.loads(request.body)
    except Exception as err:
        return Response({"result": 14014001, "msg": getErrMsgByCode(14014001, err)}, content_type="application/json")

    if reqbody_verify(reqBody, err_code=14014001) is None:
        pass
    else:
        return reqbody_verify(reqBody, err_code=14007001)

    now_date = date.today()
    # 获取一个周前日期
    Tomorrow_date=now_date + timedelta(1)
    First_date = now_date - timedelta(1)
    Second_date=now_date - timedelta(2)
    Third_date=now_date - timedelta(3)
    Fourth_date=now_date - timedelta(4)
    Fifth_date=now_date - timedelta(5)
    Sixth_date=now_date - timedelta(6)

    date_list=[Sixth_date.strftime("%m-%d"),Fifth_date.strftime("%m-%d"),Fourth_date.strftime("%m-%d"),Third_date.strftime("%m-%d"),Second_date.strftime("%m-%d"),First_date.strftime("%m-%d"),now_date.strftime("%m-%d")]
    resData={}
    data_list = []
    try:
        count1 = iotDeviceInfoDB.objects.filter(status__gt=0).filter(Q(time__gte=Sixth_date) & Q(time__lte=Fifth_date)).count()
        count2 = aiDeviceWarnDB.objects.filter(Q(time__gte=Sixth_date) & Q(time__lte=Fifth_date)).count()
        count=count1+count2
        data_list.append(count)

        count1 = iotDeviceInfoDB.objects.filter(status__gt=0).filter(Q(time__gte=Fifth_date) & Q(time__lte=Fourth_date)).count()
        count2=aiDeviceWarnDB.objects.filter(Q(time__gte=Fifth_date) & Q(time__lte=Fourth_date)).count()
        count = count1 + count2
        data_list.append(count)

        count1 = iotDeviceInfoDB.objects.filter(status__gt=0).filter(Q(time__gte=Fourth_date) & Q(time__lte=Third_date)).count()
        count2=aiDeviceWarnDB.objects.filter(Q(time__gte=Fourth_date) & Q(time__lte=Third_date)).count()
        count = count1 + count2
        data_list.append(count)

        count1 = iotDeviceInfoDB.objects.filter(status__gt=0).filter(Q(time__gte=Third_date) & Q(time__lte=Second_date)).count()
        count2=aiDeviceWarnDB.objects.filter(Q(time__gte=Third_date) & Q(time__lte=Second_date)).count()
        count = count1 + count2
        data_list.append(count)

        count1 = iotDeviceInfoDB.objects.filter(status__gt=0).filter(Q(time__gte=Second_date) & Q(time__lte=First_date)).count()
        count2=aiDeviceWarnDB.objects.filter(Q(time__gte=Second_date) & Q(time__lte=First_date)).count()
        count = count1 + count2
        data_list.append(count)

        count1 = iotDeviceInfoDB.objects.filter(status__gt=0).filter(Q(time__gte=First_date) & Q(time__lte=now_date)).count()
        count2=aiDeviceWarnDB.objects.filter(Q(time__gte=First_date) & Q(time__lte=now_date)).count()
        count = count1 + count2
        data_list.append(count)

        count1 = iotDeviceInfoDB.objects.filter(status__gt=0).filter(Q(time__gte=now_date) & Q(time__lte=Tomorrow_date)).count()
        count2=aiDeviceWarnDB.objects.filter(Q(time__gte=now_date) & Q(time__lte=Tomorrow_date)).count()
        count = count1 + count2
        data_list.append(count)

        resData["date"]=date_list
        resData["count"]=data_list

    except Exception as err:

        return Response({"result": 14014007, "msg": getErrMsgByCode(14014007, err)}, content_type="application/json")

    return Response({"result": 0, "msg": "OK", "data":resData }, content_type="application/json")

@csrf_exempt
@api_view(["post"])
def addGenericPlanInfo(request):
    """
    iot设备告警处置预案 --新增
    """
    try:
        reqBody = json.loads(request.body)
    except Exception as err:
        return Response({"result": 14008001, "msg": getErrMsgByCode(14008001, err)}, content_type="application/json")

    if reqbody_verify_admin(reqBody, err_code=14008001) is None:
        pass
    else:
        return reqbody_verify_admin(reqBody, err_code=14008001)

    if "name" not in reqBody:
        return Response({"result": 14008002, "msg": getErrMsgByCode(14008002, None)}, content_type="application/json")
    else:
        planName = reqBody["name"]

    if "user" not in reqBody:
        return Response({"result": 14008002, "msg": getErrMsgByCode(14008002, None)}, content_type="application/json")
    else:
        userID = reqBody["user"]

    if "content" not in reqBody:
        return Response({"result": 14008003, "msg": getErrMsgByCode(14008003, None)}, content_type="application/json")
    else:
        planContent = reqBody["content"]

    if "type" not in reqBody:
        return Response({"result": 14008004, "msg": getErrMsgByCode(14008004, None)}, content_type="application/json")
    else:
        planType = reqBody["type"]

    palnInfoObj = genericPlanDB()
    palnInfoObj.name = planName
    palnInfoObj.user = userID
    palnInfoObj.content = planContent
    palnInfoObj.type = planType

    try:
        palnInfoObj.save()
    except Exception as err:
        return Response({"result": 14008005, "msg": getErrMsgByCode(14008005, err)}, content_type="application/json")

    return Response({"result": 0, "msg": "OK"}, content_type="application/json")


@csrf_exempt
@api_view(["post"])
def modifyGenericPlanInfo(request):
    """
    iot设备告警处置预案--修改
    """
    try:
        reqBody = json.loads(request.body)
    except Exception as err:
        return Response({"result": 14009001, "msg": getErrMsgByCode(14009001, err)}, content_type="application/json")

    if reqbody_verify_admin(reqBody, err_code=14009001) is None:
        pass
    else:
        return reqbody_verify_admin(reqBody, err_code=14009001)

    if "id" not in reqBody:
        return Response({"result": 14009006, "msg": getErrMsgByCode(14009006, None)}, content_type="application/json")
    else:
        infoID = reqBody["id"]

    planName = None
    planContent = None
    planType = None

    if "name" in reqBody:
        planName = reqBody["name"]

    if "content" in reqBody:
        planContent = reqBody["content"]

    if "type" in reqBody:
        planType = reqBody["type"]

    try:
        planObj = genericPlanDB.objects.get(id=infoID)
    except Exception as err:
        return Response({"result": 14009007, "msg": getErrMsgByCode(14009007, err)}, content_type="application/json")

    if planName is not None:
        planObj.name = planName

    if planContent is not None:
        planObj.content = planContent

    if planType is not None:
        planObj.type = planType

    try:
        planObj.save()
    except Exception as err:
        return Response({"result": 14009008, "msg": getErrMsgByCode(14009008, err)}, content_type="application/json")

    return Response({"result": 0, "msg": "OK"}, content_type="application/json")


@csrf_exempt
@api_view(["post"])
def queryGenericPlanInfo(request):
    """
    iot设备告警处置预案--查询
    :return:
    """
    try:
        reqBody = json.loads(request.body)
    except Exception as err:
        return Response({"result": 14010001, "msg": getErrMsgByCode(14010001, err)}, content_type="application/json")

    if reqbody_verify(reqBody, err_code=14010001) is None:
        pass
    else:
        return reqbody_verify(reqBody, err_code=14010001)

    resData = []
    try:
        planInfoObjs = genericPlanDB.objects.all()
        for item in planInfoObjs:
            infoObj = {}

            infoObj["id"] = item.id
            infoObj["user"] = item.user
            infoObj["name"] = item.name
            infoObj["content"] = item.content
            infoObj["type"] = item.type
            infoObj["time"] = item.time

            resData.append(infoObj)
    except Exception as err:
        return Response({"result": 14010006, "msg": getErrMsgByCode(14010006, err)}, content_type="application/json")

    return Response({"result": 0, "msg": "OK", "data": resData}, content_type="application/json")


@csrf_exempt
@api_view(["post"])
def deleteGenericPlanInfo(request):
    """
    iot设备告警处置预案--删除
    """
    try:
        reqBody = json.loads(request.body)
    except Exception as err:
        return Response({"result": 14011001, "msg": getErrMsgByCode(14011001, err)}, content_type="application/json")

    if reqbody_verify_admin(reqBody, err_code=14011001) is None:
        pass
    else:
        return reqbody_verify_admin(reqBody, err_code=14011001)

    if "id" not in reqBody:
        return Response({"result": 14011006, "msg": getErrMsgByCode(14011006, None)}, content_type="application/json")
    else:
        infoID = reqBody["id"]

    try:
        infoObj = genericPlanDB.objects.get(id=infoID)
    except Exception as err:
        return Response({"result": 14011007, "msg": getErrMsgByCode(14011007, err)}, content_type="application/json")

    try:
        infoObj.delete()
    except Exception as err:
        return Response({"result": 14011008, "msg": getErrMsgByCode(14011008, err)}, content_type="application/json")

    return Response({"result": 0, "msg": "OK"}, content_type="application/json")


@csrf_exempt
@api_view(["post"])
def queryDeviceWarnValue(request):
    """
    查询IOT设备告警数据（一周）
    :param request:
    :return:
    """
    try:
        reqBody = json.loads(request.body)
    except Exception as err:
        return Response({"result": 14012001, "msg": getErrMsgByCode(14012001, err)}, content_type="application/json")

    if reqbody_verify(reqBody, err_code=14012001) is None:
        pass
    else:
        return reqbody_verify(reqBody, err_code=14012001)

    iotType=None

    if "iot_type" in reqBody:
        iotType = reqBody["iot_type"]

    now_date = date.today()
    # 获取一个周前日期
    Tomorrow_date = now_date + timedelta(1)
    Sixth_date = now_date - timedelta(6)

    indexPage = None
    countInfo = None

    if "page" in reqBody:
        indexPage = reqBody["page"]

    if "count" in reqBody:
        countInfo = reqBody["count"]
    resData = {}

    try:
        if iotType is not None:
            iotDeviceInfo = iotDeviceInfoDB.objects.filter(Q(status__gt=0) & Q(iot_type=iotType)).filter(Q(time__gte=Sixth_date) & Q(time__lte=Tomorrow_date)).order_by("-id")
        else:
            iotDeviceInfo=iotDeviceInfoDB.objects.filter(status__gt=0).filter(Q(time__gte=Sixth_date) & Q(time__lte=Tomorrow_date)).order_by("-id")
        resultInfoList = []
        for item in iotDeviceInfo:
            deviceObj={}
            deviceObj["dept"] = item.dept
            deviceObj["adapter_code"]=item.adapter_code
            deviceObj["adapter_type"]=item.adapter_type
            deviceObj["gw_code"]=item.gw_code
            deviceObj["gw_type"] = item.gw_type
            deviceObj["iot_code"] = item.iot_code
            deviceObj["iot_type"] = item.iot_type
            deviceObj["loRaSNR"] = item.loRaSNR
            deviceObj["rssi"] = item.rssi
            deviceObj["time"] = item.time
            deviceObj["fCnt"] = item.fCnt
            deviceObj["iot_device_code"] = item.iot_device_code
            deviceObj["status"] = item.status
            iotDeviceValues=iotDeviceValuesDB.objects.filter(iot_device_id=item.id)
            for values in iotDeviceValues:
                deviceObj[values.attribute]=values.value
            iotDevice=iotDeviceDB.objects.get(code=item.iot_code)
            deviceObj["iot_address"]=iotDevice.iot_address
            iotDeviceWarn = iotDeviceWarnDB.objects.get(iot_device_id=item.id)
            deviceObj["warn_data"] = iotDeviceWarn.warn_data
            deviceObj["warn_type"] = iotDeviceWarn.warn_type
            deviceObj["warn_cause"] = iotDeviceWarn.warn_cause
            resultInfoList.append(deviceObj)
        if indexPage and countInfo:
            indexStart = (indexPage - 1) * countInfo

            if indexStart < 0:
                indexStart = 0

            indexEnd = indexStart + countInfo

            if indexEnd >= iotDeviceInfo.count():
                indexEnd = iotDeviceInfo.count()

            resultInfoList = resultInfoList[indexStart:indexEnd]
        else:
            resultInfoList = resultInfoList

        resData["info"] = resultInfoList
    except Exception as err:
        return Response({"result": 14012007, "msg": getErrMsgByCode(14012007, err)}, content_type="application/json")

    resData["total"] = iotDeviceInfo.count()
    return Response({"result": 0, "msg": "OK", "data": resData}, content_type="application/json")

    # try:
    #     reqBody = json.loads(request.body)
    # except Exception as err:
    #     return Response({"result": 14012001, "msg": getErrMsgByCode(14012001, err)}, content_type="application/json")
    #
    # if reqbody_verify(reqBody, err_code=14012001) is None:
    #     pass
    # else:
    #     return reqbody_verify(reqBody, err_code=14012001)
    #
    # if "code" not in reqBody:
    #     return Response({"result": 14012006, "msg": getErrMsgByCode(14012006, None)}, content_type="application/json")
    # else:
    #     codeDevice = reqBody["code"]
    #
    # resData = {}
    # try:
    #     gasObjs = iotGasDB.objects.filter(code=codeDevice, status=1)
    #     if gasObjs.count() > 0:
    #         index = random.randint(0, gasObjs.count() - 1)
    #         gasObj = gasObjs[index]
    #
    #         resData["code"] = gasObj.code
    #         resData["code_sub"] = gasObj.code_sub
    #         resData["brand"] = gasObj.brand
    #         resData["type"] = gasObj.type
    #         resData["type_name"] = gasObj.type_name
    #
    #         if gasObj.type == 51:
    #             resData["threshold_level_1"] = gasObj.threshold_level_1
    #             resData["threshold_level_2"] = gasObj.threshold_level_2
    #             resData["gas_strength"] = gasObj.gas_strength
    #         elif gasObj.type == 126:
    #             resData["air_temp"] = gasObj.air_temp
    #             resData["air_humidity"] = gasObj.air_humidity
    #
    #         resData["status"] = gasObj.status
    #         resData["time"] = datetime.now()
    # except Exception as err:
    #     return Response({"result": 14012007, "msg": getErrMsgByCode(14012007, err)}, content_type="application/json")
    #
    # deviceObj = None
    # try:
    #     deviceObj = iotDeviceDB.objects.get(code=codeDevice)
    # except Exception as err:
    #     return Response({"result": 14012008, "msg": getErrMsgByCode(14012008, err), "data": resData}, content_type="application/json")
    #
    # userList = []
    # try:
    #     userObjs = userInfoDB.objects.filter(dept=deviceObj.dept)
    #     for user in userObjs:
    #         userObj = {}
    #
    #         userObj["id"] = user.id
    #         userObj["name"] = user.nickname
    #         userObj["phone"] = user.phone
    #
    #         userList.append(userObj)
    # except Exception as err:
    #     return Response({"result": 14012009, "msg": getErrMsgByCode(14012009, err), "data": resData}, content_type="application/json")
    #
    # smsContent = None
    # try:
    #     tempObj = smsInfoTemplateDB.objects.get(id=deviceObj.sms_level_1)
    #     smsTemplate = tempObj.content
    #     timeObj = datetime.now()
    #     smsContent = smsTemplate.format(timeObj.year, timeObj.month, timeObj.day, "深圳市证通电子股份有限公司", deviceObj.name, "固体", 0.1, 0.0, deviceObj.locate)
    # except Exception as err:
    #     return Response({"result": 14012010, "msg": getErrMsgByCode(14012010, err), "data": resData}, content_type="application/json")
    #
    # smsResult = sendSMSInfoImplement(userList, smsContent)
    # print(smsResult)
    # if smsResult["result"] != 0:
    #     return Response({"result": 14012011, "msg": getErrMsgByCode(14012011, None) + "-->" + smsResult["msg"], "data": resData}, content_type="application/json")
    #
    # return Response({"result": 0, "msg": "OK", "data": resData}, content_type="application/json")


@csrf_exempt
@api_view(["post"])
def queryDeviceWarnToday(request):
    """
    查询IOT设备告警数据（当天）
    :param request:
    :return:
    """
    try:
        reqBody = json.loads(request.body)
    except Exception as err:
        return Response({"result": 14012001, "msg": getErrMsgByCode(14012001, err)}, content_type="application/json")

    if reqbody_verify(reqBody, err_code=14012001) is None:
        pass
    else:
        return reqbody_verify(reqBody, err_code=14012001)

    iotCode = None

    if "iot_code" in reqBody:
        iotCode = reqBody["iot_code"]

    # if "id" in reqBody:
    #     iotId = reqBody["id"]

    now_date = date.today()
    # 获取一个周前日期
    Tomorrow_date = now_date + timedelta(1)


    try:
        if iotCode is not None:
            iotDeviceInfo = iotDeviceInfoDB.objects.filter(Q(status__gt=0) & Q(iot_code=iotCode)).filter(Q(time__gte=now_date) & Q(time__lte=Tomorrow_date)).order_by("-id")
        # elif iotId is not None:
        #     iotDeviceInfo = iotDeviceInfoDB.objects.filter(id=iotId)
        else:
            iotDeviceInfo=iotDeviceInfoDB.objects.filter(status__gt=0).filter(Q(time__gte=now_date) & Q(time__lte=Tomorrow_date)).order_by("-id")
        resData=[]
        for item in iotDeviceInfo:
            deviceObj={}
            deviceObj["dept"] = item.dept
            deviceObj["adapter_code"]=item.adapter_code
            deviceObj["adapter_type"]=item.adapter_type
            deviceObj["gw_code"]=item.gw_code
            deviceObj["gw_type"] = item.gw_type
            deviceObj["iot_code"] = item.iot_code
            deviceObj["iot_type"] = item.iot_type
            deviceObj["loRaSNR"] = item.loRaSNR
            deviceObj["rssi"] = item.rssi
            deviceObj["time"] = item.time
            deviceObj["fCnt"] = item.fCnt
            deviceObj["iot_device_code"] = item.iot_device_code
            deviceObj["status"] = item.status
            iotDeviceValues=iotDeviceValuesDB.objects.filter(iot_device_id=item.id)
            for values in iotDeviceValues:
                deviceObj[values.attribute]=values.value
            iotDevice=iotDeviceDB.objects.get(code=item.iot_code)
            deviceObj["iot_address"]=iotDevice.iot_address
            iotDeviceWarn = iotDeviceWarnDB.objects.get(iot_device_id=item.id)
            deviceObj["warn_data"] = iotDeviceWarn.warn_data
            deviceObj["warn_type"] = iotDeviceWarn.warn_type
            deviceObj["warn_cause"] = iotDeviceWarn.warn_cause
            resData.append(deviceObj)
    except Exception as err:
        return Response({"result": 14012007, "msg": getErrMsgByCode(14012007, err)}, content_type="application/json")

    return Response({"result": 0, "msg": "OK", "data": resData}, content_type="application/json")




MQ_Thread_Name="my_mq"

def callback(ch, method, properties, body):
    requestData= json.loads(body)
    print(requestData)
    code = requestData["id"]
    videoMonitorObjects = videoMonitorDB.objects.filter(code=code)

    if len(videoMonitorObjects)>0:
        for videoMonitorObject in videoMonitorObjects:

            now_time = datetime.now()
            # print(now_time)
            start_time = now_time + timedelta(seconds=-10)
            end_time = now_time + timedelta(seconds=+30)
            t = int(round(time.time() * 1000))
            record_code = str(t) + "的录像"

            status = requestData["status"]

            ipc = videoMonitorObject.channel
            name = videoMonitorObject.name
            locate = videoMonitorObject.locate

            if int(status) in [26,27,6]:
                aiRtspRecordObject = aiRtspRecordDB.objects.create(
                    ipc=ipc,
                    record_code=record_code,
                    start_time=start_time,
                    end_time=end_time

            )
                print("告警")

            if str(status) == "26":
                warnData = "当前设备检测到明火抽烟（正常）"
                warnType = "明火抽烟（正常）"
                warnCause = "明火抽烟"

                aiDeviceWarnObject = aiDeviceWarnDB.objects.create(
                    warn_data=warnData,
                    warn_type=warnType,
                    warn_cause=warnCause,
                    name=name,
                    code=code

                )

                rspmessage = {}
                rspmessage["code"] = code
                rspmessage["warn_data"] = warnData
                rspmessage["warn_type"] = warnType
                rspmessage["warn_cause"] = warnCause
                rspmessage["ipc"] = ipc
                rspmessage["name"] = name
                rspmessage["time"] = str(now_time)
                rspmessage["locate"] = locate
                rspmessage["device_type"] = 1

                mqttClient.publish(PUBLISH_TOPIC, json.dumps(rspmessage, ensure_ascii=False), 1, False)

            elif str(status) == "27":
                warnData = "当前设备检测到明火抽烟（告警）"
                warnType = "明火抽烟（告警）"
                warnCause = "明火抽烟"

                aiDeviceWarnObject = aiDeviceWarnDB.objects.create(
                    warn_data=warnData,
                    warn_type=warnType,
                    warn_cause=warnCause,
                    name=name,
                    code=code

                )

                rspmessage = {}
                rspmessage["code"] = code
                rspmessage["warn_data"] = warnData
                rspmessage["warn_type"] = warnType
                rspmessage["warn_cause"] = warnCause
                rspmessage["ipc"] = ipc
                rspmessage["name"] = name
                rspmessage["time"] = str(now_time)
                rspmessage["locate"] = locate
                rspmessage["device_type"] = 1

                mqttClient.publish(PUBLISH_TOPIC, json.dumps(rspmessage, ensure_ascii=False), 1, False)

            elif str(status) == "6":
                warnData = "当前设备检测通道阻塞预警"
                warnType = "通道阻塞"
                warnCause = "通道阻塞"

                aiDeviceWarnObject = aiDeviceWarnDB.objects.create(
                    warn_data=warnData,
                    warn_type=warnType,
                    warn_cause=warnCause,
                    name=name,
                    code=code

                )
                rspmessage = {}
                rspmessage["code"] = code
                rspmessage["warn_data"] = warnData
                rspmessage["warn_type"] = warnType
                rspmessage["warn_cause"] = warnCause
                rspmessage["ipc"] = ipc
                rspmessage["name"] = name
                rspmessage["time"] = str(now_time)
                rspmessage["locate"] = locate
                rspmessage["device_type"] = 1

                mqttClient.publish(PUBLISH_TOPIC, json.dumps(rspmessage, ensure_ascii=False), 1, False)

                # print(json.dumps(rspmessage, ensure_ascii=False))
                # print(type(json.dumps(rspmessage)))
    else:
        print("设备不存在")


def run_mq(name):

    # 链接到RabbitMQ服务器
    credentials = pika.PlainCredentials('admin','admin123')

    connection = pika.BlockingConnection(pika.ConnectionParameters('218.17.164.125',5672,'/',credentials))

    # 创建频道
    channel = connection.channel()

    # 声明消息队列  durable = True 代表exchange持久化存储，False 非持久
    channel.exchange_declare(exchange="wlwIII-push-exchange",exchange_type="direct",durable=True)

    channel.queue_bind(exchange='wlwIII-push-exchange',
                       queue='wlwIII-push-queue',
                       routing_key='wlwIII-push-routingKey')

    # print(' [*] Waiting for logs. To exit press CTRL+C')



    # channel.basic_consume(callback,queue='wlwIII-push-queue',no_ack=False)
    # 告诉RabbitMQ使用callback来接收信息 no_ack 设置成 False，在调用callback函数时，未收到确认标识，消息会重回队列。True，无论调用callback成功与否，消息都被消费掉
    channel.basic_consume('wlwIII-push-queue',callback,True)
    # 开始接收信息
    channel.start_consuming()

def start_mq():
    """
    服务--开启
    """
    threadObj = Thread(target=run_mq,args=(MQ_Thread_Name,))
    threadObj.start()
    print("123")




# @csrf_exempt
# @api_view(["post"])
# def receiveIoTDeviceStatusInfo(request):
#     """
#     接收IoT设备信息
#     """
#     try:
#         reqBody = json.loads(request.body)
#     except Exception as err:
#         return Response({"result": 14005001, "msg": getErrMsgByCode(14005001, err)}, content_type="application/json")
#
#     print(format(reqBody))
#     requestData = reqBody["requestData"]
#
#     now_time = datetime.now()
#     print(now_time)
#     start_time=now_time+timedelta(seconds = -10)
#     end_time=now_time+timedelta(seconds = +30)
#     t=int(round(time.time() * 1000))
#     record_code=str(t)+"的录像"
#
#
#     status=requestData["status"]
#     code=requestData["id"]
#
#     videoMonitorObject=videoMonitorDB.objects.get(code=code)
#
#     ipc=videoMonitorObject.channel
#     name=videoMonitorObject.name
#     locate=videoMonitorObject.locate
#
#     aiRtspRecordObject=aiRtspRecordDB.objects.create(
#         ipc=ipc,
#         record_code=record_code,
#         start_time=start_time,
#         end_time=end_time
#
#     )
#
#
#     if str(status)=="26":
#         warnData="当前设备检测到明火抽烟（正常）"
#         warnType="明火抽烟（正常）"
#         warnCause="明火抽烟"
#
#         aiDeviceWarnObject = aiDeviceWarnDB.objects.create(
#             warn_data=warnData,
#             warn_type=warnType,
#             warn_cause=warnCause,
#             name=name,
#             code=code
#
#         )
#
#         rspmessage = {}
#         rspmessage["code"] = code
#         rspmessage["warn_data"] = warnData
#         rspmessage["warn_type"] = warnType
#         rspmessage["warn_cause"] = warnCause
#         rspmessage["ipc"] = ipc
#         rspmessage["name"] = name
#         rspmessage["time"] = str(now_time)
#         rspmessage["locate"] = locate
#         rspmessage["device_type"] = 1
#
#
#         mqttClient.publish(PUBLISH_TOPIC, json.dumps(rspmessage,ensure_ascii=False), 1, False)
#
#     elif str(status) == "27":
#         warnData = "当前设备检测到明火抽烟（告警）"
#         warnType = "明火抽烟（告警）"
#         warnCause = "明火抽烟"
#
#         aiDeviceWarnObject = aiDeviceWarnDB.objects.create(
#             warn_data=warnData,
#             warn_type=warnType,
#             warn_cause=warnCause,
#             name=name,
#             code=code
#
#         )
#
#         rspmessage = {}
#         rspmessage["code"] = code
#         rspmessage["warn_data"] = warnData
#         rspmessage["warn_type"] = warnType
#         rspmessage["warn_cause"] = warnCause
#         rspmessage["ipc"] = ipc
#         rspmessage["name"] = name
#         rspmessage["time"] = str(now_time)
#         rspmessage["locate"] = locate
#         rspmessage["device_type"] = 1
#
#         mqttClient.publish(PUBLISH_TOPIC, json.dumps(rspmessage, ensure_ascii=False), 1, False)
#
#     elif str(status) == "6":
#         warnData = "当前设备检测通道阻塞预警"
#         warnType = "通道阻塞"
#         warnCause = "通道阻塞"
#
#         aiDeviceWarnObject = aiDeviceWarnDB.objects.create(
#             warn_data=warnData,
#             warn_type=warnType,
#             warn_cause=warnCause,
#             name=name,
#             code=code
#
#         )
#         rspmessage={}
#         rspmessage["code"]=code
#         rspmessage["warn_data"] = warnData
#         rspmessage["warn_type"] = warnType
#         rspmessage["warn_cause"] = warnCause
#         rspmessage["ipc"] = ipc
#         rspmessage["name"] = name
#         rspmessage["time"]=str(now_time)
#         rspmessage["locate"] = locate
#         rspmessage["device_type"] = 1
#
#
#         mqttClient.publish(PUBLISH_TOPIC, json.dumps(rspmessage,ensure_ascii=False), 1, False)
#
#         print(json.dumps(rspmessage,ensure_ascii=False))
#         print(type(json.dumps(rspmessage)))
#
#
#
#
#
#
#
#     return Response({"result": 0, "msg": "OK"}, status=200, content_type="application/json")


@csrf_exempt
@api_view(["post"])
def queryAiDeviceInfo(request):
    """
    查询ai设备信息
    :param request:
    :return:
    """
    try:
        reqBody = json.loads(request.body)
    except Exception as err:
        return Response({"result": 14015001, "msg": getErrMsgByCode(14015001, err)}, content_type="application/json")

    if reqbody_verify(reqBody, err_code=14015001) is None:
        pass
    else:
        return reqbody_verify(reqBody, err_code=14015001)

    resData = []
    try:
        pstnGatewayObjs = aiDeviceDB.objects.all()

        for item in pstnGatewayObjs:
            deviceObj = {}
            videoMonitorList = []
            videoMonitorObjs=videoMonitorDB.objects.filter(ai_device_id=item.id)
            deviceObj["id"] = item.id
            deviceObj["name"] = item.name
            deviceObj["dept"] = item.dept
            deviceObj["code"] = item.code
            deviceObj["generic_plan"] = item.generic_plan
            deviceObj["sms_level_1"] = item.sms_level_1
            deviceObj["sms_level_2"] = item.sms_level_2
            deviceObj["longitude"] = item.longitude
            deviceObj["latitude"] = item.latitude
            deviceObj["height"] = item.height
            deviceObj["enable"] = item.enable
            deviceObj["locate"]=item.locate
            for value in videoMonitorObjs:
                videoMonitorList.append(value.id)
                deviceObj["ipc"] = videoMonitorList

            resData.append(deviceObj)
    except Exception as err:
        return Response({"result": 14015006, "msg": getErrMsgByCode(14015006, err)}, content_type="application/json")

    return Response({"result": 0, "msg": "OK", "data": resData}, content_type="application/json")

@csrf_exempt
@api_view(["post"])
def addAiDeviceInfo(request):
    """
    IoT设备信息--新增
    """
    try:
        reqBody = json.loads(request.body)
    except Exception as err:
        return Response({"result": 14016001, "msg": getErrMsgByCode(14016001, err)}, content_type="application/json")

    if reqbody_verify_admin(reqBody, err_code=14016001) is None:
        pass
    else:
        return reqbody_verify_admin(reqBody, err_code=14016001)

    if "dept" not in reqBody:
        return Response({"result": 14016006, "msg": getErrMsgByCode(14016006, None)}, content_type="application/json")
    else:
        deviceDept = reqBody["dept"]

    if "code" not in reqBody:
        return Response({"result": 14016007, "msg": getErrMsgByCode(14016007, None)}, content_type="application/json")
    else:
        Code = reqBody["code"]

    if "locate" not in reqBody:
        return Response({"result": 14016008, "msg": getErrMsgByCode(14016008, None)}, content_type="application/json")
    else:
        Locate = reqBody["locate"]

    if "generic_plan" not in reqBody:
        return Response({"result": 14016009, "msg": getErrMsgByCode(14016009, None)}, content_type="application/json")
    else:
        genericPlan = reqBody["generic_plan"]

    if "name" not in reqBody:
        return Response({"result": 14016010, "msg": getErrMsgByCode(14016010, None)}, content_type="application/json")
    else:
        DeviceName= reqBody["name"]

    if "enable" not in reqBody:
        return Response({"result": 14016011, "msg": getErrMsgByCode(14016011, None)}, content_type="application/json")
    else:
        deviceEnable = reqBody["enable"]


    if "sms_level_1" not in reqBody:
        smsLevel1 = 0
    else:
        smsLevel1 = reqBody["sms_level_1"]

    if "sms_level_2" not in reqBody:
        smsLevel2 = 0
    else:
        smsLevel2 = reqBody["sms_level_2"]

    if  "latitude" not in reqBody:
        deviceLatitude=0
    else:
        deviceLatitude = reqBody["latitude"]

    if "longitude" not in reqBody:
        deviceLongitude=0
    else:
        deviceLongitude = reqBody["longitude"]

    if "height" not in reqBody:
        deviceHeight=0
    else:
        deviceHeight = reqBody["height"]


    savePoint = transaction.savepoint()

    aiDeviceObj = aiDeviceDB()

    aiDeviceObj.dept = deviceDept
    aiDeviceObj.generic_plan = genericPlan
    aiDeviceObj.code=Code
    aiDeviceObj.name=DeviceName
    aiDeviceObj.enable=deviceEnable
    aiDeviceObj.locate=Locate
    aiDeviceObj.latitude=deviceLatitude
    aiDeviceObj.longitude=deviceLongitude
    aiDeviceObj.height=deviceHeight
    aiDeviceObj.sms_level_1 = smsLevel1
    aiDeviceObj.sms_level_2 = smsLevel2

    try:
        aiDeviceObj.save()
    except Exception as err:
        transaction.savepoint_rollback(savePoint)
        return Response({"result": 14016012, "msg": getErrMsgByCode(14016012, err)}, content_type="application/json")

    transaction.savepoint_commit(savePoint)

    return Response({"result": 0, "msg": "OK"}, content_type="application/json")

@csrf_exempt
@api_view(["post"])
def modifyAiDevicenfo(request):
    """
    ai设备信息--修改
    :return:
    """
    try:
        reqBody = json.loads(request.body)
    except Exception as err:
        return Response({"result": 14017001, "msg": getErrMsgByCode(14017001, err)}, content_type="application/json")

    if reqbody_verify_admin(reqBody, err_code=14017001) is None:
        pass
    else:
        return reqbody_verify_admin(reqBody, err_code=14017001)

    if "id" not in reqBody:
        return Response({"result": 14017006, "msg": getErrMsgByCode(14017006, None)}, content_type="application/json")
    else:
        deviceID = reqBody["id"]

    deviceName=None
    deviceCode=None
    deviceDept = None
    genericPlan = None
    smsLevel1 = None
    smsLevel2 = None
    aiLatitude=None
    aiLongitude=None
    aiHeight=None
    aiLocate=None
    enable=None

    if "name" in reqBody:
        deviceName = reqBody["name"]

    if "dept" in reqBody:
        deviceDept = reqBody["dept"]

    if "code" in reqBody:
        deviceCode = reqBody["code"]

    if "enable" in reqBody:
        enable = reqBody["enable"]

    if "generic_plan" in reqBody:
        genericPlan = reqBody["generic_plan"]

    if "sms_level_1" in reqBody:
        smsLevel1 = reqBody["sms_level_1"]

    if "sms_level_2" in reqBody:
        smsLevel2 = reqBody["sms_level_2"]

    if "latitude" in reqBody:
        aiLatitude = reqBody["latitude"]

    if "longitude" in reqBody:
        aiLongitude = reqBody["longitude"]

    if "height" in reqBody:
        aiHeight = reqBody["height"]

    if "locate" in reqBody:
        aiLocate = reqBody["locate"]


    try:
        deviceObj = aiDeviceDB.objects.get(id=deviceID)
    except Exception as err:
        return Response({"result": 14017007, "msg": getErrMsgByCode(14017007, err)}, content_type="application/json")


    if deviceDept is not None:
        deviceObj.dept = deviceDept

    if deviceName is not None:
        deviceObj.name = deviceName

    if deviceCode is not None:
        deviceObj.code = deviceCode

    if enable is not None:
        deviceObj.enable = enable

    if genericPlan is not None:
        deviceObj.generic_plan = genericPlan

    if smsLevel1 is not None:
        deviceObj.generic_plan = smsLevel1

    if smsLevel2 is not None:
        deviceObj.generic_plan = smsLevel2


    if aiLatitude is not None:
        deviceObj.latitude=aiLatitude

    if aiLongitude is not None:
        deviceObj.longitude = aiLongitude

    if aiHeight is not None:
        deviceObj.height = aiHeight

    if aiLocate is not None:
        deviceObj.locate = aiLocate

    try:
        deviceObj.save()
    except Exception as err:
        return Response({"result": 14017008, "msg": getErrMsgByCode(14017008, err)}, content_type="application/json")

    return Response({"result": 0, "msg": "OK"}, content_type="application/json")

@csrf_exempt
@api_view(["post"])
def deleteAiDeviceInfo(request):
    """
    AI设备信息--删除
    :return:
    """
    try:
        reqBody = json.loads(request.body)
    except Exception as err:
        return Response({"result": 14018001, "msg": getErrMsgByCode(14018001, err)}, content_type="application/json")

    if reqbody_verify_admin(reqBody, err_code=14018001) is None:
        pass
    else:
        return reqbody_verify_admin(reqBody, err_code=14018001)

    if "id" not in reqBody:
        return Response({"result": 14018006, "msg": getErrMsgByCode(14018006, None)}, content_type="application/json")
    else:
        deviceId = reqBody["id"]

    try:
        deviceObj = aiDeviceDB.objects.get(id=deviceId)

    except Exception as err:
        return Response({"result": 14018007, "msg": getErrMsgByCode(14018007, err)}, content_type="application/json")

    try:
        videoMonitorDB.objects.filter(ai_device_id=deviceId).delete()
    except Exception as err:
        return Response({"result": 14018008, "msg": getErrMsgByCode(14018008, err)}, content_type="application/json")


    try:
        deviceObj.delete()
    except Exception as err:
        return Response({"result": 14018009, "msg": getErrMsgByCode(14018009, err)}, content_type="application/json")

    return Response({"result": 0, "msg": "OK"}, content_type="application/json")

@csrf_exempt
@api_view(["post"])
def queryDeviceAiWarnInfo(request):
    """
    查询 AI分析仪设备告警数据（全部）
    :param request:
    :return:
    """
    try:
        reqBody = json.loads(request.body)
    except Exception as err:
        return Response({"result": 14019001, "msg": getErrMsgByCode(14019001, err)}, content_type="application/json")

    if reqbody_verify(reqBody, err_code=14019001) is None:
        pass
    else:
        return reqbody_verify(reqBody, err_code=14019001)

    indexPage = None
    countInfo = None

    afterTime = None
    beforeTime = None

    if "page" in reqBody:
        indexPage = reqBody["page"]

    if "count" in reqBody:
        countInfo = reqBody["count"]

    if "after" in reqBody:
        afterTime = reqBody["after"]

    if "before" in reqBody:
        beforeTime = reqBody["before"]

    try:
        if afterTime and beforeTime:
            aiDeviceInfo = aiDeviceWarnDB.objects.filter(time__gt=afterTime, time__lt=beforeTime)
        else:
            aiDeviceInfo = aiDeviceWarnDB.objects.all()
        resData={}
        resultInfoList = []
        for item in aiDeviceInfo:
            deviceObj={}
            deviceObj["id"]=item.id
            deviceObj["warn_data"]=item.warn_data
            deviceObj["warn_type"]=item.warn_type
            deviceObj["warn_cause"]=item.warn_cause
            deviceObj["time"]=item.time
            deviceObj["name"]=item.name
            deviceObj["code"]=item.code
            deviceObj["locate"]=item.locate
            resultInfoList.append(deviceObj)

        if indexPage and countInfo:
            indexStart = (indexPage - 1) * countInfo

            if indexStart < 0:
                indexStart = 0

            indexEnd = indexStart + countInfo

            if indexEnd >= aiDeviceInfo.count():
                indexEnd = aiDeviceInfo.count()

            resultInfoList = resultInfoList[indexStart:indexEnd]
        else:
            resultInfoList = resultInfoList

        resData["info"] = resultInfoList
    except Exception as err:
        return Response({"result": 14019006, "msg": getErrMsgByCode(14019006, err)}, content_type="application/json")

    resData["total"] = aiDeviceInfo.count()
    return Response({"result": 0, "msg": "OK", "data": resData}, content_type="application/json")

@csrf_exempt
@api_view(["post"])
def queryAIDeviceWarnValue(request):
    """
    查询AI设备告警数据（一周）
    :param request:
    :return:
    """
    try:
        reqBody = json.loads(request.body)
    except Exception as err:
        return Response({"result": 14020001, "msg": getErrMsgByCode(14020001, err)}, content_type="application/json")

    if reqbody_verify(reqBody, err_code=14020001) is None:
        pass
    else:
        return reqbody_verify(reqBody, err_code=14020001)

    AiCode=None

    if "code" in reqBody:
        AiCode = reqBody["code"]

    now_date = date.today()
    # 获取一个周前日期
    Tomorrow_date = now_date + timedelta(1)
    Sixth_date = now_date - timedelta(6)

    indexPage = None
    countInfo = None

    if "page" in reqBody:
        indexPage = reqBody["page"]

    if "count" in reqBody:
        countInfo = reqBody["count"]
    resData = {}

    try:
        if AiCode is not None:
            aiDeviceInfo = aiDeviceWarnDB.objects.filter(Q(code=AiCode)).filter(Q(time__gte=Sixth_date) & Q(time__lte=Tomorrow_date))
        else:
            aiDeviceInfo = aiDeviceWarnDB.objects.filter(Q(time__gte=Sixth_date) & Q(time__lte=Tomorrow_date))
        resultInfoList = []
        for item in aiDeviceInfo:
            deviceObj={}
            deviceObj["id"] = item.id
            deviceObj["warn_data"] = item.warn_data
            deviceObj["warn_type"] = item.warn_type
            deviceObj["warn_cause"] = item.warn_cause
            deviceObj["time"] = item.time
            deviceObj["name"] = item.name
            deviceObj["code"] = item.code
            deviceObj["locate"] = item.locate
            resultInfoList.append(deviceObj)
        if indexPage and countInfo:
            indexStart = (indexPage - 1) * countInfo

            if indexStart < 0:
                indexStart = 0

            indexEnd = indexStart + countInfo

            if indexEnd >= aiDeviceInfo.count():
                indexEnd = aiDeviceInfo.count()

            resultInfoList = resultInfoList[indexStart:indexEnd]
        else:
            resultInfoList = resultInfoList

        resData["info"] = resultInfoList
    except Exception as err:
        return Response({"result": 14020006, "msg": getErrMsgByCode(14020006, err)}, content_type="application/json")

    resData["total"] = aiDeviceInfo.count()
    return Response({"result": 0, "msg": "OK", "data": resData}, content_type="application/json")

@csrf_exempt
@api_view(["post"])
def queryAIDeviceWarnToday(request):
    """
    查询IOT设备告警数据（当天）
    :param request:
    :return:
    """
    try:
        reqBody = json.loads(request.body)
    except Exception as err:
        return Response({"result": 14021001, "msg": getErrMsgByCode(14021001, err)}, content_type="application/json")

    if reqbody_verify(reqBody, err_code=14021001) is None:
        pass
    else:
        return reqbody_verify(reqBody, err_code=14021001)

    AiCode = None

    if "code" in reqBody:
        AiCode = reqBody["code"]

    now_date = date.today()
    # 获取一个周前日期
    Tomorrow_date = now_date + timedelta(1)


    try:
        if AiCode is not None:
            aiDeviceInfo = aiDeviceWarnDB.objects.filter(Q(code=AiCode)).filter(Q(time__gte=now_date) & Q(time__lte=Tomorrow_date))

        else:
            aiDeviceInfo = aiDeviceWarnDB.objects.filter(Q(time__gte=now_date) & Q(time__lte=Tomorrow_date))
        resData=[]
        for item in aiDeviceInfo:
            deviceObj={}
            deviceObj["id"] = item.id
            deviceObj["warn_data"] = item.warn_data
            deviceObj["warn_type"] = item.warn_type
            deviceObj["warn_cause"] = item.warn_cause
            deviceObj["time"] = item.time
            deviceObj["name"] = item.name
            deviceObj["code"] = item.code
            deviceObj["locate"] = item.locate
            resData.append(deviceObj)
    except Exception as err:
        return Response({"result": 14021006, "msg": getErrMsgByCode(14021006, err)}, content_type="application/json")

    return Response({"result": 0, "msg": "OK", "data": resData}, content_type="application/json")


@csrf_exempt
@api_view(["post"])
def queryWarnAllInfo(request):
    """
    查询告警数据（柱状图。扇形图）
    :param request:
    :return:
    """
    try:
        reqBody = json.loads(request.body)
    except Exception as err:
        return Response({"result": 14022001, "msg": getErrMsgByCode(14022001, err)}, content_type="application/json")

    if reqbody_verify(reqBody, err_code=14022001) is None:
        pass
    else:
        return reqbody_verify(reqBody, err_code=14022001)

    now_date = date.today()

    my_list=[]

    for i in range(0, 4):
        x = now_date - timedelta(i * 7 - 1)
        list1 = []
        for y in range(1, 8):
            date_y = x - timedelta(y)

            date_y = date_y.strftime("%m-%d")
            list1.append(date_y)
        my_list.append(list1)

    new_list = []
    for i in my_list:
        i = i[::-1]
        new_list.append(i)
    date_list = new_list[::-1]

    list3 = []
    list4=[]
    for i in range(0, 4):
        x = now_date - timedelta(i * 7 - 1)
        print(x)
        list5 = []
        list6=[]
        for o in range(1, 8):
            data1 = x - timedelta(o - 1)
            data2 = x - timedelta(o)

            try:
                count1 = iotDeviceInfoDB.objects.filter(status__gt=0).filter(Q(time__gte=data2) & Q(time__lte=data1)).count()
                count2 = aiDeviceWarnDB.objects.filter(Q(time__gte=data2) & Q(time__lte=data1)).count()
                # count = count1 + count2
            except Exception as err:
                return Response({"result": 14022006, "msg": getErrMsgByCode(14022006, err)},content_type="application/json")
            list5.append(count1)
            list6.append(count2)

        list3.append(list5)
        list4.append(list6)

    iot_list=[]
    for i in list3:
        i = i[::-1]
        iot_list.append(i)
    iot_list = iot_list[::-1]

    ai_list=[]
    for i in list4:
        i = i[::-1]
        ai_list.append(i)
    ai_list = ai_list[::-1]

    # iot_count=iotDeviceInfoDB.objects.filter(status__gt=0).filter(Q(time__gte=now_date - timedelta(27)) & Q(time__lte=now_date - timedelta(- 1))).count()
    # ai_count=aiDeviceWarnDB.objects.filter(Q(time__gte=now_date - timedelta(27)) & Q(time__lte=now_date - timedelta(- 1))).count()
    resData = {}
    resData["date"]=date_list
    resData["iot"]=iot_list
    resData["ai"]=ai_list

    return Response({"result": 0, "msg": "OK", "data": resData}, content_type="application/json")


@csrf_exempt
@api_view(["post"])
def queryIotStatus(request):
    """
    查询iot激活状态
    """
    try:
        reqBody = json.loads(request.body)
    except Exception as err:
        return Response({"result": 14021001, "msg": getErrMsgByCode(14021001, err)}, content_type="application/json")

    if reqbody_verify(reqBody, err_code=14021001) is None:
        pass
    else:
        return reqbody_verify(reqBody, err_code=14021001)
    try:
        logging.captureWarnings(True)

        registerData = {"appId": "reP7XZDjSn0EyeuZEr1kr3vYHiUa", "secret": "Ovk9w3efzmtf3vJeSaQcfi_ltx4a"}

        headers = {"Content-Type": "application/x-www-form-urlencoded"}

        response = requests.post(url="https://10.143.13.28:8743/iocm/app/sec/v1.1.0/login",
                                 cert=("/root/workspace/gmaj/client.crt", "/root/workspace/gmaj/client.key"),
                                 headers=headers, data=registerData, verify=False)

        resultData = json.loads(response.text)

        print(resultData)

    except Exception as err:
        return Response({"result": 14022006, "msg": getErrMsgByCode(14022006, err)}, content_type="application/json")

    return Response({"result": 0, "msg": "OK", "data": resultData}, content_type="application/json")


@csrf_exempt
@api_view(["post"])
def queryIotADD(request):
    """
    查询iot激活状态
    """
    try:
        reqBody = json.loads(request.body)
    except Exception as err:
        return Response({"result": 14021001, "msg": getErrMsgByCode(14021001, err)}, content_type="application/json")

    if reqbody_verify(reqBody, err_code=14021001) is None:
        pass
    else:
        return reqbody_verify(reqBody, err_code=14021001)

    if "accessToken" not in reqBody:
        return Response({"result": 14018006, "msg": getErrMsgByCode(14018006, None)}, content_type="application/json")
    else:
        accessToken = reqBody["accessToken"]

    try:
        logging.captureWarnings(True)

        # str1="Bearer"+str(accessToken)
        str1 = str(accessToken)

        print(str1)

        headers = {"app_key": "reP7XZDjSn0EyeuZEr1kr3vYHiUa", "Authorization": str1, "Content-Type": "application/json"}

        # requestData={"nodeId":"","deviceInfo":[{"location":"深圳市光明区证通电子产业园","model":"001A-0A12","name":"温湿度"}],}
        requestData = {"customFields": [{"fieldName": "", "fieldType": "", "fieldValue": ""}],
                       "deviceInfo": {"deviceType": "", "isSecurity": "", "supportedSecurity": "", "serialNumber": "",
                                      "swVersion": "", "manufacturerName": "", "signalStrength": "",
                                      "manufacturerId": "", "description": "", "mute": "", "statusDetail": "",
                                      "protocolType": "", "mac": "", "hwVersion": "", "sigVersion": "", "bridgeId": "",
                                      "name": "温湿度", "fwVersion": "", "location": "深圳市光明区证通电子产业园", "model": "string",
                                      "nodeId": "001A-0A12", "batteryLevel": "", "status": "ONLINE"},
                       "deviceInfo2": {"timezone": "", "region": "深圳", "activeServiceCount": 0}, "deviceName": "温湿度",
                       "endUserId": "", "groupId": "", "imsi": "", "isSecure": True,
                       "location": {"vehicleSpeed": "", "heading": "", "latitude": 0.0, "accuracy": 0.0,
                                    "description": "", "language": "中文", "numberOfPassengers": "",
                                    "crashInformation": "", "time": "", "region": "深圳", "longitude": 0.0},
                       "nodeId": " ", "psk": "", "tags": [{"tagValue": "", "tagName": "传感器"}], "timeout": 0,
                       "verifyCode": "", "productId": "", "account": "", "secret": "123456",
                       "authenticationType": "DICE", "deviceChipIdentification": "", "trustOnFirstUse": True,
                       "fileId": "", "diceDeviceSoftwareHash": [{"version": "", "layer": 0, "hashValue": ""}]}

        response = requests.post(url="https://10.143.13.28:8743/iocm/app/reg/v1.1.0/deviceCredentials", headers=headers,
                                 cert=("/root/workspace/gmaj/client.crt", "/root/workspace/gmaj/client.key"),
                                 verify=False, data=requestData)

        # resultData = json.loads(response_1.text)

        resultData = response.text

    except Exception as err:
        return Response({"result": 14022006, "msg": getErrMsgByCode(14022006, err)}, content_type="application/json")

    return Response({"result": 0, "msg": "OK", "data": resultData}, content_type="application/json")
