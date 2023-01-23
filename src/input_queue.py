##to be made into an object - may be re-used elsewhere and this global stuff is silly
import threading
sem = threading.Semaphore()

s = []
n = 0
MAX_SIZE = 10

def add(val):
    global n, s, MAX_SIZE
    sem.acquire()
    if(n + 1 < MAX_SIZE):
        s.append(val)
        n += 1
    ##else condition?
    print('Added to queue: ', val)
    sem.release()

def remove():
    global n, s, MAX_SIZE
    out = None
    sem.acquire()
    if(n > 0):
        n -= 1
        out =  s.pop()
        print('Removed from queue: ', out)
    sem.release()
    return out