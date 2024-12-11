from python.classes.contact import Contact
from python.classes.user import User
import ssl
import socket
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

def is_online(user: User, contact: Contact, email: str):
    try:
        udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        data = f'confirm.friend_{email}_{user.email()[0]}_{user.email()[1]}'

        # set broadcast mode for socket options
        udp_socket.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        udp_socket.settimeout(10)
        udp_socket.sendto(data.encode(), ('255.255.255.255', 9999))
        data, ret_address = udp_socket.recvfrom(1024)
        if data.decode() == 'friend_confirmed':
            contact.isfriend = True
            contact.retradd = ret_address
    except TimeoutError:
        udp_socket.close()
        contact.isfriend = False
        contact.retradd = None
        
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


def create_tls_socket(server_ip, server_port):
    #Create a plain TCP socket
    tcp_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    tcp_socket.connect((server_ip, server_port))

    #wrap the socket w/ TLS
    ssl_context = ssl.create_default_context(
        ssl.Purpose.SERVER_AUTH
    )

    ssl_context.load_cert_chain(certfile="", keyfile="insert jane/john here")
    ssl_context.load_verify_locations(cafile="insert ca_crt")
    ssl_context.check_hostname = False
    return ssl_context.wrap_socket(tcp_socket, server_hostname=None)
