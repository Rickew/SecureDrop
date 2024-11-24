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

<br>

# Requirements
## Python Execution
- Latest Version of Python.
- pycrptodome library

<br>

# Installation
## Normal Python Script Execution
### Windows & linux
1) Ensure latest version of python is installed.
    1) Open powershell and type `python3 --version`
    2) If not installed, or out of date, download the latest version [here](https://www.python.org/downloads/)
2) Clone the repository
    `git clone https://github.com/Rickew/SecureDrop.git`


## Release Installation
### Windows
1) Download the [latest release](https://github.com/Rickew/SecureDrop/releases)
2) Run the program in the terminal. 
    `./Securedrop.exe`

### Linux
1) Download the [latest release](https://github.com/Rickew/SecureDrop/releases)
2) Run 
    `chmod +x ./install.sh`
    Run with sudo if needed.
3) Run the install.sh with sudo.
    `sudo ./install.sh`
<br><br>

# Uninstallation
### Windows
1) Delete the release folder.

### Linux
1) Run
    `chmod +x ./uninstall.sh`
    Run with sudo if needed.
2) Run the uninstall.sh with sudo.
    `sudo ./uninstall.sh`
3) Delete the release folder.
<br><br>

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

## Github Scripts
The Push & Pull exe's are my own batch scripts turned exe's. They, along with this section of the documentation will be removed after the project is turned in.



##
### Ryan's comment
RICK IS COOOL and should get a Tandum BIKE!! :}