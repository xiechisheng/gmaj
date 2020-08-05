import json
import time
from django.db import transaction
from api.dept import getSubDeptList
from api.public import reqbody_verify
from api.ErrorCode import getErrMsgByCode
from api.public import reqbody_verify_admin
from rest_framework.response import Response
from rest_framework.decorators import api_view
from api.models import rtsp_info as RTSPDeviceDB
from api.models import rtsp_rolling as RTSPRollingDB
from api.models import rtsp_record as RTSPRecordDB
from django.views.decorators.csrf import csrf_exempt
from api.models import video_monitor as videoMonitorDB
from api.models import ai_rtsp_record as AiRtspRecordDB


@csrf_exempt
@api_view(["post"])
def rtspDeviceInfoAdd(request):
    """
    Rtsp设备信息--新增
    :return:
    """
    try:
        reqBody = json.loads(request.body)
    except Exception as err:
        return Response({"result": 17001001, "msg": getErrMsgByCode(17001001, err)}, content_type="application/json")

    if reqbody_verify_admin(reqBody, err_code=17001001) is None:
        pass
    else:
        return reqbody_verify_admin(reqBody, err_code=17001001)

    if "name" not in reqBody:
        return Response({"result": 17001002, "msg": getErrMsgByCode(17001002, None)}, content_type="application/json")
    else:
        deviceName = reqBody["name"]

    if "dept" not in reqBody:
        return Response({"result": 17001003, "msg": getErrMsgByCode(17001003, None)}, content_type="application/json")
    else:
        deviceDept = reqBody["dept"]

    if "type" not in reqBody:
        return Response({"result": 17001004, "msg": getErrMsgByCode(17001004, None)}, content_type="application/json")
    else:
        deviceType = reqBody["type"]

    if "server" not in reqBody:
        return Response({"result": 17001005, "msg": getErrMsgByCode(17001005, None)}, content_type="application/json")
    else:
        deviceServer = reqBody["server"]

    if "channel" not in reqBody:
        return Response({"result": 17001006, "msg": getErrMsgByCode(17001006, None)}, content_type="application/json")
    else:
        deviceChannel = reqBody["channel"]

    if "enable" not in reqBody:
        return Response({"result": 17001007, "msg": getErrMsgByCode(17001007, None)}, content_type="application/json")
    else:
        deviceEnable = reqBody["enable"]

    # if "longitude" not in reqBody:
    #     return Response({"result": 17001008, "msg": getErrMsgByCode(17001008, None)}, content_type="application/json")
    # else:
    #     deviceLon = reqBody["longitude"]

    # if "latitude" not in reqBody:
    #     return Response({"result": 17001009, "msg": getErrMsgByCode(17001009, None)}, content_type="application/json")
    # else:
    #     deviceLat = reqBody["latitude"]
    #
    # if "height" not in reqBody:
    #     return Response({"result": 17001010, "msg": getErrMsgByCode(17001010, None)}, content_type="application/json")
    # else:
    #     deviceHeight = reqBody["height"]

    if "locate" not in reqBody:
        return Response({"result": 17001011, "msg": getErrMsgByCode(17001011, None)}, content_type="application/json")
    else:
        deviceLocate = reqBody["locate"]

    if "manufacturer_type" not in reqBody:
        return Response({"result": 17001012, "msg": getErrMsgByCode(17001012, None)}, content_type="application/json")
    else:
        manufacturerType = reqBody["manufacturer_type"]

    if "permissions_info" not in reqBody:
        return Response({"result": 17001013, "msg": getErrMsgByCode(17001013, None)}, content_type="application/json")
    else:
        permissionsInfo = reqBody["permissions_info"]

    if "channel_type" not in reqBody:
        return Response({"result": 17001014, "msg": getErrMsgByCode(17001014, None)}, content_type="application/json")
    else:
        channelType = reqBody["channel_type"]

    if "inter_code_SN" not in reqBody:
        return Response({"result": 17001015, "msg": getErrMsgByCode(17001015, None)}, content_type="application/json")
    else:
        interCodeSN = reqBody["inter_code_SN"]

    # if "multicast_ip" not in reqBody:
    #     return Response({"result": 17001016, "msg": getErrMsgByCode(17001016, None)}, content_type="application/json")
    # else:
    #     multicastIp = reqBody["multicast_ip"]


    # if "multicast_port" not in reqBody:
    #     return Response({"result": 17001017, "msg": getErrMsgByCode(17001017, None)}, content_type="application/json")
    # else:
    #     multicastPort = reqBody["multicast_port"]
    deviceLon=None
    deviceLat=None
    deviceHeight=None
    multicastIp=None
    multicastPort=None

    if "longitude"  in reqBody:
        deviceLon = reqBody["longitude"]

    if "latitude"  in reqBody:
        deviceLat = reqBody["latitude"]

    if "height"  in reqBody:
        deviceHeight = reqBody["height"]

    if "multicast_ip"  in reqBody:
        multicastIp = reqBody["multicast_ip"]

    if "multicast_port"  in reqBody:
        multicastPort = reqBody["multicast_port"]

    deviceObj = RTSPDeviceDB()

    deviceObj.name = deviceName
    deviceObj.dept = deviceDept
    deviceObj.type = deviceType
    deviceObj.server = deviceServer
    deviceObj.channel = deviceChannel
    deviceObj.enable = deviceEnable
    deviceObj.longitude = deviceLon
    deviceObj.latitude = deviceLat
    deviceObj.height = deviceHeight
    deviceObj.locate = deviceLocate
    deviceObj.manufacturer_type=manufacturerType
    deviceObj.permissions_info=permissionsInfo
    deviceObj.channel_type=channelType
    deviceObj.inter_code_SN=interCodeSN
    deviceObj.multicast_ip=multicastIp
    deviceObj.multicast_port=multicastPort

    try:
        deviceObj.save()

    except Exception as err:
        Response({"result": 17001018, "msg": getErrMsgByCode(17001018, err)}, content_type="application/json")

    return Response({"result": 0, "msg": "OK"}, content_type="application/json")


@csrf_exempt
@api_view(["post"])
def rtspDeviceInfoModify(request):
    """
    Rtsp设备信息--修改
    :return:
    """
    try:
        reqBody = json.loads(request.body)
    except Exception as err:
        return Response({"result": 17002001, "msg": getErrMsgByCode(17002001, err)}, content_type="application/json")

    if reqbody_verify_admin(reqBody, err_code=17002001) is None:
        pass
    else:
        return reqbody_verify_admin(reqBody, err_code=17002001)

    if "id" not in reqBody:
        return Response({"result": 17002006, "msg": getErrMsgByCode(17002006, None)}, content_type="application/json")
    else:
        deviceID = reqBody["id"]

    deviceName = None
    deviceDept = None
    deviceType = None
    deviceServer = None
    deviceChannel = None
    deviceLon = None
    deviceLat = None
    deviceHeight = None
    deviceLocate = None
    deviceEnable = None
    deviceManufacturerType=None
    devicePermissionsInfo=None
    deviceChannelType=None
    deviceInterCodeSN=None
    deviceMulticastIp=None
    deviceMulticastPort=None


    if "name" in reqBody:
        deviceName = reqBody["name"]

    if "dept" in reqBody:
        deviceDept = reqBody["dept"]

    if "type" in reqBody:
        deviceType = reqBody["type"]

    if "server" in reqBody:
        deviceServer = reqBody["server"]

    if "channel" in reqBody:
        deviceChannel = reqBody["channel"]

    if "longitude" in reqBody:
        deviceLon = reqBody["longitude"]

    if "latitude" in reqBody:
        deviceLat = reqBody["latitude"]

    if "height" in reqBody:
        deviceHeight = reqBody["height"]

    if "locate" in reqBody:
        deviceLocate = reqBody["locate"]

    if "enable" in reqBody:
        deviceEnable = reqBody["enable"]

    if "manufacturer_type" in reqBody:
        deviceManufacturerType = reqBody["manufacturer_type"]

    if "permissions_info" in reqBody:
        devicePermissionsInfo = reqBody["permissions_info"]

    if "channel_type" in reqBody:
        deviceChannelType = reqBody["channel_type"]

    if "inter_code_SN" in reqBody:
        deviceInterCodeSN = reqBody["inter_code_SN"]

    if "multicast_ip" in reqBody:
        deviceMulticastIp = reqBody["multicast_ip"]

    if "multicast_port" in reqBody:
        deviceMulticastPort = reqBody["multicast_port"]

    try:
        deviceObj = RTSPDeviceDB.objects.get(id=deviceID)
    except Exception as err:
        return Response({"result": 17002007, "msg": getErrMsgByCode(17002007, err)}, content_type="application/json")

    if deviceName is not None:
        deviceObj.name = deviceName

    if deviceDept is not None:
        deviceObj.dept = deviceDept

    if deviceType is not None:
        deviceObj.type = deviceType

    if deviceServer is not None:
        deviceObj.server = deviceServer

    if deviceChannel is not None:
        deviceObj.channel = deviceChannel

    if deviceLon is not None:
        deviceObj.longitude = deviceLon

    if deviceLat is not None:
        deviceObj.latitude = deviceLat

    if deviceHeight is not None:
        deviceObj.height = deviceHeight

    if deviceLocate is not None:
        deviceObj.locate = deviceLocate

    if deviceEnable is not None:
        deviceObj.enable = deviceEnable

    if deviceManufacturerType is not None:
        deviceObj.manufacturer_type = deviceManufacturerType

    if devicePermissionsInfo is not None:
        deviceObj.permissions_info = devicePermissionsInfo

    if deviceChannelType is not None:
        deviceObj.channel_type = deviceChannelType

    if deviceInterCodeSN is not None:
        deviceObj.inter_code_SN = deviceInterCodeSN

    if deviceMulticastIp is not None:
        deviceObj.multicast_ip = deviceMulticastIp

    if deviceMulticastPort is not None:
        deviceObj.multicast_port = deviceMulticastPort


    try:
        deviceObj.save()
    except Exception as err:
        return Response({"result": 17002008, "msg": getErrMsgByCode(17002008, err)}, content_type="application/json")

    return Response({"result": 0, "msg": "OK"}, content_type="application/json")


@csrf_exempt
@api_view(["post"])
def rtspDeviceInfoQueryDept(request):
    """
    Rtsp设备信息--按部门查询
    :return:
    """
    print(format(request.body))
    try:
        reqBody = json.loads(request.body)
    except Exception as err:
        return Response({"result": 17003001, "msg": getErrMsgByCode(17003001, err)}, content_type="application/json")

    if reqbody_verify(reqBody, err_code=17003001) is None:
        pass
    else:
        return reqbody_verify(reqBody, err_code=17003001)

    if "id" not in reqBody:
        return Response({"result": 17003005, "msg": getErrMsgByCode(17003005, None)}, content_type="application/json")
    else:
        deptID = reqBody["id"]

    dept_li = []
    dept_li.append(deptID)

    indexPage = None
    countInfo = None

    if "page" in reqBody:
        indexPage = reqBody["page"]

    if "count" in reqBody:
        countInfo = reqBody["count"]

    subDeptList = getSubDeptList(deptID)

    resData = {}

#    if subDeptList is not None:
#        deptIDList = subDeptList
#        deptIDList.insert(0, deptID)
#    else:
#       deptIDList = dept_li

    deptIDList = dept_li
    try:
        rtspDeviceObjs = RTSPDeviceDB.objects.filter(dept__in=deptIDList).order_by("position")

        resultObjList = rtspDeviceObjs
        resultInfoList = []

        for item in resultObjList:
            deviceObj = {}

            deviceObj["id"] = item.id
            deviceObj["name"] = item.name
            deviceObj["dept"] = item.dept
            deviceObj["type"] = item.type
            deviceObj["server"] = item.server
            deviceObj["channel"] = item.channel
            deviceObj["longitude"] = item.longitude
            deviceObj["latitude"] = item.latitude
            deviceObj["height"] = item.height
            deviceObj["locate"] = item.locate
            deviceObj["enable"] = item.enable
            deviceObj["position"] = item.position
            deviceObj["manufacturer_type"]=item.manufacturer_type
            deviceObj["permissions_info"]=item.permissions_info
            deviceObj["channel_type"]=item.channel_type
            deviceObj["inter_code_SN"]=item.inter_code_SN
            deviceObj["multicast_ip"]=item.multicast_ip
            deviceObj["multicast_port"]=item.multicast_port

            resultInfoList.append(deviceObj)

        if indexPage and countInfo:
            indexStart = (indexPage - 1) * countInfo

            if indexStart < 0:
                indexStart = 0

            indexEnd = indexStart + countInfo

            if indexEnd >= rtspDeviceObjs.count():
                indexEnd = rtspDeviceObjs.count()

            resultInfoList = resultInfoList[indexStart:indexEnd]
        else:
            resultInfoList = resultInfoList

        resData["info"] = resultInfoList
    except Exception as err:
        return Response({"result": 17003006, "msg": getErrMsgByCode(17003006, err)}, content_type="application/json")

    resData["total"] = resultObjList.count()

    return Response({"result": 0, "msg": "OK", "data": resData}, content_type="application/json")


@csrf_exempt
@api_view(["post"])
def rtspDeviceInfoQuery(request):
    """
    Rtsp设备信息--按设备查询
    :return:
    """
    try:
        reqBody = json.loads(request.body)
    except Exception as err:
        return Response({"result": 17004001, "msg": getErrMsgByCode(17004001, err)}, content_type="application/json")

    if reqbody_verify(reqBody, err_code=17004001) is None:
        pass
    else:
        return reqbody_verify(reqBody, err_code=17004001)

    if "id" not in reqBody:
        return Response({"result": 17004005, "msg": getErrMsgByCode(17004005, None)}, content_type="application/json")
    else:
        deviceID = reqBody["id"]

    deviceInfo = {}

    try:
        deviceObj = RTSPDeviceDB.objects.get(id=deviceID)

        deviceInfo["id"] = deviceObj.id
        deviceInfo["name"] = deviceObj.name
        deviceInfo["dept"] = deviceObj.dept
        deviceInfo["type"] = deviceObj.type
        deviceInfo["server"] = deviceObj.server
        deviceInfo["channel"] = deviceObj.channel
        deviceInfo["longitude"] = deviceObj.longitude
        deviceInfo["latitude"] = deviceObj.latitude
        deviceInfo["height"] = deviceObj.height
        deviceInfo["locate"] = deviceObj.locate
        deviceInfo["enable"] = deviceObj.enable
        deviceInfo["position"] = deviceObj.position
        deviceInfo["manufacturer_type"] = deviceObj.manufacturer_type
        deviceInfo["permissions_info"] = deviceObj.permissions_info
        deviceInfo["channel_type"] = deviceObj.channel_type
        deviceInfo["inter_code_SN"] = deviceObj.inter_code_SN
        deviceInfo["multicast_ip"] = deviceObj.multicast_ip
        deviceInfo["multicast_port"] = deviceObj.multicast_port
    except Exception as err:
        return Response({"result": 17004006, "msg": getErrMsgByCode(17004006, err)}, content_type="application/json")

    return Response({"result": 0, "msg": "OK", "data": deviceInfo}, content_type="application/json")

@csrf_exempt
@api_view(["post"])
def rtspDeviceInfoQueryAll(request):
    """
    Rtsp设备信息--全部
    :return:
    """
    print(format(request.body))
    try:
        reqBody = json.loads(request.body)
    except Exception as err:
        return Response({"result": 17003001, "msg": getErrMsgByCode(17003001, err)}, content_type="application/json")

    if reqbody_verify(reqBody, err_code=17003001) is None:
        pass
    else:
        return reqbody_verify(reqBody, err_code=17003001)


    indexPage = None
    countInfo = None

    if "page" in reqBody:
        indexPage = reqBody["page"]

    if "count" in reqBody:
        countInfo = reqBody["count"]

    resData = {}

    try:
        rtspDeviceObjs = RTSPDeviceDB.objects.all().order_by("position")

        resultObjList = rtspDeviceObjs
        resultInfoList = []

        for item in resultObjList:
            deviceObj = {}

            deviceObj["id"] = item.id
            deviceObj["name"] = item.name
            deviceObj["dept"] = item.dept
            deviceObj["type"] = item.type
            deviceObj["server"] = item.server
            deviceObj["channel"] = item.channel
            deviceObj["longitude"] = item.longitude
            deviceObj["latitude"] = item.latitude
            deviceObj["height"] = item.height
            deviceObj["locate"] = item.locate
            deviceObj["enable"] = item.enable
            deviceObj["position"] = item.position
            deviceObj["manufacturer_type"]=item.manufacturer_type
            deviceObj["permissions_info"]=item.permissions_info
            deviceObj["channel_type"]=item.channel_type
            deviceObj["inter_code_SN"]=item.inter_code_SN
            deviceObj["multicast_ip"]=item.multicast_ip
            deviceObj["multicast_port"]=item.multicast_port

            resultInfoList.append(deviceObj)

        if indexPage and countInfo:
            indexStart = (indexPage - 1) * countInfo

            if indexStart < 0:
                indexStart = 0

            indexEnd = indexStart + countInfo

            if indexEnd >= rtspDeviceObjs.count():
                indexEnd = rtspDeviceObjs.count()

            resultInfoList = resultInfoList[indexStart:indexEnd]
        else:
            resultInfoList = resultInfoList

        resData["info"] = resultInfoList
    except Exception as err:
        return Response({"result": 17003006, "msg": getErrMsgByCode(17003006, err)}, content_type="application/json")

    resData["total"] = resultObjList.count()

    return Response({"result": 0, "msg": "OK", "data": resData}, content_type="application/json")


@csrf_exempt
@api_view(["post"])
def rtspDeviceInfoDelete(request):
    """
    Rtsp信息--删除
    :return:
    """
    try:
        reqBody = json.loads(request.body)
    except Exception as err:
        return Response({"result": 17005001, "msg": getErrMsgByCode(17005001, err)}, content_type="application/json")

    if reqbody_verify_admin(reqBody, err_code=17005001) is None:
        pass
    else:
        return reqbody_verify_admin(reqBody, err_code=17005001)

    if "id" not in reqBody:
        return Response({"result": 17005006, "msg": getErrMsgByCode(17005006, None)}, content_type="application/json")
    else:
        deviceID = reqBody["id"]

    try:
        deviceObj = RTSPDeviceDB.objects.get(id=deviceID)
    except Exception as err:
        return Response({"result": 17005007, "msg": getErrMsgByCode(17005007, err)}, content_type="application/json")

    try:
        deviceObj.delete()
    except Exception as err:
        return Response({"result": 17005008, "msg": getErrMsgByCode(17005008, err)}, content_type="application/json")

    return Response({"result": 0, "msg": "OK"}, content_type="application/json")


@csrf_exempt
@api_view(["post"])
def rtspDeviceInfoSort(request):
    """
    Rtsp设备信息--排序
    :return:
    """
    try:
        reqBody = json.loads(request.body)
    except Exception as err:
        return Response({"result": 17006001, "msg": getErrMsgByCode(17006001, err)}, content_type="application/json")

    if reqbody_verify_admin(reqBody, err_code=17006001) is None:
        pass
    else:
        return reqbody_verify_admin(reqBody, err_code=17006001)

    if "id" not in reqBody:
        return Response({"result": 17006006, "msg": getErrMsgByCode(17006006, None)}, content_type="application/json")
    else:
        deptID = reqBody["id"]

    if "devices" not in reqBody:
        return Response({"result": 17006007, "msg": getErrMsgByCode(17006007, None)}, content_type="application/json")
    else:
        deviceList = reqBody["devices"]

    savePoint = transaction.savepoint()

    try:
        i = 1

        for device in deviceList:
            RTSPDeviceDB.objects.filter(id=device).update(position=i)

            i += 1
    except Exception as err:
        transaction.savepoint_rollback(savePoint)
        return Response({"result": 17006008, "msg": getErrMsgByCode(17006008, err)}, content_type="application/json")

    transaction.savepoint_commit(savePoint)

    return Response({"result": 0, "msg": "OK"}, content_type="application/json")


@csrf_exempt
@api_view(["post"])
def rtspDeviceRollingAdd(request):
    """
    Rtsp设备轮询列表--增加
    :return:
    """
    try:
        reqBody = json.loads(request.body)
    except Exception as err:
        return Response({"result": 17007001, "msg": getErrMsgByCode(17007001, err)}, content_type="application/json")

    if reqbody_verify(reqBody, err_code=17007001) is None:
        pass
    else:
        return reqbody_verify(reqBody, err_code=17007001)

    if "user" not in reqBody:
        return Response({"result": 17007006, "msg": getErrMsgByCode(17007006, None)}, content_type="application/json")
    else:
        userID = reqBody["user"]

    if "devices" not in reqBody:
        return Response({"result": 17007007, "msg": getErrMsgByCode(17007007, None)}, content_type="application/json")
    else:
        deviceList = reqBody["devices"]

    savePoint = transaction.savepoint()

    try:
        RTSPRollingDB.objects.filter(user=userID).delete()
    except Exception as err:
        transaction.savepoint_rollback(savePoint)
        return Response({"result": 17007008, "msg": getErrMsgByCode(17007008, err)}, content_type="application/json")

    try:
        for device in deviceList:
            rollObj = RTSPRollingDB()
            rollObj.user = userID
            rollObj.ipc = device
            rollObj.enable = 1

            rollObj.save()
    except Exception as err:
        transaction.savepoint_rollback(savePoint)
        return Response({"result": 17007009, "msg": getErrMsgByCode(17007009, err)}, content_type="application/json")

    transaction.savepoint_commit(savePoint)

    return Response({"result": 0, "msg": "OK"}, content_type="application/json")


@csrf_exempt
@api_view(["post"])
def rtspDeviceRollingQuery(request):
    """
    Rtsp设备轮询列表--查询
    """
    try:
        reqBody = json.loads(request.body)
    except Exception as err:
        return Response({"result": 17008001, "msg": getErrMsgByCode(17008001, err)}, content_type="application/json")

    if reqbody_verify(reqBody, err_code=17008001) is None:
        pass
    else:
        return reqbody_verify(reqBody, err_code=17008001)

    if "user" not in reqBody:
        return Response({"result": 17008006, "msg": getErrMsgByCode(17008006, None)}, content_type="application/json")
    else:
        userID = reqBody["user"]

    resData = []
    try:
        ipcObjList = RTSPRollingDB.objects.filter(user=userID)

        for ipcItem in ipcObjList:
            ipcObj = RTSPDeviceDB.objects.filter(id=ipcItem.ipc).first()
            if not ipcObj:
                continue

            deviceInfo = {}
            deviceInfo["id"] = ipcObj.id
            deviceInfo["name"] = ipcObj.name
            deviceInfo["dept"] = ipcObj.dept
            deviceInfo["type"] = ipcObj.type
            deviceInfo["server"] = ipcObj.server
            deviceInfo["channel"] = ipcObj.channel
            deviceInfo["longitude"] = ipcObj.longitude
            deviceInfo["latitude"] = ipcObj.latitude
            deviceInfo["height"] = ipcObj.height
            deviceInfo["locate"] = ipcObj.locate
            deviceInfo["enable"] = ipcObj.enable
            deviceInfo["position"] = ipcObj.position

            resData.append(deviceInfo)
    except Exception as err:
        return Response({"result": 17008007, "msg": getErrMsgByCode(17008007, err)}, content_type="application/json")

    return Response({"result": 0, "msg": "OK", "data": resData}, content_type="application/json")


@csrf_exempt
@api_view(["post"])
def rtspRecordInfoAdd(request):
    """
    Rtsp设备录像信息--添加
    """
    try:
        reqBody = json.loads(request.body)
    except Exception as err:
        return Response({"result": 17009001, "msg": getErrMsgByCode(17009001, err)}, content_type="application/json")

    if reqbody_verify(reqBody, err_code=17009001) is None:
        pass
    else:
        return reqbody_verify(reqBody, err_code=17009001)

    if "device" not in reqBody:
        return Response({"result": 17009006, "msg": getErrMsgByCode(17009006, None)}, content_type="application/json")
    else:
        deviceID = reqBody["device"]

    if "user" not in reqBody:
        return Response({"result": 17009007, "msg": getErrMsgByCode(17009007, None)}, content_type="application/json")
    else:
        userID = reqBody["user"]

    if "type" not in reqBody:
        return Response({"result": 17009008, "msg": getErrMsgByCode(17009008, None)}, content_type="application/json")
    else:
        recordType = reqBody["type"]

    recordCode = None
    # if recordType == 1:
    if "record_code" not in reqBody:
        return Response({"result": 17009009, "msg": getErrMsgByCode(17009009, None)}, content_type="application/json")
    else:
        recordCode = reqBody["record_code"]
    # else:
    #     recordCode = str(deviceID) + "." + str(userID) + "." + str(time.time())

    try:
        recordObj = RTSPRecordDB()
        recordObj.user = userID
        recordObj.ipc = deviceID
        recordObj.type = recordType
        recordObj.record_code = recordCode

        recordObj.save()
    except Exception as err:
        return Response({"result": 17009010, "msg": getErrMsgByCode(17009010, err)}, content_type="application/json")

    return Response({"result": 0, "msg": "OK", "recordCode": recordCode}, content_type="application/json")



@csrf_exempt
@api_view(["post"])
def rtspRecordInfoQuery(request):
    """
    录像记录--查询
    """
    try:
        reqBody = json.loads(request.body)
    except Exception as err:
        return Response({"result": 17010001, "msg": getErrMsgByCode(17010001, err)}, content_type="application/json")

    if reqbody_verify_admin(reqBody, err_code=17010001) is None:
        pass
    else:
        return reqbody_verify_admin(reqBody, err_code=17010001)

    # deviceID = None
    # if "device" not in reqBody:
    #     return Response({"result": 17010006, "msg": getErrMsgByCode(17010006, None)}, content_type="application/json")
    # else:
    #     deviceID = reqBody["device"]

    afterTime = None
    beforeTime = None
    indexPage = None
    countInfo = None
    orderInfo = None

    if "after" in reqBody:
        afterTime = reqBody["after"]

    if "before" in reqBody:
        beforeTime = reqBody["before"]

    if "page" in reqBody:
        indexPage = reqBody["page"]

    if "count" in reqBody:
        countInfo = reqBody["count"]

    if "order" in reqBody:
        orderInfo = reqBody["order"]

    resData = {}
    try:
        if afterTime and beforeTime:
            recordObjs = RTSPRecordDB.objects.filter(type=0, time__gt=afterTime, time__lt=beforeTime)
        else:
            # recordObjs = RTSPRecordDB.objects.filter(ipc=deviceID, type=0)
            recordObjs = RTSPRecordDB.objects.filter(type=0)

        if orderInfo == 1:
            recordObjs = recordObjs.order_by("-time")
        else:
            recordObjs = recordObjs.order_by("time")

        resultInfoListAll = []
        for obj in recordObjs:
            imInfo = {}

            imInfo["id"] = obj.id
            imInfo["ipc"] = obj.ipc
            imInfo["user"] = obj.user
            imInfo["record_code"] = obj.record_code

            imInfo["type"] = obj.type
            imInfo["start"] = obj.time

            # endObj = RTSPRecordDB.objects.filter(ipc=deviceID, record_code=obj.record_code, type=1)
            endObj = RTSPRecordDB.objects.filter( record_code=obj.record_code, type=1)
            if endObj:
                imInfo["end"] = endObj[0].time
                resultInfoListAll.append(imInfo)

        resultInfoList = []

        if indexPage and countInfo:
            indexStart = (indexPage - 1) * countInfo

            if indexStart < 0:
                indexStart = 0

            indexEnd = indexStart + countInfo

            if indexEnd >= len(resultInfoListAll):
                indexEnd = len(resultInfoListAll)

            resultInfoList = resultInfoListAll[indexStart:indexEnd]
        else:
            resultInfoList = resultInfoListAll

        resData["total"] = len(resultInfoListAll)
        resData["info"] = resultInfoList

    except Exception as err:
        return Response({"result": 17010007, "msg": getErrMsgByCode(17010007, err)}, content_type="application/json")

    return Response({"result": 0, "msg": "OK", "data": resData}, content_type="application/json")

@csrf_exempt
@api_view(["post"])
def aiRtspDeviceInfoAdd(request):
    """
    Rtsp设备信息--新增
    :return:
    """
    try:
        reqBody = json.loads(request.body)
    except Exception as err:
        return Response({"result": 17011001, "msg": getErrMsgByCode(17011001, err)}, content_type="application/json")

    if reqbody_verify_admin(reqBody, err_code=17011001) is None:
        pass
    else:
        return reqbody_verify_admin(reqBody, err_code=17011001)

    if "ai_id" not in reqBody:
        return Response({"result": 17011006, "msg": getErrMsgByCode(17011006, None)}, content_type="application/json")
    else:
        aiId = reqBody["ai_id"]

    if "name" not in reqBody:
        return Response({"result": 17011007, "msg": getErrMsgByCode(17011007, None)}, content_type="application/json")
    else:
        deviceName = reqBody["name"]

    if "dept" not in reqBody:
        return Response({"result": 17011008, "msg": getErrMsgByCode(17011008, None)}, content_type="application/json")
    else:
        deviceDept = reqBody["dept"]

    if "code" not in reqBody:
        return Response({"result": 17011009, "msg": getErrMsgByCode(17011009, None)}, content_type="application/json")
    else:
        deviceCode = reqBody["code"]

    if "enable" not in reqBody:
        return Response({"result": 17011010, "msg": getErrMsgByCode(17011010, None)}, content_type="application/json")
    else:
        deviceEnable = reqBody["enable"]

    if "locate" not in reqBody:
        return Response({"result": 17011011, "msg": getErrMsgByCode(17011011, None)}, content_type="application/json")
    else:
        deviceLocate = reqBody["locate"]

    if "channel" not in reqBody:
        return Response({"result": 17011012, "msg": getErrMsgByCode(17011012, None)}, content_type="application/json")
    else:
        channel = reqBody["channel"]

    deviceLon = None
    deviceLat = None
    deviceHeight = None

    if "longitude"  in reqBody:
        deviceLon = reqBody["longitude"]

    if "latitude"  in reqBody:
        deviceLat = reqBody["latitude"]

    if "height"  in reqBody:
        deviceHeight = reqBody["height"]


    deviceObj = videoMonitorDB()

    deviceObj.name = deviceName
    deviceObj.ai_device_id= aiId
    deviceObj.code=deviceCode
    deviceObj.channel=channel
    deviceObj.dept = deviceDept
    deviceObj.enable = deviceEnable
    deviceObj.longitude = deviceLon
    deviceObj.latitude = deviceLat
    deviceObj.height = deviceHeight
    deviceObj.locate = deviceLocate


    try:
        deviceObj.save()

    except Exception as err:
        Response({"result": 17011013, "msg": getErrMsgByCode(17011013, err)}, content_type="application/json")

    return Response({"result": 0, "msg": "OK"}, content_type="application/json")

@csrf_exempt
@api_view(["post"])
def AIrtspDeviceInfoModify(request):
    """
     AI Rtsp设备信息--修改
    :return:
    """
    try:
        reqBody = json.loads(request.body)
    except Exception as err:
        return Response({"result": 17012001, "msg": getErrMsgByCode(17012001, err)}, content_type="application/json")

    if reqbody_verify_admin(reqBody, err_code=17012001) is None:
        pass
    else:
        return reqbody_verify_admin(reqBody, err_code=17012001)

    if "id" not in reqBody:
        return Response({"result": 17012006, "msg": getErrMsgByCode(17012006, None)}, content_type="application/json")
    else:
        deviceID = reqBody["id"]

    deviceName = None
    deviceDept = None
    # deviceAiId=None
    deviceCode=None
    deviceChannel = None
    deviceLon = None
    deviceLat = None
    deviceHeight = None
    deviceLocate = None
    deviceEnable = None



    if "name" in reqBody:
        deviceName = reqBody["name"]

    if "dept" in reqBody:
        deviceDept = reqBody["dept"]

    # if "ai_id" in reqBody:
    #     deviceAiId = reqBody["ai_id"]

    if "code" in reqBody:
        deviceCode = reqBody["code"]

    if "channel" in reqBody:
        deviceChannel = reqBody["channel"]

    if "longitude" in reqBody:
        deviceLon = reqBody["longitude"]

    if "latitude" in reqBody:
        deviceLat = reqBody["latitude"]

    if "height" in reqBody:
        deviceHeight = reqBody["height"]

    if "locate" in reqBody:
        deviceLocate = reqBody["locate"]

    if "enable" in reqBody:
        deviceEnable = reqBody["enable"]



    try:
        deviceObj = videoMonitorDB.objects.get(id=deviceID)
    except Exception as err:
        return Response({"result": 17012007, "msg": getErrMsgByCode(17012007, err)}, content_type="application/json")

    if deviceName is not None:
        deviceObj.name = deviceName

    if deviceDept is not None:
        deviceObj.dept = deviceDept

    # if deviceAiId is not None:
    #     deviceObj.ai_device_id = deviceAiId

    if deviceCode is not None:
        deviceObj.code = deviceCode

    if deviceChannel is not None:
        deviceObj.channel = deviceChannel

    if deviceLon is not None:
        deviceObj.longitude = deviceLon

    if deviceLat is not None:
        deviceObj.latitude = deviceLat

    if deviceHeight is not None:
        deviceObj.height = deviceHeight

    if deviceLocate is not None:
        deviceObj.locate = deviceLocate

    if deviceEnable is not None:
        deviceObj.enable = deviceEnable



    try:
        deviceObj.save()
    except Exception as err:
        return Response({"result": 17012008, "msg": getErrMsgByCode(17012008, err)}, content_type="application/json")

    return Response({"result": 0, "msg": "OK"}, content_type="application/json")

@csrf_exempt
@api_view(["post"])
def AIrtspDeviceInfoQueryAll(request):
    """
     AI Rtsp设备信息--全部
    :return:
    """
    try:
        reqBody = json.loads(request.body)
    except Exception as err:
        return Response({"result": 17013001, "msg": getErrMsgByCode(17013001, err)}, content_type="application/json")

    if reqbody_verify(reqBody, err_code=17013001) is None:
        pass
    else:
        return reqbody_verify(reqBody, err_code=17013001)


    resData = []

    try:
        rtspDeviceObjs = videoMonitorDB.objects.all()


        for item in rtspDeviceObjs:
            deviceObj = {}

            deviceObj["id"] = item.id
            deviceObj["name"] = item.name
            deviceObj["dept"] = item.dept
            deviceObj["ai_id"] = item.ai_device_id
            deviceObj["code"] = item.code
            deviceObj["channel"] = item.channel
            deviceObj["longitude"] = item.longitude
            deviceObj["latitude"] = item.latitude
            deviceObj["height"] = item.height
            deviceObj["locate"] = item.locate
            deviceObj["enable"] = item.enable
            resData.append(deviceObj)

    except Exception as err:
        return Response({"result": 17013006, "msg": getErrMsgByCode(17013006, err)}, content_type="application/json")


    return Response({"result": 0, "msg": "OK", "data": resData}, content_type="application/json")

@csrf_exempt
@api_view(["post"])
def AIrtspDeviceInfoDelete(request):
    """
    Rtsp信息--删除
    :return:
    """
    try:
        reqBody = json.loads(request.body)
    except Exception as err:
        return Response({"result": 17014001, "msg": getErrMsgByCode(17014001, err)}, content_type="application/json")

    if reqbody_verify_admin(reqBody, err_code=17014001) is None:
        pass
    else:
        return reqbody_verify_admin(reqBody, err_code=17005001)

    if "id" not in reqBody:
        return Response({"result": 17014006, "msg": getErrMsgByCode(17014006, None)}, content_type="application/json")
    else:
        deviceID = reqBody["id"]

    try:
        deviceObj = videoMonitorDB.objects.get(id=deviceID)
    except Exception as err:
        return Response({"result": 17014007, "msg": getErrMsgByCode(17014007, err)}, content_type="application/json")

    try:
        deviceObj.delete()
    except Exception as err:
        return Response({"result": 17014008, "msg": getErrMsgByCode(17014008, err)}, content_type="application/json")

    return Response({"result": 0, "msg": "OK"}, content_type="application/json")


@csrf_exempt
@api_view(["post"])
def AirtspRecordInfoQuery(request):
    """
    AI 录像记录--查询
    """
    try:
        reqBody = json.loads(request.body)
    except Exception as err:
        return Response({"result": 17015001, "msg": getErrMsgByCode(17015001, err)}, content_type="application/json")

    if reqbody_verify_admin(reqBody, err_code=17015001) is None:
        pass
    else:
        return reqbody_verify_admin(reqBody, err_code=17015001)

    resData = []

    try:
        AirtspDeviceObjs = AiRtspRecordDB.objects.all()

        for item in AirtspDeviceObjs:
            deviceObj = {}
            deviceObj["id"]=item.id
            deviceObj["ipc"]=item.ipc
            deviceObj["record_code"]=item.record_code
            deviceObj["start_time"]=item.start_time
            deviceObj["end_time"]=item.end_time
            resData.append(deviceObj)
    except Exception as err:
        return Response({"result": 17015006, "msg": getErrMsgByCode(17015006, err)}, content_type="application/json")


    return Response({"result": 0, "msg": "OK", "data": resData}, content_type="application/json")



