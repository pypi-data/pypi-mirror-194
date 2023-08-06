import os
import json
import sys
import shutil
import zipfile
import pkg_resources
import threading

from pathlib import Path
from mecord import xy_pb
from mecord import upload
from mecord import utils

h5_name = "h5"
script_name = "script"
def GetWidgetConfig(path):
    #search h5 folder first, netxt search this folder
    if os.path.exists(os.path.join(path, h5_name)):
        for filename in os.listdir(os.path.join(path, h5_name)):
            pathname = os.path.join(path, h5_name, filename) 
            if (os.path.isfile(pathname)) and filename == "config.json":
                with open(pathname, 'r') as f:
                    return json.load(f)
            
    for filename in os.listdir(path):
        pathname = os.path.join(path, filename) 
        if (os.path.isfile(pathname)) and filename == "config.json":
            with open(pathname, 'r') as f:
                return json.load(f)
    return {}

def configInFolder(path):
    for filename in os.listdir(path):
        pathname = os.path.join(path, filename) 
        if (os.path.isfile(pathname)) and filename == "config.json":
            return True
    return False

def PathIsEmpty(path):
    return len(os.listdir(path)) == 0

def replaceIfNeed(dstDir, name, subfix):
    newsubfix = subfix + ".py"
    if name.find(newsubfix) != -1:
        os.rename(os.path.join(dstDir, name), os.path.join(dstDir, name.replace(newsubfix, subfix)))

def copyWidgetTemplate(name, dirname):
    cwd = os.getcwd()
    templateDir = os.path.join(os.path.dirname(os.path.abspath(__file__)), name)#sys.prefix
    dstDir = os.path.join(cwd, dirname)
    shutil.copytree(templateDir, dstDir)
    shutil.rmtree(os.path.join(dstDir, "__pycache__"))
    os.remove(os.path.join(dstDir, "__init__.py"))
    for filename in os.listdir(dstDir):
        replaceIfNeed(dstDir, filename, ".json")
        replaceIfNeed(dstDir, filename, ".png")
        replaceIfNeed(dstDir, filename, ".html")

def createWidget():
    cwd = os.getcwd()
    if PathIsEmpty(cwd) == False:
        print("current folder is not empty, create widget fail!")
        return
        
    widgetid = xy_pb.CreateWidgetUUID()
    if len(widgetid) == 0:
        print("create fail! mecord server is not avalid")
        return
    
    copyWidgetTemplate("widget_template", h5_name)
    copyWidgetTemplate("script_template", script_name)
    #h5
    data = GetWidgetConfig(cwd)
    data["widget_id"] = widgetid
    data["cmd"] = os.path.join(cwd, script_name, "main.py")
    with open(os.path.join(cwd, h5_name, "config.json"), 'w') as f:
        json.dump(data, f)
    print("create widget success")

def CheckWidgetDataInPath(path):
    data = GetWidgetConfig(path)
    if "widget_id" in data:
        widget_id = data["widget_id"]
        if len(widget_id) == 0:
            print("widget_id is empty!")
            return False
    
    if "cmd" in data:
        cmd = data["cmd"]
        if os.path.exists(cmd) == False:
            print("cmd file not found!")
            return False

    return True


def publishWidget():
    cwd = os.getcwd()
    if CheckWidgetDataInPath(cwd) == False:
        return
        
    data = GetWidgetConfig(cwd)
    widget_id = data["widget_id"]

    distname = utils.generate_unique_id() + "_" + widget_id
    dist = os.path.join(os.path.dirname(cwd), distname + ".zip")
    zip = zipfile.ZipFile(dist, "w", zipfile.ZIP_DEFLATED) 

    #h5 folder
    package_folder = ""
    if configInFolder(cwd):
        package_folder = cwd
    elif configInFolder(os.path.join(cwd, h5_name)):
        package_folder = os.path.join(cwd, h5_name)

    for root,dirs,files in os.walk(package_folder):
        for file in files:
            if str(file).startswith("~$"):
                continue
            filepath = os.path.join(root, file)
            writepath = os.path.relpath(filepath, package_folder)
            zip.write(filepath, writepath)
    zip.close()

    (ossurl, checkid) = upload.uploadUseOss(dist, widget_id)
    print("=====================   " + ossurl)
    checkUploadComplate(checkid, dist)

def checkUploadComplate(checkid, dist):
        print("loop check upload task ~~~")
        rst = xy_pb.UploadWidgetCheck(checkid)
        if rst == 1: #success
            print("publish widget success")
            # xy_pb.UploadWidget(widget_id, ossurl)
            os.remove(dist)
        elif rst == -1:
            threading.Timer(1, checkUploadComplate, (checkid, dist, )).start()
        else: #fail
            return