"""
    created by mchahin at 11/2/2018
"""


class Stack:

    def __init__(self):
        self.stack = []

    def push(self, other):
        self.stack.append(other)

    def pop(self):
        return self.stack.pop()

    def peek(self):
        return self.stack[-1]

    def second_last(self):
        return self.stack[-2]

    def list_from_stack(self):
        return self.stack

    def __len__(self):
        return len(self.stack)
