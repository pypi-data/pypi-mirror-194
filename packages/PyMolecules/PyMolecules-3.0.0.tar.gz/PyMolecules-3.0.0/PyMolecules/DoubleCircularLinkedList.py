class Node:
    def __init__(self,data):
        self.data = data
        self.prev = None 
        self.next = None 

class DCLL:
    def __init__(self) -> None:
        self.head = None
        
    def insert_first(self,data):
        new_node = Node(data)
        if self.head is None:
            self.head = new_node
            new_node.next = new_node
            new_node.prev = new_node
        else:
            last_node = self.head.prev
            new_node.next = self.head
            self.head.prev = new_node
            self.head = new_node
            new_node.prev = last_node
            last_node.next = new_node
    
    def insert_last(self,data):
        new_node = Node(data)
        if self.head is None:
            self.head = new_node
            new_node.next = new_node
            new_node.prev = new_node
        else:
            last_node = self.head.prev
            last_node.next = new_node
            new_node.prev = last_node
            new_node.next = self.head
            self.head.prev = new_node
    
    def insert_at_pos(self,pos,data):
        new_node = Node(data)
        if self.head is None:
            self.head = new_node
            new_node.prev = new_node
            new_node.next = new_node
        elif pos < 0:
            raise Exception("Position should be greater than zero")
        elif pos == 0:
            last_node = self.head.prev
            new_node.next = self.head
            self.head.prev = new_node
            self.head = new_node
            last_node.next = self.head
            self.head.prev = last_node
        else: # pos > 0
            curr = self.head
            while pos-1 != 0 and curr.next is not self.head:
                curr = curr.next 
                pos -= 1
            if curr.next is not self.head:
                dummy = curr.next 
                curr.next = new_node
                new_node.prev = curr
                new_node.next = dummy
                dummy.prev = new_node
            else: # curr.next is self.head
                curr.next = new_node
                new_node.prev = curr
                new_node.next = self.head
                self.head.prev = new_node
                
    def traverse_forward(self):
        curr = self.head
        output = []
        while curr is not None:
            output.append(curr.data)
            if curr.next is not self.head:
                curr = curr.next
            else:
                break 
        print(output)
    
    def traverse_backward(self):
        curr = self.head.prev 
        output = []
        while curr is not None:
            output.append(curr.data)
            if curr.prev is not self.head.prev:
                curr = curr.prev
            else:
                break
        print(output)
    
    def delete_first(self):
        if self.head is None:
            raise Exception("Cannot delete from empty Double circular linked list")
        else:
            to_delete = self.head
            if self.head.next is self.head:
                self.head = None 
            else:
                last_node = self.head.prev 
                dummy = self.head.next 
                last_node.next = dummy
                dummy.prev = last_node
                self.head = dummy
            del to_delete
    
    def delete_last(self):
        if self.head is None:
            raise Exception("Cannot delete from empty Double circular linked list")
        else:
            if self.head.next is self.head:
                self.head = None 
            else:
                last_node = self.head.prev 
                last_before_node = last_node.prev
                last_before_node.next = self.head
                self.head.prev = last_before_node
                del last_node
    
    def delete_at_pos(self,pos):
        if self.head is None:
            raise Exception("Cannot delete from empty Double circular linked list")
        if pos < 0:
            raise Exception("The position should be greater than zero")
        elif pos == 0:
            curr = self.head
            if curr.next is not self.head:
                last_node = self.head.prev
                dummy = self.head.next 
                last_node.next = dummy
                dummy.prev = last_node
                self.head = dummy
            else:
                self.head = None 
        else: #pos > 0
            curr = self.head
            while pos-1 != 0 and curr.next is not self.head:
                curr = curr.next 
                pos -= 1
            if curr.next is not self.head:
                to_delete = curr.next 
                if curr.next.next is not self.head:
                    dummy = curr.next.next 
                    curr.next = dummy
                    dummy.prev = curr
                else:
                    curr.next = self.head
                    self.head.prev = curr
                del to_delete
            else:
                raise Exception("The position should be less than size of linkedlist")
                
    def delete(self,element):
        if self.head is None:
            raise Exception("Cannot delete from empty doubly linked list")
        if self.head.data == element:
            to_delete = self.head
            if self.head.next is not self.head:
                last_node = self.head.prev
                dummy = self.head.next
                last_node.next = dummy
                dummy.prev = last_node
                self.head = dummy
            else:
                self.head = None 
            del to_delete
        else:
            previous = None
            curr = self.head
            while curr.next is not self.head:
                if curr.data != element:
                   previous = curr
                   curr = curr.next 
                else:
                    break
            if curr.data == element and curr.next is not self.head:
                previous.next = curr.next
                curr.next.prev = previous
            elif curr.data == element and curr.next is self.head:
                previous.next = self.head
                self.head.prev = previous
            else:
                raise Exception("The element is not present in the Double circular linked list")
                
    def search(self,element):
        curr = self.head
        index = 0
        while True:
            if curr.data == element:
                return index
            curr = curr.next 
            index += 1   
            if curr == self.head:
                break 
        return -1 
    
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
        
        def mergesort(dummy):
            if dummy is None or dummy.next is None:
                return dummy
            front, back = getMiddle(dummy)
            front = mergesort(front)
            back = mergesort(back)
            return sortedMerge(front, back)
        
        # ---- Connection removal starts -----
        last_node = self.head.prev
        last_node.next = None
        self.head.prev = None
        # ---- Connection removal ends -----
        sorted_head = mergesort(self.head)
        self.head = sorted_head
        # ---- Connection starts here after sort ----
        dummy = self.head
        while dummy.next is not None:
               dummy = dummy.next 
        dummy.next = self.head 
        self.head.prev = dummy
        # ---- Connection ends here after sort ----
          
    def reverse(self):
        def remove_connection(temp):
            last_node = temp.prev 
            last_node.next = None
            temp.prev = None
            return temp 
        dummy = None 
        future_last_node = self.head 
        curr = remove_connection(self.head)
        while curr is not None:
            dummy = curr.prev
            curr.prev = curr.next 
            curr.next = dummy
            curr = curr.prev 
        if dummy is not None:
            self.head = dummy.prev
            # Making connection b/w first and last node
            future_last_node.next = self.head
            self.head.prev = future_last_node
            
    def size(self):
        count = 0
        curr = self.head
        while curr is not None:
            count += 1
            if curr.next is not self.head:
                curr = curr.next
            else:
                break 
        return count
    
    def __str__(self):
        return "<class 'DCLL'>"
    
    def first_element(self):
        if self.head is not None:
            return self.head.data
        else:
            raise Exception("No items in the doubly linked list")
    
    def last_element(self):
        if self.head is not None:
            return self.head.prev.data
        else:
            raise Exception("No items in the doubly linked list")
 






            
            
            