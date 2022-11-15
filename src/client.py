import socket
import threading
#import clientmat

device_Name = socket.gethostname()
device_IP = socket.gethostbyname(device_Name)
authSucess = False


soc = socket.socket()
server_ADD = "192.168.0.16"
server_PORT = 5001

soc.connect((server_ADD, server_PORT))
data = soc.recv(1024)
print(f"{data!r}")

sendMessage = input("Enter Authorization Key: ")
soc.sendall(sendMessage.encode())
data = soc.recv(1024)
print(f"{data!r}")

if data.decode() == "Correct authorization key, accepting connection":
    authSucess = True


def data_sending():
    while True:
        data_sent = input()
        if data_sent:
            data_transfer = device_Name + " - " + device_IP + ": " + data_sent
            soc.send(data_transfer.encode())

def data_receiving():
    while True:
        data_received = soc.recv(1024).decode()
        #if data_received:
        #    data_received = clientmat.serverPassedData(data_received)
        print(data_received)



if authSucess:
    thread_sending = threading.Thread(target=data_sending)
    thread_receiving = threading.Thread(target=data_receiving)
    thread_sending.start()
    thread_receiving.start()
