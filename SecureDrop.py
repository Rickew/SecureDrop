#!/usr/bin/python3
import signal
import os
from python.functions.login import login
from python.classes.user import User
from python.functions.registration import register_user
import python.functions.file_functions as SDFile
import python.functions.commands as CMD
from python.functions.file_functions import get_file

def stop_code(signal, frame): # this is for ctrl c handing so no errors pop up. Possible security issue if they did?
    exit()
signal.signal(signal.SIGINT, stop_code) 

# main code
filedir = get_file()
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
                SDFile.write_out(logon[1], filedir)
                exit()
            if command.lower() == 'help':
                CMD.help()
            if command.lower() == 'add':
                CMD.add(logon[1])
                SDFile.write_out(logon[1], filedir)
            if command.lower() == 'list':
                CMD.list_contacts(logon[1])
            if command.lower() == 'send':
                CMD.send()

