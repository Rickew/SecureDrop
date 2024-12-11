from python.classes.user import User
from python.functions.network import is_online

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
    for contact in contacts:
        contact_email = contact.email()
        if not (contact.isfriend):
            is_online(user, contact, contact_email)
    for contact in contacts:
        contact.display()

def send():
    print("  send function yet to be done")