import json
import requests
import time
from urllib import parse
from django.db import transaction


from api.dept import getAllDeptMemberList
from api.public import reqbody_verify
from api.public import reqbody_verify_admin
from api.ErrorCode import getErrMsgByCode
from api.public import reqbody_verify
from api.operation import addOperationLog
from api.models import info_template as infoTempDB
from api.models import sms_log as smsLogDB


from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.views.decorators.csrf import csrf_exempt


smsSystemUrl = "http://sms.api.ums86.com:8899/sms/Api/Send.do"
smsSysAccount = "admin1"
smsSysAuth = "tomorrow2003"
smsRequestID = "227313"


def sendSMSInfoImplement(userList, contentText):
    """
    发送手机短信
    """
    paramData = {}
    paramData["SpCode"] = smsRequestID
    paramData["LoginName"] = smsSysAccount
    paramData["Password"] = smsSysAuth
    paramData["MessageContent"] = contentText.encode("gb2312")
    paramData["SerialNumber"] = str(time.time())
    paramData["ScheduleTime"] = ""
    paramData["ExtendAccessNum"] = ""
    paramData["f"] = "1"

    numList = ""
    for user in userList:
        if len(numList) > 0:
            numList += ","
        userPhone = user["phone"]
        numList += userPhone
    paramData["UserNumber"] = numList

    try:
        resultResponse = requests.get(smsSystemUrl, params=paramData, timeout=2)
    except Exception as err:
        return {"result": 1, "msg": "短信发送请求失败!<" + format(err) + ">"}
    else:
        resultDict = parse.parse_qs(resultResponse.text)
        result = resultDict["result"][0]
        if int(result) != 0:
            return {"result": 1, "msg": resultDict["description"][0]}
        else:
            fallList = []
            if "faillist" in resultDict.keys():
                fallList = resultDict["faillist"][0].split(",")

            logList = []
            for user in userList:
                logObj = {}
                logObj["user_id"] = user["id"]
                logObj["name"] = user["name"]
                logObj["phone"] = user["phone"]
                logObj["content"] = contentText

                if user["phone"] in fallList:
                    logObj["type"] = 0
                else:
                    logObj["type"] = 1

                logList.append(logObj)

            savePoint = transaction.savepoint()
            try:
                for item in logList:
                    logInfoObj = smsLogDB()

                    logInfoObj.user_id = item["user_id"]
                    logInfoObj.name = item["name"]
                    logInfoObj.phone = item["phone"]
                    logInfoObj.content = item["content"]
                    logInfoObj.type = item["type"]

                    logInfoObj.save()
            except Exception as err:
                transaction.savepoint_rollback(savePoint)
                return {"result": 1, "msg": "短信记录存储失败!<" + format(err) + ">"}
            transaction.savepoint_commit(savePoint)

            return {"result": 0, "msg": "短信发送成功"}


@csrf_exempt
@api_view(["post"])
def sendSMSInfo(request):
    """
    发送手机短信
    """
    try:
        reqBody = json.loads(request.body)
    except Exception as err:
        return Response({"result": 19001001, "msg": getErrMsgByCode(19001001, err)}, content_type="application/json")

    if reqbody_verify(reqBody, err_code=19001001) is None:
        pass
    else:
        return reqbody_verify(reqBody, err_code=19001001)

    if "user_list" not in reqBody:
        return Response({"result": 19001006, "msg": getErrMsgByCode(19001006, None)}, content_type="application/json")
    else:
        userList = reqBody["user_list"]

    if "content" not in reqBody:
        return Response({"result": 19001007, "msg": getErrMsgByCode(19001007, None)}, content_type="application/json")
    else:
        contentText = reqBody["content"]

    numList = ""
    for user in userList:
        if len(numList) > 0:
            numList += ","
        userPhone = user["phone"]
        numList += userPhone

    paramData = {}
    paramData["SpCode"] = smsRequestID
    paramData["LoginName"] = smsSysAccount
    paramData["Password"] = smsSysAuth
    paramData["MessageContent"] = contentText.encode("gb2312")
    paramData["SerialNumber"] = str(time.time())
    paramData["ScheduleTime"] = ""
    paramData["ExtendAccessNum"] = ""
    paramData["f"] = "1"
    paramData["UserNumber"] = numList

    try:
        resultResponse = requests.get(smsSystemUrl, params=paramData, timeout=2)
    except Exception as err:
        return Response({"result": 19001008, "msg": getErrMsgByCode(19001008, err)}, content_type="application/json")
    else:
        resultDict = parse.parse_qs(resultResponse.text)
        result = resultDict["result"][0]
        if int(result) != 0:
            print(int(result))
            print(resultDict["description"][0])
            return Response({"result": 19001009, "msg": getErrMsgByCode(19001009, resultDict["description"][0])}, content_type="application/json")
        else:
            fallList = []
            if "faillist" in resultDict.keys():
                fallList = resultDict["faillist"][0].split(",")

            logList = []
            for user in userList:
                logObj = {}
                logObj["user_id"] = user["id"]
                logObj["name"] = user["name"]
                logObj["phone"] = user["phone"]
                logObj["content"] = contentText

                if user["phone"] in fallList:
                    logObj["type"] = 0
                else:
                    logObj["type"] = 1

                logList.append(logObj)

            savePoint = transaction.savepoint()
            try:
                for item in logList:
                    logInfoObj = smsLogDB()

                    logInfoObj.user_id = item["user_id"]
                    logInfoObj.name = item["name"]
                    logInfoObj.phone = item["phone"]
                    logInfoObj.content = item["content"]
                    logInfoObj.type = item["type"]

                    logInfoObj.save()
            except Exception as err:
                transaction.savepoint_rollback(savePoint)
                return Response({"result": 19001010, "msg": getErrMsgByCode(19001010, err)}, content_type="application/json")
            transaction.savepoint_commit(savePoint)

    return Response({"result": 0, "msg": "OK"}, content_type="application/json")


@csrf_exempt
@api_view(["post"])
def addSMSTemplateInfo(request):
    """
    SMS短信模板--新增
    """
    try:
        reqBody = json.loads(request.body)
    except Exception as err:
        return Response({"result": 19002001, "msg": getErrMsgByCode(19002001, err)}, content_type="application/json")

    if reqbody_verify_admin(reqBody, err_code=19002001) is None:
        pass
    else:
        return reqbody_verify_admin(reqBody, err_code=19002001)

    if "user" not in reqBody:
        return Response({"result": 19002006, "msg": getErrMsgByCode(19002006, None)}, content_type="application/json")
    else:
        userID = reqBody["user"]

    if "name" not in reqBody:
        return Response({"result": 19002007, "msg": getErrMsgByCode(19002007, None)}, content_type="application/json")
    else:
        tempName = reqBody["name"]

    if "content" not in reqBody:
        return Response({"result": 19002008, "msg": getErrMsgByCode(19002008, None)}, content_type="application/json")
    else:
        tempContent = reqBody["content"]

    if "type" not in reqBody:
        return Response({"result": 19002009, "msg": getErrMsgByCode(19002009, None)}, content_type="application/json")
    else:
        tempType = reqBody["type"]

    tempInfoObj = infoTempDB()
    tempInfoObj.user = userID
    tempInfoObj.name = tempName
    tempInfoObj.content = tempContent
    tempInfoObj.type = tempType

    try:
        tempInfoObj.save()
    except Exception as err:
        return Response({"result": 19002010, "msg": getErrMsgByCode(19002010, err)}, content_type="application/json")

    return Response({"result": 0, "msg": "OK"}, content_type="application/json")


@csrf_exempt
@api_view(["post"])
def modifyTemplateInfo(request):
    """
    SMS短信模板--修改
    """
    try:
        reqBody = json.loads(request.body)
    except Exception as err:
        return Response({"result": 19003001, "msg": getErrMsgByCode(19003001, err)}, content_type="application/json")

    if reqbody_verify_admin(reqBody, err_code=19003001) is None:
        pass
    else:
        return reqbody_verify_admin(reqBody, err_code=19003001)

    if "id" not in reqBody:
        return Response({"result": 19003006, "msg": getErrMsgByCode(19003006, None)}, content_type="application/json")
    else:
        infoID = reqBody["id"]

    tempName = None
    tempContent = None
    tempType = None

    if "name" in reqBody:
        tempName = reqBody["name"]

    if "content" in reqBody:
        tempContent = reqBody["content"]

    if "type" in reqBody:
        tempType = reqBody["type"]

    try:
        infoObj = infoTempDB.objects.get(id=infoID)
    except Exception as err:
        return Response({"result": 19003007, "msg": getErrMsgByCode(19003007, err)}, content_type="application/json")

    if tempName is not None:
        infoObj.name = tempName

    if tempContent is not None:
        infoObj.content = tempContent

    if tempType is not None:
        infoObj.type = tempType

    try:
        infoObj.save()
    except Exception as err:
        return Response({"result": 19003008, "msg": getErrMsgByCode(19003008, err)}, content_type="application/json")

    return Response({"result": 0, "msg": "OK"}, content_type="application/json")


@csrf_exempt
@api_view(["post"])
def queryTemplateInfo(request):
    """
    SMS短信模板--查询
    :return:
    """
    try:
        reqBody = json.loads(request.body)
    except Exception as err:
        return Response({"result": 19004001, "msg": getErrMsgByCode(19004001, err)}, content_type="application/json")

    if reqbody_verify(reqBody, err_code=19004001) is None:
        pass
    else:
        return reqbody_verify(reqBody, err_code=19004001)

    resData = []
    try:
        hazardsInfoObjs = infoTempDB.objects.all()
        for item in hazardsInfoObjs:
            infoObj = {}

            infoObj["id"] = item.id
            infoObj["user"] = item.user
            infoObj["name"] = item.name
            infoObj["content"] = item.content
            infoObj["type"] = item.type
            infoObj["time"] = item.time

            resData.append(infoObj)
    except Exception as err:
        return Response({"result": 19004006, "msg": getErrMsgByCode(19004006, err)}, content_type="application/json")

    return Response({"result": 0, "msg": "OK", "data": resData}, content_type="application/json")


@csrf_exempt
@api_view(["post"])
def deleteTemplateInfo(request):
    """
    SMS短信模板--删除
    """
    try:
        reqBody = json.loads(request.body)
    except Exception as err:
        return Response({"result": 19005001, "msg": getErrMsgByCode(19005001, err)}, content_type="application/json")

    if reqbody_verify_admin(reqBody, err_code=19005001) is None:
        pass
    else:
        return reqbody_verify_admin(reqBody, err_code=19005001)

    if "id" not in reqBody:
        return Response({"result": 19005006, "msg": getErrMsgByCode(19005006, None)}, content_type="application/json")
    else:
        infoID = reqBody["id"]

    try:
        infoObj = infoTempDB.objects.get(id=infoID)
    except Exception as err:
        return Response({"result": 19005007, "msg": getErrMsgByCode(19005007, err)}, content_type="application/json")

    try:
        infoObj.delete()
    except Exception as err:
        return Response({"result": 19005008, "msg": getErrMsgByCode(19005008, err)}, content_type="application/json")

    return Response({"result": 0, "msg": "OK"}, content_type="application/json")


@csrf_exempt
@api_view(["post"])
def querySMSLogInfo(request):
    """
    SMS信息记录--查询
    """
    try:
        reqBody = json.loads(request.body)
    except Exception as err:
        return Response({"result": 19006001, "msg": getErrMsgByCode(19006001, err)}, content_type="application/json")

    if reqbody_verify(reqBody, err_code=19006001) is None:
        pass
    else:
        return reqbody_verify(reqBody, err_code=19006001)

    deptID = None

    if "dept" in reqBody:
        deptID = reqBody["dept"]

    if "user_id_list" in reqBody:
        userIDList = reqBody["user_id_list"]
    else:
        userIDList = getAllDeptMemberList(deptID)

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
            smsLogObjs = smsLogDB.objects.filter(user_id__in=userIDList, time__gt=afterTime, time__lt=beforeTime)
        else:
            smsLogObjs = smsLogDB.objects.filter(user_id__in=userIDList)

        if orderInfo == 1:
            smsLogObjs = smsLogObjs.order_by("-time")
        else:
            smsLogObjs = smsLogObjs.order_by("time")

        if indexPage and countInfo:
            indexStart = (indexPage - 1) * countInfo

            if indexStart < 0:
                indexStart = 0

            indexEnd = indexStart + countInfo

            if indexEnd >= smsLogObjs.count():
                indexEnd = smsLogObjs.count()

            resultObjList = smsLogObjs[indexStart:indexEnd]
        else:
            resultObjList = smsLogObjs

        resultInfoList = []

        print(format(resultObjList))
        for obj in resultObjList:
            smsInfo = {}

            smsInfo["id"] = obj.id
            smsInfo["user_id"] = obj.user_id
            smsInfo["name"] = obj.name
            smsInfo["phone"] = obj.phone
            smsInfo["content"] = obj.content
            smsInfo["type"] = obj.type
            smsInfo["time"] = obj.time

            resultInfoList.append(smsInfo)

        resData["total"] = smsLogObjs.count()
        resData["info"] = resultInfoList
    except Exception as err:
        return Response({"result": 19006006, "msg": getErrMsgByCode(19006006, err)}, content_type="application/json")

    return Response({"result": 0, "msg": "OK", "data": resData}, content_type="application/json")

