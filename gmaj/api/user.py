import json
import datetime
from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.views.decorators.csrf import csrf_exempt


from api.ErrorCode import getErrMsgByCode
from api.public import tokenQuery
from django.db import transaction
from api.public import tokenEncode
from api.public import tokenDecode
from api.public import tokenDelete
from api.models import user_info as userDB
from api.public import mysql_password
from api.public import reqbody_verify
from api.public import reqbody_verify_admin
from api.operation import addOperationLog


@csrf_exempt
@api_view(["post"])
def userLogin(request):
    """
    用户信息--登录
    enable: 0禁用, 1可用
    :return:
    """
    try:
        reqBody = json.loads(request.body)
    except Exception as err:
        return Response({"result": 10000001, "msg": getErrMsgByCode(10000001, err)}, content_type="application/json")

    if "login" not in reqBody:
        return Response({"result": 10000002, "msg": getErrMsgByCode(10000002, None)}, content_type="application/json")
    else:
        loginName = reqBody["login"]

    if "password" not in reqBody:
        return Response({"result": 10000003, "msg": getErrMsgByCode(10000003, None)}, content_type="application/json")
    else:
        loginPwd = reqBody["password"]

    if "role" not in reqBody:
        return Response({"result": 10000004, "msg": getErrMsgByCode(10000004, None)}, content_type="application/json")
    else:
        loginRole = reqBody["role"]

    try:
        userObj = userDB.objects.get(login=loginName)
    except userDB.DoesNotExist:
        return Response({"result": 10000005, "msg": getErrMsgByCode(10000005, None)}, content_type="application/json")

    if userObj.password != mysql_password(loginPwd):
        return Response({"result": 10000006, "msg": getErrMsgByCode(10000006, None)}, content_type="application/json")

    if userObj.enable == 0:
        return Response({"result": 10000007, "msg": getErrMsgByCode(10000007, None)}, content_type="application/json")

    if userObj.role != loginRole:
        return Response({"result": 10000008, "msg": getErrMsgByCode(10000008, None)}, content_type="application/json")

    strTime = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    tokenValue = tokenEncode({"id": userObj.id, "login": userObj.login, "role": userObj.role, "dept": userObj.dept, "time": strTime})

    if tokenValue is None:
        return Response({"result": 10000009, "msg": getErrMsgByCode(10000009, None)}, content_type="application/json")

    resData = {}

    resData["id"] = userObj.id
    resData["login"] = userObj.login
    resData["nickname"] = userObj.nickname
    resData["dept"] = userObj.dept
    resData["email"] = userObj.email
    resData["enable"] = userObj.enable
    resData["height"] = userObj.height
    resData["latitude"] = userObj.latitude

    resData["level"] = userObj.level
    resData["locate"] = userObj.locate
    resData["longitude"] = userObj.longitude
    resData["mobile"] = userObj.mobile
    resData["phone"] = userObj.phone
    resData["position"] = userObj.position
    resData["register"] = userObj.register
    resData["role"] = userObj.role

    resData["token"] = tokenValue

    addOperationLog(userObj.login, "用户登陆", "登陆成功", "登陆成功")
    return Response({"result": 0, "msg": "OK", "data": resData}, content_type="application/json")



@csrf_exempt
@api_view(["post"])
def userLogout(request):
    """
    用户信息--登出
    :return:
    """
    try:
        reqBody = json.loads(request.body)
    except Exception as err:
        return Response({"result": 10001001, "msg": getErrMsgByCode(10001001, err)}, content_type="application/json")

    if "login" not in reqBody:
        return Response({"result": 10001002, "msg": getErrMsgByCode(10001002, None)}, content_type="application/json")
    else:
        loginName = reqBody["login"]

    if "token" not in reqBody:
        return Response({"result": 10001003, "msg": getErrMsgByCode(10002002, None)}, content_type="application/json")
    else:
        loginToken = reqBody["token"]

    tokenInfo = tokenDecode(loginToken)

    if tokenInfo is None:
        return Response({"result": 10001004, "msg": getErrMsgByCode(10001004, None)}, content_type="application/json")

    tokenCache = tokenQuery(loginName)

    if tokenCache != loginToken:
        return Response({"result": 10001005, "msg": getErrMsgByCode(10001005, None)}, content_type="application/json")

    if tokenDelete(loginName) is False:
        return Response({"result": 10001006, "msg": getErrMsgByCode(10001006, None)}, content_type="application/json")

    addOperationLog(reqBody["login"], "用户登出", "登出成功", "登出成功")
    return Response({"result": 0, "msg": "OK"}, content_type="application/json")


@csrf_exempt
@api_view(["post"])
def userInfoAdd(request):
    """
    用户信息--新增
    :return:
    """
    try:
        reqBody = json.loads(request.body)
    except Exception as err:
        return Response({"result": 10002001, "msg": getErrMsgByCode(10002001, err)}, content_type="application/json")

    if reqbody_verify_admin(reqBody, err_code=10002001) is None:
        pass
    else:
        return reqbody_verify_admin(reqBody, err_code=10002001)

    if "login" not in reqBody:
        return Response({"result": 10002006, "msg": getErrMsgByCode(10002006, None)}, content_type="application/json")
    else:
        userLogin = reqBody["login"]

    if userDB.objects.filter(login=userLogin):
        return Response({"result": 10002007, "msg": getErrMsgByCode(10002007, None)}, content_type="application/json")

    if "password" not in reqBody:
        return Response({"result": 10002008, "msg": getErrMsgByCode(10002008, None)}, content_type="application/json")
    else:
        userPwd = reqBody["password"]

    if "nickname" not in reqBody:
        return Response({"result": 10002009, "msg": getErrMsgByCode(10002009, None)}, content_type="application/json")
    else:
        userName = reqBody["nickname"]

    if "dept" not in reqBody:
        return Response({"result": 10002010, "msg": getErrMsgByCode(10002010, None)}, content_type="application/json")
    else:
        userDept = reqBody["dept"]

    if "enable" not in reqBody:
        return Response({"result": 10002012, "msg": getErrMsgByCode(10002012, None)}, content_type="application/json")
    else:
        userEnable = reqBody["enable"]

    if "role" not in reqBody:
        return Response({"result": 10002013, "msg": getErrMsgByCode(10002013, None)}, content_type="application/json")
    else:
        userRole = reqBody["role"]

    userLat = None
    userLon = None
    userHeight = None
    userLocal = None

    if userRole < 10:
        if "latitude" not in reqBody:
            userLat = 0.0
        else:
            userLat = reqBody["latitude"]

        if "longitude" not in reqBody:
            userLon = 0.0
        else:
            userLon = reqBody["longitude"]

        if "height" not in reqBody:
            userHeight = 0.0
        else:
            userHeight = reqBody["height"]

        if "locate" not in reqBody:
            userLocal = ""
        else:
            userLocal = reqBody["locate"]

    userObj = userDB()

    userObj.login = userLogin
    userObj.password = mysql_password(userPwd)
    userObj.nickname = userName
    userObj.dept = userDept

    userObj.enable = userEnable
    userObj.role = userRole

    if userRole < 10:
        userObj.latitude = userLat
        userObj.longitude = userLon
        userObj.height = userHeight
        userObj.locate = userLocal

    if "email" in reqBody:
        userObj.email = reqBody["email"]

    if "mobile" in reqBody:
        userObj.mobile = reqBody["mobile"]

    if "phone" in reqBody:
        userObj.phone = reqBody["phone"]

    if "level" in reqBody:
        userObj.level = reqBody["level"]

    savePoint = transaction.savepoint()

    try:
        userObj.save()
    except Exception as err:
        transaction.savepoint_rollback(savePoint)
        Response({"result": 10002019, "msg": getErrMsgByCode(10002019, None)}, content_type="application/json")

    transaction.savepoint_commit(savePoint)

    addOperationLog(reqBody["login"], "添加用户", "用户添加成功", "用户添加成功")
    return Response({"result": 0, "msg": "OK"}, content_type="application/json")



@csrf_exempt
@api_view(["post"])
def userInfoModify(request):
    """
    用户信息--修改
    :return:
    """
    try:
        reqBody = json.loads(request.body)
    except Exception as err:
        return Response({"result": 10003001, "msg": getErrMsgByCode(10003001, err)}, content_type="application/json")

    if reqbody_verify(reqBody, err_code=10003001) is None:
        pass
    else:
        return reqbody_verify(reqBody, err_code=10003001)

    tokenInfo = tokenDecode(reqBody["token"])

    if "id" not in reqBody:
        return Response({"result": 10003005, "msg": getErrMsgByCode(10003005, None)}, content_type="application/json")
    else:
        userID = reqBody["id"]

    if (tokenInfo["role"] < 10) and (tokenInfo["id"] != reqBody["id"]):
        return Response({"result": 10003006, "msg": getErrMsgByCode(10003006, None)}, content_type="application/json")

    if userDB.objects.filter(id=userID).count() == 0:
        return Response({"result": 10003007, "msg": getErrMsgByCode(10003007, None)}, content_type="application/json")

    userPwd = None
    userName = None
    userDept = None
    userEmail = None
    userEnable = None
    userHeight = None

    userLat = None
    userLevel = None
    userLocate = None
    userLon = None
    userMobile = None
    userPhone = None

    if "password" not in reqBody:
        pass
    else:
        userPwd = reqBody["password"]

    if "nickname" not in reqBody:
        pass
    else:
        userName = reqBody["nickname"]

    if "dept" not in reqBody:
        pass
    else:
        userDept = reqBody["dept"]

    if "default_group" not in reqBody:
        pass
    else:
        userGroup = reqBody["default_group"]

    if "email" not in reqBody:
        pass
    else:
        userEmail = reqBody["email"]

    if "enable" not in reqBody:
        pass
    else:
        userEnable = reqBody["enable"]

    if "height" not in reqBody:
        pass
    else:
        userHeight = reqBody["height"]

    if "latitude" not in reqBody:
        pass
    else:
        userLat = reqBody["latitude"]

    if "level" not in reqBody:
        pass
    else:
        userLevel = reqBody["level"]

    if "locate" not in reqBody:
        pass
    else:
        userLocate = reqBody["locate"]

    if "longitude" not in reqBody:
        pass
    else:
        userLon = reqBody["longitude"]

    if "mobile" not in reqBody:
        pass
    else:
        userMobile = reqBody["mobile"]

    if "phone" not in reqBody:
        pass
    else:
        userPhone = reqBody["phone"]

    userObj = userDB.objects.get(id=userID)

    if userPwd is not None:
        userObj.password = mysql_password(userPwd)

    if userName is not None:
        userObj.nickname = userName

    if userDept is not None:
        userObj.dept = userDept

    if userEmail is not None:
        userObj.email = userEmail

    if userEnable is not None:
        userObj.enable = userEnable

    if userHeight is not None:
        userObj.height = userHeight

    if userLat is not None:
        userObj.latitude = userLat

    if userLevel is not None:
        userObj.level = userLevel

    if userLocate is not None:
        userObj.locate = userLocate

    if userLon is not None:
        userObj.longitude = userLon

    if userMobile is not None:
        userObj.mobile = userMobile

    if userPhone is not None:
        userObj.phone = userPhone

    savePoint = transaction.savepoint()

    try:
        userObj.save()
    except Exception as err:
        transaction.savepoint_rollback(savePoint)
        return Response({"result": 10003008, "msg": getErrMsgByCode(10003008, err)}, content_type="application/json")

    transaction.savepoint_commit(savePoint)

    addOperationLog(userObj.login, "修改用户信息", "用户信息修改成功", "用户信息修改成功")
    return Response({"result": 0, "msg": "OK"}, content_type="application/json")


@csrf_exempt
@api_view(["post"])
def userInfoQuery(request):
    """
    用户信息--查询
    :return:
    """
    print(format(request.body))
    try:
        reqBody = json.loads(request.body)
    except Exception as err:
        return Response({"result": 10004001, "msg": getErrMsgByCode(10004001, err)}, content_type="application/json")

    if reqbody_verify(reqBody, err_code=10004001) is None:
        pass
    else:
        return reqbody_verify(reqBody, err_code=10004001)

    tokenInfo = tokenDecode(reqBody["token"])

    if "id" not in reqBody:
        userID = tokenInfo["id"]
    else:
        userID = reqBody["id"]

    if (tokenInfo["role"] < 9) and (tokenInfo["id"] != reqBody["id"]):
        return Response({"result": 10004006, "msg": getErrMsgByCode(10004006, None)}, content_type="application/json")

    try:
        userObj = userDB.objects.get(id=userID)
    except Exception as err:
        return Response({"result": 10004007, "msg": getErrMsgByCode(10004007, err)}, content_type="application/json")

    resData = {}

    resData["id"] = userObj.id
    resData["login"] = userObj.login
    resData["nickname"] = userObj.nickname
    resData["dept"] = userObj.dept
    resData["email"] = userObj.email
    resData["enable"] = userObj.enable
    resData["height"] = userObj.height
    resData["latitude"] = userObj.latitude

    resData["level"] = userObj.level
    resData["locate"] = userObj.locate
    resData["longitude"] = userObj.longitude
    resData["mobile"] = userObj.mobile
    resData["phone"] = userObj.phone
    resData["register"] = userObj.register
    resData["role"] = userObj.role
    resData["position"] = userObj.position

    addOperationLog(userObj.login, "查询用户信息", "查询用户信息成功", "查询用户信息成功")
    return Response({"result": 0, "msg": "OK", "data": resData}, content_type="application/json")


@csrf_exempt
@api_view(["post"])
def userInfoDelete(request):
    """
    用户信息--删除
    :return:
    """
    try:
        reqBody = json.loads(request.body)
    except Exception as err:
        return Response({"result": 10005001, "msg": getErrMsgByCode(10005001, err)}, content_type="application/json")

    if reqbody_verify(reqBody, err_code=10005001) is None:
        pass
    else:
        return reqbody_verify(reqBody, err_code=10005001)

    tokenInfo = tokenDecode(reqBody["token"])

    if "id" not in reqBody:
        return Response({"result": 10005005, "msg": getErrMsgByCode(10005005, None)}, content_type="application/json")
    else:
        userID = reqBody["id"]

    if (tokenInfo["role"] < 10) or (tokenInfo["id"] == userID):
        return Response({"result": 10005006, "msg": getErrMsgByCode(10005006, None)}, content_type="application/json")

    try:
        userObj = userDB.objects.get(id=userID)
    except Exception as err:
        return Response({"result": 10005007, "msg": getErrMsgByCode(10005007, err)}, content_type="application/json")

    if userObj.login == "admin":
        return Response({"result": 10005008, "msg": getErrMsgByCode(10005008, None)}, content_type="application/json")

    savePoint = transaction.savepoint()

    try:
        userObj.delete()
    except Exception as err:
        transaction.savepoint_rollback(savePoint)
        return Response({"result": 10005009, "msg": getErrMsgByCode(10005009, err)}, content_type="application/json")

    transaction.savepoint_commit(savePoint)

    addOperationLog(tokenInfo["login"], "删除用户信息", "删除用户信息成功", "删除用户信息成功")
    return Response({"result": 0, "msg": "OK"}, content_type="application/json")


@csrf_exempt
@api_view(["post"])
def userAccountRegistered(request):
    """
    用户信息--是否注册
    registered: 0未注册, 1已注册
    """
    try:
        reqBody = json.loads(request.body)
    except Exception as err:
        return Response({"result": 10006001, "msg": getErrMsgByCode(10006001, err)}, content_type="application/json")

    if reqbody_verify_admin(reqBody, err_code=10006001) is None:
        pass
    else:
        return reqbody_verify_admin(reqBody, err_code=10006001)

    if "login" not in reqBody:
        return Response({"result": 10006006, "msg": getErrMsgByCode(10006006, None)}, content_type="application/json")
    else:
        userLogin = reqBody["login"]

    resData = {}

    try:
        userObj = userDB.objects.filter(login=userLogin)

        for item in userObj:
            print(item.login)

        if userObj:
            resData["registered"] = 1
        else:
            resData["registered"] = 0
    except Exception as err:
        return Response({"result": 10006007, "msg": getErrMsgByCode(10006007, None)}, content_type="application/json")

    return Response({"result": 0, "msg": "OK", "data": resData}, content_type="application/json")



