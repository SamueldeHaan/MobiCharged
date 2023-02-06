import client
import threading
import input_queue as q
import time
#from server import inputSize
import server
##main script


client.client_init()
if not(client.authSucess):
    quit()

def user_input():
    inputSizeGood = False
    outputSizeGood = False



    while True:

        ##add input validation - need a lot here its a user so
        temp_List = []
        for numIn in range(4): 
        #for numIn in range(int(server.inputSize)): 
            #val = input("Input your desired data for the optimization problem: ")
            temp = False
            while not(temp):
                val = input(f"Input parameter {numIn+1} for the optimization problem:")
                if(val.isnumeric()):
                    temp_List.append(val)
                    temp = True
                else:
                    print("Input must be numeric 0-9")
            
        q.add(temp_List)
        time.sleep(15)

thread_user = threading.Thread(target=user_input)
thread_user.start()



