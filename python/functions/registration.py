import json
from sys import exit
import os
from Crypto.Cipher import AES
from Crypto.Hash import SHA256
from python.functions.login import password_input
from python.functions.file_functions import get_file

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
    clientdata = {"name": f"{enc_name.hex()}\0\0{name_tag.hex()}\0\0{namenonce.hex()}",
                    "email":hashemail.hexdigest(),
                    "password":hashpass.hexdigest()}
    hs = None # stop snooping in my RAM!!!

    # Write to the json file, located in the same directory as the program.
    try:
        with open(get_file(), "w") as file:
            json.dump(clientdata,file, indent=4)
            print("\nPasswords Match.\nUser Registered.\nExiting SecureDrop.")
            file.close()
            exit()
    except FileNotFoundError:
        os.mkdir("scdusers")
        with open(get_file(), "w") as file:
            json.dump(clientdata,file, indent=4)
            print("\nPasswords Match.\nUser Registered.\nExiting SecureDrop.")
            file.close()
            exit()