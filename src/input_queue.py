##to be made into an object - may be re-used elsewhere and this global stuff is silly
import threading
sem = threading.Semaphore()

s = []
n = 0
MAX_SIZE = 3

def add(val):
    global n, s, MAX_SIZE
    sem.acquire()
    if(n + 1 <= MAX_SIZE):
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

def qSize():
    global s
    return len(s) 

def isEmpty():
    global s
    if len(s) == 0:
        return True
    else:
        return False


def isFull():
    global s, MAX_SIZE
    if len(s) >= MAX_SIZE:
        return True
    else:
        return False