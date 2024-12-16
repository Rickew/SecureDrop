import json
from sys import exit
import os
from Crypto.Cipher import AES
from Crypto.Hash import SHA256
from python.functions.login import password_input
from python.functions.file_functions import get_userfile

def register_user():
    while True:
        print("No users are registered with this client.")             # --------------- ISSUE: If there is an empty json file by the same name it will cause an error in the code. ---------------
        yn = input("Do you want to register a new user (y/n)? ")
        if yn.lower() in ['yes', 'y']:
            break
        elif yn.lower() in ['no', 'n']:
            print("Exiting SecureDrop\n")
            exit()
    
    name = input("\nEnter Full Name: ")
    email = input("Enter Email Address: ").lower() # for no case sensitivity on email
    password = password_input()
    es = os.urandom(32).hex()
    ps = os.urandom(32).hex()

    # hashing the password and email
    hashemail = SHA256.new((email+es).encode())
    hashpass = SHA256.new((password+ps).encode())

    # first time around is just a quick registration
    aes_obj = AES.new(bytes.fromhex(SHA256.new((password).encode()).hexdigest()), AES.MODE_GCM)
    enc_name, name_tag = aes_obj.encrypt_and_digest(name.encode())
    namenonce = aes_obj.nonce
    clientdata = {"name": f"{enc_name.hex()}\0\0{name_tag.hex()}\0\0{namenonce.hex()}",
                    "email":f"{hashemail.hexdigest()}\0\0{es}",
                    "password":f"{hashpass.hexdigest()}\0\0{ps}"}

    # Write to the json file, located in the same directory as the program.
    try:
        with open(get_userfile(), "w") as file:
            json.dump(clientdata,file, indent=4)
            print("\nPasswords Match.\nUser Registered.\nExiting SecureDrop.")
            file.close()
            exit()
    except FileNotFoundError:
        os.mkdir("scdusers")
        with open(get_userfile(), "w") as file:
            json.dump(clientdata,file, indent=4)
            print("\nPasswords Match.\nUser Registered.\nExiting SecureDrop.")
            file.close()
            exit()
