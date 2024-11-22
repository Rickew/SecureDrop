from getpass import getpass
from Crypto.Hash import SHA256
from python.classes.user import User
from python.functions.file_functions import get_file
import json



def password_input(): # just used for password input so it doesn't clutter the register_user() function
    while True:
        temppass = getpass("Enter Password: ")
        password = getpass("Re-enter Password: ")
        if password_checker(temppass, password):
            return password
        elif (not password_checker(temppass, password)):
            print("Password did not meet complexity requirement")
            continue
        print("Passwords do not match, try again")

def password_checker(pass1, pass2):                         # password complexity: 
    special_characters = "!@#$%&?" # <-- special chars      # 8 characters minimum, at least 1 special character,
    if pass1 == pass2 and len(pass1) >= 8:                  # 1 number, 1 lowercase, 1 uppercase
        if(any(ch.isupper() for ch in pass1) and 
           any(ch.isdigit() for ch in pass1) and    
           any(ch.islower() for ch in pass1)and 
           any(ch in special_characters for ch in pass1)):
            return True
    return False

def login():
    userfile = open(get_file(), "r")
    tmp = userfile.read()
    if(type(tmp) == str and tmp[0] != "{"): # if the json file isn't empty but is not a dict type, exit() (error checking)
        print("ALERT: USERS FILE HAS BEEN TAMPERED WITH! Exiting Immediately!")
        exit()
    userfile.close()
    userfile = open(get_file(), "r")
    clientdata: dict[str, str] = json.load(userfile)
    if (not "email" in clientdata.keys() or not "password" in clientdata.keys()): # error checking... for security reasons trust.
        print("ALERT: USERS FILE HAS BEEN TAMPERED WITH! Exiting Immediately!")
        exit()
    while True:
        tempname = input("Enter Email Address: ").lower() # for no case sensitivity on email
        temppass = getpass("Enter Password: ")
        hs = "a35#Hq34te!@$EF" # ignore me...

        # testing entered email and password against known creds
        if (SHA256.new((tempname+hs).encode()).hexdigest() == clientdata["email"]
        and SHA256.new((temppass+hs).encode()).hexdigest() == clientdata["password"]):
            hs = None # stop snooping in my RAM!!!
            user = User(clientdata)
            return True, user # if correct let them in, returns a bool that can change for any security reason, and the user profile.
        else: 
            print("Email and Password Combination Invalid.\n") # if wrong tell them to try again