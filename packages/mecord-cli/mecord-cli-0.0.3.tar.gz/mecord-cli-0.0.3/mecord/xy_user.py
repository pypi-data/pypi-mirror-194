import base64
import time
import signal
import threading
import qrcode_terminal

from mecord import store 
from mecord import xy_pb 
from mecord import utils 

def singleton(cls):
    _instance = {}

    def inner():
        if cls not in _instance:
            _instance[cls] = cls()
        return _instance[cls]
    return inner

@singleton
class User(object):
    logined = False
    login_data = None

    def __init__(self):
        self.checkLoginStatus()

    def checkLoginStatus(self):
        if store.uid() and store.token():
            self.logined = True
            return True
        self.logined = False        
        
    def isLogin(self):
        self.checkLoginStatus()
        return self.logined
    
    def logout(self):
        store.clear()
        self.logined = False

    def loginIfNeed(self):
        self.checkLoginStatus()
            
        if self.isLogin() == False:
            #need login
            logincode = xy_pb.GetQrcodeLoginCode()
            if logincode:
                logincode_encoded = base64.b64encode(bytes(logincode, 'utf-8')).decode('utf-8').replace("==","fuckEqual")
                uuid = utils.generate_unique_id()
                qrcode = f"https://main_page.html?action=scan&code={logincode_encoded}&deviceCode=143383612&deviceId={uuid}"
                # utils.displayQrcode(qrcode)
                # qrcode_terminal.draw(qrcode)
                print(qrcode)
                utils.displayQRcodeOnTerminal(qrcode)
                self.checkLoginComplate(logincode)


    def checkLoginComplate(self, qrcode):
        print("loop check login~~~")
        rst = xy_pb.CheckLoginLoop(qrcode)
        if rst == 1: #success
            print("login success")
            self.logined = True
        elif rst == -1:
            threading.Timer(1, self.checkLoginComplate, (qrcode, )).start()
        else: #fail
            print("login fail !!!")