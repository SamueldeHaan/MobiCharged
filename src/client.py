import socket
import threading
import input_queue as q
import time
import matlab.engine

import firestore
import pickle


device_Name = socket.gethostname()
device_IP = socket.gethostbyname(device_Name)
authSucess = False

soc = socket.socket()

server_ADD ="192.168.1.109"
#server_ADD = socket.gethostbyname(socket.gethostname())
print(server_ADD)
server_PORT = 5001

try:
    eng = matlab.engine.start_matlab()

    path = eng.genpath('src')
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
        input = q.remove()
        if not(input):
            time.sleep(5) ##this can be avoided with signals in the future
            print('No inputs to work on!')
            continue

        #this is hard-coded like crazy, need to fix dynamic inputs

        temp_input = str(input) #'1,2,3,4'
        a = input.split(',') #['1','2','3','4']
        b = list(map(int,a)) # [1,2,3,4]
        A= b[0]
        B= b[1]
        C= b[2]
        D= b[3]

        y = eng.unknown_poly_type(A,B,C,D,nargout = 1)


        #y = eng.sample_simulation2(int(input), nargout=1) #output - hardcoded right now 
        #y = eng.sample_simulation1(int(input), nargout=1) #output - hardcoded right now 
        print('Optimal output:', y)
        count = firestore.check_count() + 1 #take the current number of simulations in the db.
        if y:
            data = {
                'ID' : str(count), #DOCUMENT WILL ONYL WRITE IF THIS IS A STRING
                'Input' : input, 
                'Output' : y,
            }

            data_string = pickle.dumps(data) #i used pickle to send an array
            soc.send(data_string)
            #soc.send(str(y).encode())
        input = None
        
    ##need to quit eng upon connection cancellation / program termination
    eng.quit()

def data_receiving():
    while True:
        data_received = soc.recv(1024).decode()
        if data_received:
            q.add(data_received)
            print("Received data: ", data_received)
        time.sleep(10)
#client_init()