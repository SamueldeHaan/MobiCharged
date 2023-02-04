import client
import threading
import input_queue as q
import time

##main script

client.client_init()
if not(client.authSucess):
    quit()

def user_input():
    while True:
        val = input("Input your desired data for the optimization problem: ")
        ##add input validation - need a lot here its a user so
        if(val):
            q.add(val)
        time.sleep(10)

thread_user = threading.Thread(target=user_input)
thread_user.start()



