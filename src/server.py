import socket
import threading
import tqdm
import write_table_test
import read_table_test
import time
soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

server_ADD = "192.168.1.107"
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

#may need to change the location of this message; currently used for testing.- EN

modeMessage = ("")
inputMessage = ("Input antenna parameters for simulation seperated by a space \nExample Format: Antenna_Type Antenna_Length Antenna_Width Antenna_Thickness]").encode()


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
        client_socket.send(inputMessage)
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

                ### CALL THE MYSQL DB MODULE HERE; 
                ##Take client's input and pass to ml_hyperparameters table
                
                x = received_data #debugging

                test = write_table_test.write_to_table(str(received_data))
                if (test != None): #send client the errors
                    sendDataClient = (str(test)).encode()
                    c_socket.send(sendDataClient)
                else: #no errors, continue
                    sendDataClient = ("Succesfully inputted into database").encode()
                    c_socket.send(sendDataClient)

                    time.sleep(2)
                    sendDataClient = ("Running Matlab optimization... \n").encode()
                    c_socket.send(sendDataClient)

                    ## Matlab will write to output table using the same write_to_table function
                    ##feed dummy data (int) into input_output table (this is done in write_table_test.py for POC DEMO ONLY)
                    print("write #2")
          
                    dummy_output = '5'#link this to eamon

                    current_row = str(write_table_test.write_to_table(dummy_output))

                    #for some reason, this won't fetch the current row. it's lagging by 1
                    #total_input_output = read_table_test.read_table("input_output")
                    #print(total_input_output)
                    
                    
                    #current_row = read_table_test.most_recent("input_output")
                    #print(current_row)

                    sendDataClient = ("[Simulation # | Input | Output |\n").encode()
                    #sendDataClient  = read_table_test.read_table("input_output").encode()
                    c_socket.send(sendDataClient)

                    sendDataClient  = current_row.encode()
                    #sendDataClient  = read_table_test.read_table("input_output").encode()
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