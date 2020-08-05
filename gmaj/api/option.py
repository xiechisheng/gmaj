import json
from api.public import reqbody_verify
from api.ErrorCode import getErrMsgByCode
from api.public import reqbody_verify_admin
from rest_framework.response import Response
from rest_framework.decorators import api_view
from api.models import option_sys as OptionSysDB
from django.views.decorators.csrf import csrf_exempt


@csrf_exempt
@api_view(["post"])
def addOptionInfo(request):
    """
    配置信息--新增
    :return:
    """
    try:
        reqBody = json.loads(request.body)
    except Exception as err:
        return Response({"result": 28001001, "msg": getErrMsgByCode(28001001, err)}, content_type="application/json")

    if reqbody_verify_admin(reqBody, err_code=28001001) is None:
        pass
    else:
        return reqbody_verify_admin(reqBody, err_code=28001001)

    if "name" not in reqBody:
        return Response({"result": 28001006, "msg": getErrMsgByCode(28001006, None)}, content_type="application/json")
    else:
        optName = reqBody["name"]

    if "key" not in reqBody:
        return Response({"result": 28001007, "msg": getErrMsgByCode(28001007, None)}, content_type="application/json")
    else:
        optKey = reqBody["key"]

    if "value" not in reqBody:
        return Response({"result": 28001008, "msg": getErrMsgByCode(28001008, None)}, content_type="application/json")
    else:
        optValue = reqBody["value"]

    if "modify" not in reqBody:
        return Response({"result": 28001009, "msg": getErrMsgByCode(28001009, None)}, content_type="application/json")
    else:
        optModify = reqBody["modify"]

    try:
        optObj = OptionSysDB.objects.filter(opt_key=optKey)
    except Exception as err:
        return Response({"result": 28001010, "msg": getErrMsgByCode(28001010, err)}, content_type="application/json")

    if optObj:
        return Response({"result": 28001011, "msg": getErrMsgByCode(28001011, None)}, content_type="application/json")

    optObj = OptionSysDB()

    optObj.opt_name = optName
    optObj.opt_key = optKey
    optObj.opt_value = optValue
    optObj.opt_modify = optModify

    try:
        optObj.save()
    except Exception as err:
        return Response({"result": 28001012, "msg": getErrMsgByCode(28001012, err)}, content_type="application/json")

    return Response({"result": 0, "msg": "OK", "data": optObj.id}, content_type="application/json")


@csrf_exempt
@api_view(["post"])
def modifyOptionInfo(request):
    """
    配置信息--修改

    modify: 0不可修改, 1可修改
    :return:
    """
    try:
        reqBody = json.loads(request.body)
    except Exception as err:
        return Response({"result": 28002001, "msg": getErrMsgByCode(28002001, err)}, content_type="application/json")

    if reqbody_verify_admin(reqBody, err_code=28002001) is None:
        pass
    else:
        return reqbody_verify_admin(reqBody, err_code=28002001)

    if "id" not in reqBody:
        return Response({"result": 28002006, "msg": getErrMsgByCode(28002006, None)}, content_type="application/json")
    else:
        optID = reqBody["id"]

    try:
        optObj = OptionSysDB.objects.get(id=optID)
    except Exception as err:
        return Response({"result": 28002007, "msg": getErrMsgByCode(28002007, err)}, content_type="application/json")

    if optObj.opt_modify == 0:
        return Response({"result": 28002008, "msg": getErrMsgByCode(28002008, None)}, content_type="application/json")

    if "name" in reqBody:
        optObj.opt_name = reqBody["name"]

    if "value" in reqBody:
        optObj.opt_value = reqBody["value"]

    if "modify" in reqBody:
        optObj.opt_modify = reqBody["modify"]

    try:
        optObj.save()
    except Exception as err:
        return Response({"result": 28002009, "msg": getErrMsgByCode(28002009, err)}, content_type="application/json")

    return Response({"result": 0, "msg": "OK"}, content_type="application/json")


@csrf_exempt
@api_view(["post"])
def queryOptionInfo(request):
    """
    配置信息--查询
    :return:
    """
    try:
        reqBody = json.loads(request.body)
    except Exception as err:
        return Response({"result": 28003001, "msg": getErrMsgByCode(28003001, err)}, content_type="application/json")

    if reqbody_verify(reqBody, err_code=28003001) is None:
        pass
    else:
        return reqbody_verify(reqBody, err_code=28003001)

    try:
        optObjs = OptionSysDB.objects.all()
    except Exception as err:
        return Response({"result": 28003005, "msg": getErrMsgByCode(28003005, err)}, content_type="application/json")

    resData = []

    for opt in optObjs:
        optInfo = {}

        optInfo["id"] = opt.id
        optInfo["name"] = opt.opt_name
        optInfo["key"] = opt.opt_key
        optInfo["value"] = opt.opt_value
        optInfo["modify"] = opt.opt_modify

        resData.append(optInfo)

    return Response({"result": 0, "msg": "OK", "data": resData}, content_type="application/json")


@csrf_exempt
@api_view(["post"])
def deleteOptionInfo(request):
    """
    配置信息--删除
    :return:
    """
    try:
        reqBody = json.loads(request.body)
    except Exception as err:
        return Response({"result": 28004001, "msg": getErrMsgByCode(28004001, err)}, content_type="application/json")

    if reqbody_verify_admin(reqBody, err_code=28004001) is None:
        pass
    else:
        return reqbody_verify_admin(reqBody, err_code=28004001)

    if "id" not in reqBody:
        return Response({"result": 28004006, "msg": getErrMsgByCode(28004006, None)}, content_type="application/json")
    else:
        optID = reqBody["id"]

    try:
        optObj = OptionSysDB.objects.get(id=optID)
    except Exception as err:
        return Response({"result": 28004007, "msg": getErrMsgByCode(28004007, err)}, content_type="application/json")

    try:
        optObj.delete()
    except Exception as err:
        return Response({"result": 28004008, "msg": getErrMsgByCode(28004008, err)}, content_type="application/json")

    return Response({"result": 0, "msg": "OK"}, content_type="application/json")


