import json
from api.public import tokenDecode
from api.public import reqbody_verify
from api.ErrorCode import getErrMsgByCode
from api.public import reqbody_verify_admin
from rest_framework.response import Response
from rest_framework.decorators import api_view
from api.models import rtsp_server as RTSPServerDB
from django.views.decorators.csrf import csrf_exempt


@csrf_exempt
@api_view(["post"])
def addRtspServerInfo(request):
    """
    Rtsp服务信息--新增
    :return:
    """
    try:
        reqBody = json.loads(request.body)
    except Exception as err:
        return Response({"result": 16001001, "msg": getErrMsgByCode(16001001, err)}, content_type="application/json")

    if reqbody_verify_admin(reqBody, err_code=16001001) is None:
        pass
    else:
        return reqbody_verify_admin(reqBody, err_code=16001001)

    if "name" not in reqBody:
        return Response({"result": 16001006, "msg": getErrMsgByCode(16001006, None)}, content_type="application/json")
    else:
        serverName = reqBody["name"]

    if "ip" not in reqBody:
        return Response({"result": 16001007, "msg": getErrMsgByCode(16001007, None)}, content_type="application/json")
    else:
        serverIP = reqBody["ip"]

    if "port" not in reqBody:
        return Response({"result": 16001008, "msg": getErrMsgByCode(16001008, None)}, content_type="application/json")
    else:
        serverPort = reqBody["port"]

    if "user" not in reqBody:
        return Response({"result": 16001009, "msg": getErrMsgByCode(16001009, None)}, content_type="application/json")
    else:
        serverUser = reqBody["user"]

    if "password" not in reqBody:
        return Response({"result": 16001010, "msg": getErrMsgByCode(16001010, None)}, content_type="application/json")
    else:
        serverPassword = reqBody["password"]

    if "channels" not in reqBody:
        return Response({"result": 16001011, "msg": getErrMsgByCode(16001011, None)}, content_type="application/json")
    else:
        serverChannels = reqBody["channels"]

    if "type" not in reqBody:
        return Response({"result": 16001012, "msg": getErrMsgByCode(16001012, None)}, content_type="application/json")
    else:
        serverType = reqBody["type"]

    if "enable" not in reqBody:
        return Response({"result": 16001013, "msg": getErrMsgByCode(16001013, None)}, content_type="application/json")
    else:
        serverEnable = reqBody["enable"]

    rtspServerObj = RTSPServerDB()

    rtspServerObj.name = serverName
    rtspServerObj.ip = serverIP
    rtspServerObj.port = serverPort
    rtspServerObj.user = serverUser

    rtspServerObj.password = serverPassword
    rtspServerObj.channels = serverChannels
    rtspServerObj.type = serverType
    rtspServerObj.enable = serverEnable

    try:
        rtspServerObj.save()
    except Exception as err:
        return Response({"result": 16001014, "msg": getErrMsgByCode(16001014, err)}, content_type="application/json")

    return Response({"result": 0, "msg": "OK"}, content_type="application/json")


@csrf_exempt
@api_view(["post"])
def modifyRtspServerInfo(request):
    """
    Rtsp服务信息--修改
    :return:
    """
    try:
        reqBody = json.loads(request.body)
    except Exception as err:
        return Response({"result": 16002001, "msg": getErrMsgByCode(16002001, err)}, content_type="application/json")

    if reqbody_verify_admin(reqBody, err_code=16002001) is None:
        pass
    else:
        return reqbody_verify_admin(reqBody, err_code=16002001)

    if "id" not in reqBody:
        return Response({"result": 16002006, "msg": getErrMsgByCode(16002006, None)}, content_type="application/json")
    else:
        serverID = reqBody["id"]

    serverName = None
    serverIP = None
    serverPort = None
    serverUser = None

    serverPassword = None
    serverChannels = None
    serverType = None
    serverEnable = None

    if "name" in reqBody:
        serverName = reqBody["name"]

    if "ip" in reqBody:
        serverIP = reqBody["ip"]

    if "port" in reqBody:
        serverPort = reqBody["port"]

    if "user" in reqBody:
        serverUser = reqBody["user"]

    if "password" in reqBody:
        serverPassword = reqBody["password"]

    if "channels" in reqBody:
        serverChannels = reqBody["channels"]

    if "type" in reqBody:
        serverType = reqBody["type"]

    if "enable" in reqBody:
        serverEnable = reqBody["enable"]

    try:
        rtspServerObj = RTSPServerDB.objects.get(id=serverID)
    except Exception as err:
        return Response({"result": 16002007, "msg": getErrMsgByCode(16002007, err)}, content_type="application/json")

    if serverName is not None:
        rtspServerObj.name = serverName

    if serverIP is not None:
        rtspServerObj.ip = serverIP

    if serverPort is not None:
        rtspServerObj.port = serverPort

    if serverUser is not None:
        rtspServerObj.user = serverUser

    if serverPassword is not None:
        rtspServerObj.password = serverPassword

    if serverChannels is not None:
        rtspServerObj.channels = serverChannels

    if serverType is not None:
        rtspServerObj.type = serverType

    if serverEnable is not None:
        rtspServerObj.enable = serverEnable

    try:
        rtspServerObj.save()
    except Exception as err:
        return Response({"result": 16002008, "msg": getErrMsgByCode(16002008, err)}, content_type="application/json")

    return Response({"result": 0, "msg": "OK"}, content_type="application/json")


@csrf_exempt
@api_view(["post"])
def queryRtspServerInfo(request):
    """
    Rtsp服务信息--查询
    :return:
    """
    try:
        reqBody = json.loads(request.body)
    except Exception as err:
        return Response({"result": 16003001, "msg": getErrMsgByCode(16003001, err)}, content_type="application/json")

    if reqbody_verify(reqBody, err_code=16003001) is None:
        pass
    else:
        return reqbody_verify(reqBody, err_code=16003001)

    tokenInfo = tokenDecode(reqBody["token"])
    serverID = None

    if tokenInfo["role"] >= 10:
        if "id" in reqBody:
            serverID = reqBody["id"]
    else:
        if "id" in reqBody:
            serverID = reqBody["id"]
        else:
            return Response({"result": 16003005, "msg": getErrMsgByCode(16003005, None)},  content_type="application/json")

    resData = []

    try:
        if serverID is None:
            sipServerObjs = RTSPServerDB.objects.all()
        else:
            sipServerObjs = RTSPServerDB.objects.filter(id=serverID)

        for item in sipServerObjs:
            serverObj = {}

            serverObj["id"] = item.id
            serverObj["name"] = item.name
            serverObj["ip"] = item.ip
            serverObj["port"] = item.port

            serverObj["user"] = item.user
            serverObj["password"] = item.password
            serverObj["channels"] = item.channels
            serverObj["type"] = item.type
            serverObj["enable"] = item.enable

            resData.append(serverObj)
    except Exception as err:
        return Response({"result": 16003006, "msg": getErrMsgByCode(16003006, err)}, content_type="application/json")

    return Response({"result": 0, "msg": "OK", "data": resData}, content_type="application/json")


@csrf_exempt
@api_view(["post"])
def deleteRtspServerInfo(request):
    """
    Rtsp服务信息--删除
    :return:
    """
    try:
        reqBody = json.loads(request.body)
    except Exception as err:
        return Response({"result": 16004001, "msg": getErrMsgByCode(16004001, err)}, content_type="application/json")

    if reqbody_verify_admin(reqBody, err_code=16004001) is None:
        pass
    else:
        return reqbody_verify_admin(reqBody, err_code=16004001)

    if "id" not in reqBody:
        return Response({"result": 16004006, "msg": getErrMsgByCode(16004006, None)}, content_type="application/json")
    else:
        serverID = reqBody["id"]

    try:
        rtspServerObj = RTSPServerDB.objects.get(id=serverID)
    except Exception as err:
        return Response({"result": 16004007, "msg": getErrMsgByCode(16004007, err)}, content_type="application/json")

    try:
        rtspServerObj.delete()
    except Exception as err:
        return Response({"result": 16004008, "msg": getErrMsgByCode(16004008, err)}, content_type="application/json")

    return Response({"result": 0, "msg": "OK"}, content_type="application/json")


