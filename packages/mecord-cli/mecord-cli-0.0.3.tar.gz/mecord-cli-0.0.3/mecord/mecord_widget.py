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

def PathIsWidget(path):
    data = GetWidgetConfig(path)
    if "widget_id" in data and "group_id" in data and "cmd" in data:
        widget_id = data["widget_id"]
        group_id = data["group_id"]
        cmd = data["cmd"]
        if len(widget_id) > 0 and len(str(group_id)) > 0 and os.path.exists(cmd):
            return True
    return False

def GetWidgetConfig(path):
    for filename in os.listdir(path):
        pathname = os.path.join(path, filename) 
        if (os.path.isfile(pathname)) and filename == "config.json":
            with open(pathname, 'r') as f:
                return json.load(f)
    return {}

def PathIsEmpty(path):
    return len(os.listdir(path)) == 0

def createWidget():
    cwd = os.getcwd()
    if PathIsEmpty(cwd) == False:
        print("current folder is not empty, create widget fail!")
        return
        
    widgetTemplateDir = os.path.join(sys.prefix, "widget_template")
    for filename in os.listdir(widgetTemplateDir):
        shutil.copy(os.path.join(widgetTemplateDir, filename) , os.path.join(cwd, filename) )
    # shutil.copytree(widgetTemplateDir, cwd)
    print("create widget success")


def publishWidget():
    cwd = os.getcwd()
    if PathIsWidget(cwd) == False:
        print("current folder is not avalid widget folder")
        return
        
    data = GetWidgetConfig(cwd)
    widget_id = data["widget_id"]

    distname = utils.generate_unique_id() + "_" + widget_id
    dist = os.path.join(os.path.dirname(cwd), distname + ".zip")
    zip = zipfile.ZipFile(dist, "w", zipfile.ZIP_DEFLATED) 
    for root,dirs,files in os.walk(cwd):
        for file in files:
            if str(file).startswith("~$"):
                continue
            filepath = os.path.join(root, file)
            writepath = os.path.relpath(filepath, cwd)
            zip.write(filepath, writepath)
    zip.close()

    oss_path = upload.upload(dist)
    xy_pb.UploadWidget(widget_id, oss_path)
    os.remove(dist)
