#!/usr/bin/python3
import signal
import os
from getpass import getpass
import json
from Crypto.Hash import SHA256
from Crypto.Cipher import AES

class Contact:
    def __init__(self, name: str, email: str): # default constructor
        self.__name = name
        self.__email = email

    def name(self):
        return self.__name
    
    def email(self):
        return self.__email
    
    def display(self): # displays the contact information
        print(f'  {self.name()} <{self.email()}>')

class User:
    def __init__(self, name: str, email: str, password: str): # constructor for initial user registration
        self.__name = name
        self.__email_hash = email
        self.__pass_hash = password
        self.__contacts: list[Contact] = []

    def __init__(self, data: dict[str, str]): # constructor used for user importation
        if ("name" in data.keys() and       # not needed, but slight error checking,
            "email" in data.keys() and      # its checked again before this at the login().
            "password" in data.keys()):    

            # setting normal vars
            self.__email_hash = data["email"]
            self.__pass_hash = data["password"]
            e_name = data[f"name"].split("\x00\x00")
            aes_o = AES.new(bytes.fromhex(self.__pass_hash), AES.MODE_GCM, nonce=bytes.fromhex(e_name[2]))
            self.__name = aes_o.decrypt_and_verify(bytes.fromhex(e_name[0]), bytes.fromhex(e_name[1])).decode()
            self.__contacts: list[Contact] = [] # list to store contacts
            n_end = int(len(data) - 3 / 2) # gets the correct number of contacts in the data
            for n in range(n_end):
                if (f"contact{n}" in data.keys()):
                    
                    # spliting the encrypted contact data on the delimeter
                    e_name = data[f"contact{n}"].split("\x00\x00")
                    e_email = data[f"email{n}"].split("\x00\x00")

                    # Decryption
                    aes_o = AES.new(bytes.fromhex(self.__pass_hash), AES.MODE_GCM, nonce=bytes.fromhex(e_name[2]))
                    name = aes_o.decrypt_and_verify(bytes.fromhex(e_name[0]), bytes.fromhex(e_name[1]))
                    aes_o = AES.new(bytes.fromhex(self.__pass_hash), AES.MODE_GCM, nonce=bytes.fromhex(e_email[2]))
                    email = aes_o.decrypt_and_verify(bytes.fromhex(e_email[0]), bytes.fromhex(e_email[1]))

                    # add the contact, rinse and repeat
                    self.add_contact(name.decode(), email.decode())
                else:
                    break # until there are no more left to add
        else:
            print("ALERT: USERS FILE HAS BEEN TAMPERED WITH! Exiting Immediately!")
            exit()
    def name(self):
        return self.__name
    def email(self):
        return self.__email_hash
    def password(self):
        return self.__pass_hash
    
    def printcontacts(self): # used for the incomplete list() function, prints contacts.
        for contact in self.__contacts:
            contact.display()

    def add_contact(self, name: str, email: str): # adds a contact.
        self.__contacts.append(Contact(name, email))

    def export_user(self): # exports the user + contacts to a json format
        aes_obj = AES.new(bytes.fromhex(self.__pass_hash), AES.MODE_GCM)
        enc_name, name_tag = aes_obj.encrypt_and_digest(self.__name.encode())
        namenonce = aes_obj.nonce
        jsonDict = {f"name": f"{enc_name.hex()}\0\0{name_tag.hex()}\0\0{namenonce.hex()}", "email": self.__email_hash, "password": self.__pass_hash} # user vals
        for n in range(len(self.__contacts)):

            # encypting contact[n] name
            aes_obj = AES.new(bytes.fromhex(self.__pass_hash), AES.MODE_GCM)
            enc_name, name_tag = aes_obj.encrypt_and_digest(self.__contacts[n].name().encode())
            namenonce = aes_obj.nonce

            # encypting contact[n] email
            aes_obj = AES.new(bytes.fromhex(self.__pass_hash), AES.MODE_GCM)
            enc_email, email_tag = aes_obj.encrypt_and_digest(self.__contacts[n].email().encode())
            emailnonce = aes_obj.nonce

            # adding contact[n] onto the final output dict using sperator \0\0 for the ciphertext|tag|nonce
            jsonDict.update({f"contact{n}": f"{enc_name.hex()}\0\0{name_tag.hex()}\0\0{namenonce.hex()}",
            f"email{n}":f"{enc_email.hex()}\0\0{email_tag.hex()}\0\0{emailnonce.hex()}"})
        return jsonDict

def register_user():
    name = input("\nEnter Full Name: ")
    email = input("Enter Email Address: ").lower() # for no case sensitivity on email
    password = password_input()
    hs = "a35#Hq34te!@$EF" # ignore me...

    # hashing the password and email
    hashemail = SHA256.new((email+hs).encode())
    hashpass = SHA256.new((password+hs).encode())

    # first time around is just a quick registration
    aes_obj = AES.new(bytes.fromhex(hashpass.hexdigest()), AES.MODE_GCM)
    enc_name, name_tag = aes_obj.encrypt_and_digest(name.encode())
    namenonce = aes_obj.nonce
    clientdata = {f"name": f"{enc_name.hex()}\0\0{name_tag.hex()}\0\0{namenonce.hex()}",
                    "email":hashemail.hexdigest(),
                    "password":hashpass.hexdigest()}
    hs = None # stop snooping in my RAM!!!

    # Write to the json file, located in the same directory as the program.
    with open(filedir, "w") as file:
            json.dump(clientdata,file, indent=4)
            print("\nPasswords Match.\nUser Registered.\nExiting SecureDrop.")
            exit()

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
    userfile = open(filedir, "r")
    tmp = userfile.read()
    if(type(tmp) == str and tmp[0] != "{"): # if the json file isn't empty but is not a dict type, exit() (error checking)
        print("ALERT: USERS FILE HAS BEEN TAMPERED WITH! Exiting Immediately!")
        exit()
    userfile.close()
    userfile = open(filedir, "r")
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

def write_out(user: User, filedir):     # used to write out the json when exiting the program normally.
    with open(filedir, "w") as file:    # triggered on the commands: exit, add. so the file stays fine and doesn't corrupt
        json.dump(user.export_user(),file, indent = 4) # nice format to look at.

#all user commands definitions
def help():
    print('  "add"  -> Add a new contact')
    print('  "list" -> List all online contacts')
    print('  "send" -> Transfer file to contact')
    print('  "exit" -> Exit SecureDrop')

def add(user: User):
    Name = input("  Enter Full Name: ")
    Email = input("  Enter Email Address: ").lower() # for no case sensitivity on email
    user.add_contact(Name, Email)
    print("  Conact Added.")

def list_contacts(user: User):
    print("  list function yet to be done, but here, have some contacts:")
    user.printcontacts()

def send():
    print("  send function yet to be done")

# This is where the program actually begins technically.

def stop_code(signal, frame): # this is for ctrl c handing so no errors pop up. Possible security issue if they did?
    exit()
signal.signal(signal.SIGINT, stop_code) 

# main code
filedir = os.path.dirname(__file__) # gets the directory of the program
filedir += "\\usersfile.json" # sets the json file dir to the same dir as the program. To be used later.

if (not os.path.exists(filedir)):                                  # if client file doesn't exist, ask to register, then register if they want to, else exit
    print("No users are registered with this client.")             # --------------- ISSUE: If there is an empty json file by the same name it will cause an error in the code. ---------------
    yn = input("Do you want to register a new user (y/n)? ")
    if yn.lower() in ['yes', 'y']:
        register_user()
        exit()
    else:
        print("Exiting SecureDrop\n")
        exit()
elif (os.path.exists(filedir)): # If client file exists, prompt for client login
    if (os.path.getsize(filedir) == 0): # checking if file has data, if it is empty prompt for a registration.
        print("No users are registered with this client.")             # --------------- ISSUE: If there is an empty json file by the same name it will cause an error in the code. ---------------
        yn = input("Do you want to register a new user (y/n)? ")
        if yn.lower() in ['yes', 'y']:
            register_user()
            exit()
        else:
            print("Exiting SecureDrop\n")
            exit()
    logon = login() # login() returns a tupple of type [Bool, User] to be used for practical security applications.
    if not logon[0]: # impossible edge case
        exit()

    # hit them with the motd
    print(f"Welcome to SecureDrop.")     
    print("Type \"help\" For Commands.\n\n")

    while logon[0]: # and then start the while loop                                                
            command = input('secure_drop> ') # Wait for user input, check it against known command, execute command given
            if command.lower() in ['exit']:
                write_out(logon[1], filedir)
                exit()
            if command.lower() == 'help':
                help()
            if command.lower() == 'add':
                add(logon[1])
                write_out(logon[1], filedir)
            if command.lower() == 'list':
                list_contacts(logon[1])
            if command.lower() == 'send':
                send()

