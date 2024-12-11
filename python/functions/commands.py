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
    for contact in contacts: #Access private contacts list
        contact_email = contact.email()

        #What we need
        # 1. Contact's email exists in the user's contact list
        # 2. Contact has added the user's email
        # 3. Contact is online in the 'online_contacts' set
        if (is_online(user, contact_email)[0] == 1):
            print(" GOTEM BITCH")


    #print("  list function yet to be done, but here, have some contacts:")
    #user.printcontacts()


def send():
    print("  send function yet to be done")