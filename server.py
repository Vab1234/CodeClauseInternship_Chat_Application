import socket
import threading
from tkinter import *

HOST = '127.0.0.1'
PORT = 1234
LIMIT = 7
CLIENTS = []

def listen_msg(client , username):
    while True:
        response = client.recv(2048).decode("utf-8")
        if response != "":

            message = username + " : " + response
            send_message_to_all(message)

        else:
            print(f"The message is empty from {username}")

def send_msg_to_a_client(client , message): 
    client.sendall(message.encode())




def send_message_to_all(message):
    for user in CLIENTS:
        send_msg_to_a_client(user[1] , message)


def handle_client(client):
    while True:
        username = client.recv(2048).decode('utf-8')
        if username == "":
            print("Username is empty")
        else:
            CLIENTS.append((username , client))
            added_msg = "SERVER : " + f"{username} added to chat"
            send_message_to_all(added_msg)
            break
    threading.Thread(target=listen_msg , args = (client , username ,)).start()





def main():

    my_server = socket.socket(socket.AF_INET , socket.SOCK_STREAM)

    try:
        my_server.bind((HOST , PORT))
        print(f"Server is running on {HOST} {PORT}")
    except:
        print(f"Sorry , Not able to bind to the host {HOST} and port {PORT}")

    my_server.listen(LIMIT)
 
    while True:
        client , address = my_server.accept()
        print(f"Successfully connected to client {address[0]} {address[1]}")

        threading.Thread(target=handle_client , args = (client ,)).start()

if __name__ == '__main__':
    main()
