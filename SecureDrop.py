#!/usr/bin/python3
import os
import signal
import threading
from sys import exit
import python.functions.network as Network
import python.functions.commands as CMD
from python.functions.login import login
import python.functions.file_functions as SDFile
from python.functions.file_functions import get_userfile
from python.functions.registration import register_user
from time import sleep
global command

def stop_code(signal, frame): # this is for ctrl c handing so no errors pop up. Possible security issue if they did?
    Network.stopthreads = True
    exit()
signal.signal(signal.SIGINT, stop_code) 

# main code
filedir = get_userfile()
if (not os.path.exists(filedir) or os.path.getsize(filedir) == 0): # if client file doesn't exist, ask to register, then register if they want to, else exit
    register_user()                                                # also checking if file has data, if it is empty prompt for a registration.
elif (os.path.exists(filedir)): # If client file exists, prompt for client login
    logon = login() # login() returns a tupple of type [Bool, User] to be used for practical security applications.
    if logon == (0, None):
        register_user()

    thread1 = threading.Thread(target=Network.udp_listen, args=[logon[1]])
    thread2 = threading.Thread(target=Network.tls_listener, args=[logon[1]], daemon=True)
    thread1.start()
    thread2.start()
    
    # hit them with the motd
    print(f"Welcome to SecureDrop.")     
    print("Type \"help\" For Commands.\n\n")

    while logon[0]: # and then start the while loop                                                
            command = input('secure_drop> ') # Wait for user input, check it against known command, execute command given
            if command.lower() in ['exit']:
                Network.stopthreads = True
                SDFile.write_out(logon[1], filedir)
                exit()
            if command.lower() == 'help':
                CMD.help()
            if command.lower() == 'add':
                CMD.add(logon[1])
                SDFile.write_out(logon[1], filedir)
            if command.lower() == 'list':
                CMD.list_contacts(logon[1])
            if len(command.lower()) > 4:
                data = command.split(" ")
                if data[0] == "send":
                    CMD.send(logon[1], data)
