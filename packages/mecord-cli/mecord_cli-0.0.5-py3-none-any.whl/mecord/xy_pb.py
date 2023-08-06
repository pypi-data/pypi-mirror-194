import json
import hashlib
import time
import requests

from mecord import uauth_common_pb2 
from mecord import uauth_ext_pb2 
from mecord import aigc_ext_pb2 
from mecord import rpcinput_pb2 
from mecord import store 
from mecord import utils 

uuid = utils.generate_unique_id()

def _aigc_post(request, function):
    return _post(url="https://mecord-beta.2tianxin.com/proxymsg", 
                 objStr="mecord.aigc.AigcExtObj", 
                 request=request, 
                 function=function)
    
def _common_post(request, function):
    return _post(url="https://beta.xiaohuxi.cn/proxymsg", 
                 objStr="mizacommon.uauth.AuthExtObj", 
                 request=request, 
                 function=function)
    
def _post(url, objStr, request, function):
    req = request.SerializeToString()
    opt = {
        "lang": "zh-Hans",
        "region": "CN",
        "appid": "80",
        "application": "mecord",
        "version": "1.0",
        "X-Token": store.token(),
        "uid": "1",
    }
    input_req = rpcinput_pb2.RPCInput(obj=objStr, func=function, req=req, opt=opt)
    res = requests.post(url=url, data=input_req.SerializeToString())
    pb_rsp = rpcinput_pb2.RPCOutput()
    pb_rsp.ParseFromString(res.content)
    if pb_rsp.ret == 0:
        return pb_rsp.rsp
    else:
        print(pb_rsp)
        return ""
    

def GetQrcodeLoginCode():
    req = uauth_ext_pb2.GetQrcodeLoginCodeReq()
    req.login_type = uauth_common_pb2.UauthLoginType.LT_QRCODE_SCAN
    req.device_type = uauth_common_pb2.UauthDeviceType.DT_WINDOWS_PC
    req.device_id = uuid
    req.u_meng_device_id = ""

    rsp = uauth_ext_pb2.GetQrcodeLoginCodeRes()
    rsp.ParseFromString(_common_post(req, "GetQrcodeLoginCode"))
    s = rsp.login_code
    return s

def CheckLoginLoop(code):
    req = uauth_ext_pb2.GetQrcodeLoginStatusReq()
    req.login_code = code
    req.device_id = uuid
    req.u_meng_device_id = ""

    rsp = uauth_ext_pb2.GetQrcodeLoginStatusRes()
    rsp.ParseFromString(_common_post(req, "GetQrcodeLoginStatus"))
    if rsp.status == uauth_ext_pb2.GetQrcodeLoginStatus.SUCCESS:
        sp = store.Store()
        data = sp.read()
        data["uid"] = rsp.commonSignInRes.user_id
        data["token"] = rsp.commonSignInRes.login_token
        data["nickname"] = rsp.userNickname
        data["icon"] = rsp.userIconUrl
        sp.write(data)
        return 1
    elif rsp.status == uauth_ext_pb2.GetQrcodeLoginStatus.EXPIRED or rsp.status == uauth_ext_pb2.GetQrcodeLoginStatus.CANCEL:
        return 0
    else:
        return -1
    
    
def GetTask():
    req = aigc_ext_pb2.GetTaskReq()
    req.DeviceKey = uuid
    req.limit = 1

    rsp = aigc_ext_pb2.GetTaskRes()
    rsp.ParseFromString(_aigc_post(req, "GetTask"))
    datas = []
    for it in rsp.list:
        datas.append({
            "taskUUID": it.taskUUID,
            "config": it.config,
            "data": it.data,
        })
    return datas

def TaskNotify(taskUUID, status, msg, data):
    req = aigc_ext_pb2.TaskNotifyReq()
    req.taskUUID = taskUUID
    if status:
        req.taskStatus = aigc_ext_pb2.TaskStatus.TS_Success
    else:
        req.taskStatus = aigc_ext_pb2.TaskStatus.TS_Failure
    req.failReason = msg
    req.data = data

    rsp = aigc_ext_pb2.TaskNotifyRes()
    rsp.ParseFromString(_aigc_post(req, "TaskNotify"))
    return True

# def RegisterDevice(groupid):
#     req = aigc_ext_pb2.RegisterDeviceReq()
#     req.deviceKey = uuid
#     req.groupId = groupid

#     rsp = aigc_ext_pb2.RegisterDeviceRes()
#     rsp.ParseFromString(_aigc_post(req, "RegisterDevice"))
#     return True

def CreateWidgetUUID():
    req = aigc_ext_pb2.CreateWidgetReq()
    rsp = aigc_ext_pb2.CreateWidgetRes()
    rsp.ParseFromString(_aigc_post(req, "CreateWidget"))
    return rsp.widgetUUID


def UploadWidget(widgetid, oss_path):
    req = aigc_ext_pb2.UploadWidgetReq()
    req.fileUrl = oss_path

    rsp = aigc_ext_pb2.UploadWidgetRes()
    rsp.ParseFromString(_aigc_post(req, "UploadWidget"))
    if rsp.widgetUUID:
        return True
    else:
        return False