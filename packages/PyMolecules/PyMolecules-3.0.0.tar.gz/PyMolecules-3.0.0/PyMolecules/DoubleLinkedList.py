class Node:
    def __init__(self,data) -> None:
        self.data = data
        self.prev = None
        self.next = None

class DLL:
    def __init__(self) -> None:
        self.head = None
        self.tail = None
    
    def insert_first(self,data):
        new_node = Node(data)
        if self.head is None and self.tail is None:
            self.head = self.tail = new_node
        else:
            new_node.next = self.head
            self.head.prev = new_node
            self.head = new_node
    
    def insert_last(self,data):
        new_node = Node(data)
        if self.head is None and self.tail is None:
            self.head = self.tail = new_node
        else:
            self.tail.next = new_node
            new_node.prev = self.tail
            self.tail = new_node
    
    def insert_at_pos(self,pos,data):
        new_node = Node(data)
        if self.head is None and self.tail is None:
            self.head = self.tail = new_node
        elif pos < 0:
            raise Exception("Position should be greater than zero")
        elif pos == 0:
            new_node.next = self.head
            self.head.prev = new_node
            self.head = new_node
        else: # pos > 0
            curr = self.head
            while pos-1 != 0 and curr.next is not None:
                curr = curr.next
                pos -= 1
            if curr.next is not None:
                dummy = curr.next
                curr.next = new_node
                new_node.prev = curr
                new_node.next = dummy
                dummy.prev = new_node
            else: # curr.next is None
                curr.next = new_node
                new_node.prev = curr
                self.tail = new_node
                
    def traverse_forward(self):
        curr = self.head
        output = []
        while curr is not None:
            output.append(curr.data)
            curr = curr.next
        print(output)
        
    def traverse_backward(self):
        curr = self.tail
        output = []
        while curr is not None:
            output.append(curr.data)
            curr = curr.prev
        print(output)
    
    def search(self,element):
        index = 0
        curr = self.head
        while curr is not None:
            if curr.data == element:
                return index
            else:
                curr = curr.next
                index += 1
        return -1
            
    def delete_first(self):
        if self.head is None and self.tail is None:
            raise Exception("Cannot delete from empty doubly linked list")
        else:
            to_delete = self.head
            if self.head.next is None and self.tail.next is None:
                self.head = self.tail = None 
            else: # self.head.next is not None
                self.head = self.head.next 
            del to_delete
                
    def delete_last(self):
        if self.head is None and self.tail is None:
            raise Exception("Cannot delete from empty doubly linked list")
        else:
            if self.head.next is None and self.tail.next is None:
                self.head = self.tail = None 
            else:
                previous = None
                curr = self.head
                while curr.next is not None:
                    previous = curr
                    curr = curr.next
                if previous is not None:
                    previous.next = None
                    self.tail = previous
                else:
                    self.head = self.tail = None
                del curr 
    
    def delete(self,element):
        if self.head is None and self.tail is None:
            raise Exception("Cannot delete from empty doubly linked list")
        if self.head.data == element:
            to_delete = self.head
            self.head = self.head.next
            if self.head is not None:
               self.head.prev = None
            else:
                self.tail = None
            del to_delete
        else:
            previous = None
            curr = self.head
            while curr is not None:
                if curr.data != element:
                    previous = curr
                    curr = curr.next
                else:
                    break
            if curr is not None:
                to_delete = curr 
                if curr.next is not None:
                    dummy = curr.next
                    previous.next = dummy
                    dummy.prev = previous
                else:
                    previous.next = None
                    self.tail = previous
                del to_delete
            else:
                 raise Exception("The element is not present in the doubly linked list")
    
    def delete_at_pos(self,pos):
        if self.head is None:
            raise Exception("Cannot delete from empty doubly linked list")
        if pos < 0:
            raise Exception("The position should be greater than zero")
        if pos == 0:
            to_delete = self.head
            self.head = self.head.next
            if self.head is not None:
               self.head.prev = None
            else:
                self.tail = None
            del to_delete
        if pos > 0:
            curr = self.head
            while pos-1 != 0 and curr.next is not None:
                curr = curr.next
                pos -= 1
            if curr.next is not None:
                to_delete = curr.next 
                if curr.next.next is not None:
                    dummy = curr.next.next
                    curr.next = dummy
                    dummy.prev = curr
                else:
                    curr.next = None 
                    self.tail = curr 
                del to_delete
            else:
                raise Exception("The position should be less than size of linkedlist")
    
    def reverse(self):
        dummy = None
        curr = self.head
        future_tail = self.head
        while curr is not None:
            dummy = curr.prev
            curr.prev = curr.next
            curr.next = dummy
            curr = curr.prev
        if dummy is not None:
            self.head = dummy.prev
            self.tail = future_tail
    
    def sort(self):
        def getMiddle(dummy):
            if (dummy == None):
                return dummy
            slow = dummy
            fast = dummy
            while (fast.next != None and fast.next.next != None):
                slow = slow.next
                fast = fast.next.next
            tup = dummy, slow.next
            slow.next = None
            return tup
        
        def sortedMerge(a,b):
            if a is None:
                return b
            if b is None:
                return a
            if a.data < b.data:
                a.next = sortedMerge(a.next,b)
                a.next.prev = a
                a.prev = None
                return a
            else:
                b.next = sortedMerge(a,b.next)
                b.next.prev = b
                b.prev = None
                return b
        
        def find_tail():
            curr = self.head
            while curr.next is not None:
                curr = curr.next
            return curr
            
        def mergesort(dummy):
            if dummy is None or dummy.next is None:
                return dummy
            front, back = getMiddle(dummy)
            front = mergesort(front)
            back = mergesort(back)
            return sortedMerge(front, back)
        
        sorted_head = mergesort(self.head)
        self.head = sorted_head
        self.tail = find_tail()
        
    def size(self):
        curr = self.head
        count = 0
        while curr is not None:
            count += 1
            curr = curr.next 
        return count
               
    def __str__(self):
        return "<class 'DLL'>"
    
    def first_element(self):
        if self.head is not None:
            return self.head.data
        else:
            raise Exception("No items in the doubly linked list")
    
    def last_element(self):
        if self.head is not None and self.tail is not None:
            return self.tail.data
        else:
            raise Exception("No items in the doubly linked list")


















