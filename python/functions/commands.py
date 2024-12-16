import python.functions.file_functions as scdfile
import python.functions.network as Network
from python.classes.user import User
import threading
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
        print("  * ", end="")
        contact.display()
    for contact in contacts:
        if(contact.isfriend):
            threading.Thread(target=Network.verify_addr,args=[user, contact]).start()

def send(user: User, data: list[str]):
    try:
        data[2]
    except IndexError:
        return
    email = data[1]
    file = scdfile.get_userfile().strip("usersfile.json") + data[2]
    file2 = scdfile.get_upload() + data[2]
    fileisgood = False, None
    if os.path.exists(file):
        fileisgood = True, file
    elif os.path.exists(file2):
        fileisgood = True, file2
    if not (fileisgood[0]):
        print("File could not be found")
        return
    contacts = user.return_contacts()
    contactfound = False
    for contact in contacts:
        if email == contact.email():
            contactfound = True
            if contact.isfriend:
                if Network.is_online(contact) and Network.verify_addr(user, contact):
                    try:
                        Network.file_sender(user, contact, fileisgood[1])
                    except Network.FileTransferError:
                        print("File was not successfully transfered without error, please try again.")
                        return
                else:
                    print("Cannot send file, contact could not be verified as legitemate, or is not online.")
                    return
            else:
                print("broadcasting online")
                Network.broadcast_online(user, True)
                if contact.isfriend:
                    if Network.verify_addr(user, contact):
                        try: 
                            Network.file_sender(user, contact, fileisgood[1])
                        except [Network.FileTransferError , Network.FileTransferTimeout] as e:
                            print(e)
                            return
                else:
                    print("Cannot send file, contact could not be verified as legitemate, or is not online.")
                    return
    if not contactfound:
        print("Contact not listed")
    return
                    



    # username = input("Enter the person's name or email: ").strip()
    # local_path = input("Enter the local path to the file you want to send: ").strip()
# 
    # #Verify recipient address and retrieve preferred remote path
    # contact = next((c for c in user.return_contacts() if c.name() == username or c.email() == username), None)
    # if not contact:
    #     print(f"Contact '{username}' not found in your list.")
    #     return
    # 
    # if not contact.isfriend:
    #     print(f"Unable to verify {username}. The contact might not be online")
    #     return
    # 
    # print(f"Contact '{contact.name()} <{contact.email()}>' is sending a file. Accept (y/n)?")
    # approval = input().strip().lower()
    # if approval != 'y':
    #     print("File transfer canceled.")
    #     return
    # try:
    #     remote_path = f"/uploads{local_path.split('/')[-1]}" # Set the recievers preferred path
    #     print(f"Sending file '{local_path}' to {contact.name()}...")
# 
    #     sftp_sender(
    #         username=contact.retradd,
    #         port=22,
    #         local_path=local_path,
    #         remote_path=remote_path,
    #     )
    #     
    #     print(f"File '{local_path}' successfully sent to {contact.name()}")
    #    
    #     local_checksum = calculate_checksum(local_path)
    #     remote_checksum = input("Enter the checksum provided by the recipient: ").strip()
# 
    #     if local_checksum == remote_checksum:
    #         print("File integrity verified successfully.")
    #     else:
    #         print("File integrity check failed. Please try resending.")
    # except Exception as e:
    #     print(f"Error during file transfer: {e}")
# 