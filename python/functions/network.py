from python.classes.contact import Contact
from python.classes.user import User
import os
import ssl
import socket
import paramiko
from threading import Thread
from time import sleep
from Crypto.Hash import SHA256
import threading

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

def broadcast_online(user: User):
        udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        data = f'online_{user.email()[0]}_{user.email()[1]}'

        # set broadcast mode for socket options
        udp_socket.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        udp_socket.settimeout(3)
        udp_socket.sendto(data.encode(), ('255.255.255.255', 9999))
        while True:
            try:
                data, ret_add = udp_socket.recvfrom(1024)
                threading.Thread(target=broadcast_handler, args=[user,data,ret_add]).start()
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
    tcp_socket.timeout(3)
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
                if data[0] == "confirm.friend":
                    emailhash = user.email()
                    hashdata = SHA256.new((data[1]+emailhash[1]).encode())
                    if (emailhash[0] == hashdata.hexdigest()):
                        contacts = user.return_contacts()
                        for contact in contacts:
                            conemail = contact.email()
                            hashedemail = SHA256.new((conemail+data[3]).encode())
                            if (data[2] == hashedemail.hexdigest()):
                                udp_rec_sock.sendto(b'friend_confirmed', client_address)
                elif data[0] == "online":
                    contacts = user.return_contacts()
                    for contact in contacts:
                        hashemail = SHA256.new((contact.email()+data[2]).encode())
                        if hashemail.hexdigest() == data[1]:
                            contact.isfriend = 1
                            contact.retradd = client_address
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
    ssl_context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)

    ssl_context.load_cert_chain(certfile=f"{user.keys}.pem", keyfile=f"{user.keys}.key", password=user.keypass)
    os.remove(f"{user.keys}temp.key")
    ssl_context.load_verify_locations(cafile=user.cacrt)  # CA certificate
    ssl_context.verify_mode = ssl.CERT_REQUIRED
    while True:
        if stopthreads:
            tcp_socket.close()
            exit()
        try:
            client_socket, client_address = tcp_socket.accept()
            print(f"Incoming connection from {client_address}")
            # Wrap the accepted socket with TLS
            tls_socket = ssl_context.wrap_socket(client_socket, server_side=True)
            tls_socket.timeout(5)
            # Start a thread to handle the client
            try:
                data = tls_socket.recv(1024)
                data = data.decode('utf-8').split('_')
                if data[0] == "verify":
                    message = f"confirming"
                    tls_socket.send(message.encode(), client_address)
                    tls_socket.close()
            except TimeoutError:
                tls_socket.close()
        except TimeoutError:
            None

def verify_addr(contact: Contact):
    ssl_context = ssl.create_default_context(ssl.Purpose.SERVER_AUTH, cafile="ca.crt")
    tcp_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    tcp_socket.settimeout(10)
    tls_socket = ssl_context.wrap_socket(tcp_socket, server_hostname=contact.name())
    try:
        tls_socket.connect((contact.retradd, 9999))
        tls_socket.send(data)
        data = tls_socket.recv(1024)
        print(f"Received from server: {data}")
    except TimeoutError or ConnectionRefusedError:
        None
    tls_socket.close()
    return

def sftp_sender(username, port, local_path, remote_path):

    try:
        #Creates an SSH client
        ssh_client = paramiko.SSHClient()
        #Sets a policy to automatically add the host key if it's not known
        ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        #Connects to the SFTP server
        ssh_client.connect(hostname, port, username, password)

        #Opens an SFTP session
        sftp = ssh_client.open_sftp()
        #upload the local file to the remote path
        sftp.put(local_path, remote_path)
        #closes the sftp and ssh connection
        sftp.close()
        print("File sent succcessfully!")

    except Exception as e:
        print(f"Error sending file: {e}")
    
    finally:
        ssh_client.close()
    
def recieve_file(hostname, port, username, password, remote_path, local_path):

    try:
        #Creates an SSH Client
        ssh_client = paramiko.SSHClient()
        #Sets a policy to automatically add the host key if it's not known
        ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        #Connects to the sftp server
        ssh_client.connect(hostname, port, username, password)

        #opens an SFTP session
        sftp = ssh_client.open_sftp()

        #Used to download a file from a remote server to the local machine
        sftp.get(remote_path, local_path)
        #close the sftp and ssh connection
        sftp.close()
        print("File recieve successfully!")

    except Exception as e:
        print(f"Error receiving file: {e}")

    finally:
        ssh_client.close()

if __name__ == "__main__":
    hostname = "your_sftp_server"
    port = 22
    username = "your_username"
    password = "your_username"

    local_file = "local_file.txt"
    remote_file = "/remote/path/remote_file.txt"

#Calling functions
    # Send a file
    #send_file(hostname, port, username, password, local_file, remote_file)

    # Receive a file
    #receive_file(hostname, port, username, password, remote_file, local_file)
        

