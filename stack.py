class Stack:
    def __init__(self):
        self.items = []

    def is_empty(self):
        return not self.items

    def push(self, item):
        self.items.append(item)

    def pop(self):
        if not self.is_empty():
            return self.items.pop()
        return None

    def peek(self):
        if not self.is_empty():
            return self.items[-1]
        return None

    def size(self):
        return len(self.items)
    
    def lastEnv(self):
        for item in reversed(self.items):
            if isinstance(item, dict):
                return item
        return None
    
    def lastEnv(self, previous_env=None):
        found = previous_env is None
        for item in reversed(self.items):
            if found and isinstance(item, dict):
                return item
            if item is previous_env:
                found = True
        return None
    
    def setVariable(self, name, value):
        self.lastEnv()[name] = value
  
    def getVariable(self, variable_name):
        for item in reversed(self.items):
            if isinstance(item, dict):
                for element in item:
                    if element == variable_name:
                        return item[element]
        return None