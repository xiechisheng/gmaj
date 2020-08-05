import json
from api.ErrorCode import getErrMsgByCode
from api.public import reqbody_verify_admin
from api.dept import getAllDeptMemberLoginList
from rest_framework.response import Response
from rest_framework.decorators import api_view
from api.models import operation_log as OperationLogDB
from django.views.decorators.csrf import csrf_exempt

import logging as logObj
logger = logObj.getLogger("gmaj")


def addOperationLog(user, type, result, note):

    operationObj = OperationLogDB()

    operationObj.user = user
    operationObj.type = type
    operationObj.result = result
    operationObj.note = note

    try:
        operationObj.save()
    except Exception as err:
        err_msg = "操作日志记录失败失败[" + user + "->" + type + "]<" + format(err) + ">"
        logger.error(err_msg)
        return False
    return True


@csrf_exempt
@api_view(["post"])
def queryOperationInfo(request):
    """
    操作日志--查询
    """
    try:
        reqBody = json.loads(request.body)
    except Exception as err:
        return Response({"result": 23002001, "msg": getErrMsgByCode(23002001, err)}, content_type="application/json")

    if reqbody_verify_admin(reqBody, err_code=23002001) is None:
        pass
    else:
        return reqbody_verify_admin(reqBody, err_code=23002001)

    deptID = None

    if "dept" in reqBody:
        deptID = reqBody["dept"]

    if "user_login_list" in reqBody:
        userLoginList = reqBody["user_login_list"]
    else:
        userLoginList = getAllDeptMemberLoginList(deptID)

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
            imLogObjs = OperationLogDB.objects.filter(user__in=userLoginList, time__gt=afterTime, time__lt=beforeTime)
        else:
            imLogObjs = OperationLogDB.objects.filter(user__in=userLoginList)

        if orderInfo == 1:
            imLogObjs = imLogObjs.order_by("-time")
        else:
            imLogObjs = imLogObjs.order_by("time")

        if indexPage and countInfo:
            indexStart = (indexPage - 1) * countInfo

            if indexStart < 0:
                indexStart = 0

            indexEnd = indexStart + countInfo

            if indexEnd >= imLogObjs.count():
                indexEnd = imLogObjs.count()

            resultObjList = imLogObjs[indexStart:indexEnd]
        else:
            resultObjList = imLogObjs

        resultInfoList = []

        for obj in resultObjList:
            imInfo = {}

            imInfo["id"] = obj.id
            imInfo["user"] = obj.user
            imInfo["type"] = obj.type
            imInfo["result"] = obj.result

            imInfo["note"] = obj.note
            imInfo["time"] = obj.time

            resultInfoList.append(imInfo)

        resData["total"] = imLogObjs.count()
        resData["info"] = resultInfoList
    except Exception as err:
        return Response({"result": 23002006, "msg": getErrMsgByCode(23002006, err)}, content_type="application/json")

    return Response({"result": 0, "msg": "OK", "data": resData}, content_type="application/json")


