"""gmaj URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path

from api import dept as DeptApi
from api import user as UserApi
from api import RtspServer as RtspServer
from api import RtspDevice as RtspDevice
from api import option as OptionInfo
from api import operation as OperationInfo
from api import iotSystem as IOTSystemInfo
from api import InfoManage as InfoManage
from api import sms as smsManage


from django_cas_ng import views as casViews
from api.ssoLogin import ssoLoginView
from api import tests as testData


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/login', ssoLoginView.as_view(), name='cas_ng_login'),
    path('api/logout', casViews.LogoutView.as_view(), name='cas_ng_logout'),
    path('api/callback', casViews.CallbackView.as_view(), name='cas_ng_proxy_callback'),

    path('api/user/login', UserApi.userLogin, name="userLogin"),
    path("api/user/logout", UserApi.userLogout, name="userLogout"),
    path("api/user/logout", UserApi.userLogout, name="userLogout"),
    path("api/user/add", UserApi.userInfoAdd, name="userInfoAdd"),
    path("api/user/modify", UserApi.userInfoModify, name="userInfoModify"),
    path("api/user/query", UserApi.userInfoQuery, name="userInfoQuery"),
    path("api/user/delete", UserApi.userInfoDelete, name="userInfoDelete"),
    path("api/user/registered", UserApi.userAccountRegistered, name="userAccountRegistered"),

    path('api/dept/add', DeptApi.addDeptInfo, name="addDeptInfo"),
    path("api/dept/modify", DeptApi.modifyDeptInfo, name="modifyDeptInfo"),
    path("api/dept/query", DeptApi.queryDeptInfo, name="queryDeptInfo"),
    path("api/dept/member", DeptApi.queryDeptMember, name="queryDeptMember"),
    path("api/dept/delete", DeptApi.deleteDeptInfo, name="deleteDeptInfo"),
    path("api/dept/sub/sort", DeptApi.subDeptInfoSort, name="subDeptInfoSort"),

    path("api/rtsp/server/add", RtspServer.addRtspServerInfo, name="addRtspServerInfo"),
    path("api/rtsp/server/modify", RtspServer.modifyRtspServerInfo, name="modifyRtspServerInfo"),
    path("api/rtsp/server/query", RtspServer.queryRtspServerInfo, name="queryRtspServerInfo"),
    path("api/rtsp/server/delete", RtspServer.deleteRtspServerInfo, name="deleteRtspServerInfo"),

    # 路由--Rtsp设备模块
    path("api/rtsp/device/add", RtspDevice.rtspDeviceInfoAdd, name="rtspDeviceInfoAdd"),
    path("api/rtsp/device/modify", RtspDevice.rtspDeviceInfoModify, name="rtspDeviceInfoModify"),
    path("api/rtsp/device/query/dept", RtspDevice.rtspDeviceInfoQueryDept, name="rtspDeviceInfoQueryDept"),
    path("api/rtsp/device/query", RtspDevice.rtspDeviceInfoQuery, name="rtspDeviceInfoQuery"),
    path("api/rtsp/device/delete", RtspDevice.rtspDeviceInfoDelete, name="rtspDeviceInfoDelete"),
    path("api/rtsp/device/sort", RtspDevice.rtspDeviceInfoSort, name="rtspDeviceInfoSort"),
    path("api/rtsp/rolling/add", RtspDevice.rtspDeviceRollingAdd, name="rtspDeviceRollingAdd"),
    path("api/rtsp/rolling/query", RtspDevice.rtspDeviceRollingQuery, name="rtspDeviceRollingQuery"),
    path("api/rtsp/record/add", RtspDevice.rtspRecordInfoAdd, name="rtspRecordInfoAdd"),
    path("api/rtsp/record/query", RtspDevice.rtspRecordInfoQuery, name="rtspRecordInfoQuery"),

    # 路由--配置模块
    path("api/option/add", OptionInfo.addOptionInfo, name="addOptionInfo"),
    path("api/option/modify", OptionInfo.modifyOptionInfo, name="modifyOptionInfo"),
    path("api/option/query", OptionInfo.queryOptionInfo, name="queryOptionInfo"),
    path("api/option/delete", OptionInfo.deleteOptionInfo, name="deleteOptionInfo"),

    path("api/operation/log", OperationInfo.queryOperationInfo, name="queryOperationInfo"),

    path("api/iot/device/add", IOTSystemInfo.addIoTDeviceInfo, name="addIoTDeviceInfo"),
    path("api/iot/device/modify", IOTSystemInfo.modifyIoTDevicenfo, name="modifyIoTDevicenfo"),
    path("api/iot/device/query", IOTSystemInfo.queryIoTDeviceInfo, name="queryIoTDeviceInfo"),
    path("api/iot/device/delete", IOTSystemInfo.deleteIoTDeviceInfo, name="deleteIoTDeviceInfo"),
    path("api/iot/gas/query", IOTSystemInfo.queryGasDeviceValue, name="queryGasDeviceValue"),
    path("api/iot/warn/query", IOTSystemInfo.queryDeviceWarnValue, name="queryDeviceWarnValue"),
    path("api/iot/online/query", IOTSystemInfo.queryDeviceOnlineValue, name="queryDeviceOnlineValue"),
    path("api/iot/warn/query", IOTSystemInfo.queryDeviceWarnValue, name="queryDeviceWarnValue"),
    path("api/iot/plan/add", IOTSystemInfo.addGenericPlanInfo, name="addGenericPlanInfo"),
    path("api/iot/plan/modify", IOTSystemInfo.modifyGenericPlanInfo, name="modifyGenericPlanInfo"),
    path("api/iot/plan/query", IOTSystemInfo.queryGenericPlanInfo, name="queryGenericPlanInfo"),
    path("api/iot/plan/delete", IOTSystemInfo.deleteGenericPlanInfo, name="deleteGenericPlanInfo"),

    path("api/info/hazards/add", InfoManage.addHazardsInfo, name="addHazardsInfo"),
    path("api/info/hazards/modify", InfoManage.modifyHazardsInfo, name="modifyHazardsInfo"),
    path("api/info/hazards/query", InfoManage.queryHazardsInfo, name="queryHazardsInfo"),
    path("api/info/hazards/delete", InfoManage.deleteHazardsInfo, name="deleteHazardsInfo"),

    path("api/info/license/add", InfoManage.addAdminLicenseInfo, name="addAdminLicenseInfo"),
    path("api/info/license/modify", InfoManage.modifyAdminLicenseInfo, name="modifyAdminLicenseInfo"),
    path("api/info/license/query", InfoManage.queryAdminLicenseInfo, name="queryAdminLicenseInfo"),
    path("api/info/license/delete", InfoManage.deleteAdminLicenseInfo, name="deleteAdminLicenseInfo"),

    path("api/info/enterprise/add", InfoManage.addEnterpriseInfo, name="addEnterpriseInfo"),
    path("api/info/enterprise/modify", InfoManage.modifyEnterpriseInfo, name="modifyEnterpriseInfo"),
    path("api/info/enterprise/query", InfoManage.queryEnterpriseInfo, name="queryEnterpriseInfo"),
    path("api/info/enterprise/delete", InfoManage.deleteEnterpriseInfo, name="deleteEnterpriseInfo"),

    path("api/info/plan/add", InfoManage.addPlanInfo, name="addPlanInfo"),
    path("api/info/plan/modify", InfoManage.modifyPlanInfo, name="modifyPlanInfo"),
    path("api/info/plan/query", InfoManage.queryPlanInfo, name="queryPlanInfo"),
    path("api/info/plan/delete", InfoManage.deletePlanInfo, name="deletePlanInfo"),

    path("api/info/trouble/add", InfoManage.addTroubleInfo, name="addTroubleInfo"),
    path("api/info/trouble/modify", InfoManage.modifyTroubleInfo, name="modifyTroubleInfo"),
    path("api/info/trouble/query", InfoManage.queryTroubleInfo, name="queryTroubleInfo"),
    path("api/info/trouble/delete", InfoManage.deleteTroubleInfo, name="deleteTroubleInfo"),

    path("api/info/check/add", InfoManage.addCheckLogInfo, name="addCheckLogInfo"),
    path("api/info/check/modify", InfoManage.modifyCheckLogInfo, name="modifyCheckLogInfo"),
    path("api/info/check/query", InfoManage.queryCheckLogInfo, name="queryCheckLogInfo"),
    path("api/info/check/delete", InfoManage.deleteCheckLogInfo, name="deleteCheckLogInfo"),

    path("api/sms/send", smsManage.sendSMSInfo, name="sendSMSInfo"),
    path("api/sms/template/add", smsManage.addSMSTemplateInfo, name="addSMSTemplateInfo"),
    path("api/sms/template/modify", smsManage.modifyTemplateInfo, name="modifyTemplateInfo"),
    path("api/sms/template/query", smsManage.queryTemplateInfo, name="queryTemplateInfo"),
    path("api/sms/template/delete", smsManage.deleteTemplateInfo, name="deleteTemplateInfo"),
    path("api/sms/log/query", smsManage.querySMSLogInfo, name="querySMSLogInfo"),

    path("api/test/save/data", testData.saveJsonData, name="saveJsonData"),
    path("api/test/query/data", testData.getJsonData, name="getJsonData"),
]

