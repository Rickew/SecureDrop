import os
import sys
import json
import hashlib
from platform import system
from getpass import getuser
from python.classes.user import User


def get_userfile() -> str:
    var = getattr(sys, "frozen", False), system()
    if var[0]:
        if var[1] == "Linux":
            u = getuser()
            filedir = f"/home/{u}/.scdusers/usersfile.json" # linux path if it is installed
        else:
            filedir = os.path.dirname(sys.executable) # gets the directory of the program, if the program if an exectutable
            filedir += "\\scdusers\\usersfile.json" # windows path
    elif (var[1] == "Linux"):
        filedir = os.path.dirname(__file__) # gets the directory of the program
        filedir = filedir.replace("python/functions","")
        filedir += "scdusers/usersfile.json" # linux path
    else:
        filedir = os.path.dirname(__file__) # gets the directory of the program
        filedir = filedir.replace("python\\functions","")
        filedir += "scdusers\\usersfile.json" # windows path
    return filedir

def get_upload() -> str:
    var = getattr(sys, "frozen", False), system()
    if var[0]:
        if var[1] == "Linux":
            u = getuser()
            filedir = f"/home/{u}/.scdusers/uploads/" # linux path if it is installed
        else:
            filedir = os.path.dirname(sys.executable) # gets the directory of the program, if the program if an exectutable
            filedir += "\\scdusers\\uploads\\" # windows path
    elif (var[1] == "Linux"):
        filedir = os.path.dirname(__file__) # gets the directory of the program
        filedir = filedir.replace("python/functions","")
        filedir += "scdusers/uploads/" # linux path
    else:
        filedir = os.path.dirname(__file__) # gets the directory of the program
        filedir = filedir.replace("python\\functions","")
        filedir += "scdusers\\uploads\\" # windows path
    return filedir

def get_download() -> str:
    var = getattr(sys, "frozen", False), system()
    if var[0]:
        if var[1] == "Linux":
            u = getuser()
            filedir = f"/home/{u}/.scdusers/downloads/" # linux path if it is installed
        else:
            filedir = os.path.dirname(sys.executable) # gets the directory of the program, if the program if an exectutable
            filedir += "\\scdusers\\downloads\\" # windows path
    elif (var[1] == "Linux"):
        filedir = os.path.dirname(__file__) # gets the directory of the program
        filedir = filedir.replace("python/functions","")
        filedir += "scdusers/downloads/" # linux path
    else:
        filedir = os.path.dirname(__file__) # gets the directory of the program
        filedir = filedir.replace("python\\functions","")
        filedir += "scdusers\\downloads\\" # windows path
    return filedir

def write_out(user: User, filedir):     # used to write out the json when exiting the program normally.
    with open(filedir, "w") as file:    # triggered on the commands: exit, add. so the file stays fine and doesn't corrupt
        exp = user.export_user()
        json.dump(exp, file, indent = 4) # nice format to look at.

