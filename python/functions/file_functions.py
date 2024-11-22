import os
from python.classes.user import User
import json

def get_file() -> str:
    filedir = os.path.dirname(__file__) # gets the directory of the program
    filedir = filedir.replace("python\\functions","")
    filedir += "users\\usersfile.json" # sets the json file dir to the same dir as the program. To be used later.
    return filedir


def write_out(user: User, filedir):     # used to write out the json when exiting the program normally.
    with open(filedir, "w") as file:    # triggered on the commands: exit, add. so the file stays fine and doesn't corrupt
        json.dump(user.export_user(),file, indent = 4) # nice format to look at.