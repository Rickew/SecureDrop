from python.classes.contact import Contact
from python.classes.user import User
import ssl
import socket
from threading import Thread
from time import sleep
from Crypto.Hash import SHA256

global stopthreads
stopthreads = False

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
    udp_rec_sock.settimeout(5)

    while True:
        if stopthreads:
            udp_rec_sock.close()
            exit()
        try:
            data, client_address = udp_rec_sock.recvfrom(1024)
            try:
                data = data.decode()
                data = data.split('_')
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
            except IndexError:
                None
        except TimeoutError:
            None
