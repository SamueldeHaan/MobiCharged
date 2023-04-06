import queue
import threading

global queue_updated

# Create a lock
lock = threading.Lock()

# Create a queue
my_queue = queue.Queue()

# Flag to indicate if the queue has been updated
queue_updated = False

#Flag to indicate that a new image has been generated after saving a model



# Function to add an item to the queue and set the flag
def add_item(item):
    global queue_updated, lock
    with lock:
        my_queue.put(item)
        queue_updated = True
    #print(queue_updated,item)

# Function to retrieve an item from the queue and clear the flag
def get_item():
    global queue_updated, lock
    with lock:
        queue_updated = False
        return my_queue.get()