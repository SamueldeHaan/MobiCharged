import threading

class ConcurrencyMonitor:
    def __init__(self, payload):
        self.lock = threading.Lock()
        self.data = payload 
    
    def get_payload(self):
        with self.lock:
            return self.data
    
    def set_payload(self, payload):
        with self.lock:
            self.data = payload