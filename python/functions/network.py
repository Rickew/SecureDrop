import ssl
import socket
from threading import Thread
from time import sleep

def server_socket(server_ip, server_port):
    udps_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    udps_socket.bind((server_ip, server_port))
    
def client_socket(data, client_ip, client_port):
    udpc_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    udpc_socket.sendto(data, (client_ip, client_port))



def reciever(udp_socket):
    try:
        data = udp_socket.recv(1024)
        print(f"Recieved: {data.decode('utf-8')}")
        udp_socket.send(data)
    except Exception as e:
        print(f"Error handling client: {e}")
    finally:
        udp_socket.close()


def online(user):
    """Broadcast user's online status and collect responses."""
    server_ip =  "0.0.0.0"
    server_port = 9999

    client_ip = '192.168.3.38'
    client_port = 9999

    

    #udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    #udp_socket.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
    #udp_socket.settimeout(5)
    #thread = Thread(target = thread_Function, args = (10, ))
    #thread.start()
    #thread.join()
    # Broadcast the user's online status
    #data = user.encode('utf-8')
    #udp_socket.sendto(data, (server_ip, server_port))
    print(f"Broadcasting online status for user: {user}")

    online_users = []

    #try:
    #    while True:
    #       response, _ = udp_socket.recvfrom(1024)
    #        online_users.append(response.decode('utf-8'))
    #except socket.timeout:
    #    print("Broadcast complete.")
    #finally:
    #    udp_socket.close()

    return online_users

def display_contact(user, contact):
    """Check and display contact's status."""
    if not friend_check(user, contact):
        print(f"{contact} is not a friend of {user}.")
        return

    online_users = online(user)
    if contact not in online_users:
        print(f"{contact} is not online.")
        return

    # All conditions met
    print(f"Contact {contact} is online and a verified friend!")



if __name__ == "__main__":
    user = input("Enter your username: ")
    contact = input("Enter the contact's username: ")

    # Add sample data for testing
    add_friend(user, "friend1")  # Add "friend1" as a friend
    add_friend("friend1", user)

    # Simulate online response for testing
    print("Simulating online response... (no actual response expected)")

    # Check and display contact info
    display_contact(user, contact)


