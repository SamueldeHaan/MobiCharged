import client
import threading
import input_queue as q
import time
#from server import inputSize
#import server
##main script

"""
Author: Mustafa Choueib
Last Revision Date: March 23rd, 2023.
Purpose: The purpose of this script is to allow users to set an initial input configuration that is passed to the Server socket.
"""



#Ensures client can be initialized before proceeding
client.client_init()
if not(client.authSucess):
    quit()

def User_Input():
    inputSizeGood = False
    outputSizeGood = False
    while True:
        ##add input validation - need a lot here its a user so
        tempList = []
        for numIn in range(4): 
            temp = False
            #Ensures the input is a float value
            while not(temp):
                val = input(f"Input parameter {numIn+1} for the optimization problem:")
                if(val.isnumeric()):
                    tempList.append(float(val))
                    temp = True
                else:
                    print("Input must be numeric 0-9")
            
        q.add(tempList)
        time.sleep(15)

thread_user = threading.Thread(target=User_Input)
thread_user.start()



