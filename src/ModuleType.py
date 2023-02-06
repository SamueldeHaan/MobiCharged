import numpy as np
import threading as th 
import importlib
import matplotlib.pyplot as plt
from PIL import Image
import re
import time

#In the future, the true MLBlackboard will be primarily a scheduler and task manager

##THIS WILL BE A CLASS IN THE FUTURE
stack_pointer = 0
input_size = 4
init = False
module = 'polyfit'
# model = None
img = None
##needs editing to accept only 4
pattern = "^(?:\d+(?:\.\d*)?|\.\d+)(?:,(?:\d+(?:\.\d*)?|\.\d+))*$"
update_predictive_model = th.Event()

# validation_data = 10 ##points to the data saved for validation (about 1/5th of how much we keep for training)

p = importlib.import_module(module)

##THIS WILL BE BLACKBOARD BEHAVIOUR - INPUT HANDLING NEEDS WORK
def prediction_thread(module):
    # global update_predictive_model
    print("------------------------------------------------------------------------------------------")
    print("Wait a couple of seconds for the process to get ready.")
    def input_thread(result, lock):
        # print("made it to input")
        result.append(input())
        lock.release()
        # print("lock released")

    def get_input_with_timeout(timeout):
        lock = th.Lock()
        # print("here?")
        lock.acquire()
        # print("Lock acquired")
        result = []
        t = th.Thread(target=input_thread, args=[result, lock])
        t.daemon = True
        t.start()
        t.join(timeout)
        if lock.locked():
            return None
        else:
            return result[0]

    def validate_input(input):
        match = re.fullmatch(pattern, input)
        return match is not None

    while True:
        print("The current accuracy of the " + module + " model can be seen in " + module + ".png !")
        print("Please provide the input you wish to predict in the following format: input1,input2,input3,input4 (no spaces) - where each input is required and must be a real number.")
        # NEED TO FIGURE OUT WHY SELECT DOESN'T WORK AND WHAT ALTERNATIVES THERE ARE
        
        while True:
            if(update_predictive_model.is_set()):
                break
            x = get_input_with_timeout(10)
            # print("what about here?")
            if x:
                # print("value provided")
                break

        if(update_predictive_model.is_set()):
            break
        # print("input:" + x)
        if validate_input(x):
            ##implement semaphore for shared access between MLBlackboard and UI prediction, both use the same model
            x = x.split(',')
            x = [float(i) for i in x]
            if len(x) == input_size: 
                ##ensures model isn't being tested - waits if it is
                ##right now only accepting one prediction at a time
                predictions = p.pred(x)
                print("Prediction(s): " + str(predictions))
                continue
        print("Invalid input!")

thread = th.Thread(target=prediction_thread, args=[module]) #thread used for showing 

#control the main loop
def run(epochs, input_data, output_data):
    global thread
    if not(init):
        return ##might need better messaging than this
    not_first_run = thread.is_alive()
    if not_first_run:
        update_predictive_model.set()
        print("Halting process - new model to be trained.")
        thread.join()
    ##THIS LINE NEEDS TO BE BROKEN UP - TOO MUCH HAPPENING IN ONE PLACE
    save_and_show_run_graph(p.run(epochs, np.array(input_data).astype(float, copy=False), np.array(output_data).astype(float, copy=False)), epochs)
    update_predictive_model.clear()

    thread = th.Thread(target=prediction_thread, args=[module])
    thread.start()
    

def init_module(): ##is there a way to confirm we have room for the data before we read it? maybe handled in param_read()
    ##this creates object with table name, the model filename, the quota number
    global init, model
    model = p.setup() 
    init = True
    return

# def data_read(): ##error handling - duplicate checking
#     return

# don't 100% have this behaviour yet
# def param_read():
#     return

# def param_write():
#     return

def save_and_show_run_graph(history, epoch_num): 
    global img
    if img:
        img.close()
    textstr = 'Training error=%.2f\nValidation error=%.2f\n'%(history.losses[-1], history.val_losses[-1])
    plt.plot(history.losses)
    plt.plot(history.val_losses)
    plt.title('Model Loss Over ' + str(epoch_num) + ' Epochs With Early Stopping')
    plt.text(0.02, 0.5, textstr, fontsize=14, transform=plt.gcf().transFigure)
    plt.subplots_adjust(left=0.4)
    plt.ylabel('Loss')
    plt.xlabel('Epoch')
    plt.legend(['Train', 'Validation'], loc='upper right')
    plt.savefig( module + '.png')
    img = Image.open(module + '.png')
    img.show()
    plt.clf()

# init_module()
# run(10)
# time.sleep(5)
# run(100)

# init_module()
# run(10)

# time.sleep(5)
# run(100)


##########Tables hold their associated model