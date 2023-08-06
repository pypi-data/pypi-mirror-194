class Node:
    def __init__(self,data) -> None:
        self.data = data 
        self.next = None 
        
class SCLL:
    def __init__(self) -> None:
        self.head = None 
    
    def insert_first(self,data):
        new_node = Node(data)
        if self.head is None:
            self.head = new_node
            new_node.next = new_node
        else:
            new_node.next = self.head 
            curr = self.head
            while curr.next is not self.head:
                curr = curr.next 
            curr.next = new_node
            self.head = new_node
            
    
    def insert_last(self,data):
        new_node = Node(data)
        if self.head is None:
            self.head = new_node
            new_node.next = new_node
        else:
            curr = self.head
            while curr.next is not self.head:
                curr = curr.next
            curr.next = new_node
            new_node.next = self.head
    
    def insert_at_pos(self,pos, data):
        new_node = Node(data)
        if self.head is None:
            self.head = new_node
            new_node.next = new_node
        elif pos < 0:
            raise Exception("Position should be greater than zero")
        elif pos == 0:
            new_node.next = self.head
            curr = self.head
            while curr.next is not self.head:
                curr = curr.next
            curr.next = new_node
            self.head = new_node
        else: # pos > 0
            curr = self.head
            while pos-1 != 0 and curr.next is not self.head:
                curr = curr.next
                pos -= 1
            if curr.next is not self.head:
                dummy = curr.next
                curr.next = new_node
                new_node.next = dummy
            else: # curr.next is self.head
                curr.next = new_node
                new_node.next = self.head
                
    def traverse(self):
        curr = self.head
        output = []
        while curr is not None:
            output.append(curr.data)
            if curr.next is not self.head:
               curr = curr.next
            else:
                break
        print(output)
        
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
    
    def delete_first(self):
        if self.head is None:
            raise Exception("Cannot delete from empty Single circular linked list")
        else:
            if self.head.next is not self.head:
                curr = self.head
                while curr.next is not self.head:
                   curr = curr.next 
                curr.next = self.head.next 
                self.head = self.head.next 
            else:
                self.head = None 
            
    def delete_last(self):
        if self.head is None:
            raise Exception("Cannot delet from empty Single circular linked list")
        else:
            if self.head.next is not self.head:
                previous = None 
                curr = self.head
                while curr.next is not self.head:
                   previous = curr
                   curr = curr.next 
                previous.next = self.head 
            else:
                self.head = None 
    
    def delete(self,element):
        if self.head is None:
            raise Exception("Cannot delete from empty Single circular linked list")
        else:
            previous = None 
            curr = self.head
            while curr.next is not self.head and curr.data != element:
                previous = curr
                curr = curr.next 
            if previous is not None:
                previous.next = curr.next 
            else:
                temp = self.head
                while temp.next is not self.head:
                    temp = temp.next
                if self.head.next is not self.head: 
                    temp.next = self.head.next 
                    self.head = self.head.next
                else:
                    if self.head.data == element:
                       self.head = None 
                    else:
                        raise Exception("The element is not present in the Single circular linked list")

                
    def delete_at_pos(self,pos):
        if self.head is None:
            raise Exception("Cannot delete from empty Single circular linked list")
        if pos < 0:
            raise Exception("The position should be greater than zero")
        if pos == 0:
            if self.head.next is not self.head:
                curr = self.head
                while curr.next is not self.head:
                    curr = curr.next 
                curr.next = self.head.next 
                self.head = self.head.next 
            else:
                self.head = None 
        if pos > 0:
            curr = self.head
            while pos-1 != 0 and curr.next is not self.head:
                curr = curr.next 
                pos -= 1
            if curr.next is not self.head:
                dummy = curr.next.next 
                if dummy is not self.head:
                    curr.next = dummy
                else:
                    curr.next = self.head
            else:
                raise Exception("The position should be less than size of linkedlist") 
                
    def reverse(self):
        if self.head is not None:
            prev = None
            curr = self.head
            after = curr.next 
            curr.next = prev 
            prev = curr
            curr = after
            while curr is not self.head:
                after = curr.next 
                curr.next = prev 
                prev = curr
                curr = after 
            self.head.next = prev 
            self.head = prev 
    
    def sort(self):
        def remove_connection(dummy):
            curr = dummy
            while curr.next is not self.head:
                curr = curr.next 
            curr.next = None 
            return dummy 
        
        def make_connection(dummy):
            curr = dummy
            while curr.next is not None:
                curr = curr.next 
            curr.next = self.head 
        
        def get_middle(dummy):
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
        
        def sorted_merge(a,b):
            if a is None:
                return b
            if b is None:
                return a 
            if a.data <= b.data:
                result = a
                result.next = sorted_merge(a.next,b)
            else:
                result = b
                result.next = sorted_merge(a,b.next)
            return result
        
        def merge_sort(dummy):
            if dummy is None or dummy.next is None:
                return dummy
            else:
                front, back = get_middle(dummy)
                front = merge_sort(front)
                back = merge_sort(back)
                return sorted_merge(front,back)
        
        sll_head = remove_connection(self.head)
        final_head = merge_sort(sll_head)
        self.head = final_head
        make_connection(self.head)
        
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
        return "<class 'SCLL'>"
    


    





