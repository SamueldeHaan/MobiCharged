class Node:
    def __init__(self, data):
        self.data = data
        self.next = None

#Invariant: nodes expected to be a non-empty array
class LearnerLinkedList:
    def __init__(self, nodes):
        self.head = Node(None)
        self.tail = Node(None)
        self.head.next = self.head
        self.active = self.head
        self.active_count = 0
        for i in nodes:
            self.add(i)
        
    def add(self, data):
        new_node = Node(data)
        temp = self.head.next
        self.head.next = new_node 
        new_node.next = temp
        self.active_count += 1
    
    def next(self):
        if self.active_count > 0:
            self.active = self.active.next
        return self.active

    def is_last_item(self):
        return self.active_count == 1

    def remove_active(self):
        if self.active_count < 1:
            return
        current = self.head
        while current.next != self.active:
            current = current.next
        prev = current
        #case when last real item being removed
        if prev == self.active.next:
            self.head.next = self.head 
            self.active = self.head
        else:
            prev.next = self.active.next
            self.active = self.active.next
        self.active_count -= 1
        
    def print_list(self):
        current = self.head.next
        while current is not self.head:
            print(current.data)
            current = current.next


# ##test 
# list = LearnerLinkedList([1,2,3,4,5])
# list.print_list()

# ##print(list.active_count)
# print("--------------------------------")


# list.next()
# list.next()
# list.remove_active()
# list.print_list()

# print("--------------------------------")

# list.remove_active()
# list.print_list()