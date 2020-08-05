import hashlib
from django.core.cache import cache
from django.core import signing
from rest_framework.response import Response
from django.conf import settings


def setValueToCache(strKey, strValue):
    """
    缓存信息--设置
    :return:
    """
    try:
        cache.set(strKey, strValue, settings.TOKEN_TIME_OUT)
    except Exception as err:
        return False
    else:
        return True


def mysql_password(str):
    """
    Mysql密码--编码
    :return:
    """
    value = hashlib.sha1(str.encode(encoding="UTF-8", errors="strict")).digest()
    value = hashlib.sha1(value).hexdigest()

    pwdStr = "*" + value.upper()

    return pwdStr


def tokenEncode(objDict):
    """
    Token信息--编码
    :return:
    """
    try:
        tokenValue = signing.dumps(objDict)
        cache.set(objDict["login"], tokenValue, settings.TOKEN_TIME_OUT)
    except Exception as err:
        print(format(err))
        return None
    else:
        return tokenValue


def tokenDecode(objToken):
    """
    Token信息--解码
    :return:
    """
    try:
        src = signing.loads(objToken)
    except Exception as err:
        return None
    else:
        return src


def tokenQuery(login):
    """
    Token信息--查询
    :return:
    """
    try:
        tokenValue = cache.get(login)
    except Exception as err:
        return None
    else:
        return tokenValue


def tokenDelete(login):
    """
    Token信息--删除
    :return:
    """
    try:
        tokenValue = cache.get(login)
    except Exception as err:
        return False
    else:
        if tokenValue is None:
            return True
        else:
            cache.delete(login)
            return True


def reqbody_verify(reqBody, err_code):
    """
    请求体信息--验证
    :return:
    """
    if "token" not in reqBody:
        return Response({"result": err_code + 1, "msg": "缺少参数: token"}, content_type="application/json")
    else:
        logintoken = reqBody["token"]

    tokeninfo = tokenDecode(logintoken)

    if tokeninfo is None:
        return Response({"result": err_code + 2, "msg": "Token信息解析失败"}, content_type="application/json")

    tokencache = tokenQuery(tokeninfo["login"])

    if tokencache != logintoken:
        return Response({"result": err_code + 3, "msg": "账号未登录或登录超时"}, content_type="application/json")


def reqbody_verify_admin(reqBody, err_code):
    """
    请求体信息--管理员权限验证
    :return:
    """
    if "token" not in reqBody:
        return Response({"result": err_code + 1, "msg": "缺少参数: token"}, content_type="application/json")
    else:
        logintoken = reqBody["token"]

    tokeninfo = tokenDecode(logintoken)

    if tokeninfo is None:
        return Response({"result": err_code + 2, "msg": "Token信息解析失败"}, content_type="application/json")

    tokencache = tokenQuery(tokeninfo["login"])

    if tokencache != logintoken:
        return Response({"result": err_code + 3, "msg": "账号未登录或登录超时"}, content_type="application/json")

    if tokeninfo["role"] < 9:
        return Response({"result": err_code + 4, "msg": "没有管理员权限"}, content_type="application/json")

