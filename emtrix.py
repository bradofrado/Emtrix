from enum import Enum
#import numpy as np

class ObjectType(Enum):
    Matrix = 0
    Int = 1

class OperatorType(Enum):
    Plus = 0
    Minus = 1
    Multiply = 2
    Divide = 3
    Det = 4

operations = {
    OperatorType.Plus: lambda x,y: x.getValue() + y.getValue(),
    OperatorType.Minus: lambda x,y: x.getValue() - y.getValue(),
    OperatorType.Multiply: lambda x,y: x.getValue() * y.getValue(),
    OperatorType.Divide: lambda x,y: x.getValue() / y.getValue(),
    OperatorType.Det: lambda x: x.getValue()
}

class Value():
    def __init__(self):
        self.value = None
        pass
    def __str__(self) -> str:
        return str(self.value)
    def __repr__(self) -> str:
        return self.__str__()
    def getValue(self):
        return self.value
        pass

class Number(Value):
    def __init__(self, value):
        super().__init__()
        self.value = value
    def getValue(self):
        return int(self.value)
class Matrix(Value):
    def __init__(self, rows):
        super().__init__()
        self.value = rows
    def getValue(self):
        return 0

class Function(Value):
    def __init__(self, value : Value, type : OperatorType):
        super().__init__()
        self.value = value
        self.type = type
    def getValue(self):
        return operations[self.type](self.value)

class Computation(Value):
    def __init__(self, leftValue : Value, rightValue : Value, operator : OperatorType):
        self.leftValue = leftValue
        self.rightValue = rightValue
        self.operator = operator
        super().__init__()
    def getValue(self):
        return operations[self.operator](self.leftValue, self.rightValue)
    
class Variable(Value):
    def __init__(self, name, value):
        super().__init__()
        self.name = name
        self.value = value
        pass
    def getValue(self):
        return self.value.getValue()
    def __str__(self) -> str:
        return self.name + " = " + super().__str__()

class Print():
    def __init__(self, value : Value):
        self.value = value
    def print(self):
        print(str(self.value.getValue()))


class Emtrix():
    def __init__(self):
        self.variables = []
        self.prints = []
        pass
    def __str__(self) -> str:
        _str = ''
        for i in range(len(self.variables)):
            _str += str(self.variables[i])

            if (i < len(self.variables) -1):
                _str += '\n'
        return _str
    def addPrint(self, _print):
        self.prints.append(_print)

    def printAll(self):
        for x in self.prints:
            x.print()
    def printVariables(self):
        print(self.__str__())
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
    