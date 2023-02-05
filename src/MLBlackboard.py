import numpy as np
import threading as th 
import importlib
import matplotlib.pyplot as plt
from PIL import Image
import sys
import re

#In the future, the true MLBlackboard will be primarily a scheduler and task manager

##THIS WILL BE A CLASS IN THE FUTURE
stack_pointer = 0
input_size = 4
init = False
module = 'polyfit'
# model = None
img = None
##needs editing to accept only 4
pattern = "/^(?:\d+(?:\.\d*)?|\.\d+)(?:,(?:\d+(?:\.\d*)?|\.\d+))*$/"
update_predictive_model = th.Event()

# validation_data = 10 ##points to the data saved for validation (about 1/5th of how much we keep for training)

p = importlib.import_module(module)

##THIS WILL BE BLACKBOARD BEHAVIOUR
def prediction_thread(event, module):
    def validate_input(input):
        match = re.fullmatch(pattern, input)
        return match is not None

    while event.is_set:
        print("The current accuracy of the " + module + " model can be seen in " + module + ".png !")
        print("Please provide the input you wish to predict in the following format: input1, input2, input3, input4 - where each input is required and must be a real number.")
        input = sys.stdin.readline().strip
        if validate_input(input):
            ##implement semaphore for shared access between MLBlackboard and UI prediction, both use the same model
            input = input.split(',')
            input = [float(i) for i in input]
            print(input)
            if len(input) == input_size: 
                ##ensures model isn't being tested - waits if it is
                predictions = p.pred(input)
                print("Prediction(s): " + predictions)
                continue
        print("Invalid input!")

thread = th.Thread(target=prediction_thread, args=[update_predictive_model, module]) #thread used for showing 

#control the main loop
def run(epochs):
    if not(init):
        return ##might need better messaging than this
    if thread.is_alive():
        update_predictive_model.clear()
        print("thread cancelled!!!!!")
        thread.join()
    save_and_show_run_graph(p.run(epochs), epochs)
    update_predictive_model.set()
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

init_module()
run(10)
##########Tables hold their associated model