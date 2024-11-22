from contact import Contact
from Crypto.Cipher import AES

class User:
    def __init__(self, name: str, email: str, password: str): # constructor for initial user registration
        self.__name = name
        self.__email_hash = email
        self.__pass_hash = password
        self.__contacts: list[Contact] = []

    def __init__(self, data: dict[str, str]): # constructor used for user importation
        if ("name" in data.keys() and       # not needed, but slight error checking,
            "email" in data.keys() and      # its checked again before this at the login().
            "password" in data.keys()):    

            # setting normal vars
            self.__email_hash = data["email"]
            self.__pass_hash = data["password"]
            e_name = data[f"name"].split("\x00\x00")
            aes_o = AES.new(bytes.fromhex(self.__pass_hash), AES.MODE_GCM, nonce=bytes.fromhex(e_name[2]))
            self.__name = aes_o.decrypt_and_verify(bytes.fromhex(e_name[0]), bytes.fromhex(e_name[1])).decode()
            self.__contacts: list[Contact] = [] # list to store contacts
            n_end = int(len(data) - 3 / 2) # gets the correct number of contacts in the data
            for n in range(n_end):
                if (f"contact{n}" in data.keys()):
                    
                    # spliting the encrypted contact data on the delimeter
                    e_name = data[f"contact{n}"].split("\x00\x00")
                    e_email = data[f"email{n}"].split("\x00\x00")

                    # Decryption
                    aes_o = AES.new(bytes.fromhex(self.__pass_hash), AES.MODE_GCM, nonce=bytes.fromhex(e_name[2]))
                    name = aes_o.decrypt_and_verify(bytes.fromhex(e_name[0]), bytes.fromhex(e_name[1]))
                    aes_o = AES.new(bytes.fromhex(self.__pass_hash), AES.MODE_GCM, nonce=bytes.fromhex(e_email[2]))
                    email = aes_o.decrypt_and_verify(bytes.fromhex(e_email[0]), bytes.fromhex(e_email[1]))

                    # add the contact, rinse and repeat
                    self.add_contact(name.decode(), email.decode())
                else:
                    break # until there are no more left to add
        else:
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
        aes_obj = AES.new(bytes.fromhex(self.__pass_hash), AES.MODE_GCM)
        enc_name, name_tag = aes_obj.encrypt_and_digest(self.__name.encode())
        namenonce = aes_obj.nonce
        jsonDict = {f"name": f"{enc_name.hex()}\0\0{name_tag.hex()}\0\0{namenonce.hex()}", "email": self.__email_hash, "password": self.__pass_hash} # user vals
        for n in range(len(self.__contacts)):

            # encypting contact[n] name
            aes_obj = AES.new(bytes.fromhex(self.__pass_hash), AES.MODE_GCM)
            enc_name, name_tag = aes_obj.encrypt_and_digest(self.__contacts[n].name().encode())
            namenonce = aes_obj.nonce

            # encypting contact[n] email
            aes_obj = AES.new(bytes.fromhex(self.__pass_hash), AES.MODE_GCM)
            enc_email, email_tag = aes_obj.encrypt_and_digest(self.__contacts[n].email().encode())
            emailnonce = aes_obj.nonce

            # adding contact[n] onto the final output dict using sperator \0\0 for the ciphertext|tag|nonce
            jsonDict.update({f"contact{n}": f"{enc_name.hex()}\0\0{name_tag.hex()}\0\0{namenonce.hex()}",
            f"email{n}":f"{enc_email.hex()}\0\0{email_tag.hex()}\0\0{emailnonce.hex()}"})
        return jsonDict