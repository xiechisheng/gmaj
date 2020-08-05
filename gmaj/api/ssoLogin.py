import datetime
from django_cas_ng.views import LoginView
from django.http import HttpResponseRedirect
from rest_framework.response import Response
from api.public import tokenEncode
from api.models import user_info as userDB


def getSSOToken(userLogin):
    try:
        userObj = userDB.objects.get(login=userLogin)
    except Exception as err:
        return None

    strTime = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    tokenValue = tokenEncode({"id": userObj.id, "login": userObj.login, "role": userObj.role, "dept": userObj.dept, "time": strTime})

    return tokenValue


class ssoLoginView(LoginView):
    def successful_login(self, request, next_page):
        """
        This method is called on successful login. Override this method for
        custom post-auth actions (i.e, to add a cookie with a token).

        :param request:
        :param next_page:
        :return:
        """
        print("test----------------------------------")
        print(format(next_page))
        print(format(request))
        userToken = getSSOToken(request.user.get_username())
        if userToken is None:
            return HttpResponseRedirect(next_page)

        response = HttpResponseRedirect(next_page)
        response.set_cookie("gmaj_token", userToken)
        response.delete_cookie("sessionid")

        return response

