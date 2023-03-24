import socket
import threading
import input_queue as output_q
import random
import json
import os

import pickle
import firestore

import ast

"""
Author: Mustafa Choueib
Last Revision Date: March 23rd, 2023.
Purpose: The purpose of this script is to serve as the Server socket that collects the matlab simulation results from specific input values and stores them.
         The server also allows for multiple authorized clients to connect from any network and receive random input from the server to complete a autonomous loop.
"""

global inputSize, inputList, outputSize, simFileName
global soc, server_ADD, server_PORT, connected_clients, authorizationKey, authorizationMessage, refusedMessage, acceptMessage, sem, displayConnectedClients

def Server_init():
    #Initializes the Server socket with specified configuration
    global soc, server_ADD, server_PORT, connected_clients, authorizationKey, authorizationMessage, refusedMessage, acceptMessage, sem, displayConnectedClients
    soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    server_ADD = ""
    server_PORT = 5001

    connected_clients = []
    displayConnectedClients = []

    soc.bind((server_ADD, server_PORT))

    sem = threading.Semaphore()

    #Authorization Key
    authorizationKey = "mobicharged"

    #Message sent by server for authorization key
    authorizationMessage = ("Please send in the verification key: ").encode()
    #Message sent if refused connection
    refusedMessage = ("Incorrect authorization key, refusing connection").encode()
    #Message sent if accepted connection
    acceptMessage = ("Correct authorization key, accepting connection... The MATLAB simulation file being used by the server is: " + simFileName + " Please use this simulation file or you may experience issues.").encode()

    print("Checking Local Data Repository")
    RestoreCheck()

    print("MobiCharged Server is now running....")
    Client_Connections()

def RestoreCheck():
    #This function will ensure that the server is starting from the last point in which is ended. 
    #If the server unexpectedly closed while there was local data that has not been transfered to main database, it will load that data to the current queue automatically
    file_name = "database.txt"
    if not os.path.exists(file_name):
        file = open('database.txt', 'w+')
        file.close()
        print("Local Data Repository not found, creating new one!")

    if os.path.getsize(file_name) == 0:
        print("Clean Local Database, Current Queue is empty!")
    else:    
        with open('database.txt', 'r') as file:
            lines = file.readlines()
            for line in lines:
                line_ast = ast.literal_eval(line)
                output_q.add(line_ast)
        print("Local Queue Restored, Current Queue Size: " + str(output_q.qSize()))



#Grabs the desired configuration from the GUI and initializes them
def Server_Configuration(inputSizelo, outputSizelo, inputRangeList, simFile):
    global inputSize, outputSize, inputList, simFileName
    inputSize = int(inputSizelo)
    outputSize = int(outputSizelo)
    inputList = inputRangeList
    simFileName = simFile
    Server_init()


def Client_Connections():
    while True:
        #Listen for connections (no limit to number of connections allowed)
        soc.listen()
        c_socket, c_add = soc.accept()
        print(f"[+] {c_add} is connected. Requesting Authorization ....")
        authSuccess = authorizationAccess(c_socket, c_add)
        #Requests the authorization key from the client, and allows client to connect if given the correct key
        if authSuccess:
            print(f"[+] {c_add} Authorized Successfully")
            connected_clients.append(c_socket)
            displayConnectedClients.append(c_add)
            #Adds the new client to the receiver thread to enable communication with the client
            client_data_receiver_thread(c_socket, c_add)
            print("Currently Connected Clients: ")
            print(displayConnectedClients)


#This function ensures authorized access
def authorizationAccess(client_socket, c_add):
    authSuccess = False
    client_socket.send(authorizationMessage)
    try:
        keyData = client_socket.recv(1024)
    except:
        keyData = ""
        keyData = keyData.encode()
        print("No Response Received From Client, Disconnected!")

    try:
        #Refuses connection if the wrong key is given
        if(keyData.decode() != authorizationKey):
            client_socket.send(refusedMessage)
            client_socket.close()
            s = socket.socket()
            print(f"[-] {c_add} is disconnected. (Authorization Failed)")
        else:
            client_socket.send(acceptMessage)
            authSuccess = True
            return authSuccess
    except:
        print("Client Disconnected")

#Starts the receiver thread responsible for receiving messages from the clients
def client_data_receiver_thread(c_socket, c_add):
    c_thread = threading.Thread(target=receive_thread, args=((c_socket, c_add),))
    c_thread.start()

def receive_thread(c_socket):
    #c_socket is a tuple containing socket object in position 0, and the address in position 1
    while True:
        try:
            #Waits until a message is received from a client
            received_data = c_socket[0].recv(1024)#.decode()
            received_data = pickle.loads(received_data)

            #Make sure received data is not null or empty
            sem.acquire()
            if received_data:
                print(f"Received Optimized Simulation from {c_socket[1]}: {received_data}")
                
                if not(output_q.isFull()):
                    #At some point, have current queue locally backed up for sake of preservation
                    #Add each individual input/output pair to local database, once full transfer data and clear local database.
                    #Adding new input/output pair to queue

                    #Adds the received input/output pair to a local queue and writes it to a 'local database'
                    output_q.add(received_data)
                    file = open('database.txt', 'a')
                    file.write(str(received_data) + "\n")
                    file.close()

                    print("Current Queue Size: " + str(output_q.qSize()))
                    #Generates new random inputs based on the input ranges specified
                    newResponse = newInput()
                    newEncodedResponse = newResponse.encode()
                    print(f"Sending Random Input To {c_socket[1]}: " + newResponse)
                    c_socket[0].send(newEncodedResponse)
                    print("\n")
                else:
                    #If the queue is full, currently set to 5 input/output pairs, the data in the queue is transfered to the database
                    DataTransfer()
                    output_q.add(received_data)
                    #Begins storing new batch of data to local database
                    file = open('database.txt', 'a')
                    file.write(str(received_data) + "\n")
                    file.close()

                    print("Current Queue Size: " + str(output_q.qSize()))
                    #Generating new inputs
                    newResponse = newInput()
                    newEncodedResponse = newResponse.encode()
                    print(f"Sending Random Input To {c_socket[1]}: " + newResponse)
                    c_socket[0].send(newEncodedResponse)
                    print("\n")
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
    #Creating new input to keep simulation autonomous after being initialized using the ranges provided by the original server configuration
    tempList = []
    for inputVal in inputList:
        intData = random.uniform(float(inputVal[0]), float(inputVal[1]))
        tempList.append(intData)
        
    #intData = int(intData)
    #newInput = str(intData)
    newInputParam = json.dumps(tempList)
    return newInputParam

def DataTransfer():
    #Temporarily writing to text file (this is where data will be pushed to database)
    #file = open('Tdatabase.txt', 'a')
    print("Data Transfer beginning.")
    for dataT in range(output_q.qSize()):
        #Add confirmation that data was transfered successfully.
        currentVal = output_q.remove()
        firestore.write_data(currentVal) #FIX OBJECT TYPE
        print("Transfering: " + str(currentVal))
        #file.write(str(currentVal) + "\n")
        
    #file.close()
    print("Data Transfer Complete, current queue: " + str(output_q.s))
    print("Clearing Local Data Storage")
    with open('database.txt', 'r+') as file:
        file.truncate(0)
    file.close()

    

#Client_Connections()
#Server_Configuration()