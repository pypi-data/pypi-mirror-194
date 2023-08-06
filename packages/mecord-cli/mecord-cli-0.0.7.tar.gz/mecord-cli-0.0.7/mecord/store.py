import os
import json

def singleton(cls):
    _instance = {}

    def inner():
        if cls not in _instance:
            _instance[cls] = cls()
        return _instance[cls]
    return inner

@singleton
class Store(object):
    def __init__(self):
        self.path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data.json")
        
        if not os.path.exists(self.path):
            with open(self.path, 'w') as f:
                json.dump({}, f)
                
    def read(self):
        with open(self.path, 'r') as f:
            data = json.load(f)
            
        return data
    
    def write(self, data):
        with open(self.path, 'w') as f:
            json.dump(data, f)


def uid():
    sp = Store()
    login_data = sp.read()
    if "uid" in login_data:
        return login_data["uid"]
    else:
        return ""
    
def token():
    sp = Store()
    login_data = sp.read()
    if "token" in login_data:
        return login_data["token"]
    else:
        return ""
    
def clear():
    sp = Store()
    sp.write("{}")
    login_data = sp.read()