import socket
import threading
import firestore
import pickle

soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)


server_ADD ="192.168.1.109"
#server_ADD = socket.gethostbyname(socket.gethostname())
print(server_ADD)
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

firestore.initalize_firestore()



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

##testing
Obj1 = {
    'Model': '1',
    'Input' : [5,11],
    'Output' : [1,2,3]
}
Obj2 = {
    'Model': '2',                                                                                                   
    'Input' : [1,13],
    'Output' : [1,5,2]
}
data = Obj1



def receive_thread(c_socket):
    while True:
        try:
            #received_data = c_socket.recv(1024).decode()
            received_data_pickle = c_socket.recv(1024)
            received_data = pickle.loads(received_data_pickle)

            #Make sure received data is not null or empty
            if received_data:
                print(f"Received message: {received_data}")
                print("RECEIVED")
                # sendDataClient = ("Did it work").encode() THIS IS WHERE WE WILL SEND DATA TO THE MYSQL DBs
                # c_socket.send(sendDataClient)
                #broadcast(received_data)

                #Send received data to firestore
                #firestore.write_data(data)
                firestore.write_data(received_data)
                #firestore.write_data_test(received_data)
                #firestore.write_data_test(received_data)


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