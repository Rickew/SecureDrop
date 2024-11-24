# SecureDrop
This is a UML COMP.2300 Project Assignment<br>This program is a file transfer service, and uses TCP/UDP and TLS to transfer files.

## Using the program
When using the program, on first launch, it will prompt you for a new user to be made, you can then make a new user and it will exit.<br>Upon second launch, it will now prompt you to login.<br>When in the environment, you can use the help command to list all the available commands, and what they do.

Currently, if you clone this repo there is already a default user.<br>
### Default user and pass:
Email (username): john.doe@gmail.com<br>Pass: P4$$word


## Security
The user information is stored in userfile.json, and is encrypted.<br>The Full name, email, and all contact information is encrypted using AES in GCM mode.<br>The user password is hashed with salt.

If the userfile is touched in any way that isn't simply changing the data so anything read will be correctly decrpyted, the program will alert the user upon login and exit.


## Error handling
Feel free to prove me wrong, however after going over the entire code, I found all the exceptions I needed to catch NOMRALLY. They all involve the json file decoding, and AES decrpytion.<br>
When caught they inform the user that the usersfile.json has been tampered with and exits the program.


# Requirements
- Latest Version of Python.
- pycrptodome
- Compiling requires pyinstaller


# Installation
### Windows
1) Ensure latest version of python is installed.
    1) Open powershell and type `python3 --version`
    2) If not installed, or out of date, download the latest version [here](https://www.python.org/downloads/)
1) Download the [latest release](https://github.com/Rickew/SecureDrop/releases)

### Linux
1) Download the [latest release](https://github.com/Rickew/SecureDrop/releases)
2) Navigate into SecureDrop directory and run<br>
`sudo chmod +x install.sh`<br>
3) Run the install.sh file

### Manual install on linux
1) Make sure latest python version is installed<br>
    1) Check python version<br>
    `python3 --version`
    2) update python if needed
    3) if python is not downloaded, download it [here](https://www.python.org/downloads/)

2) install pycryptodome library<br>
    `pip install pycryptodome`
3) download the [linux release](https://github.com/Rickew/SecureDrop/releases)
4) Move the something into the bin


# Other Documentation
## This project is technically open source!
This program was made by CS students who don't have years experience in coding.<br>
So, feel free to mess with it, break it, do whatever you want to it. Fix problems, create problems, optimize our code, the sky is the limit.<br>
All the source code is done in python, and everything, even the releases folder where all the binaries are all in the repo.

## Compiling
I (Rickew) have provided 2 compiling scripts that simply run the compiling command which compiles the new release and then move the executable into the main directory for ease of access.<br><bR>
The compile command is very simple, and the only difference between windows and linux is the paths for the releases.
`pyinstaller ./Securedrop.py --distpath ./releases/windows --onefile`<br><br>
The script extensions are for powershell (windows) and any terminal that can run a .sh<br><br>
The copied executables are ignored in the .gitignore file.



##
### Ryan's comment
RICK IS COOOL and should get a Tandum BIKE!! :}