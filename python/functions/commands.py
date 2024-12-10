from python.classes.user import User

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
        
        #if(contact_email in online_contacts and any(user.email() == other.email() for other in contact._Contact__contacts)):
        #        print(f"* {contact.name()} <{contact.email}>")
        #        displayed = True
    #if not displayed:
     #    print("Not FRIENDS!!")

    #print("  list function yet to be done, but here, have some contacts:")
    #user.printcontacts()


def send():
    print("  send function yet to be done")