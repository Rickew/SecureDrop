from python.classes.user import User
import python.functions.network as Network
from python.functions.network import sftp_sender
import threading

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
    for contact in contacts:
        if(contact.isfriend):
            threading.Thread(target=Network.verify_addr,args=[contact, user.cacrt]).start()

def send(user: User):
    sftp_sender(input(" "), 22,input(" "), )
