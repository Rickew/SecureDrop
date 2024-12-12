from python.classes.user import User
import python.functions.network as Network
from python.functions.network import sftp_sender, verify_addr

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
    username = input("Enter who you want to send to: ")
    local_path = input("Enter the local path of your file: ")

    #Verify recipient address and retrieve preferred remote path
    contact = next((c for c in user.return_contacts() if c.name() == username), None)
    if not contact:
        print(f"Contact '{username}' not found in your list.")
        return
    
    try:
        print(f"Verifying addrss of {username}...")
        verify_addr(contact)

        print("Requesting preferred remote path from recipient...")

        remote_path = input("Enter the recipient's remote path: ")
        
        print(f"Sending file to {username}...")
        sftp_sender(contact.retradd[0], 22, local_path, remote_path)
        print(f"File sent successfully to {username}.")
    except Exception as e:
        print(f"Error during file transfer: {e}")
        