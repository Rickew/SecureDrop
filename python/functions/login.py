import json
from sys import exit
from getpass import getpass
from Crypto.Hash import SHA256
from python.classes.user import User
from python.functions.file_functions import get_userfile



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
    if pass1 == pass2 and len(pass1) >= 8 and len(pass1) <= 24:                  # 1 number, 1 lowercase, 1 uppercase
        if(any(ch.isupper() for ch in pass1) and 
           any(ch.isdigit() for ch in pass1) and    
           any(ch.islower() for ch in pass1)and 
           any(ch in special_characters for ch in pass1)):
            return True
    return False

def login():
    try:
        userfile = open(get_userfile(), "r")
        clientdata: dict[str, str] = json.load(userfile)
    except json.decoder.JSONDecodeError:
        print("ALERT: USERS FILE HAS BEEN TAMPERED WITH! Exiting Immediately!")
        exit()
    if (not clientdata):
        return False, None
    while True:
        tempemail = input("Enter Email Address: ").lower() # for no case sensitivity on email
        temppass = getpass("Enter Password: ")

        # testing entered email and password against known creds
        try:
            clientdata["name"]
            clientdata["email"]
            clientdata["password"]
        except KeyError:
            print("ALERT: USERS FILE HAS BEEN TAMPERED WITH! Exiting Immediately!")
            exit()
        e = clientdata["email"].split("\x00\x00")
        p = clientdata["password"].split("\x00\x00")
        if (SHA256.new((tempemail+e[1]).encode()).hexdigest() == e[0]
        and SHA256.new((temppass+p[1]).encode()).hexdigest() == p[0]):
            user = User(clientdata, SHA256.new((temppass).encode()).hexdigest())
        # tempcode purely for codedemo in the presentation, because making logic and methods of making ans signing keys is not one of the objectives, and I was told I didn't have to do it.
            keyfile = tempemail.split('.')[0]
            path = get_userfile().rstrip('usersfile.json')
            user.cacrt = path + "ca.crt"
            user.keys = path + keyfile
            user.keypass = temppass



            return True, user # if correct let them in, returns a bool that can change for any security reason, and the user profile.
        else: 
            print("Email and Password Combination Invalid.\n") # if wrong tell them to try again
            