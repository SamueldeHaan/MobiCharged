import socket
import threading
import input_queue as output_q
import random
import json

global inputSize
global outputSize
global inputList
global soc, server_ADD, server_PORT, connected_clients, authorizationKey, authorizationMessage, refusedMessage, acceptMessage, sem

def Server_init():
    global soc, server_ADD, server_PORT, connected_clients, authorizationKey, authorizationMessage, refusedMesasged, acceptMessage, sem
    soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    server_ADD = ""
    server_PORT = 5001

    connected_clients = []

    soc.bind((server_ADD, server_PORT))

    sem = threading.Semaphore()

    #Authorization Key
    authorizationKey = "mobicharged"

    #Message sent by server for authorization key
    authorizationMessage = ("Please send in the verification key: ").encode()
    #Message sent if refused connection
    refusedMessage = ("Incorrect authorization key, refusing connection").encode()
    #Message sent if accepted connection
    acceptMessage = ("Correct authorization key, accepting connection").encode()

    print("LAN Server is now running....")
    Client_Connections()

def Server_Configuration(inputSizelo, outputSizelo, inputRangeList):
    global inputSize, outputSize, inputList
    inputSize = int(inputSizelo)
    outputSize = int(outputSizelo)
    inputList = inputRangeList
    Server_init()


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
            client_data_receiver_thread(c_socket, c_add)
            print("Currently Connected Clients: ")
            print(connected_clients)


#This function ensures authorized access
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


def client_data_receiver_thread(c_socket, c_add):
    c_thread = threading.Thread(target=receive_thread, args=((c_socket, c_add),))
    c_thread.start()

def receive_thread(c_socket):
    #c_socket is a tuple containing socket object in position 0, and the address in position 1
    while True:
        try:
            received_data = c_socket[0].recv(1024).decode()
            #Make sure received data is not null or empty
            sem.acquire()
            if received_data:
                print(f"Received Optimized Simulation from {c_socket[1]}: {received_data}")
                splitList = received_data.split("/")
                if not(output_q.isFull()):
                    #At some point, have current queue locally backed up for sake of preservation
                    #Add each individual input/output pair to local database, once full transfer data and clear local database.

                    #Adding new input/output pair to queue
                    output_q.add((splitList[0], splitList[1]))
                    #print(output_q.qSize())
                    print("Current Queue Size: " + str(output_q.qSize()))
                    #Generating new inputs
                    newResponse = newInput()
                    newEncodedResponse = newResponse.encode()
                    print(f"Sending Random Input To {c_socket[1]}: " + newResponse)
                    c_socket[0].send(newEncodedResponse)
                else:
                    DataTransfer(output_q)
                    output_q.add((splitList[0], splitList[1]))
                    print("Current Queue Size: " + str(output_q.qSize()))
                    #Generating new inputs
                    newResponse = newInput()
                    newEncodedResponse = newResponse.encode()
                    print(f"Sending Random Input To {c_socket[1]}: " + newResponse)
                    c_socket[0].send(newEncodedResponse)
                # sendDataClient = ("Did it work").encode() THIS IS WHERE WE WILL SEND DATA TO THE MYSQL DBs
                # c_socket.send(sendDataClient)
                #broadcast(received_data)
            else:
                print(f"Client disconnected: {c_socket[1]}")
                return
            sem.release()

        except:
            connected_clients.remove(c_socket[0])
            print(f"Client Disconnected: {c_socket[1]}")
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

def newInput():
    #Creating new input to keep simulation autonomous after being initialized
    tempList = []
    for inputVal in inputList:
        intData = random.uniform(float(inputVal[0]), float(inputVal[1]))
        tempList.append(intData)
        
    #intData = int(intData)
    #newInput = str(intData)
    newInputParam = json.dumps(tempList)
    print(newInputParam)
    return newInputParam

def DataTransfer(output_queue):
    #Temporarily writing to text file (this is where data will be pushed to database)
    file = open("\\root\\Mobicharged-Server\\database.txt", 'a')
    for dataT in output_q:
        print("Transfering: " + dataT)
        file.write(dataT + "\n")
    file.close()
    output_q.qClear()
    print("Data Transfer Complete, current queue: " + output_q)
    

#Client_Connections()
#Server_Configuration()