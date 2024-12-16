from python.classes.user import User
import python.functions.network as Network
from python.functions.file_functions import calculate_checksum
from python.functions.network import sftp_sender, verify_addr
import threading
import python.functions.file_functions as scdfile
import os

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
        print("  * ")
        contact.display()
    for contact in contacts:
        if(contact.isfriend):
            threading.Thread(target=Network.verify_addr,args=[user, contact, user.cacrt]).start()

def send(user: User, data: list[str]):
    email = data[1]
    file = data[2]
    file = scdfile.get_userfile().strip("usersfile.json") + data[2]
    if not os.path.exists(file):
        print("File does not exist")
        return
    contacts = user.return_contacts()
    for contact in contacts:
        if email == contact.email():
            if contact.isfriend:
                if Network.is_online(contact) and Network.verify_addr(user, contact, user.cacrt):
                    result = Network.file_sender(user, contact, user.cacrt)
                else:
                    print("Cannot send file, contact could not be verified as legitemate, or is not online.")
                    return
            else:
                Network.broadcast_online(user)
                if contact.isfriend and contact.verified:
                    result = print("sent") #send function
                else:
                    print("Cannot send file, contact could not be verified as legitemate, or is not online.")
                    return
    if not result:
        print("Contact not listed")
    return
                    



    username = input("Enter the person's name or email: ").strip()
    local_path = input("Enter the local path to the file you want to send: ").strip()

    #Verify recipient address and retrieve preferred remote path
    contact = next((c for c in user.return_contacts() if c.name() == username or c.email() == username), None)
    if not contact:
        print(f"Contact '{username}' not found in your list.")
        return
    
    if not contact.isfriend:
        print(f"Unable to verify {username}. The contact might not be online")
        return
    
    print(f"Contact '{contact.name()} <{contact.email()}>' is sending a file. Accept (y/n)?")
    approval = input().strip().lower()
    if approval != 'y':
        print("File transfer canceled.")
        return
    try:
        remote_path = f"/uploads{local_path.split('/')[-1]}" # Set the recievers preferred path
        print(f"Sending file '{local_path}' to {contact.name()}...")

        sftp_sender(
            username=contact.retradd,
            port=22,
            local_path=local_path,
            remote_path=remote_path,
        )
        
        print(f"File '{local_path}' successfully sent to {contact.name()}")
       
        local_checksum = calculate_checksum(local_path)
        remote_checksum = input("Enter the checksum provided by the recipient: ").strip()

        if local_checksum == remote_checksum:
            print("File integrity verified successfully.")
        else:
            print("File integrity check failed. Please try resending.")
    except Exception as e:
        print(f"Error during file transfer: {e}")
