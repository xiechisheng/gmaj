from django.test import TestCase
import json
from api.public import reqbody_verify
from api.ErrorCode import getErrMsgByCode
from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.views.decorators.csrf import csrf_exempt

from api.public import setValueToCache
from api.public import tokenQuery

# Create your tests here.

@csrf_exempt
@api_view(["post"])
def saveJsonData(request):
    try:
        reqBody = json.loads(request.body)
    except Exception as err:
        return Response({"result": 24001001, "msg": getErrMsgByCode(24001001, err)}, content_type="application/json")

    if reqbody_verify(reqBody, err_code=24001001) is None:
        pass
    else:
        return reqbody_verify(reqBody, err_code=24001001)

    userLogin = None
    if "login" in reqBody:
        userLogin = reqBody["login"]
    else:
        return Response({"result": 24001006, "msg": getErrMsgByCode(24001006, None)}, content_type="application/json")

    userData = None
    if "data" in reqBody:
        userData = reqBody["data"]
    else:
        return Response({"result": 24001007, "msg": getErrMsgByCode(24001007, None)}, content_type="application/json")

    result = None
    if userLogin and userData:
        userLogin = "user_data_" + userLogin
        result = setValueToCache(userLogin, userData)

    if result is None:
        return Response({"result": 24001008, "msg": getErrMsgByCode(24001008, None)}, content_type="application/json")

    return Response({"result": 0, "msg": "OK"}, content_type="application/json")


@csrf_exempt
@api_view(["post"])
def getJsonData(request):
    try:
        reqBody = json.loads(request.body)
    except Exception as err:
        return Response({"result": 24002001, "msg": getErrMsgByCode(24002001, err)}, content_type="application/json")

    if reqbody_verify(reqBody, err_code=24002001) is None:
        pass
    else:
        return reqbody_verify(reqBody, err_code=24002001)

    userLogin = None
    if "login" in reqBody:
        userLogin = reqBody["login"]
    else:
        return Response({"result": 24002006, "msg": getErrMsgByCode(24002006, None)}, content_type="application/json")

    result = None
    if userLogin:
        userLogin = "user_data_" + userLogin
        result = tokenQuery(userLogin)

    if result is None:
        return Response({"result": 24002007, "msg": getErrMsgByCode(24002007, None)}, content_type="application/json")

    return Response({"result": 0, "msg": "OK", "data": result}, content_type="application/json")


