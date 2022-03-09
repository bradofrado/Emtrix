from enum import Enum
#import numpy as np

class ObjectType(Enum):
    Matrix = 0
    Int = 0

class Variable():
    def __init__(self, name, type):
        self.name = name
        self.type = type
        self.value = None
        pass
    def addValue(self, value):
        if self.type == ObjectType.Int:
            self.value = value
        elif self.type == ObjectType.Matrix:
            if self.value == None:
                self.value = []
            self.value.append(value)
        pass

class Emtrix():
    def __init__(self):
        pass