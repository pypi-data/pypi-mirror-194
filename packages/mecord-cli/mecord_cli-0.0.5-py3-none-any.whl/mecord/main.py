import sys

from mecord import utils
from mecord import xy_user
from mecord import mecord_service
from mecord import mecord_widget
from mecord import store

def service():
    if xy_user.User().isLogin() == False:
        print('please login first! \nUsage: mecord login')
        return

    command = sys.argv[2]
    service = mecord_service.MecordService()
    if command == 'start':
        if service.is_running():
            print('Service is already running.')
        else:
            print('Starting service...')
            service.start()
    elif command == 'stop':
        if not service.is_running():
            print('Service is not running.')
        else:
            print('Stopping service...')
            service.stop()
    elif command == 'restart':
        print('Restarting service...')
        service.restart()
    elif command == 'status':
        if service.is_running():
            print('Service is running.')
        else:
            print('Service is not running.')
    else:
        print("Unknown command:", command)
        print("Usage: python service.py [start|stop|restart|status]")
        
def widget():
    if xy_user.User().isLogin() == False:
        print('please login first! \nUsage: mecord login')
        return

    command = sys.argv[2] 
    if command == 'init':
        mecord_widget.createWidget()
    elif command == 'publish':
        mecord_widget.publishWidget()
    else:
        print("Unknown command:", command)
        print("Usage: python service.py [start|stop|restart|status]")
        
def deviceid():
    uuid = utils.generate_unique_id()
    utils.displayQrcode(uuid)
    print(uuid)

def login():
    usr = xy_user.User()
    if usr.isLogin():
        print('you are logined')
    else:
        usr.loginIfNeed()

def logout():
    usr = xy_user.User()
    usr.logout()
    print('logout success')

def fakeuser():
    sp = store.Store()
    data = sp.read()
    data["uid"] = "001"
    data["token"] = "002"
    data["nickname"] = "pengjun"
    data["icon"] = ""
    sp.write(data)

module_func = {
    "login": login,
    "logout": logout,
    "fakeuser": fakeuser,
    "widget": widget,
    "service": service,
    "deviceid": deviceid,
}

def main():
    module = sys.argv[1]
    if module in module_func:
        module_func[module]()
    else:
        print("Unknown command:", module)
        print("Usage: mecord [login|service|widget]")
        sys.exit(0)
        
if __name__ == '__main__':
    main()
