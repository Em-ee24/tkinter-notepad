class Stack:

    def __init__(self):
        self.stack = []
        self.pointer = -1

    def pop(self):
        if self.pointer == -1:
            return None
        else:
            value = self.stack.pop(self.pointer)
            self.pointer -= 1
            return value

    def push(self, value):
        self.stack.append(value)
        self.pointer += 1
        return

class CustomNode:

    def __init__(self):
        self.text = ""
        self.cursorPosition = ""