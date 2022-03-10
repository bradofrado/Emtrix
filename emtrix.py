from enum import Enum
#import numpy as np

class ObjectType(Enum):
    Matrix = 0
    Int = 1

class Value():
    def __init__(self):
        self.value = None
        pass
    def __str__(self) -> str:
        return str(self.value)
    def __repr__(self) -> str:
        return self.__str__()
    def getValue(self):
        pass

class Number(Value):
    def __init__(self, value):
        super().__init__()
        self.value = value
    # def __str__(self) -> str:
    #     return super().__str__()
    def getValue(self):
        return 0
class Computation(Value):
    def __init__(self):
        super().__init__()
    
class Variable(Value):
    def __init__(self, name, type):
        super().__init__()
        self.name = name
        self.type = type
        pass
    def addValue(self, value):
        if self.type == ObjectType.Int:
            self.value = value
        elif self.type == ObjectType.Matrix:
            if self.value == None:
                self.value = []
            self.value.append(value)
        pass
    def __str__(self) -> str:
        return self.name + " = " + super().__str__()
class Emtrix():
    def __init__(self):
        self.variables = []
        pass
    def __str__(self) -> str:
        _str = ''
        for x in self.variables:
            _str += str(x)
            _str += '\n'
        return _str
    def addVariable(self, value):
        var = self.__find__(value.name)

        if (var == None):
            self.variables.append(value)
        else:
            index = self.variables.index(var)
            self.variables[index] = value
    def getVariable(self, name):
        var = self.__find__(name)
        if (var == None):
            raise Exception("Cannot find the variable with name " + name)
        return var
    def containsVariable(self, name):
        var = self.__find__(name)
        return var != None

    def __find__(self, name):
        predicate = lambda x: x.name == name
        for var in self.variables:
            if (predicate(var)):
                return var
        return None
    