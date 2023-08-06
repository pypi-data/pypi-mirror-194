import os
import json
import sys
import shutil
import zipfile
import pkg_resources

from pathlib import Path
from mecord import xy_pb
from mecord import upload
from mecord import utils

h5_name = "h5"
script_name = "script"
def GetWidgetConfig(path):
    #search h5 folder first, netxt search this folder
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

def copytree(name, dirname):
    cwd = os.getcwd()
    templateDir = os.path.join(sys.prefix, name)
    shutil.copytree(templateDir, os.path.join(cwd, dirname))
    # for filename in os.listdir(templateDir):
    #     print("===============")
    #     print(os.path.join(templateDir, filename))
    #     print(os.path.join(cwd, dirname, filename) )
    #     print("===============")
    #     shutil.copy(os.path.join(templateDir, filename) , os.path.join(cwd, dirname, filename) )

def createWidget():
    cwd = os.getcwd()
    if PathIsEmpty(cwd) == False:
        print("current folder is not empty, create widget fail!")
        return
        
    widgetid = xy_pb.CreateWidgetUUID()
    if len(widgetid) == 0:
        print("create fail! mecord server is not avalid")
        return
    
    copytree("widget_template", h5_name)
    copytree("script_template", script_name)
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

    oss_path = upload.upload(dist)
    if xy_pb.UploadWidget(widget_id, oss_path) == False:
        print("publish fail!")
    os.remove(dist)
