class Stack():

    stack = []
    numelements = 0

    def push(self,value):
        self.stack.append(value)
        self.numelements+=1
    
    def pop(self):
        value = 0
        if self.numelements == 0:
            raise Exception("Trying to pop on a empty stack")
        else:
            self.numelements-=1
            value = self.stack.pop()
            return value
    
    def empty(self):
        if self.numelements == 0:
            return True
        else:
            return False
    
    def top(self):
        if self.numelements == 0:
            raise Exception("Trying to get the top of a empty stack")
        else:
            return self.stack[self.numelements-1]
    
    def size(self):
        return self.numelements


    
    