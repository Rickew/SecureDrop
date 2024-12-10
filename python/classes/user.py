from sys import exit
from Crypto.Cipher import AES
from python.classes.contact import Contact
from python.functions.network import broadcast_server
from python.functions.network import broadcast_reciever
import socket
from threading import Thread
import ssl

def encrypt(input: str, key: str):
    aes_o = AES.new(bytes.fromhex(key), AES.MODE_GCM)
    output, tag = aes_o.encrypt_and_digest(input.encode())
    return output, tag, aes_o.nonce

def decrypt(key: str, input: str, tag: str, nonce:str):
    aes_o = AES.new(bytes.fromhex(key), AES.MODE_GCM, nonce=bytes.fromhex(nonce))
    output = aes_o.decrypt_and_verify(bytes.fromhex(input), bytes.fromhex(tag)).decode()
    return output

class User:
    def __init__(self, data: dict[str, str], aes_key): # constructor used for user importation
        try:
            self.__aes_key = aes_key
            # setting normal vars
            n_end = int(len(data) - 3 / 2) # gets the correct number of contacts in the data
            try:
                if data[f"contact{n_end}"]:
                    None
            except KeyError:
                None
            
            self.__email_hash = data["email"].split("\x00\x00")
            self.__pass_hash = data["password"].split("\x00\x00")
            e_name = data[f"name"].split("\x00\x00")
            self.__name = decrypt(self.__aes_key, e_name[0], e_name[1], e_name[2]) # decrypting the name
            self.__contacts: list[Contact] = [] # list to store contacts
            for n in range(n_end):
                if (f"contact{n}" in data.keys()):

                    # spliting the encrypted contact data on the delimeter
                    e_name = data[f"contact{n}"].split("\x00\x00")
                    e_email = data[f"email{n}"].split("\x00\x00")

                    # Decryption
                    name = decrypt(self.__aes_key, e_name[0], e_name[1], e_name[2])
                    email = decrypt(self.__aes_key, e_email[0], e_email[1], e_email[2])

                    # add the contact, rinse and repeat
                    self.add_contact(name, email)
                else:
                    break # until there are no more left to add
        except ValueError or IndexError or KeyError:
            print("ALERT: USERS FILE HAS BEEN TAMPERED WITH! Exiting Immediately!")
            exit()
    def name(self):
        return self.__name
    def email(self):
        return self.__email_hash
    def password(self):
        return self.__pass_hash
    
    def printcontacts(self): # used for the incomplete list() function, prints contacts.
        for contact in self.__contacts:
            contact.display()

    def add_contact(self, name: str, email: str): # adds a contact.
        self.__contacts.append(Contact(name, email))

    def export_user(self): # exports the user + contacts to a json format
        e_email = encrypt(self.__name,self.__aes_key)
        jsonDict = {"name": f"{e_email[0].hex()}\0\0{e_email[1].hex()}\0\0{e_email[2].hex()}",
                    "email": f"{self.__email_hash[0]}\0\0{self.__email_hash[1]}",
                    "password": f"{self.__pass_hash[0]}\0\0{self.__pass_hash[1]}"} # user vals
        for n in range(len(self.__contacts)):

            # encypting contact[n] name
            e_name = encrypt(self.__contacts[n].name(), self.__aes_key)

            # encypting contact[n] email
            e_email = encrypt(self.__contacts[n].email(), self.__aes_key)

            # adding contact[n] onto the final output dict using sperator \0\0 for the ciphertext|tag|nonce
            jsonDict.update({f"contact{n}": f"{e_name[0].hex()}\0\0{e_name[1].hex()}\0\0{e_name[2].hex()}",
            f"email{n}":f"{e_email[0].hex()}\0\0{e_email[1].hex()}\0\0{e_email[2].hex()}"})
        return jsonDict
#if command.lower() == 'list':
#    list_contacts(logon[1], online_contacts)
online_contacts = set()
broadcast_port = 9999
Thread(target=broadcast_server, args=(User.email(), broadcast_port), daemon=True).start()
Thread(target=broadcast_reciever, args=(broadcast_port, online_contacts), daemon=True).start()