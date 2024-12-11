from Crypto.Cipher import AES 
from Crypto.Random import get_random_bytes
from python.classes.user import User
import ssl
import socket
from threading import Thread
from time import sleep
from Crypto.Hash import SHA256

global stopthreads
stopthreads = False

def is_online(user: User, email: str):
    try:
        udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        data = f'confirm.friend_{email}_{user.email()[0]}_{user.email()[1]}'

        # set broadcast mode for socket options
        udp_socket.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        udp_socket.settimeout(10)
        print (f"sending: {data}")
        udp_socket.sendto(data.encode(), ('255.255.255.255', 9999))
        data, ret_address = udp_socket.recvfrom(1024)
        print(f"recieved: {data}")
        if data.decode() == 'friend_confirmed':
            return 1, ret_address
    except TimeoutError:
        udp_socket.close()
        return 0, 0

def udp_listen(user: User):
    udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    udp_socket.bind(('0.0.0.0', 9999))
    udp_socket.settimeout(5)

    while True:
            if stopthreads:
                udp_socket.close()
                exit()
            try:
                data, client_address = udp_socket.recvfrom(1024)
                data = data.decode()
                data = data.split('_')
                try:
                    if data[0] == "confirm.friend":
                        emailhash = user.email()
                        hashdata = SHA256.new((data[1]+emailhash[1]).encode())
                        if (emailhash == hashdata.hexdigest()):
                            contacts = user.return_contacts()
                            for contact in contacts:
                                conemail = contact.email()
                                hashedemail = SHA256.new((conemail+data[3]).encode())
                                if (data[2] == hashedemail.hexdigest()):
                                    udp_socket.sendto(b'friend_confirmed', client_address)
                    udp_socket.close()
                except IndexError:
                    udp_socket.close()
            except TimeoutError:
                None


#PUT THIS IN MAIN
#online_contacts = set()
#broadcast_port = 9999
#Thread(target=broadcast_server, args=(user.email(), broadcast_port), daemon=True).start()
#Thread(target=broadcast_reciever, args=(broadcast_port, online_contacts), daemon=True).start()