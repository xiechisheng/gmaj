import json
from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.views.decorators.csrf import csrf_exempt

from django.db.models import Q
from django.db import transaction
from api.models import user_info as userDB
from api.models import rtsp_info as rtspDeviceDB
from api.models import iot_device as iotDeviceDB
from api.models import dept as deptDB
from api.public import tokenDecode
from api.public import reqbody_verify
from api.public import reqbody_verify_admin
from api.models import operation_log as OperationLogDB

from api.ErrorCode import getErrMsgByCode

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


def getSubDeptList(deptID):
    """
    子部门成员ID列表--获取
    :return:
    """
    dept_contain = "/" + str(deptID) + "/"
    dept_end = "/" + str(deptID)

    subdept_list = deptDB.objects.filter(Q(path__contains=dept_contain) | Q(path__endswith=dept_end))

    if subdept_list.count() == 0:
        return None
    else:
        subdept_idlist = []

        for st in subdept_list:
            subdept_idlist.append(st.id)

        return subdept_idlist


def getDeptMemeberLoginList(deptID):
    """
    部门成员ID列表--获取
    :return:
    """
    memberList = userDB.objects.filter(dept=deptID)

    if memberList.count() == 0:
        return None
    else:
        deptMemberLogin = []

        for obj in memberList:
            deptMemberLogin.append(obj.login)

        return deptMemberLogin


def getAllDeptMemberLoginList(deptID):
    """
    部门全部成员ID列表--获取
    :return:
    """
    subDeptList = getSubDeptList(deptID)
    memberLoginList = []

    if subDeptList:
        subDeptList.insert(0, deptID)
    else:
        memberList = getDeptMemeberLoginList(deptID)

        for member in memberList:
            memberLoginList.append(member)

        return memberLoginList

    for deptID in subDeptList:
        memberList = getDeptMemeberLoginList(deptID)

        if memberList is None:
            continue

        for member in memberList:
            memberLoginList.append(member)

    return memberLoginList


def getDeptMemeberList(deptID):
    """
    部门成员ID列表--获取
    :return:
    """
    memberList = userDB.objects.filter(dept=deptID)

    if memberList.count() == 0:
        return None
    else:
        deptMemberIDs = []

        for obj in memberList:
            deptMemberIDs.append(obj.id)

        return deptMemberIDs


def getAllDeptMemberList(deptID):
    """
    部门全部成员ID列表--获取
    :return:
    """
    subDeptList = getSubDeptList(deptID)
    memberIDList = []

    if subDeptList:
        subDeptList.insert(0, deptID)
    else:
        memberList = getDeptMemeberList(deptID)

        for member in memberList:
            memberIDList.append(member)

        return memberIDList

    for deptID in subDeptList:
        memberList = getDeptMemeberList(deptID)

        if memberList is None:
            continue

        for member in memberList:
            memberIDList.append(member)

    return memberIDList


def getSubDeptTreeList(deptID, deptInfoList):
    """
    子部门信息树列表--获取
    :return:
    """
    subInfo = deptDB.objects.filter(pid=deptID).order_by("position")

    if subInfo.exists():
        for itemSub in subInfo:
            deptInfo = {}

            deptInfo["id"] = itemSub.id
            deptInfo["name"] = itemSub.name
            deptInfo["pid"] = itemSub.pid
            deptInfo["path"] = itemSub.path

            deptInfo["enable"] = itemSub.enable
            deptInfo["register"] = itemSub.register
            deptInfo["children"] = []

            getSubDeptTreeList(deptInfo["id"], deptInfo["children"])

            deptInfoList.append(deptInfo)


def getSubDeptTreeListMy(deptID, deptInfoList):
    """
    子部门信息树列表--获取
    :return:
    """
    subInfo = deptDB.objects.filter(pid=deptID).order_by("position")

    if subInfo.exists():
        for itemSub in subInfo:
            deptInfo = {}

            deptInfo["id"] = itemSub.id
            deptInfo["name"] = itemSub.name
            deptInfo["pid"] = itemSub.pid
            deptInfo["path"] = itemSub.path
            deptInfo["value"] = itemSub.id
            deptInfo["label"] = itemSub.name


            deptInfo["children"] = []

            getSubDeptTreeListMy(deptInfo["id"], deptInfo["children"])

            deptInfoList.append(deptInfo)


@csrf_exempt
@api_view(["post"])
def addDeptInfo(request):
    """
        部门信息--新增
        :return:
        """
    try:
        reqBody = json.loads(request.body)
    except Exception as err:
        return Response({"result": 11001001, "msg": getErrMsgByCode(11001001, err)}, content_type="application/json")

    if reqbody_verify_admin(reqBody, err_code=11001001) is None:
        pass
    else:
        return reqbody_verify_admin(reqBody, err_code=11001001)

    tokenInfo = tokenDecode(reqBody["token"])

    if "name" not in reqBody:
        return Response({"result": 11001006, "msg": getErrMsgByCode(11001006, None)}, content_type="application/json")
    else:
        deptName = reqBody["name"]

    if "pid" not in reqBody:
        return Response({"result": 11001007, "msg": getErrMsgByCode(11001007, None)}, content_type="application/json")
    else:
        deptPID = reqBody["pid"]

    if "enable" not in reqBody:
        return Response({"result": 11001008, "msg": getErrMsgByCode(11001008, None)}, content_type="application/json")
    else:
        deptEnable = reqBody["enable"]

    if "position" not in reqBody:
        deptPosition = 32767
    else:
        deptPosition = reqBody["position"]

    try:
        pDeptObj = deptDB.objects.get(id=deptPID)

        if pDeptObj.path == "/":
            deptPath = pDeptObj.path + str(deptPID)
        else:
            deptPath = pDeptObj.path + "/" + str(deptPID)
    except deptDB.DoesNotExist:
        return Response({"result": 11001009, "msg": getErrMsgByCode(11001009, None)}, content_type="application/json")

    try:
        deptInfo = deptDB(name=deptName, pid=deptPID, enable=deptEnable, path=deptPath, position=deptPosition)
        deptInfo.save()
    except Exception as err:
        return Response({"result": 11001010, "msg": getErrMsgByCode(11001010, err)}, content_type="application/json")

    addOperationLog(tokenInfo["login"], "新增部门信息", "新增部门信息成功", "新增部门信息成功")
    return Response({"result": 0, "msg": "OK"}, content_type="application/json")


@csrf_exempt
@api_view(["post"])
def modifyDeptInfo(request):
    """
    部门信息--修改
    :return:
    """
    try:
        reqBody = json.loads(request.body)
    except Exception as err:
        return Response({"result": 11002001, "msg": getErrMsgByCode(11002001, err)}, content_type="application/json")

    if reqbody_verify_admin(reqBody, err_code=11002001) is None:
        pass
    else:
        return reqbody_verify_admin(reqBody, err_code=11002001)

    tokenInfo = tokenDecode(reqBody["token"])

    if "id" not in reqBody:
        return Response({"result": 11002006, "msg": getErrMsgByCode(11002006, None)}, content_type="application/json")
    else:
        deptID = reqBody["id"]

    deptName = None
    deptPID = None
    deptEnable = None

    if "name" in reqBody:
        deptName = reqBody["name"]

    if "pid" in reqBody:
        deptPID = reqBody["pid"]

    if "enable" in reqBody:
        deptEnable = reqBody["enable"]

    deptPath = None

    if deptPID is not None:
        try:
            pDeptObj = deptDB.objects.get(id=deptPID)

            if pDeptObj.path == "/":
                deptPath = pDeptObj.path + str(deptPID)
            else:
                deptPath = pDeptObj.path + "/" + str(deptPID)
        except deptDB.DoesNotExist:
            return Response({"result": 11002007, "msg": getErrMsgByCode(11002007, None)}, content_type="application/json")

    try:
        deptObj = deptDB.objects.get(id=deptID)

        if deptName is not None:
            deptObj.name = deptName

        if deptPID is not None:
            deptObj.pid = deptPID

        if deptEnable is not None:
            deptObj.enable = deptEnable

        if deptPath is not None:
            deptObj.path = deptPath

        deptObj.save()
    except Exception as err:
        return Response({"result": 11002008, "msg": getErrMsgByCode(11002008, err)}, content_type="application/json")

    addOperationLog(tokenInfo["login"], "修改部门信息", "修改部门信息成功", "修改部门信息成功")
    return Response({"result": 0, "msg": "OK"}, content_type="application/json")



@csrf_exempt
@api_view(["post"])
def queryDeptInfo(request):
    """
    部门信息--查询
    :return:
    """
    try:
        reqBody = json.loads(request.body)
    except Exception as err:
        return Response({"result": 11003001, "msg": getErrMsgByCode(11003001, err)}, content_type="application/json")

    if reqbody_verify(reqBody, err_code=11003001) is None:
        pass
    else:
        return reqbody_verify(reqBody, err_code=11003001)

    resData = {}

    tokenInfo = tokenDecode(reqBody["token"])
    deptID = tokenInfo["dept"]

    try:
        deptInfo = deptDB.objects.get(id=deptID)

        resData["id"] = deptInfo.id
        resData["name"] = deptInfo.name
        resData["pid"] = deptInfo.pid
        resData["path"] = deptInfo.path
        resData["enable"] = deptInfo.enable
        resData["register"] = deptInfo.register

        subDeptList = []
        getSubDeptTreeList(deptID, subDeptList)

        resData["children"] = subDeptList
    except Exception as err:
        return Response({"result": 11003005, "msg": getErrMsgByCode(11003005, err)}, content_type="application/json")

    addOperationLog(tokenInfo["login"], "查询部门信息", "查询部门信息成功", "查询部门信息成功")
    return Response({"result": 0, "msg": "OK", "data": resData}, content_type="application/json")


@csrf_exempt
@api_view(["post"])
def queryDeptMember(request):
    """
    部门成员信息--查询
    :return:
    """
    try:
        reqBody = json.loads(request.body)
    except Exception as err:
        return Response({"result": 11005001, "msg": getErrMsgByCode(11005001, err)}, content_type="application/json")

    if reqbody_verify(reqBody, err_code=11005001) is None:
        pass
    else:
        return reqbody_verify(reqBody, err_code=11005001)

    tokenInfo = tokenDecode(reqBody["token"])
    if "id" not in reqBody:
        return Response({"result": 11005005, "msg": getErrMsgByCode(11005005, None)}, content_type="application/json")
    else:
        deptID = reqBody["id"]

    resData = []

    try:
        memberInfoList = userDB.objects.filter(dept=deptID).order_by("position")

        if memberInfoList:
            for obj in memberInfoList:
                userObj = {}

                userObj["id"] = obj.id
                userObj["login"] = obj.login
                userObj["nickname"] = obj.nickname
                userObj["dept"] = obj.dept
                userObj["email"] = obj.email
                userObj["enable"] = obj.enable
                userObj["height"] = obj.height
                userObj["latitude"] = obj.latitude

                userObj["level"] = obj.level
                userObj["locate"] = obj.locate
                userObj["longitude"] = obj.longitude
                userObj["mobile"] = obj.mobile
                userObj["phone"] = obj.phone
                userObj["position"] = obj.position
                userObj["role"] = obj.role
                userObj["register"] = obj.register

                resData.append(userObj)
    except Exception as err:
        return Response({"result": 11005006, "msg": getErrMsgByCode(11005006, None)}, content_type="application/json")

    addOperationLog(tokenInfo["login"], "查询部门成员信息", "查询部门成员信息成功", "查询部门成员信息成功")
    return Response({"result": 0, "msg": "OK", "data": resData}, content_type="application/json")



@csrf_exempt
@api_view(["post"])
def deleteDeptInfo(request):
    """
    部门信息--删除
    :return:
    """
    try:
        reqBody = json.loads(request.body)
    except Exception as err:
        return Response({"result": 11004001, "msg": getErrMsgByCode(11004001, err)}, content_type="application/json")

    if reqbody_verify_admin(reqBody, err_code=11004001) is None:
        pass
    else:
        return reqbody_verify_admin(reqBody, err_code=11004001)

    tokenInfo = tokenDecode(reqBody["token"])

    if "id" not in reqBody:
        return Response({"result": 11004006, "msg": getErrMsgByCode(11004006, None)}, content_type="application/json")
    else:
        deptID = reqBody["id"]

    subDeptIDs = getSubDeptList(deptID)

    if subDeptIDs is None:
        pass
    else:
        return Response({"result": 11004007, "msg": getErrMsgByCode(11004007, None)}, content_type="application/json")

    deptMemberIDs = getDeptMemeberList(deptID)

    if deptMemberIDs is None:
        pass
    else:
        return Response({"result": 11004008, "msg": getErrMsgByCode(11004008, None)}, content_type="application/json")

    try:
        deptObj = deptDB.objects.get(id=deptID)
        deptObj.delete()
    except Exception as err:
        return Response({"result": 11004009, "msg": getErrMsgByCode(11004009, err)}, content_type="application/json")

    addOperationLog(tokenInfo["login"], "删除部门信息", "删除部门信息成功", "删除部门信息成功")
    return Response({"result": 0, "msg": "OK"}, content_type="application/json")



@csrf_exempt
@api_view(["post"])
def subDeptInfoSort(request):
    """
    子部门信息--排序
    :return:
    """
    try:
        reqBody = json.loads(request.body)
    except Exception as err:
        return Response({"result": 11006001, "msg": getErrMsgByCode(11006001, err)}, content_type="application/json")

    if reqbody_verify_admin(reqBody, err_code=11006001) is None:
        pass
    else:
        return reqbody_verify_admin(reqBody, err_code=11006001)

    if "id" not in reqBody:
        return Response({"result": 11006006, "msg": getErrMsgByCode(11006006, None)}, content_type="application/json")
    else:
        deptID = reqBody["id"]

    if "sub" not in reqBody:
        return Response({"result": 11006007, "msg": getErrMsgByCode(11006007, None)}, content_type="application/json")
    else:
        subDeptList = reqBody["sub"]

    savePoint = transaction.savepoint()

    try:
        i = 1

        for subDept in subDeptList:
            deptDB.objects.filter(id=subDept, pid=deptID).update(position=i)
            i += 1
    except Exception as err:
        transaction.savepoint_rollback(savePoint)
        return Response({"result": 11006008, "msg": getErrMsgByCode(11006008, err)}, content_type="application/json")

    transaction.savepoint_commit(savePoint)

    return Response({"result": 0, "msg": "OK"}, content_type="application/json")


@csrf_exempt
@api_view(["post"])
def memberInfoSort(request):
    """
    部门成员信息--排序
    :return:
    """
    try:
        reqBody = json.loads(request.body)
    except Exception as err:
        return Response({"result": 11007001, "msg": getErrMsgByCode(11007001, err)}, content_type="application/json")

    if reqbody_verify_admin(reqBody, err_code=11007001) is None:
        pass
    else:
        return reqbody_verify_admin(reqBody, err_code=11007001)

    if "id" not in reqBody:
        return Response({"result": 11007006, "msg": getErrMsgByCode(11007006, None)}, content_type="application/json")
    else:
        deptID = reqBody["id"]

    if "member" not in reqBody:
        return Response({"result": 11007007, "msg": getErrMsgByCode(11007007, None)}, content_type="application/json")
    else:
        memberList = reqBody["member"]

    savePoint = transaction.savepoint()

    try:
        i = 1

        for member in memberList:
            userDB.objects.filter(id=member, dept=deptID).update(position=i)
            i += 1
    except Exception as err:
        transaction.savepoint_rollback(savePoint)
        return Response({"result": 11007008, "msg": getErrMsgByCode(11007008, err)}, content_type="application/json")

    transaction.savepoint_commit(savePoint)

    return Response({"result": 0, "msg": "OK"}, content_type="application/json")


@csrf_exempt
@api_view(["post"])
def queryDeptDevice(request):
    """
    部门设备信息--查询
    :return:
    """
    try:
        reqBody = json.loads(request.body)
    except Exception as err:
        return Response({"result": 11008001, "msg": getErrMsgByCode(11008001, err)}, content_type="application/json")

    if reqbody_verify(reqBody, err_code=11008001) is None:
        pass
    else:
        return reqbody_verify(reqBody, err_code=11008001)

    tokenInfo = tokenDecode(reqBody["token"])

    if "id" not in reqBody:
        return Response({"result": 11008006, "msg": getErrMsgByCode(11008006, None)}, content_type="application/json")
    else:
        deptID = reqBody["id"]

    deptList = getSubDeptList(deptID)
    if deptList:
        deptList.insert(0, deptID)
    else:
        deptList = [].append(deptID)

    resData = {}
    try:
        ipcObjList = rtspDeviceDB.objects.filter(dept__in=deptList).order_by("position")
        iotObjList = iotDeviceDB.objects.filter(dept__in=deptList)

        if ipcObjList:
            ipcInfoList = []
            for ipcObj in ipcObjList:
                ipcInfo = {}
                ipcInfo["id"] = ipcObj.id
                ipcInfo["name"] = ipcObj.name
                ipcInfo["dept"] = ipcObj.dept
                ipcInfo["type"] = ipcObj.type
                ipcInfo["server"] = ipcObj.server
                ipcInfo["channel"] = ipcObj.channel
                ipcInfo["longitude"] = ipcObj.longitude
                ipcInfo["latitude"] = ipcObj.latitude
                ipcInfo["height"] = ipcObj.height
                ipcInfo["locate"] = ipcObj.locate
                ipcInfo["enable"] = ipcObj.enable

                ipcInfoList.append(ipcInfo)

            resData["ipc"] = ipcInfoList

        if iotObjList:
            iotInfoList = []
            for iotObj in iotObjList:
                iotInfo = {}
                iotInfo["id"] = iotObj.id
                iotInfo["name"] = iotObj.name
                iotInfo["dept"] = iotObj.dept
                iotInfo["code"] = iotObj.code
                iotInfo["type"] = iotObj.type
                iotInfo["type_name"] = iotObj.type_name
                iotInfo["ipc"] = iotObj.ipc
                iotInfo["generic_plan"] = iotObj.generic_plan
                iotInfo["sms_level_1"] = iotObj.sms_level_1
                iotInfo["sms_level_2"] = iotObj.sms_level_2
                iotInfo["longitude"] = iotObj.longitude
                iotInfo["latitude"] = iotObj.latitude
                iotInfo["height"] = iotObj.height
                iotInfo["locate"] = iotObj.locate
                iotInfo["enable"] = iotObj.enable

                iotInfoList.append(iotInfo)

            resData["iot"] = iotInfoList
    except Exception as err:
        return Response({"result": 11008007, "msg": getErrMsgByCode(11008007, err)}, content_type="application/json")

    addOperationLog(tokenInfo["login"], "查询部门设备信息", "查询部门设备信息成功", "查询部门设备信息成功")
    return Response({"result": 0, "msg": "OK", "data": resData}, content_type="application/json")


def tree(data, root, root_field, node_field):
    """
    解析list数据为树结构
    :param data:  被解析的数据
    :param root: 根节点值
    :param root_field: 根节点字段
    :param node_field: 节点字段
    :return: list
    """
    l = []
    for i in data:
        if i.get(root_field) == root:

            l.append(i)
    for i in data:
        node = i.get(node_field)
        children = []
        for j in data:
            parent = j.get(root_field)
            if node == parent:
                children.append(j)
        i['children'] = children
    return l


# @csrf_exempt
# @api_view(["post"])
# def getDeptIotDevice(request):
#     """
#     获取部门树状IOT设备
#     """
#     try:
#         reqBody = json.loads(request.body)
#     except Exception as err:
#         return Response({"result": 11008001, "msg": getErrMsgByCode(11008001, err)}, content_type="application/json")
#     try:
#         deptData=[]
#         deptInfo=deptDB.objects.all().order_by("position")
#         # iotInfo=iotDeviceDB.objects.all()
#         for dept in deptInfo:
#             valueObj = {}
#             deviceObjlist=[]
#             # for item in iotInfo:
#             #     if int(dept.id)==int(item.dept):
#             #         deviceObj = {}
#             #         deviceObj["iot_id"] = item.id
#             #         deviceObj["iot_name"] = item.name
#             #         deviceObj["dept"] = item.dept
#             #         deviceObj["code"] = item.code
#             #         deviceObj["device_type"] = item.device_type
#             #         deviceObj["gateway_server_id"] = item.gateway_server_id
#             #         deviceObj["gateway_server"] = item.gateway_server
#             #         deviceObj["iot_device_code"] = item.iot_device_code
#             #         deviceObj["flag"] = item.flag
#             #         deviceObj["ipc"] = item.ipc
#             #         deviceObj["generic_plan"] = item.generic_plan
#             #         deviceObj["sms_level_1"] = item.sms_level_1
#             #         deviceObj["sms_level_2"] = item.sms_level_2
#             #         deviceObj["longitude"] = item.longitude
#             #         deviceObj["latitude"] = item.latitude
#             #         deviceObj["height"] = item.height
#             #         deviceObj["iot_address"] = item.iot_address
#             #         deviceObj["enable"] = item.enable
#             #         deviceObj["device_type_name"] = item.device_type_name
#             #         deviceObj["device_brand_name"] = item.device_brand_name
#             #         deviceObj["label"]=item.name
#             #         deviceObj["valie"]=item.id
#             #         deviceObjlist.append(deviceObj)
#             valueObj["id"]=dept.id
#             valueObj["name"]=dept.name
#             valueObj["pid"]=dept.pid
#             valueObj["label"]=dept.name
#             valueObj["value"] = dept.id
#             valueObj["path"]=dept.path
#             # valueObj["iot"]=deviceObjlist
#             deptData.append(valueObj)
#
#         resultData=tree(deptData,0,"pid","id")
#
#     except Exception as err:
#         return Response({"result": 11008008, "msg": getErrMsgByCode(11008008, err)}, content_type="application/json")
#
#     return Response({"result": 0, "msg": "OK", "data": resultData}, content_type="application/json")

@csrf_exempt
@api_view(["post"])
def queryDeptMemberInfo(request):
    """
    部门成员信息--查询
    :return:
    """
    try:
        reqBody = json.loads(request.body)
    except Exception as err:
        return Response({"result": 11005001, "msg": getErrMsgByCode(11005001, err)}, content_type="application/json")

    if reqbody_verify(reqBody, err_code=11005001) is None:
        pass
    else:
        return reqbody_verify(reqBody, err_code=11005001)

    tokenInfo = tokenDecode(reqBody["token"])
    if "id" not in reqBody:
        return Response({"result": 11005005, "msg": getErrMsgByCode(11005005, None)}, content_type="application/json")
    else:
        deptID = reqBody["id"]

    resData = []

    try:
        if int(deptID) ==1:
            memberInfoList = userDB.objects.all().order_by("position")
        else:
            memberInfoList = userDB.objects.filter(dept=deptID).order_by("position")

        if memberInfoList:
            for obj in memberInfoList:
                userObj = {}

                userObj["id"] = obj.id
                userObj["login"] = obj.login
                userObj["nickname"] = obj.nickname
                userObj["dept"] = obj.dept
                userObj["email"] = obj.email
                userObj["enable"] = obj.enable
                userObj["height"] = obj.height
                userObj["latitude"] = obj.latitude

                userObj["level"] = obj.level
                userObj["locate"] = obj.locate
                userObj["longitude"] = obj.longitude
                userObj["mobile"] = obj.mobile
                userObj["phone"] = obj.phone
                userObj["position"] = obj.position
                userObj["role"] = obj.role
                userObj["register"] = obj.register

                resData.append(userObj)
    except Exception as err:
        return Response({"result": 11005006, "msg": getErrMsgByCode(11005006, None)}, content_type="application/json")

    return Response({"result": 0, "msg": "OK", "data": resData}, content_type="application/json")





@csrf_exempt
@api_view(["post"])
def getDeptIotDevice(request):
    """
    获取部门树状IOT设备
    """
    try:
        reqBody = json.loads(request.body)
    except Exception as err:
        return Response({"result": 11008001, "msg": getErrMsgByCode(11008001, err)}, content_type="application/json")

    try:
        deptID=1
        deptInfo = deptDB.objects.get(id=1)
        resdata = []
        resData={}
        resData["id"] = deptInfo.id
        resData["name"] = deptInfo.name
        resData["pid"] = deptInfo.pid
        resData["path"] = deptInfo.path
        resData["label"] = deptInfo.name
        resData["value"] = deptInfo.id

        subDeptList = []
        getSubDeptTreeListMy(deptID, subDeptList)

        resData["children"] = subDeptList
        resdata.append(resData)
    except Exception as err:
        return Response({"result": 11003005, "msg": getErrMsgByCode(11003005, err)}, content_type="application/json")

    return Response({"result": 0, "msg": "OK", "data": resdata}, content_type="application/json")