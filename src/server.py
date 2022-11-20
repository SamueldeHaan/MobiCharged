import socket
import threading
# import tqdm

soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

server_ADD = "192.168.0.15"
server_PORT = 5001

connected_clients = []

soc.bind((server_ADD, server_PORT))

#Authorization Key
authorizationKey = "mobicharged"

#Message sent by server for authorization key
authorizationMessage = ("Please send in the verification key: ").encode()
#Message sent if refused connection
refusedMessage = ("Incorrect authorization key, refusing connection").encode()
#Message sent if accepted connection
acceptMessage = ("Correct authorization key, accepting connection").encode()

print("LAN Server is now running....")

def Client_Connections():
    while True:
        #Listen for connections (no limit to number of connections allowed)
        soc.listen()
        c_socket, c_add = soc.accept()
        print(f"[+] {c_add} is connected. Requesting Authorization ....")
        authSuccess = authorizationAccess(c_socket, c_add)
        if authSuccess:
            print(f"[+] {c_add} Authorized Successfully")
            connected_clients.append(c_socket)
            client_data_receiver_thread(c_socket)
            print("Currently Connected Clients: ")
            print(connected_clients)



def authorizationAccess(client_socket, c_add):
    authSuccess = False
    client_socket.send(authorizationMessage)
    keyData = client_socket.recv(1024)

    if(keyData.decode() != authorizationKey):
        client_socket.send(refusedMessage)
        client_socket.close()
        s = socket.socket()
        print(f"[-] {c_add} is disconnected. (Authorization Failed)")
    else:
        client_socket.send(acceptMessage)
        authSuccess = True
        return authSuccess


def client_data_receiver_thread(c_socket):
    c_thread = threading.Thread(target=receive_thread, args=(c_socket,))
    c_thread.start()

def receive_thread(c_socket):
    while True:
        try:
            received_data = c_socket.recv(1024).decode()
            #Make sure received data is not null or empty
            if received_data:
                print(f"Received message: {received_data}")
                sendDataClient = ("Did it work").encode()
                c_socket.send(sendDataClient)
                #broadcast(received_data)
            else:
                print(f"Client disconnected: {c_socket}")
                return
        except:
            connected_clients.remove(c_socket)
            print(f"Client Disconnected: {c_socket}")
            print("Currently Connected Clients: ")
            print(connected_clients)
            return


def broadcast(message):
    for c_socket in connected_clients:
        try:
            c_socket.send(message.encode())
        except:
            connected_clients.remove(c_socket)
            print(f"Removed Client From Connected Clients: {c_socket}")


Client_Connections()