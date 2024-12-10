from Crypto.Cipher import AES 
from Crypto.Random import get_random_bytes
import ssl
import socket
from threading import Thread
from time import sleep


def is_online(username):

    udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    udp_socket.setsockopt(socket.SQL_SOCKET, socket.SO_BROADCAST, 1)
    while True:
        message = f"{username}".encode('utf-8')
        udp_socket.sendto(message, ('0.0.0.0', 9999))
        sleep(5)

def udp_receiver():
    hostname = socket.gethostname()
    udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    udp_socket.bind((socket.gethostbyname(hostname), 9999))
    while True:
        data, addr = udp_socket.recvfrom(1024)

#PUT THIS IN MAIN
#online_contacts = set()
#broadcast_port = 9999
#Thread(target=broadcast_server, args=(user.email(), broadcast_port), daemon=True).start()
#Thread(target=broadcast_reciever, args=(broadcast_port, online_contacts), daemon=True).start()