import json
from api.ErrorCode import getErrMsgByCode
from api.public import reqbody_verify
from api.public import reqbody_verify_admin
from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.views.decorators.csrf import csrf_exempt

from api.models import info_hazards as infoHazardsDB
from api.models import info_admin_license as infoAdminLicenseDB
from api.models import info_enterprise as infoEnterpriseDB
from api.models import info_plan as infoPlanDB
from api.models import info_trouble as infoTroubleDB
from api.models import info_check_log as infoCheckLogDB
from api.models import info_check_checker as infoCheckerDB
from django.db import transaction
import logging
import requests
from api.models import administration_punish_info as administrationPunishInfoDB

@csrf_exempt
@api_view(["post"])
def addHazardsInfo(request):
    """
    重大危险源信息--新增
    """
    try:
        reqBody = json.loads(request.body)
    except Exception as err:
        return Response({"result": 18001001, "msg": getErrMsgByCode(18001001, err)}, content_type="application/json")

    if reqbody_verify_admin(reqBody, err_code=18001001) is None:
        pass
    else:
        return reqbody_verify_admin(reqBody, err_code=18001001)

    if "unit_name" not in reqBody:
        return Response({"result": 18001006, "msg": getErrMsgByCode(18001006, None)}, content_type="application/json")
    else:
        unitName = reqBody["unit_name"]

    if "address" not in reqBody:
        return Response({"result": 18001007, "msg": getErrMsgByCode(18001007, None)}, content_type="application/json")
    else:
        unitAddress = reqBody["address"]

    if "region" not in reqBody:
        return Response({"result": 18001008, "msg": getErrMsgByCode(18001008, None)}, content_type="application/json")
    else:
        unitRegion = reqBody["region"]

    if "contact" not in reqBody:
        return Response({"result": 18001009, "msg": getErrMsgByCode(18001009, None)}, content_type="application/json")
    else:
        unitContact = reqBody["contact"]

    if "phone" not in reqBody:
        return Response({"result": 18001010, "msg": getErrMsgByCode(18001010, None)}, content_type="application/json")
    else:
        unitPhone = reqBody["phone"]

    if "type" not in reqBody:
        return Response({"result": 18001011, "msg": getErrMsgByCode(18001011, None)}, content_type="application/json")
    else:
        hazardsType = reqBody["type"]

    if "name" not in reqBody:
        return Response({"result": 18001012, "msg": getErrMsgByCode(18001012, None)}, content_type="application/json")
    else:
        hazardsName = reqBody["name"]

    if "level" not in reqBody:
        return Response({"result": 18001013, "msg": getErrMsgByCode(18001013, None)}, content_type="application/json")
    else:
        hazardsLevel = reqBody["level"]

    hazardsInfoObj = infoHazardsDB()
    hazardsInfoObj.unit_name = unitName
    hazardsInfoObj.address = unitAddress
    hazardsInfoObj.region = unitRegion
    hazardsInfoObj.contact = unitContact
    hazardsInfoObj.phone = unitPhone
    hazardsInfoObj.type = hazardsType
    hazardsInfoObj.name = hazardsName
    hazardsInfoObj.level = hazardsLevel

    try:
        hazardsInfoObj.save()
    except Exception as err:
        return Response({"result": 18001014, "msg": getErrMsgByCode(18001014, err)}, content_type="application/json")

    return Response({"result": 0, "msg": "OK"}, content_type="application/json")


@csrf_exempt
@api_view(["post"])
def modifyHazardsInfo(request):
    """
    重大危险源信息--修改
    :return:
    """
    try:
        reqBody = json.loads(request.body)
    except Exception as err:
        return Response({"result": 18002001, "msg": getErrMsgByCode(18002001, err)}, content_type="application/json")

    if reqbody_verify_admin(reqBody, err_code=18002001) is None:
        pass
    else:
        return reqbody_verify_admin(reqBody, err_code=18002001)

    if "id" not in reqBody:
        return Response({"result": 18002006, "msg": getErrMsgByCode(18002006, None)}, content_type="application/json")
    else:
        infoID = reqBody["id"]

    unitName = None
    unitAddress = None
    unitRegion = None
    unitContact = None
    unitPhone = None
    hazardsType = None
    hazardsName = None
    hazardsLevel = None

    if "unit_name" in reqBody:
        unitName = reqBody["unit_name"]

    if "address" in reqBody:
        unitAddress = reqBody["address"]

    if "region" in reqBody:
        unitRegion = reqBody["region"]

    if "contact" in reqBody:
        unitContact = reqBody["contact"]

    if "phone" in reqBody:
        unitPhone = reqBody["phone"]

    if "type" in reqBody:
        hazardsType = reqBody["type"]

    if "name" in reqBody:
        hazardsName = reqBody["name"]

    if "level" in reqBody:
        hazardsLevel = reqBody["level"]

    try:
        infoObj = infoHazardsDB.objects.get(id=infoID)
    except Exception as err:
        return Response({"result": 18002007, "msg": getErrMsgByCode(18002007, err)}, content_type="application/json")

    if unitName is not None:
        infoObj.unit_name = unitName

    if unitAddress is not None:
        infoObj.address = unitAddress

    if unitRegion is not None:
        infoObj.region = unitRegion

    if unitContact is not None:
        infoObj.contact = unitContact

    if unitPhone is not None:
        infoObj.phone = unitPhone

    if hazardsType is not None:
        infoObj.type = hazardsType

    if hazardsName is not None:
        infoObj.name = hazardsName

    if hazardsLevel is not None:
        infoObj.level = hazardsLevel

    try:
        infoObj.save()
    except Exception as err:
        return Response({"result": 18002008, "msg": getErrMsgByCode(18002008, err)}, content_type="application/json")

    return Response({"result": 0, "msg": "OK"}, content_type="application/json")


@csrf_exempt
@api_view(["post"])
def queryHazardsInfo(request):
    """
    重大危险源信息--查询
    :return:
    """
    try:
        reqBody = json.loads(request.body)
    except Exception as err:
        return Response({"result": 18003001, "msg": getErrMsgByCode(18003001, err)}, content_type="application/json")

    if reqbody_verify(reqBody, err_code=18003001) is None:
        pass
    else:
        return reqbody_verify(reqBody, err_code=18003001)

    resData = []
    try:
        hazardsInfoObjs = infoHazardsDB.objects.all()
        for item in hazardsInfoObjs:
            infoObj = {}

            infoObj["id"] = item.id
            infoObj["unit_name"] = item.unit_name
            infoObj["address"] = item.address
            infoObj["region"] = item.region
            infoObj["contact"] = item.contact
            infoObj["phone"] = item.phone
            infoObj["type"] = item.type
            infoObj["name"] = item.name
            infoObj["level"] = item.level

            resData.append(infoObj)
    except Exception as err:
        return Response({"result": 18003006, "msg": getErrMsgByCode(18003006, err)}, content_type="application/json")

    return Response({"result": 0, "msg": "OK", "data": resData}, content_type="application/json")


@csrf_exempt
@api_view(["post"])
def deleteHazardsInfo(request):
    """
    重大危险源信息--删除
    :return:
    """
    try:
        reqBody = json.loads(request.body)
    except Exception as err:
        return Response({"result": 18004001, "msg": getErrMsgByCode(18004001, err)}, content_type="application/json")

    if reqbody_verify_admin(reqBody, err_code=18004001) is None:
        pass
    else:
        return reqbody_verify_admin(reqBody, err_code=18004001)

    if "id" not in reqBody:
        return Response({"result": 18004006, "msg": getErrMsgByCode(18004006, None)}, content_type="application/json")
    else:
        infoID = reqBody["id"]

    try:
        infoObj = infoHazardsDB.objects.get(id=infoID)
    except Exception as err:
        return Response({"result": 18004007, "msg": getErrMsgByCode(18004007, err)}, content_type="application/json")

    try:
        infoObj.delete()
    except Exception as err:
        return Response({"result": 18004008, "msg": getErrMsgByCode(18004008, err)}, content_type="application/json")

    return Response({"result": 0, "msg": "OK"}, content_type="application/json")


@csrf_exempt
@api_view(["post"])
def addAdminLicenseInfo(request):
    """
    重大危险源信息--新增
    """
    try:
        reqBody = json.loads(request.body)
    except Exception as err:
        return Response({"result": 18005001, "msg": getErrMsgByCode(18005001, err)}, content_type="application/json")

    if reqbody_verify_admin(reqBody, err_code=18005001) is None:
        pass
    else:
        return reqbody_verify_admin(reqBody, err_code=18001001)

    if "type" not in reqBody:
        return Response({"result": 18005006, "msg": getErrMsgByCode(18005006, None)}, content_type="application/json")
    else:
        licenseType = reqBody["type"]

    if "name" not in reqBody:
        return Response({"result": 18005007, "msg": getErrMsgByCode(18005007, None)}, content_type="application/json")
    else:
        licenseName = reqBody["name"]

    if "code" not in reqBody:
        return Response({"result": 18005008, "msg": getErrMsgByCode(18005008, None)}, content_type="application/json")
    else:
        licenseCode = reqBody["code"]

    if "result" not in reqBody:
        return Response({"result": 18005009, "msg": getErrMsgByCode(18005009, None)}, content_type="application/json")
    else:
        licenseResult = reqBody["result"]

    if "organization" not in reqBody:
        return Response({"result": 18005010, "msg": getErrMsgByCode(18005010, None)}, content_type="application/json")
    else:
        licenseOrganization = reqBody["organization"]

    if "time" not in reqBody:
        return Response({"result": 18005011, "msg": getErrMsgByCode(18005011, None)}, content_type="application/json")
    else:
        licenseTime = reqBody["time"]

    if "validity" not in reqBody:
        return Response({"result": 18005012, "msg": getErrMsgByCode(18005012, None)}, content_type="application/json")
    else:
        licenseValidity = reqBody["validity"]

    licenseInfoObj = infoAdminLicenseDB()
    licenseInfoObj.type = licenseType
    licenseInfoObj.name = licenseName
    licenseInfoObj.code = licenseCode
    licenseInfoObj.result = licenseResult
    licenseInfoObj.organization = licenseOrganization
    licenseInfoObj.time = licenseTime
    licenseInfoObj.validity = licenseValidity

    try:
        licenseInfoObj.save()
    except Exception as err:
        return Response({"result": 18005013, "msg": getErrMsgByCode(18005013, err)}, content_type="application/json")

    return Response({"result": 0, "msg": "OK"}, content_type="application/json")


@csrf_exempt
@api_view(["post"])
def modifyAdminLicenseInfo(request):
    """
    安全生产许可信息--修改
    :return:
    """
    try:
        reqBody = json.loads(request.body)
    except Exception as err:
        return Response({"result": 18006001, "msg": getErrMsgByCode(18006001, err)}, content_type="application/json")

    if reqbody_verify_admin(reqBody, err_code=18006001) is None:
        pass
    else:
        return reqbody_verify_admin(reqBody, err_code=18006001)

    if "id" not in reqBody:
        return Response({"result": 18006006, "msg": getErrMsgByCode(18006006, None)}, content_type="application/json")
    else:
        infoID = reqBody["id"]

    licenseType = None
    licenseName = None
    licenseCode = None
    licenseResult = None
    licenseOrganization = None
    licenseTime = None
    licenseValidity = None

    if "type" in reqBody:
        licenseType = reqBody["type"]

    if "name" in reqBody:
        licenseName = reqBody["name"]

    if "code" in reqBody:
        licenseCode = reqBody["code"]

    if "result" in reqBody:
        licenseResult = reqBody["result"]

    if "organization" in reqBody:
        licenseOrganization = reqBody["organization"]

    if "time" in reqBody:
        licenseTime = reqBody["time"]

    if "validity" in reqBody:
        licenseValidity = reqBody["validity"]

    try:
        infoObj = infoAdminLicenseDB.objects.get(id=infoID)
    except Exception as err:
        return Response({"result": 18006007, "msg": getErrMsgByCode(18006007, err)}, content_type="application/json")

    if licenseType is not None:
        infoObj.type = licenseType

    if licenseName is not None:
        infoObj.name = licenseName

    if licenseCode is not None:
        infoObj.code = licenseCode

    if licenseResult is not None:
        infoObj.result = licenseResult

    if licenseOrganization is not None:
        infoObj.organization = licenseOrganization

    if licenseTime is not None:
        infoObj.time = licenseTime

    if licenseValidity is not None:
        infoObj.validity = licenseValidity

    try:
        infoObj.save()
    except Exception as err:
        return Response({"result": 18006008, "msg": getErrMsgByCode(18006008, err)}, content_type="application/json")

    return Response({"result": 0, "msg": "OK"}, content_type="application/json")


@csrf_exempt
@api_view(["post"])
def queryAdminLicenseInfo(request):
    """
    安全生产许可信息--查询
    :return:
    """
    try:
        reqBody = json.loads(request.body)
    except Exception as err:
        return Response({"result": 18007001, "msg": getErrMsgByCode(18007001, err)}, content_type="application/json")

    if reqbody_verify(reqBody, err_code=18007001) is None:
        pass
    else:
        return reqbody_verify(reqBody, err_code=18007001)

    resData = []
    try:
        licenseInfoObjs = infoAdminLicenseDB.objects.all()
        for item in licenseInfoObjs:
            infoObj = {}

            infoObj["id"] = item.id
            infoObj["type"] = item.type
            infoObj["name"] = item.name
            infoObj["code"] = item.code
            infoObj["result"] = item.result
            infoObj["organization"] = item.organization
            infoObj["time"] = item.time
            infoObj["validity"] = item.validity

            resData.append(infoObj)
    except Exception as err:
        return Response({"result": 18007006, "msg": getErrMsgByCode(18007006, err)}, content_type="application/json")

    return Response({"result": 0, "msg": "OK", "data": resData}, content_type="application/json")


@csrf_exempt
@api_view(["post"])
def deleteAdminLicenseInfo(request):
    """
    安全生产许可信息--删除
    """
    try:
        reqBody = json.loads(request.body)
    except Exception as err:
        return Response({"result": 18008001, "msg": getErrMsgByCode(18008001, err)}, content_type="application/json")

    if reqbody_verify_admin(reqBody, err_code=18008001) is None:
        pass
    else:
        return reqbody_verify_admin(reqBody, err_code=18008001)

    if "id" not in reqBody:
        return Response({"result": 18008006, "msg": getErrMsgByCode(18008006, None)}, content_type="application/json")
    else:
        infoID = reqBody["id"]

    try:
        infoObj = infoAdminLicenseDB.objects.get(id=infoID)
    except Exception as err:
        return Response({"result": 18008007, "msg": getErrMsgByCode(18008007, err)}, content_type="application/json")

    try:
        infoObj.delete()
    except Exception as err:
        return Response({"result": 18008008, "msg": getErrMsgByCode(18008008, err)}, content_type="application/json")

    return Response({"result": 0, "msg": "OK"}, content_type="application/json")


@csrf_exempt
@api_view(["post"])
def addEnterpriseInfo(request):
    """
    企业基本信息--新增
    """
    try:
        reqBody = json.loads(request.body)
    except Exception as err:
        return Response({"result": 18009001, "msg": getErrMsgByCode(18009001, err)}, content_type="application/json")

    if reqbody_verify_admin(reqBody, err_code=18009001) is None:
        pass
    else:
        return reqbody_verify_admin(reqBody, err_code=18009001)

    if "name" not in reqBody:
        return Response({"result": 18009006, "msg": getErrMsgByCode(18009006, None)}, content_type="application/json")
    else:
        enterpriseName = reqBody["name"]

    if "type" not in reqBody:
        return Response({"result": 18009007, "msg": getErrMsgByCode(18009007, None)}, content_type="application/json")
    else:
        enterpriseType = reqBody["type"]

    if "address" not in reqBody:
        return Response({"result": 18009008, "msg": getErrMsgByCode(18009008, None)}, content_type="application/json")
    else:
        enterpriseAddress = reqBody["address"]

    if "corporate_name" not in reqBody:
        return Response({"result": 18009009, "msg": getErrMsgByCode(18009009, None)}, content_type="application/json")
    else:
        enterpriseCorporateName = reqBody["corporate_name"]

    if "corporate_job" not in reqBody:
        return Response({"result": 18009010, "msg": getErrMsgByCode(18009010, None)}, content_type="application/json")
    else:
        enterpriseCorporateJob = reqBody["corporate_job"]

    if "corporate_phone" not in reqBody:
        return Response({"result": 18009011, "msg": getErrMsgByCode(18009011, None)}, content_type="application/json")
    else:
        enterpriseCorporatePhone = reqBody["corporate_phone"]

    if "safety_name" not in reqBody:
        return Response({"result": 18009012, "msg": getErrMsgByCode(18009012, None)}, content_type="application/json")
    else:
        enterpriseSafetyName = reqBody["safety_name"]

    if "safety_job" not in reqBody:
        return Response({"result": 18009013, "msg": getErrMsgByCode(18009013, None)}, content_type="application/json")
    else:
        enterpriseSafetyJob = reqBody["safety_job"]

    if "safety_phone" not in reqBody:
        return Response({"result": 18009014, "msg": getErrMsgByCode(18009014, None)}, content_type="application/json")
    else:
        enterpriseSafetyPhone = reqBody["safety_phone"]

    enterpriseInfoObj = infoEnterpriseDB()
    enterpriseInfoObj.name = enterpriseName
    enterpriseInfoObj.type = enterpriseType
    enterpriseInfoObj.address = enterpriseAddress
    enterpriseInfoObj.corporate_name = enterpriseCorporateName
    enterpriseInfoObj.corporate_job = enterpriseCorporateJob
    enterpriseInfoObj.corporate_phone = enterpriseCorporatePhone
    enterpriseInfoObj.safety_name = enterpriseSafetyName
    enterpriseInfoObj.safety_job = enterpriseSafetyJob
    enterpriseInfoObj.safety_phone = enterpriseSafetyPhone

    try:
        enterpriseInfoObj.save()
    except Exception as err:
        return Response({"result": 18009015, "msg": getErrMsgByCode(18009015, err)}, content_type="application/json")

    return Response({"result": 0, "msg": "OK"}, content_type="application/json")


@csrf_exempt
@api_view(["post"])
def modifyEnterpriseInfo(request):
    """
    企业基本信息--修改
    """
    try:
        reqBody = json.loads(request.body)
    except Exception as err:
        return Response({"result": 18010001, "msg": getErrMsgByCode(18010001, err)}, content_type="application/json")

    if reqbody_verify_admin(reqBody, err_code=18010001) is None:
        pass
    else:
        return reqbody_verify_admin(reqBody, err_code=18010001)

    if "id" not in reqBody:
        return Response({"result": 18010006, "msg": getErrMsgByCode(18010006, None)}, content_type="application/json")
    else:
        infoID = reqBody["id"]

    enterpriseName = None
    enterpriseType = None
    enterpriseAddress = None
    enterpriseCorporateName = None
    enterpriseCorporateJob = None
    enterpriseCorporatePhone = None
    enterpriseSafetyName = None
    enterpriseSafetyJob = None
    enterpriseSafetyPhone = None

    if "name" in reqBody:
        enterpriseName = reqBody["name"]

    if "type" in reqBody:
        enterpriseType = reqBody["type"]

    if "address" in reqBody:
        enterpriseAddress = reqBody["address"]

    if "corporate_name" in reqBody:
        enterpriseCorporateName = reqBody["corporate_name"]

    if "corporate_job" in reqBody:
        enterpriseCorporateJob = reqBody["corporate_job"]

    if "corporate_phone" in reqBody:
        enterpriseCorporatePhone = reqBody["corporate_phone"]

    if "safety_name" in reqBody:
        enterpriseSafetyName = reqBody["safety_name"]

    if "safety_job" in reqBody:
        enterpriseSafetyJob = reqBody["safety_job"]

    if "safety_phone" in reqBody:
        enterpriseSafetyPhone = reqBody["safety_phone"]

    try:
        infoObj = infoEnterpriseDB.objects.get(id=infoID)
    except Exception as err:
        return Response({"result": 18010007, "msg": getErrMsgByCode(18010007, err)}, content_type="application/json")

    if enterpriseName is not None:
        infoObj.name = enterpriseName

    if enterpriseType is not None:
        infoObj.type = enterpriseType

    if enterpriseAddress is not None:
        infoObj.address = enterpriseAddress

    if enterpriseCorporateName is not None:
        infoObj.corporate_name = enterpriseCorporateName

    if enterpriseCorporateJob is not None:
        infoObj.corporate_job = enterpriseCorporateJob

    if enterpriseCorporatePhone is not None:
        infoObj.corporate_phone = enterpriseCorporatePhone

    if enterpriseSafetyName is not None:
        infoObj.safety_name = enterpriseSafetyName

    if enterpriseSafetyJob is not None:
        infoObj.safety_job = enterpriseSafetyJob

    if enterpriseSafetyPhone is not None:
        infoObj.safety_phone = enterpriseSafetyPhone

    try:
        infoObj.save()
    except Exception as err:
        return Response({"result": 18010008, "msg": getErrMsgByCode(18010008, err)}, content_type="application/json")

    return Response({"result": 0, "msg": "OK"}, content_type="application/json")


@csrf_exempt
@api_view(["post"])
def queryEnterpriseInfo(request):
    """
    企业基本信息--查询
    """
    try:
        reqBody = json.loads(request.body)
    except Exception as err:
        return Response({"result": 18011001, "msg": getErrMsgByCode(18011001, err)}, content_type="application/json")

    if reqbody_verify(reqBody, err_code=18011001) is None:
        pass
    else:
        return reqbody_verify(reqBody, err_code=18011001)

    resData = []
    try:
        licenseInfoObjs = infoEnterpriseDB.objects.all()
        for item in licenseInfoObjs:
            infoObj = {}

            infoObj["id"] = item.id
            infoObj["name"] = item.name
            infoObj["type"] = item.type
            infoObj["address"] = item.address
            infoObj["corporate_name"] = item.corporate_name
            infoObj["corporate_job"] = item.corporate_job
            infoObj["corporate_phone"] = item.corporate_phone
            infoObj["safety_name"] = item.safety_name
            infoObj["safety_job"] = item.safety_job
            infoObj["safety_phone"] = item.safety_phone

            resData.append(infoObj)
    except Exception as err:
        return Response({"result": 18011006, "msg": getErrMsgByCode(18011006, err)}, content_type="application/json")

    return Response({"result": 0, "msg": "OK", "data": resData}, content_type="application/json")


@csrf_exempt
@api_view(["post"])
def deleteEnterpriseInfo(request):
    """
    企业基本信息--删除
    """
    try:
        reqBody = json.loads(request.body)
    except Exception as err:
        return Response({"result": 18012001, "msg": getErrMsgByCode(18012001, err)}, content_type="application/json")

    if reqbody_verify_admin(reqBody, err_code=18012001) is None:
        pass
    else:
        return reqbody_verify_admin(reqBody, err_code=18012001)

    if "id" not in reqBody:
        return Response({"result": 18012006, "msg": getErrMsgByCode(18012006, None)}, content_type="application/json")
    else:
        infoID = reqBody["id"]

    try:
        infoObj = infoEnterpriseDB.objects.get(id=infoID)
    except Exception as err:
        return Response({"result": 18012007, "msg": getErrMsgByCode(18012007, err)}, content_type="application/json")

    try:
        infoObj.delete()
    except Exception as err:
        return Response({"result": 18012008, "msg": getErrMsgByCode(18012008, err)}, content_type="application/json")

    return Response({"result": 0, "msg": "OK"}, content_type="application/json")


@csrf_exempt
@api_view(["post"])
def addPlanInfo(request):
    """
    预案信息--新增
    """
    try:
        reqBody = json.loads(request.body)
    except Exception as err:
        return Response({"result": 18013001, "msg": getErrMsgByCode(18013001, err)}, content_type="application/json")

    if reqbody_verify_admin(reqBody, err_code=18013001) is None:
        pass
    else:
        return reqbody_verify_admin(reqBody, err_code=18013001)

    if "plan_name" not in reqBody:
        return Response({"result": 18013006, "msg": getErrMsgByCode(18013006, None)}, content_type="application/json")
    else:
        planName = reqBody["plan_name"]

    if "plan_time" not in reqBody:
        return Response({"result": 18013007, "msg": getErrMsgByCode(18013007, None)}, content_type="application/json")
    else:
        planTime = reqBody["plan_time"]

    if "scheme_name" not in reqBody:
        return Response({"result": 18013008, "msg": getErrMsgByCode(18013008, None)}, content_type="application/json")
    else:
        schemeName = reqBody["scheme_name"]

    if "scheme_time" not in reqBody:
        return Response({"result": 18013009, "msg": getErrMsgByCode(18013009, None)}, content_type="application/json")
    else:
        schemeTime = reqBody["scheme_time"]

    if "commanding_organization" not in reqBody:
        return Response({"result": 18013010, "msg": getErrMsgByCode(18013010, None)}, content_type="application/json")
    else:
        commandingOrganization = reqBody["commanding_organization"]

    if "risk_assessment" not in reqBody:
        return Response({"result": 18013011, "msg": getErrMsgByCode(18013011, None)}, content_type="application/json")
    else:
        riskAssessment = reqBody["risk_assessment"]

    if "commander_name" not in reqBody:
        return Response({"result": 18013012, "msg": getErrMsgByCode(18013012, None)}, content_type="application/json")
    else:
        commanderName = reqBody["commander_name"]

    if "commander_phone" not in reqBody:
        return Response({"result": 18013013, "msg": getErrMsgByCode(18013013, None)}, content_type="application/json")
    else:
        commanderPhone = reqBody["commander_phone"]

    if "resource_investigation" not in reqBody:
        return Response({"result": 18013014, "msg": getErrMsgByCode(18013014, None)}, content_type="application/json")
    else:
        resourceInvestigation = reqBody["resource_investigation"]

    if "plan_record" not in reqBody:
        return Response({"result": 18013015, "msg": getErrMsgByCode(18013015, None)}, content_type="application/json")
    else:
        planRecord = reqBody["plan_record"]

    planInfoObj = infoPlanDB()
    planInfoObj.plan_name = planName
    planInfoObj.plan_time = planTime
    planInfoObj.scheme_name = schemeName
    planInfoObj.scheme_time = schemeTime
    planInfoObj.commanding_organization = commandingOrganization
    planInfoObj.risk_assessment = riskAssessment
    planInfoObj.commander_name = commanderName
    planInfoObj.commander_phone = commanderPhone
    planInfoObj.resource_investigation = resourceInvestigation
    planInfoObj.plan_record = planRecord

    try:
        planInfoObj.save()
    except Exception as err:
        return Response({"result": 18013016, "msg": getErrMsgByCode(18013016, err)}, content_type="application/json")

    return Response({"result": 0, "msg": "OK"}, content_type="application/json")


@csrf_exempt
@api_view(["post"])
def modifyPlanInfo(request):
    """
    预案信息--修改
    """
    try:
        reqBody = json.loads(request.body)
    except Exception as err:
        return Response({"result": 18014001, "msg": getErrMsgByCode(18014001, err)}, content_type="application/json")

    if reqbody_verify_admin(reqBody, err_code=18014001) is None:
        pass
    else:
        return reqbody_verify_admin(reqBody, err_code=18014001)

    if "id" not in reqBody:
        return Response({"result": 18014006, "msg": getErrMsgByCode(18014006, None)}, content_type="application/json")
    else:
        infoID = reqBody["id"]

    planName = None
    planTime = None
    schemeName = None
    schemeTime = None
    commandingOrganization = None
    riskAssessment = None
    commanderName = None
    commanderPhone = None
    resourceInvestigation = None
    planRecord = None

    if "plan_name" in reqBody:
        planName = reqBody["plan_name"]

    if "plan_time" in reqBody:
        planTime = reqBody["plan_time"]

    if "scheme_name" in reqBody:
        schemeName = reqBody["scheme_name"]

    if "scheme_time" in reqBody:
        schemeTime = reqBody["scheme_time"]

    if "commanding_organization" in reqBody:
        commandingOrganization = reqBody["commanding_organization"]

    if "risk_assessment" in reqBody:
        riskAssessment = reqBody["risk_assessment"]

    if "commander_name" in reqBody:
        commanderName = reqBody["commander_name"]

    if "commander_phone" in reqBody:
        commanderPhone = reqBody["commander_phone"]

    if "resource_investigation" in reqBody:
        resourceInvestigation = reqBody["resource_investigation"]

    if "plan_record" in reqBody:
        planRecord = reqBody["plan_record"]

    try:
        infoObj = infoPlanDB.objects.get(id=infoID)
    except Exception as err:
        return Response({"result": 18014007, "msg": getErrMsgByCode(18014007, err)}, content_type="application/json")

    if planName is not None:
        infoObj.plan_name = planName

    if planTime is not None:
        infoObj.plan_time = planTime

    if schemeName is not None:
        infoObj.scheme_name = schemeName

    if schemeTime is not None:
        infoObj.scheme_time = schemeTime

    if commandingOrganization is not None:
        infoObj.commanding_organization = commandingOrganization

    if riskAssessment is not None:
        infoObj.risk_assessment = riskAssessment

    if commanderName is not None:
        infoObj.commander_name = commanderName

    if commanderPhone is not None:
        infoObj.commander_phone = commanderPhone

    if resourceInvestigation is not None:
        infoObj.resource_investigation = resourceInvestigation

    if planRecord is not None:
        infoObj.plan_record = planRecord

    try:
        infoObj.save()
    except Exception as err:
        return Response({"result": 18014008, "msg": getErrMsgByCode(18014008, err)}, content_type="application/json")

    return Response({"result": 0, "msg": "OK"}, content_type="application/json")


@csrf_exempt
@api_view(["post"])
def queryPlanInfo(request):
    """
    预案信息信息--查询
    """
    try:
        reqBody = json.loads(request.body)
    except Exception as err:
        return Response({"result": 18015001, "msg": getErrMsgByCode(18015001, err)}, content_type="application/json")

    if reqbody_verify(reqBody, err_code=18015001) is None:
        pass
    else:
        return reqbody_verify(reqBody, err_code=18015001)

    resData = []
    try:
        licenseInfoObjs = infoPlanDB.objects.all()
        for item in licenseInfoObjs:
            infoObj = {}

            infoObj["id"] = item.id
            infoObj["plan_name"] = item.plan_name
            infoObj["plan_time"] = item.plan_time
            infoObj["scheme_name"] = item.scheme_name
            infoObj["scheme_time"] = item.scheme_time
            infoObj["commanding_organization"] = item.commanding_organization
            infoObj["risk_assessment"] = item.risk_assessment
            infoObj["commander_name"] = item.commander_name
            infoObj["commander_phone"] = item.commander_phone
            infoObj["resource_investigation"] = item.resource_investigation
            infoObj["plan_record"] = item.plan_record

            resData.append(infoObj)
    except Exception as err:
        return Response({"result": 18015006, "msg": getErrMsgByCode(18015006, err)}, content_type="application/json")

    return Response({"result": 0, "msg": "OK", "data": resData}, content_type="application/json")


@csrf_exempt
@api_view(["post"])
def deletePlanInfo(request):
    """
    预案信息--删除
    """
    try:
        reqBody = json.loads(request.body)
    except Exception as err:
        return Response({"result": 18016001, "msg": getErrMsgByCode(18016001, err)}, content_type="application/json")

    if reqbody_verify_admin(reqBody, err_code=18016001) is None:
        pass
    else:
        return reqbody_verify_admin(reqBody, err_code=18016001)

    if "id" not in reqBody:
        return Response({"result": 18016006, "msg": getErrMsgByCode(18016006, None)}, content_type="application/json")
    else:
        infoID = reqBody["id"]

    try:
        infoObj = infoPlanDB.objects.get(id=infoID)
    except Exception as err:
        return Response({"result": 18016007, "msg": getErrMsgByCode(18016007, err)}, content_type="application/json")

    try:
        infoObj.delete()
    except Exception as err:
        return Response({"result": 18016008, "msg": getErrMsgByCode(18016008, err)}, content_type="application/json")

    return Response({"result": 0, "msg": "OK"}, content_type="application/json")


@csrf_exempt
@api_view(["post"])
def addTroubleInfo(request):
    """
    隐患信息--新增
    """
    try:
        reqBody = json.loads(request.body)
    except Exception as err:
        return Response({"result": 18017001, "msg": getErrMsgByCode(18017001, err)}, content_type="application/json")

    if reqbody_verify_admin(reqBody, err_code=18017001) is None:
        pass
    else:
        return reqbody_verify_admin(reqBody, err_code=18017001)

    if "code" not in reqBody:
        return Response({"result": 18017006, "msg": getErrMsgByCode(18017006, None)}, content_type="application/json")
    else:
        troubleCode = reqBody["code"]

    if "source" not in reqBody:
        return Response({"result": 18017007, "msg": getErrMsgByCode(18017007, None)}, content_type="application/json")
    else:
        troubleSource = reqBody["source"]

    if "type" not in reqBody:
        return Response({"result": 18017008, "msg": getErrMsgByCode(18017008, None)}, content_type="application/json")
    else:
        troubleType = reqBody["type"]

    if "describe" not in reqBody:
        return Response({"result": 18017009, "msg": getErrMsgByCode(18017009, None)}, content_type="application/json")
    else:
        troubleDescribe = reqBody["describe"]

    if "level" not in reqBody:
        return Response({"result": 18017010, "msg": getErrMsgByCode(18017010, None)}, content_type="application/json")
    else:
        troubleLevel = reqBody["level"]

    if "status" not in reqBody:
        return Response({"result": 18017011, "msg": getErrMsgByCode(18017011, None)}, content_type="application/json")
    else:
        troubleStatus = reqBody["status"]

    if "dept" not in reqBody:
        return Response({"result": 18017012, "msg": getErrMsgByCode(18017012, None)}, content_type="application/json")
    else:
        troubleDept = reqBody["dept"]

    if "enterprise" not in reqBody:
        return Response({"result": 18017013, "msg": getErrMsgByCode(18017013, None)}, content_type="application/json")
    else:
        troubleEnterprise = reqBody["enterprise"]

    if "reporter" not in reqBody:
        return Response({"result": 18017014, "msg": getErrMsgByCode(18017014, None)}, content_type="application/json")
    else:
        troubleReporter = reqBody["reporter"]

    if "time" not in reqBody:
        return Response({"result": 18017015, "msg": getErrMsgByCode(18017015, None)}, content_type="application/json")
    else:
        troubleTime = reqBody["time"]

    troubleInfoObj = infoTroubleDB()
    troubleInfoObj.code = troubleCode
    troubleInfoObj.source = troubleSource
    troubleInfoObj.type = troubleType
    troubleInfoObj.describe = troubleDescribe
    troubleInfoObj.level = troubleLevel
    troubleInfoObj.status = troubleStatus
    troubleInfoObj.dept = troubleDept
    troubleInfoObj.enterprise = troubleEnterprise
    troubleInfoObj.reporter = troubleReporter
    troubleInfoObj.time = troubleTime

    try:
        troubleInfoObj.save()
    except Exception as err:
        return Response({"result": 18017016, "msg": getErrMsgByCode(18017016, err)}, content_type="application/json")

    return Response({"result": 0, "msg": "OK"}, content_type="application/json")


@csrf_exempt
@api_view(["post"])
def modifyTroubleInfo(request):
    """
    隐患信息--修改
    """
    try:
        reqBody = json.loads(request.body)
    except Exception as err:
        return Response({"result": 18018001, "msg": getErrMsgByCode(18018001, err)}, content_type="application/json")

    if reqbody_verify_admin(reqBody, err_code=18018001) is None:
        pass
    else:
        return reqbody_verify_admin(reqBody, err_code=18018001)

    if "id" not in reqBody:
        return Response({"result": 18018006, "msg": getErrMsgByCode(18018006, None)}, content_type="application/json")
    else:
        infoID = reqBody["id"]

    troubleCode = None
    troubleSource = None
    troubleType = None
    troubleDescribe = None
    troubleLevel = None
    troubleStatus = None
    troubleDept = None
    troubleEnterprise = None
    troubleReporter = None
    troubleTime = None

    if "code" in reqBody:
        troubleCode = reqBody["code"]

    if "source" in reqBody:
        troubleSource = reqBody["source"]

    if "type" in reqBody:
        troubleType = reqBody["type"]

    if "describe" in reqBody:
        troubleDescribe = reqBody["describe"]

    if "level" in reqBody:
        troubleLevel = reqBody["level"]

    if "status" in reqBody:
        troubleStatus = reqBody["status"]

    if "dept" in reqBody:
        troubleDept = reqBody["dept"]

    if "enterprise" in reqBody:
        troubleEnterprise = reqBody["enterprise"]

    if "reporter" in reqBody:
        troubleReporter = reqBody["reporter"]

    if "time" in reqBody:
        troubleTime = reqBody["time"]

    try:
        infoObj = infoTroubleDB.objects.get(id=infoID)
    except Exception as err:
        return Response({"result": 18018007, "msg": getErrMsgByCode(18018007, err)}, content_type="application/json")

    if troubleCode is not None:
        infoObj.code = troubleCode

    if troubleSource is not None:
        infoObj.source = troubleSource

    if troubleType is not None:
        infoObj.type = troubleType

    if troubleDescribe is not None:
        infoObj.describe = troubleDescribe

    if troubleLevel is not None:
        infoObj.level = troubleLevel

    if troubleStatus is not None:
        infoObj.status = troubleStatus

    if troubleDept is not None:
        infoObj.dept = troubleDept

    if troubleEnterprise is not None:
        infoObj.enterprise = troubleEnterprise

    if troubleReporter is not None:
        infoObj.reporter = troubleReporter

    if troubleTime is not None:
        infoObj.time = troubleTime

    try:
        infoObj.save()
    except Exception as err:
        return Response({"result": 18018008, "msg": getErrMsgByCode(18018008, err)}, content_type="application/json")

    return Response({"result": 0, "msg": "OK"}, content_type="application/json")


@csrf_exempt
@api_view(["post"])
def queryTroubleInfo(request):
    """
    隐患信息信息--查询
    """
    try:
        reqBody = json.loads(request.body)
    except Exception as err:
        return Response({"result": 18019001, "msg": getErrMsgByCode(18019001, err)}, content_type="application/json")

    if reqbody_verify(reqBody, err_code=18019001) is None:
        pass
    else:
        return reqbody_verify(reqBody, err_code=18019001)

    resData = []
    try:
        licenseInfoObjs = infoTroubleDB.objects.all()
        for item in licenseInfoObjs:
            infoObj = {}

            infoObj["id"] = item.id
            infoObj["code"] = item.code
            infoObj["source"] = item.source
            infoObj["type"] = item.type
            infoObj["describe"] = item.describe
            infoObj["level"] = item.level
            infoObj["status"] = item.status
            infoObj["dept"] = item.dept
            infoObj["enterprise"] = item.enterprise
            infoObj["reporter"] = item.reporter
            infoObj["time"] = item.time

            resData.append(infoObj)
    except Exception as err:
        return Response({"result": 18019006, "msg": getErrMsgByCode(18019006, err)}, content_type="application/json")

    return Response({"result": 0, "msg": "OK", "data": resData}, content_type="application/json")


@csrf_exempt
@api_view(["post"])
def deleteTroubleInfo(request):
    """
    隐患信息--删除
    """
    try:
        reqBody = json.loads(request.body)
    except Exception as err:
        return Response({"result": 18020001, "msg": getErrMsgByCode(18020001, err)}, content_type="application/json")

    if reqbody_verify_admin(reqBody, err_code=18020001) is None:
        pass
    else:
        return reqbody_verify_admin(reqBody, err_code=18020001)

    if "id" not in reqBody:
        return Response({"result": 18020006, "msg": getErrMsgByCode(18020006, None)}, content_type="application/json")
    else:
        infoID = reqBody["id"]

    try:
        infoObj = infoTroubleDB.objects.get(id=infoID)
    except Exception as err:
        return Response({"result": 18020007, "msg": getErrMsgByCode(18020007, err)}, content_type="application/json")

    try:
        infoObj.delete()
    except Exception as err:
        return Response({"result": 18020008, "msg": getErrMsgByCode(18020008, err)}, content_type="application/json")

    return Response({"result": 0, "msg": "OK"}, content_type="application/json")


@csrf_exempt
@api_view(["post"])
def addCheckLogInfo(request):
    """
    行政执法许可信息--新增
    """
    print("test")
    try:
        reqBody = json.loads(request.body)
    except Exception as err:
        return Response({"result": 18021001, "msg": getErrMsgByCode(18021001, err)}, content_type="application/json")

    if reqbody_verify_admin(reqBody, err_code=18021001) is None:
        pass
    else:
        return reqbody_verify_admin(reqBody, err_code=18021001)

    if "code" not in reqBody:
        return Response({"result": 18021006, "msg": getErrMsgByCode(18021006, None)}, content_type="application/json")
    else:
        checkCode = reqBody["code"]

    if "enterprise" not in reqBody:
        return Response({"result": 18021007, "msg": getErrMsgByCode(18021007, None)}, content_type="application/json")
    else:
        checkEnterprise = reqBody["enterprise"]

    if "address" not in reqBody:
        return Response({"result": 18021008, "msg": getErrMsgByCode(18021008, None)}, content_type="application/json")
    else:
        checkAddress = reqBody["address"]

    if "corporate_name" not in reqBody:
        return Response({"result": 18021009, "msg": getErrMsgByCode(18021009, None)}, content_type="application/json")
    else:
        corporateName = reqBody["corporate_name"]

    if "corporate_job" not in reqBody:
        return Response({"result": 18021010, "msg": getErrMsgByCode(18021010, None)}, content_type="application/json")
    else:
        corporateJob = reqBody["corporate_job"]

    if "corporate_phone" not in reqBody:
        return Response({"result": 18021011, "msg": getErrMsgByCode(18021011, None)}, content_type="application/json")
    else:
        corporatePhone = reqBody["corporate_phone"]

    if "place" not in reqBody:
        return Response({"result": 18021012, "msg": getErrMsgByCode(18021012, None)}, content_type="application/json")
    else:
        checkPlace = reqBody["place"]

    if "begin_time" not in reqBody:
        return Response({"result": 18021013, "msg": getErrMsgByCode(18021013, None)}, content_type="application/json")
    else:
        beginTime = reqBody["begin_time"]

    if "end_time" not in reqBody:
        return Response({"result": 18021014, "msg": getErrMsgByCode(18021014, None)}, content_type="application/json")
    else:
        endTime = reqBody["end_time"]

    if "checkers" not in reqBody:
        return Response({"result": 18021014, "msg": getErrMsgByCode(18021014, None)}, content_type="application/json")
    else:
        checkerList = reqBody["checkers"]

    if "checkerIDs" not in reqBody:
        return Response({"result": 18021014, "msg": getErrMsgByCode(18021014, None)}, content_type="application/json")
    else:
        checkerIDList = reqBody["checkerIDs"]

    checkInfoObj = infoCheckLogDB()
    checkInfoObj.code = checkCode
    checkInfoObj.enterprise = checkEnterprise
    checkInfoObj.address = checkAddress
    checkInfoObj.corporate_name = corporateName
    checkInfoObj.corporate_job = corporateJob
    checkInfoObj.corporate_phone = corporatePhone
    checkInfoObj.place = checkPlace
    checkInfoObj.begin_time = beginTime
    checkInfoObj.end_time = endTime

    savePoint = transaction.savepoint()
    try:
        checkInfoObj.save()
    except Exception as err:
        transaction.savepoint_rollback(savePoint)
        return Response({"result": 18021015, "msg": getErrMsgByCode(18021015, err)}, content_type="application/json")

    try:
        i = 0
        while i < len(checkerList):
            checkerName = checkerList[i]
            checkerID = checkerIDList[i]

            checkerObj = infoCheckerDB()
            checkerObj.log_id = checkInfoObj.id
            checkerObj.checker_name = checkerName
            checkerObj.checker_id = checkerID

            i += 1
            checkerObj.save()
    except Exception as err:
        transaction.savepoint_rollback(savePoint)
        return Response({"result": 18021016, "msg": getErrMsgByCode(18021016, err)}, content_type="application/json")

    transaction.savepoint_commit(savePoint)
    return Response({"result": 0, "msg": "OK"}, content_type="application/json")


@csrf_exempt
@api_view(["post"])
def modifyCheckLogInfo(request):
    """
    行政执法信息--修改
    """
    try:
        reqBody = json.loads(request.body)
    except Exception as err:
        return Response({"result": 18022001, "msg": getErrMsgByCode(18022001, err)}, content_type="application/json")

    if reqbody_verify_admin(reqBody, err_code=18022001) is None:
        pass
    else:
        return reqbody_verify_admin(reqBody, err_code=18022001)

    if "id" not in reqBody:
        return Response({"result": 18022006, "msg": getErrMsgByCode(18022006, None)}, content_type="application/json")
    else:
        infoID = reqBody["id"]

    checkCode = None
    checkEnterprise = None
    checkAddress = None
    corporateName = None
    corporateJob = None
    corporatePhone = None
    checkPlace = None
    beginTime = None
    endTime = None
    checkerList = None
    checkerIDList = None

    if "code" in reqBody:
        checkCode = reqBody["code"]

    if "enterprise" in reqBody:
        checkEnterprise = reqBody["enterprise"]

    if "address" in reqBody:
        checkAddress = reqBody["address"]

    if "corporate_name" in reqBody:
        corporateName = reqBody["corporate_name"]

    if "corporate_job" in reqBody:
        corporateJob = reqBody["corporate_job"]

    if "corporate_phone" in reqBody:
        corporatePhone = reqBody["corporate_phone"]

    if "place" in reqBody:
        checkPlace = reqBody["place"]

    if "begin_time" in reqBody:
        beginTime = reqBody["begin_time"]

    if "end_time" in reqBody:
        endTime = reqBody["end_time"]

    if "checkers" in reqBody:
        checkerList = reqBody["checkers"]

    if "checkerIDs" in reqBody:
        checkerIDList = reqBody["checkerIDs"]

    try:
        infoObj = infoCheckLogDB.objects.get(id=infoID)
    except Exception as err:
        return Response({"result": 18022007, "msg": getErrMsgByCode(18022007, err)}, content_type="application/json")

    if checkCode is not None:
        infoObj.code = checkCode

    if checkEnterprise is not None:
        infoObj.enterprise = checkEnterprise

    if checkAddress is not None:
        infoObj.address = checkAddress

    if corporateName is not None:
        infoObj.corporate_name = corporateName

    if corporateJob is not None:
        infoObj.corporate_job = corporateJob

    if corporatePhone is not None:
        infoObj.corporate_phone = corporatePhone

    if checkPlace is not None:
        infoObj.place = checkPlace

    if beginTime is not None:
        infoObj.begin_time = beginTime

    if endTime is not None:
        infoObj.end_time = endTime

    if endTime is not None:
        infoObj.time = endTime

    savePoint = transaction.savepoint()
    try:
        infoObj.save()
    except Exception as err:
        transaction.savepoint_rollback(savePoint)
        return Response({"result": 18022008, "msg": getErrMsgByCode(18022008, err)}, content_type="application/json")

    try:
        if checkerList and checkerIDList:
            infoCheckerDB.objects.filter(log_id=infoID).delete()

            i = 0
            while i < len(checkerList):
                checkerName = checkerList[i]
                checkerID = checkerIDList[i]

                checkerObj = infoCheckerDB()
                checkerObj.log_id = infoID
                checkerObj.checker_name = checkerName
                checkerObj.checker_id = checkerID

                i += 1
                checkerObj.save()

    except Exception as err:
        transaction.savepoint_rollback(savePoint)
        return Response({"result": 18022009, "msg": getErrMsgByCode(18022009, err)}, content_type="application/json")

    transaction.savepoint_commit(savePoint)
    return Response({"result": 0, "msg": "OK"}, content_type="application/json")


@csrf_exempt
@api_view(["post"])
def queryCheckLogInfo(request):
    """
    行政执法信息--查询
    """
    try:
        reqBody = json.loads(request.body)
    except Exception as err:
        return Response({"result": 18023001, "msg": getErrMsgByCode(18023001, err)}, content_type="application/json")

    if reqbody_verify(reqBody, err_code=18023001) is None:
        pass
    else:
        return reqbody_verify(reqBody, err_code=18023001)

    resData = []
    try:
        checkLogObjs = infoCheckLogDB.objects.all()
        for item in checkLogObjs:
            infoObj = {}

            infoObj["id"] = item.id
            infoObj["code"] = item.code
            infoObj["enterprise"] = item.enterprise
            infoObj["address"] = item.address
            infoObj["corporate_name"] = item.corporate_name
            infoObj["corporate_job"] = item.corporate_job
            infoObj["corporate_phone"] = item.corporate_phone
            infoObj["place"] = item.place
            infoObj["begin_time"] = item.begin_time
            infoObj["end_time"] = item.end_time

            checkerNameList = []
            checkerIDList = []
            checkerObjs = infoCheckerDB.objects.filter(log_id=item.id)
            for checker in checkerObjs:
                checkerNameList.append(checker.checker_name)
                checkerIDList.append(checker.checker_id)

            infoObj["checkers"] = checkerNameList
            infoObj["checkerIDs"] = checkerIDList

            resData.append(infoObj)
    except Exception as err:
        return Response({"result": 18023006, "msg": getErrMsgByCode(18023006, err)}, content_type="application/json")

    return Response({"result": 0, "msg": "OK", "data": resData}, content_type="application/json")


@csrf_exempt
@api_view(["post"])
def deleteCheckLogInfo(request):
    """
    行政执法信息--删除
    """
    try:
        reqBody = json.loads(request.body)
    except Exception as err:
        return Response({"result": 18024001, "msg": getErrMsgByCode(18024001, err)}, content_type="application/json")

    if reqbody_verify_admin(reqBody, err_code=18024001) is None:
        pass
    else:
        return reqbody_verify_admin(reqBody, err_code=18024001)

    if "id" not in reqBody:
        return Response({"result": 18024006, "msg": getErrMsgByCode(18024006, None)}, content_type="application/json")
    else:
        infoID = reqBody["id"]

    try:
        infoObj = infoCheckLogDB.objects.get(id=infoID)
    except Exception as err:
        return Response({"result": 18024007, "msg": getErrMsgByCode(18024007, err)}, content_type="application/json")

    savePoint = transaction.savepoint()
    try:
        infoObj.delete()
        checkerObj = infoCheckerDB.objects.filter(log_id=infoID).delete()
    except Exception as err:
        transaction.savepoint_rollback(savePoint)
        return Response({"result": 18024008, "msg": getErrMsgByCode(18024008, err)}, content_type="application/json")

    transaction.savepoint_commit(savePoint)
    return Response({"result": 0, "msg": "OK"}, content_type="application/json")



@csrf_exempt
@api_view(["post"])
def hiddenDangerInfoQuery(request):
    """
    隐患信息查询

    """

    try:
        reqBody = json.loads(request.body)
    except Exception as err:
        return Response({"result": 18025001, "msg": getErrMsgByCode(18025001, err)}, content_type="application/json")

    if reqbody_verify(reqBody, err_code=18025001) is None:
        pass
    else:
        return reqbody_verify(reqBody, err_code=18025001)

    try:

        logging.captureWarnings(True)


        registerData = {"start_time":"2018-07-20","end_time":"2018-07-25"}

        response = requests.get(url="https://203.91.35.44:81/ComSyncData/GetHiddenEventList",verify=False,params=registerData)

        resultData=response.text

    except Exception as err:
        return Response({"result": 18025006, "msg": getErrMsgByCode(18025006, err)}, content_type="application/json")

    return Response(json.loads(resultData), content_type="application/json")


@csrf_exempt
@api_view(["post"])
def incidentreporting(request):
    """
    事件上报

    """

    try:
        reqBody = json.loads(request.body)
    except Exception as err:
        return Response({"result": 18026001, "msg": getErrMsgByCode(18026001, err)}, content_type="application/json")

    if reqbody_verify(reqBody, err_code=18026001) is None:
        pass
    else:
        return reqbody_verify(reqBody, err_code=18026001)

    registerData={}

    if "authorName" not in reqBody:
        return Response({"result": 18026006, "msg": getErrMsgByCode(18026006, None)}, content_type="application/json")
    else:
        authorName = reqBody["authorName"]
        registerData["authorName"]=authorName

    if "authorCode" not in reqBody:
        return Response({"result": 18026007, "msg": getErrMsgByCode(18026007, None)}, content_type="application/json")
    else:
        authorCode = reqBody["authorCode"]
        registerData["authorCode"]=authorCode

    if "eventCode" not in reqBody:
        return Response({"result": 18026008, "msg": getErrMsgByCode(18026008, None)}, content_type="application/json")
    else:
        eventCode = reqBody["eventCode"]
        registerData["eventCode"]=eventCode

    if "address" not in reqBody:
        return Response({"result": 18026009, "msg": getErrMsgByCode(18026009, None)}, content_type="application/json")
    else:
        address = reqBody["address"]
        registerData["address"]=address

    if "describe" not in reqBody:
        return Response({"result": 18026010, "msg": getErrMsgByCode(18026010, None)}, content_type="application/json")
    else:
        describe = reqBody["describe"]
        registerData["describe"]=describe

    if "channelNo" not in reqBody:
        return Response({"result": 18026011, "msg": getErrMsgByCode(18026011, None)}, content_type="application/json")
    else:
        channelNo = reqBody["channelNo"]
        registerData["channelNo"]=channelNo

    if "formNo" not in reqBody:
        return Response({"result": 18026012, "msg": getErrMsgByCode(18026012, None)}, content_type="application/json")
    else:
        formNo = reqBody["formNo"]
        registerData["formNo"]=formNo

    if "userName" not in reqBody:
        return Response({"result": 18026013, "msg": getErrMsgByCode(18026013, None)}, content_type="application/json")
    else:
        userName = reqBody["userName"]
        registerData["userName"]=userName

    if "phone" not in reqBody:
        return Response({"result": 18026014, "msg": getErrMsgByCode(18026014, None)}, content_type="application/json")
    else:
        phone = reqBody["phone"]
        registerData["phone"]=phone

    if "lat" in reqBody:
        lat = reqBody["lat"]
        registerData["lat"] = lat

    if "lng" in reqBody:
        lng = reqBody["lng"]
        registerData["lng"] = lng

    if "additionalAddress" in reqBody:
        additionalAddress = reqBody["additionalAddress"]
        registerData["additionalAddress"] = additionalAddress

    if "streetName" in reqBody:
        streetName = reqBody["streetName"]
        registerData["streetName"] = streetName

    if "communityNam" in reqBody:
        communityNam = reqBody["communityNam"]
        registerData["communityNam"] = communityNam

    if "gridName" in reqBody:
        gridName = reqBody["gridName"]
        registerData["gridName"] = gridName

    if "imageUrl" in reqBody:
        imageUrl = reqBody["imageUrl"]
        registerData["imageUrl"] = imageUrl

    if "message" in reqBody:
        message = reqBody["message"]
        registerData["message"] = message

    try:


        response = requests.post(url="http://218.17.164.124:10087/tyfb-api/eventFlow/eventUpload",params=registerData)

        resultData = json.loads(response.text)
    except Exception as err:
        return Response({"result": 18026015, "msg": getErrMsgByCode(18026015, err)}, content_type="application/json")

    if resultData["flag"]:
        return Response({"result": 0, "msg": "OK"}, content_type="application/json")
    else:
        return Response({"result": 18026016, "msg": getErrMsgByCode(18026016, None)}, content_type="application/json")

@csrf_exempt
@api_view(["post"])
def administrationPunishInfoadd(request):
    """
行政处罚信息新增
    """
    try:
        reqBody = json.loads(request.body)
    except Exception as err:
        return Response({"result": 18027001, "msg": getErrMsgByCode(18027001, err)}, content_type="application/json")

    if reqbody_verify_admin(reqBody, err_code=18027001) is None:
        pass
    else:
        return reqbody_verify_admin(reqBody, err_code=18027001)

    if "administration_name" not in reqBody:
        return Response({"result": 18027006, "msg": getErrMsgByCode(18027006, None)}, content_type="application/json")
    else:
        administration_name = reqBody["administration_name"]

    if "administration_type" not in reqBody:
        return Response({"result": 18027007, "msg": getErrMsgByCode(18027007, None)}, content_type="application/json")
    else:
        administration_type = reqBody["administration_type"]

    if "administration_punish_number" not in reqBody:
        return Response({"result": 18027008, "msg": getErrMsgByCode(18027008, None)}, content_type="application/json")
    else:
        administration_punish_number = reqBody["administration_punish_number"]

    if "lllegal_type" not in reqBody:
        return Response({"result": 18027009, "msg": getErrMsgByCode(18027009, None)}, content_type="application/json")
    else:
        lllegal_type = reqBody["lllegal_type"]

    if "lllegal_fact" not in reqBody:
        return Response({"result": 18027010, "msg": getErrMsgByCode(18027010, None)}, content_type="application/json")
    else:
        lllegal_fact = reqBody["lllegal_fact"]

    if "punishment_basis" not in reqBody:
        return Response({"result": 18027011, "msg": getErrMsgByCode(18027011, None)}, content_type="application/json")
    else:
        punishment_basis = reqBody["punishment_basis"]

    if "punishment_type" not in reqBody:
        return Response({"result": 18027012, "msg": getErrMsgByCode(18027012, None)}, content_type="application/json")
    else:
        punishment_type = reqBody["punishment_type"]

    if "punishment_content" not in reqBody:
        return Response({"result": 18027013, "msg": getErrMsgByCode(18027013, None)}, content_type="application/json")
    else:
        punishment_content = reqBody["punishment_content"]

    if "punish_date" not in reqBody:
        return Response({"result": 18027014, "msg": getErrMsgByCode(18027014, None)}, content_type="application/json")
    else:
        punish_date = reqBody["punish_date"]

    if "punish_valid_date" not in reqBody:
        return Response({"result": 18027015, "msg": getErrMsgByCode(18027015, None)}, content_type="application/json")
    else:
        punish_valid_date = reqBody["punish_valid_date"]

    if "penalty_authorities" not in reqBody:
        return Response({"result": 18027016, "msg": getErrMsgByCode(18027016, None)}, content_type="application/json")
    else:
        penalty_authorities = reqBody["penalty_authorities"]

    if "penalty_authorities_code" not in reqBody:
        return Response({"result": 18027017, "msg": getErrMsgByCode(18027017, None)}, content_type="application/json")
    else:
        penalty_authorities_code = reqBody["penalty_authorities_code"]

    if "data_source" not in reqBody:
        return Response({"result": 18027018, "msg": getErrMsgByCode(18027018, None)}, content_type="application/json")
    else:
        data_source = reqBody["data_source"]

    if "data_source_code" not in reqBody:
        return Response({"result": 18027019, "msg": getErrMsgByCode(18027019, None)}, content_type="application/json")
    else:
        data_source_code = reqBody["data_source_code"]

    administration_code_1=None
    administration_code_2=None
    administration_code_3=None
    administration_code_4=None
    administration_code_5=None
    administration_code_6=None
    legal_representative=None
    certificates_type=None
    certificates_number=None
    fine_money=None
    confiscate_money=None
    Revocation_licence=None
    deadline_publicity=None

    if "administration_code_1"  in reqBody:
        administration_code_1 = reqBody["administration_code_1"]

    if "administration_code_2"  in reqBody:
        administration_code_2 = reqBody["administration_code_2"]

    if "administration_code_3"  in reqBody:
        administration_code_3 = reqBody["administration_code_3"]

    if "administration_code_4"  in reqBody:
        administration_code_4 = reqBody["administration_code_4"]

    if "administration_code_5"  in reqBody:
        administration_code_5 = reqBody["administration_code_5"]

    if "administration_code_6" in reqBody:
        administration_code_6 = reqBody["administration_code_6"]

    if "legal_representative" in reqBody:
        legal_representative = reqBody["legal_representative"]

    if "certificates_type" in reqBody:
        certificates_type = reqBody["certificates_type"]

    if "certificates_number" in reqBody:
        certificates_number = reqBody["certificates_number"]

    if "fine_money" in reqBody:
        fine_money = reqBody["fine_money"]

    if "confiscate_money" in reqBody:
        confiscate_money = reqBody["confiscate_money"]

    if "Revocation_licence" in reqBody:
        Revocation_licence = reqBody["Revocation_licence"]

    if "deadline_publicity" in reqBody:
        deadline_publicity = reqBody["deadline_publicity"]

    administrationObj=administrationPunishInfoDB()
    administrationObj.administration_name=administration_name
    administrationObj.administration_type=administration_type
    administrationObj.administration_code_1=administration_code_1
    administrationObj.administration_code_2=administration_code_2
    administrationObj.administration_code_3=administration_code_3
    administrationObj.administration_code_4=administration_code_4
    administrationObj.administration_code_5=administration_code_5
    administrationObj.administration_code_6=administration_code_6
    administrationObj.legal_representative=legal_representative
    administrationObj.certificates_type=certificates_type
    administrationObj.certificates_number=certificates_number
    administrationObj.administration_punish_number=administration_punish_number
    administrationObj.lllegal_type=lllegal_type
    administrationObj.lllegal_fact=lllegal_fact
    administrationObj.punishment_basis=punishment_basis
    administrationObj.punishment_type=punishment_type
    administrationObj.punishment_content=punishment_content
    administrationObj.fine_money=fine_money
    administrationObj.confiscate_money=confiscate_money
    administrationObj.Revocation_licence=Revocation_licence
    administrationObj.punish_date=punish_date
    administrationObj.punish_valid_date=punish_valid_date
    administrationObj.deadline_publicity=deadline_publicity
    administrationObj.penalty_authorities=penalty_authorities
    administrationObj.penalty_authorities_code=penalty_authorities_code
    administrationObj.data_source=data_source
    administrationObj.data_source_code=data_source_code


    try:
        administrationObj.save()

    except Exception as err:
        Response({"result": 18027020, "msg": getErrMsgByCode(18027020, err)}, content_type="application/json")

    return Response({"result": 0, "msg": "OK"}, content_type="application/json")


@csrf_exempt
@api_view(["post"])
def administrationPunishInfoModify(request):
    """
    行政处罚信息修改
    """
    try:
        reqBody = json.loads(request.body)
    except Exception as err:
        return Response({"result": 18028001, "msg": getErrMsgByCode(18028001, err)}, content_type="application/json")

    if reqbody_verify_admin(reqBody, err_code=18028001) is None:
        pass
    else:
        return reqbody_verify_admin(reqBody, err_code=18028001)

    if "id" not in reqBody:
        return Response({"result": 18028006, "msg": getErrMsgByCode(18028006, None)}, content_type="application/json")
    else:
        infoID = reqBody["id"]

    administration_name=None
    administration_type=None
    administration_code_1=None
    administration_code_2=None
    administration_code_3=None
    administration_code_4=None
    administration_code_5=None
    administration_code_6=None
    legal_representative=None
    certificates_type=None
    certificates_number=None
    administration_punish_number=None
    lllegal_type=None
    lllegal_fact=None
    punishment_basis=None
    punishment_type=None
    punishment_content=None
    fine_money=None
    confiscate_money=None
    Revocation_licence=None
    punish_date=None
    punish_valid_date=None
    deadline_publicity=None
    penalty_authorities=None
    penalty_authorities_code=None
    data_source=None
    data_source_code=None

    if "administration_name" in reqBody:
        administration_name = reqBody["administration_name"]

    if "administration_type" in reqBody:
        administration_type = reqBody["administration_type"]

    if "administration_code_1" in reqBody:
        administration_code_1 = reqBody["administration_code_1"]

    if "administration_code_2" in reqBody:
        administration_code_2 = reqBody["administration_code_2"]

    if "administration_code_3" in reqBody:
        administration_code_3 = reqBody["administration_code_3"]

    if "administration_code_4" in reqBody:
        administration_code_4 = reqBody["administration_code_4"]

    if "administration_code_5" in reqBody:
        administration_code_5 = reqBody["administration_code_5"]

    if "administration_code_6" in reqBody:
        administration_code_6 = reqBody["administration_code_6"]

    if "legal_representative" in reqBody:
        legal_representative = reqBody["legal_representative"]

    if "certificates_type" in reqBody:
        certificates_type = reqBody["certificates_type"]

    if "certificates_number" in reqBody:
        certificates_number = reqBody["certificates_number"]

    if "administration_punish_number" in reqBody:
        administration_punish_number = reqBody["administration_punish_number"]

    if "lllegal_type" in reqBody:
        lllegal_type = reqBody["lllegal_type"]

    if "lllegal_fact" in reqBody:
        lllegal_fact = reqBody["lllegal_fact"]

    if "punishment_basis" in reqBody:
        punishment_basis = reqBody["punishment_basis"]

    if "punishment_type" in reqBody:
        punishment_type = reqBody["punishment_type"]

    if "punishment_content" in reqBody:
        punishment_content = reqBody["punishment_content"]

    if "fine_money" in reqBody:
        fine_money = reqBody["fine_money"]

    if "confiscate_money" in reqBody:
        confiscate_money = reqBody["confiscate_money"]

    if "Revocation_licence" in reqBody:
        Revocation_licence = reqBody["Revocation_licence"]

    if "punish_date" in reqBody:
        punish_date = reqBody["punish_date"]

    if "punish_valid_date" in reqBody:
        punish_valid_date = reqBody["punish_valid_date"]

    if "deadline_publicity" in reqBody:
        deadline_publicity = reqBody["deadline_publicity"]

    if "penalty_authorities" in reqBody:
        penalty_authorities = reqBody["penalty_authorities"]

    if "penalty_authorities_code" in reqBody:
        penalty_authorities_code = reqBody["penalty_authorities_code"]

    if "data_source" in reqBody:
        data_source = reqBody["data_source"]

    if "data_source_code" in reqBody:
        data_source_code = reqBody["data_source_code"]

    try:
        administrationObj=administrationPunishInfoDB.objects.get(id=infoID)
    except Exception as err:
        return Response({"result": 18028007, "msg": getErrMsgByCode(18028007, err)}, content_type="application/json")

    if administration_name is not None:
        administrationObj.administration_name = administration_name

    if administration_type is not None:
        administrationObj.administration_type = administration_type

    if administration_code_2 is not None:
        administrationObj.administration_code_2 = administration_code_2

    if administration_code_3 is not None:
        administrationObj.administration_code_3 = administration_code_3

    if administration_code_4 is not None:
        administrationObj.administration_code_4 = administration_code_4

    if administration_code_5 is not None:
        administrationObj.administration_code_5 = administration_code_5

    if administration_code_6 is not None:
        administrationObj.administration_code_6 = administration_code_6

    if administration_code_1 is not None:
        administrationObj.administration_code_1 = administration_code_1

    if legal_representative is not None:
        administrationObj.legal_representative = legal_representative

    if certificates_type is not None:
        administrationObj.certificates_type = certificates_type

    if certificates_number is not None:
        administrationObj.certificates_number = certificates_number

    if administration_punish_number is not None:
        administrationObj.administration_punish_number = administration_punish_number

    if lllegal_type is not None:
        administrationObj.lllegal_type = lllegal_type

    if lllegal_fact is not None:
        administrationObj.lllegal_fact = lllegal_fact

    if punishment_basis is not None:
        administrationObj.punishment_basis = punishment_basis

    if punishment_type is not None:
        administrationObj.punishment_type = punishment_type

    if punishment_content is not None:
        administrationObj.punishment_content = punishment_content

    if fine_money is not None:
        administrationObj.fine_money = fine_money

    if confiscate_money is not None:
        administrationObj.confiscate_money = confiscate_money

    if Revocation_licence is not None:
        administrationObj.Revocation_licence = Revocation_licence

    if punish_date is not None:
        administrationObj.punish_date = punish_date

    if punish_valid_date is not None:
        administrationObj.punish_valid_date = punish_valid_date

    if deadline_publicity is not None:
        administrationObj.deadline_publicity = deadline_publicity

    if penalty_authorities is not None:
        administrationObj.penalty_authorities = penalty_authorities

    if penalty_authorities_code is not None:
        administrationObj.penalty_authorities_code = penalty_authorities_code

    if data_source is not None:
        administrationObj.data_source = data_source

    if data_source_code is not None:
        administrationObj.data_source_code = data_source_code

    try:
        administrationObj.save()
    except Exception as err:
        return Response({"result": 18028008, "msg": getErrMsgByCode(18028008, err)}, content_type="application/json")

    return Response({"result": 0, "msg": "OK"}, content_type="application/json")

@csrf_exempt
@api_view(["post"])
def administrationPunishInfoQuery(request):
    """
    行政处罚信息查询
    """
    print(format(request.body))
    try:
        reqBody = json.loads(request.body)
    except Exception as err:
        return Response({"result": 18029001, "msg": getErrMsgByCode(18029001, err)}, content_type="application/json")

    if reqbody_verify(reqBody, err_code=18029001) is None:
        pass
    else:
        return reqbody_verify(reqBody, err_code=18029001)

    indexPage = None
    countInfo = None



    if "page" in reqBody:
        indexPage = reqBody["page"]

    if "count" in reqBody:
        countInfo = reqBody["count"]

    try:
        administrationObj=administrationPunishInfoDB.objects.all()
        resData={}
        resultInfoList = []
        for item in administrationObj:
            infoObj={}
            infoObj["id"]=item.id
            infoObj["administration_name"]=item.administration_name
            infoObj["administration_type"]=item.administration_type
            infoObj["administration_code_1"]=item.administration_code_1
            infoObj["administration_code_2"]=item.administration_code_2
            infoObj["administration_code_3"]=item.administration_code_3
            infoObj["administration_code_4"]=item.administration_code_4
            infoObj["administration_code_5"]=item.administration_code_5
            infoObj["administration_code_6"]=item.administration_code_6
            infoObj["legal_representative"]=item.legal_representative
            infoObj["certificates_type"]=item.certificates_type
            infoObj["certificates_number"]=item.certificates_number
            infoObj["administration_punish_number"]=item.administration_punish_number
            infoObj["lllegal_type"]=item.lllegal_type
            infoObj["lllegal_fact"]=item.lllegal_fact
            infoObj["punishment_basis"]=item.punishment_basis
            infoObj["punishment_type"]=item.punishment_type
            infoObj["punishment_content"]=item.punishment_content
            infoObj["fine_money"]=item.fine_money
            infoObj["confiscate_money"]=item.confiscate_money
            infoObj["Revocation_licence"]=item.Revocation_licence
            infoObj["punish_date"]=item.punish_date
            infoObj["punish_valid_date"]=item.punish_valid_date
            infoObj["deadline_publicity"]=item.deadline_publicity
            infoObj["penalty_authorities"]=item.penalty_authorities
            infoObj["penalty_authorities_code"]=item.penalty_authorities_code
            infoObj["data_source"]=item.data_source
            infoObj["data_source_code"]=item.data_source_code
            resultInfoList.append(infoObj)

        if indexPage and countInfo:
            indexStart = (indexPage - 1) * countInfo

            if indexStart < 0:
                indexStart = 0

            indexEnd = indexStart + countInfo

            if indexEnd >= administrationObj.count():
                indexEnd = administrationObj.count()

            resultInfoList = resultInfoList[indexStart:indexEnd]
        else:
            resultInfoList = resultInfoList

        resData["info"] = resultInfoList
    except Exception as err:
        return Response({"result": 18029006, "msg": getErrMsgByCode(18029006, err)}, content_type="application/json")

    resData["total"] = administrationObj.count()
    return Response({"result": 0, "msg": "OK", "data": resData}, content_type="application/json")



@csrf_exempt
@api_view(["post"])
def administrationPunishInfoDelete(request):
    """
    行政处罚信息删除
    """
    try:
        reqBody = json.loads(request.body)
    except Exception as err:
        return Response({"result": 18030001, "msg": getErrMsgByCode(18030001, err)}, content_type="application/json")

    if reqbody_verify_admin(reqBody, err_code=18030001) is None:
        pass
    else:
        return reqbody_verify_admin(reqBody, err_code=18030001)

    if "id" not in reqBody:
        return Response({"result": 18030006, "msg": getErrMsgByCode(18030006, None)}, content_type="application/json")
    else:
        infoID = reqBody["id"]

    try:
        administrationObj=administrationPunishInfoDB.objects.get(id=infoID)
    except Exception as err:
        return Response({"result": 18030007, "msg": getErrMsgByCode(18030007, err)}, content_type="application/json")

    try:
        administrationObj.delete()
    except Exception as err:
        return Response({"result": 18030008, "msg": getErrMsgByCode(18030008, err)}, content_type="application/json")

    return Response({"result": 0, "msg": "OK"}, content_type="application/json")


@csrf_exempt
@api_view(["post"])
def administrationPunishInfoBatchadd(request):
    """
行政处罚信息批量新增
    """
    try:
        reqBodys = json.loads(request.body)
    except Exception as err:
        return Response({"result": 18031001, "msg": getErrMsgByCode(18031001, err)}, content_type="application/json")

    if reqbody_verify_admin(reqBodys, err_code=18031001) is None:
        pass
    else:
        return reqbody_verify_admin(reqBodys, err_code=18031001)

    if "infoList" not in reqBodys:
        return Response({"result": 18031021, "msg": getErrMsgByCode(18031021, None)}, content_type="application/json")
    else:
        infoList = reqBodys["infoList"]

    savePoint = transaction.savepoint()

    for reqBody in infoList:

        if "administration_name" not in reqBody:
            return Response({"result": 18031006, "msg": getErrMsgByCode(18031006, None)}, content_type="application/json")
        else:
            administration_name = reqBody["administration_name"]

        if "administration_type" not in reqBody:
            return Response({"result": 18031007, "msg": getErrMsgByCode(18031007, None)}, content_type="application/json")
        else:
            administration_type = reqBody["administration_type"]

        if "administration_punish_number" not in reqBody:
            return Response({"result": 18031008, "msg": getErrMsgByCode(18031008, None)}, content_type="application/json")
        else:
            administration_punish_number = reqBody["administration_punish_number"]

        if "lllegal_type" not in reqBody:
            return Response({"result": 18031009, "msg": getErrMsgByCode(18031009, None)}, content_type="application/json")
        else:
            lllegal_type = reqBody["lllegal_type"]

        if "lllegal_fact" not in reqBody:
            return Response({"result": 18031010, "msg": getErrMsgByCode(18031010, None)}, content_type="application/json")
        else:
            lllegal_fact = reqBody["lllegal_fact"]

        if "punishment_basis" not in reqBody:
            return Response({"result": 18031011, "msg": getErrMsgByCode(18031011, None)}, content_type="application/json")
        else:
            punishment_basis = reqBody["punishment_basis"]

        if "punishment_type" not in reqBody:
            return Response({"result": 18031012, "msg": getErrMsgByCode(18031012, None)}, content_type="application/json")
        else:
            punishment_type = reqBody["punishment_type"]

        if "punishment_content" not in reqBody:
            return Response({"result": 18031013, "msg": getErrMsgByCode(18031013, None)}, content_type="application/json")
        else:
            punishment_content = reqBody["punishment_content"]

        if "punish_date" not in reqBody:
            return Response({"result": 18031014, "msg": getErrMsgByCode(18031014, None)}, content_type="application/json")
        else:
            punish_date = reqBody["punish_date"]

        if "punish_valid_date" not in reqBody:
            return Response({"result": 18031015, "msg": getErrMsgByCode(18031015, None)}, content_type="application/json")
        else:
            punish_valid_date = reqBody["punish_valid_date"]

        if "penalty_authorities" not in reqBody:
            return Response({"result": 18031016, "msg": getErrMsgByCode(18031016, None)}, content_type="application/json")
        else:
            penalty_authorities = reqBody["penalty_authorities"]

        if "penalty_authorities_code" not in reqBody:
            return Response({"result": 18031017, "msg": getErrMsgByCode(18031017, None)}, content_type="application/json")
        else:
            penalty_authorities_code = reqBody["penalty_authorities_code"]

        if "data_source" not in reqBody:
            return Response({"result": 18031018, "msg": getErrMsgByCode(18031018, None)}, content_type="application/json")
        else:
            data_source = reqBody["data_source"]

        if "data_source_code" not in reqBody:
            return Response({"result": 18031019, "msg": getErrMsgByCode(18031019, None)}, content_type="application/json")
        else:
            data_source_code = reqBody["data_source_code"]

        administration_code_1=None
        administration_code_2=None
        administration_code_3=None
        administration_code_4=None
        administration_code_5=None
        administration_code_6=None
        legal_representative=None
        certificates_type=None
        certificates_number=None
        fine_money=None
        confiscate_money=None
        Revocation_licence=None
        deadline_publicity=None

        if "administration_code_1"  in reqBody:
            administration_code_1 = reqBody["administration_code_1"]

        if "administration_code_2"  in reqBody:
            administration_code_2 = reqBody["administration_code_2"]

        if "administration_code_3"  in reqBody:
            administration_code_3 = reqBody["administration_code_3"]

        if "administration_code_4"  in reqBody:
            administration_code_4 = reqBody["administration_code_4"]

        if "administration_code_5"  in reqBody:
            administration_code_5 = reqBody["administration_code_5"]

        if "administration_code_6" in reqBody:
            administration_code_6 = reqBody["administration_code_6"]

        if "legal_representative" in reqBody:
            legal_representative = reqBody["legal_representative"]

        if "certificates_type" in reqBody:
            certificates_type = reqBody["certificates_type"]

        if "certificates_number" in reqBody:
            certificates_number = reqBody["certificates_number"]

        if "fine_money" in reqBody:
            fine_money = reqBody["fine_money"]

        if "confiscate_money" in reqBody:
            confiscate_money = reqBody["confiscate_money"]

        if "Revocation_licence" in reqBody:
            Revocation_licence = reqBody["Revocation_licence"]

        if "deadline_publicity" in reqBody:
            deadline_publicity = reqBody["deadline_publicity"]

        administrationObj=administrationPunishInfoDB()
        administrationObj.administration_name=administration_name
        administrationObj.administration_type=administration_type
        administrationObj.administration_code_1=administration_code_1
        administrationObj.administration_code_2=administration_code_2
        administrationObj.administration_code_3=administration_code_3
        administrationObj.administration_code_4=administration_code_4
        administrationObj.administration_code_5=administration_code_5
        administrationObj.administration_code_6=administration_code_6
        administrationObj.legal_representative=legal_representative
        administrationObj.certificates_type=certificates_type
        administrationObj.certificates_number=certificates_number
        administrationObj.administration_punish_number=administration_punish_number
        administrationObj.lllegal_type=lllegal_type
        administrationObj.lllegal_fact=lllegal_fact
        administrationObj.punishment_basis=punishment_basis
        administrationObj.punishment_type=punishment_type
        administrationObj.punishment_content=punishment_content
        administrationObj.fine_money=fine_money
        administrationObj.confiscate_money=confiscate_money
        administrationObj.Revocation_licence=Revocation_licence
        administrationObj.punish_date=punish_date
        administrationObj.punish_valid_date=punish_valid_date
        administrationObj.deadline_publicity=deadline_publicity
        administrationObj.penalty_authorities=penalty_authorities
        administrationObj.penalty_authorities_code=penalty_authorities_code
        administrationObj.data_source=data_source
        administrationObj.data_source_code=data_source_code


        try:
            administrationObj.save()

        except Exception as err:
            transaction.savepoint_rollback(savePoint)
            Response({"result": 18031020, "msg": getErrMsgByCode(18031020, err)}, content_type="application/json")

    transaction.savepoint_commit(savePoint)

    return Response({"result": 0, "msg": "OK"}, content_type="application/json")