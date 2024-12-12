from python.classes.user import User
<<<<<<< HEAD
import python.functions.network as Network
=======
from python.functions.network import is_online
from python.functions.network import sftp_sender
>>>>>>> 9d20157e4d532d463c66b208124502e85683e44d

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
    contacts = user.return_contacts()
    Network.broadcast_online(user)
    print("  The following contacts are online:")
    for contact in contacts:
        contact.display()

def send(user: User):
<<<<<<< HEAD
    print("  send function yet to be done")
=======
    sftp_sender(input(" "), 22,input(" "), )
>>>>>>> 9d20157e4d532d463c66b208124502e85683e44d
