# SecureDrop
This is a UML COMP.2300 Project Assignment

This program is a file transfer service, and uses TCP/UDP and TLS to transfer files.

## Using the program

When using the program, on first launch, it will prompt you for a new user to be made, you can then make a new user and it will exit.
Currently, if you clone this repo there is already a default user.
Email (username): john.doe@gmail.com
Pass: P4$$word

Upon second launch, it will now prompt you to login.

When in the environment, you can use the help command to list all the available commands, and what they do.


## Security
The user information is stored in userfile.json, and is encrypted.
The Full name, email, and all contact information is encrypted using AES in GCM mode.
The user password is hashed with salt.

If the userfile is touched in any way that isn't simply changing the data so anything read will be correctly decrpyted, the program will alert the user upon login and exit.


## Error handling
None yet :D



### Ryan's comment
PAT IS COOOL and should get a Tandum BIKE!! :}