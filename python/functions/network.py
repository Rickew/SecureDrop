import ssl
import socket
import threading
from Crypto.Hash import SHA256
from python.classes.user import User
from python.classes.contact import Contact
from python.functions.file_functions import get_download

class FileTransferError(Exception):
    def __init__(self):
        self.message = "File was not successfully transfered without error, please try again."
        pass
    def __str__(self):
        return self.message
class FileTransferTimeout(Exception):
    def __init__(self):
        self.message = "Cannot send file, contact could not be verified as legitemate, or is not online."
        pass
    def __str__(self):
        return self.message

global stopthreads
stopthreads = False

def test_UDP_port(port):
    try:
        udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        udp_socket.bind(("0.0.0.0", port))
        udp_socket.close()
        return port, port-1
    except:
        return port-1, port

def broadcast_online(user: User, clause = False):
        udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        data = f'online_{user.email()[0]}_{user.email()[1]}'

        # set broadcast mode for socket options
        udp_socket.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        udp_socket.settimeout(3)
        udp_socket.sendto(data.encode(), ('255.255.255.255', 9999))
        while True:
            try:
                data, ret_add = udp_socket.recvfrom(1024)
                threading.Thread(target=broadcast_handler, args=[user,data,ret_add[0]]).start()
            except TimeoutError:
                udp_socket.close()
                return

def broadcast_handler(user: User, data: bytes, ret_add):
    data = data.decode().split('_')
    if data[0] == "true":
        contacts = user.return_contacts()
        for contact in contacts:
            hashemail = SHA256.new((contact.email()+data[2]).encode())
            if hashemail.hexdigest() == data[1]:
                contact.isfriend = 1
                contact.retradd = ret_add
                break

def is_online(contact: Contact):
    tcp_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    tcp_socket.settimeout(3)
    try:
        tcp_socket.connect((contact.retradd, 9999))
    except TimeoutError:
        contact.isfriend = False
        contact.retradd = None
        contact.verified = False
        return False
    return True
    
        
def udp_listen(user: User):
    udp_rec_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    udp_rec_sock.bind(('0.0.0.0', 9999))
    udp_rec_sock.settimeout(3)

    while True:
        if stopthreads:
            udp_rec_sock.close()
            exit()
        try:
            data, client_address = udp_rec_sock.recvfrom(1024)
            try:
                data = data.decode().split('_')
                # if data[0] == "confirm.friend":
                #     emailhash = user.email()
                #     hashdata = SHA256.new((data[1]+emailhash[1]).encode())
                #     if (emailhash[0] == hashdata.hexdigest()):
                #         contacts = user.return_contacts()
                #         for contact in contacts:
                #             conemail = contact.email()
                #             hashedemail = SHA256.new((conemail+data[3]).encode())
                #             if (data[2] == hashedemail.hexdigest()):
                #                 udp_rec_sock.sendto(b'friend_confirmed', client_address)
                if data[0] == "online":
                    contacts = user.return_contacts()
                    for contact in contacts:
                        hashemail = SHA256.new((contact.email()+data[2]).encode())
                        if hashemail.hexdigest() == data[1]:
                            resend = f'true_{user.email()[0]}_{user.email()[1]}'
                            udp_rec_sock.sendto(resend.encode(), client_address)
                            break
            except IndexError:
                None
        except TimeoutError:
            None

def tls_listener(user: User):
    tcp_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    tcp_socket.bind(('0.0.0.0', 9999))
    tcp_socket.listen(1)
    tcp_socket.settimeout(2)
    ssl_context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
    ssl_context.load_cert_chain(certfile=f"{user.keys}.pem", keyfile=f"{user.keys}.key", password=user.keypass)
    ssl_context.load_verify_locations(cafile=user.cacrt)  # CA certificate
    ssl_context.verify_mode = ssl.CERT_REQUIRED
    FileRec = False
    while True:
        if stopthreads:
            tcp_socket.close()
            exit()
        try:
            if FileRec:
                tls_socket.settimeout(10)
                filepath = get_download() + "tempfilename"
                with open(filepath, "w") as file:
                    while FileRec:
                        data = tls_socket.recv(1024).decode()
                        rechash = data.split('_')[0]
                        data = data.lstrip(rechash)
                        calchash = SHA256.new(data.encode()).hexdigest()
                        if (rechash != calchash):
                            tls_socket.send(b"hash-error")
                        file.write(data)
                        tls_socket.send(b"ack")
        except TimeoutError:
            FileRec = False
            tls_socket.close()
        try:
            client_socket, client_address = tcp_socket.accept()
            try:
                # Wrap the accepted socket with TLS
                tls_socket = ssl_context.wrap_socket(client_socket, server_side=True)
                tls_socket.settimeout(3)
                data = tls_socket.recv(1024)
                data = data.decode('utf-8').split('_')
                if data[0] == "verify":
                    message = b"confirming"
                    tls_socket.send(message)
                    tls_socket.close()
                if data[0] == "file-send":
                    contacts = user.return_contacts()
                    for contact in contacts:
                        hashemail = SHA256.new((contact.email()+data[2]).encode())
                        if hashemail.hexdigest() == data[1]:
                            if contact.verified:
                                ans = input(f"Contact {contact.name()} {contact.email()}' is sending a file. Accept (y/n)? ")
                                if ans.lower()[0] == 'y':
                                    message = b"send-file"
                                    tls_socket.send(message)
                                    FileRec = True
                            else:
                                verify_addr(user, contact, user.cacrt)
                            break
            except (TimeoutError, ssl.SSLError):
                None
        except TimeoutError:
            None

def get_clientContext(user: User):
    ssl_context = ssl.create_default_context(ssl.Purpose.SERVER_AUTH, cafile=user.cacrt)
    ssl_context.verify_mode = ssl.CERT_REQUIRED
    ssl_context.load_cert_chain(certfile=f"{user.keys}.pem", keyfile=f"{user.keys}.key", password=user.keypass)
    return ssl_context

def verify_addr(user: User, contact: Contact):
    print("verify_addr:")
    try:
        ssl_context = get_clientContext(user)
        tcp_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        tcp_socket.settimeout(10)
        tls_socket = ssl_context.wrap_socket(tcp_socket, server_hostname=contact.name())
        tls_socket.connect((contact.retradd, 9999))
        tls_socket.send(b'verify')
        data = tls_socket.recv(1024)
        print(data)
        if data != b"confirming":
            return False
    except (TimeoutError, ConnectionRefusedError, ssl.SSLCertVerificationError):
        contact.verified = False
    tls_socket.close()
    contact.verified = True
    return True

def file_sender(user: User, contact: Contact, filepath):
    ssl_context = get_clientContext(user)
    tcp_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    tcp_socket.settimeout(10)
    tls_socket = ssl_context.wrap_socket(tcp_socket, server_hostname=contact.name())
    tls_socket.connect((contact.retradd, 9999))
    data = f'file-send_{user.email()[0]}_{user.email()[1]}'.encode()
    tls_socket.send(data)
    try:
        data = tls_socket.recv(1024)
        if (data.decode() != "send-file"):
            return
        try:
            with open(filepath, "r") as file:
                while True:
                    filedata = file.read(200)
                    if not filedata:
                        tls_socket.close()
                        print("File Transfer Successful")
                        break
                    hash = SHA256.new(filedata.encode()).hexdigest()
                    data = f"{hash, filedata}".encode()
                    tls_socket.send(data)
                    data = tls_socket.recv(1024)
                    if data.decode() == "ack":
                        continue
                    elif(data.decode() == "hash-error"):
                        tls_socket.close()
                        raise FileTransferError

        except TypeError:
            tls_socket.close()
            return
    except TimeoutError:
        raise FileTransferTimeout
