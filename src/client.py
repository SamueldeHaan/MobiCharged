import socket
import threading
import input_queue as q
import time
import matlab.engine
import json

#import firestore
import pickle
import uuid 

device_Name = socket.gethostname()
device_IP = socket.gethostbyname(device_Name)
authSucess = False

soc = socket.socket()
server_ADD = "172.105.14.186"
server_PORT = 5001

try:
    eng = matlab.engine.start_matlab()
    #Add check to make sure path works
    path = eng.genpath('matlab')
    if path == "":
        newPath = input("Please Enter the Full Path of the Matlab Simulation File: ")
        newPath.replace("\\", "\\\\")
        path = eng.genpath(newPath)
    eng.addpath(path, nargout=0)

except Exception as e:
    print(e)
    quit()

def client_init():
    global authSucess
    soc.connect((server_ADD, server_PORT))
    data = soc.recv(1024)
    print(f"{data!r}")

    sendMessage = input("Enter Authorization Key: ")
    soc.sendall(sendMessage.encode())
    data = soc.recv(1024)
    print(f"{data!r}")

    if data.decode() == "Correct authorization key, accepting connection":
        authSucess = True
        thread_sending = threading.Thread(target=data_sending)
        thread_receiving = threading.Thread(target=data_receiving)
        thread_sending.start()
        thread_receiving.start()

def data_sending():
    while True:
        #Testing to see if system is idle for 10 minutes, then providing a notice
        t0 = time.time()
        while(q.isEmpty()):
            t1 = time.time()
            if((t1-t0) >= 600):
                t0 = time.time()
                print("\nQueue is currently empty, please provide optimization inputs: ")
            pass
        inputParams = q.remove()
        
        #Temporarily set to inputParams[0] as the actual simulation file is not available yet
        #Setting inputParams[0] is only passing 1 of the input values in the list. 
        b = list(map(float,inputParams))
        A= b[0]
        B= b[1]
        C= b[2]
        D= b[3]
        y = eng.unknown_poly_type(A,B,C,D, nargout=1) #output - hardcoded right now 
        print('Optimal output:', y)
        
        #outputInputPair = str(inputParams) + "/" + str(y)

        #count = firestore.check_count() + 1 #take the current number of simulations in the db.
        UID = uuid.uuid4()
        if y:
            data = {
                "ID" : str(UID), #DOCUMENT WILL ONYL WRITE IF THIS IS A STRING
                "Input" : inputParams, 
                "Output" : y,
            }

            data_string = pickle.dumps(data) #i used pickle to send an array
            soc.send(data_string)
            #soc.send(outputInputPair.encode())

        #if q.isEmpty():
         #   time.sleep(5) ##this can be avoided with signals in the future
            #print('\nNo inputs to work on!')
          #  continue
        inputParams = None

    ##need to quit eng upon connection cancellation / program termination
    eng.quit()

def data_receiving():
    while True:
        data_received = soc.recv(1024).decode()
        if data_received:
            print("Received New Input: ", data_received)
            newInputReceived = json.loads(data_received)
            q.add(newInputReceived)
        time.sleep(10)