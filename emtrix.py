from enum import Enum
import re
import numpy as np
from LUsolver import LU_solver, row_echelon

from tokens import TokenType

def isNumPyArray(value):
    return type(value).__module__ == np.__name__ 
def isMatrix(value):
        return isinstance(value, Value) and isNumPyArray(value.getValue())

class ObjectType(Enum):
    Matrix = 0
    Int = 1

class Callable:
    def __init__(self, function):
        self.function = function
    def __call__(self, *args, **kwargs):
        return self.function(*args, **kwargs)

class MatrixCallable(Callable):
    def __call__(self, *args, **kwds):
        if isMatrix(args[0]) == False:
            raise Exception("Cannot perform the operation on this data type")
        return super().__call__(*args, **kwds)

class OperatorType(Enum):
    PLUS = Callable(lambda x, y: x + y)
    MINUS = Callable(lambda x, y: x - y)
    MULTIPLY = Callable(lambda x, y: x * y)
    DIVIDE = Callable(lambda x, y: x / y)
    DET = MatrixCallable(lambda x: np.linalg.det(x.getValue()))
    EIG = MatrixCallable(lambda x: np.linalg.eig(x.getValue()))
    INV = MatrixCallable(lambda x: np.linalg.inv(x.getValue()))
    POWER = MatrixCallable(lambda x,y: x**y)
    SOLVE = MatrixCallable(lambda x,y: LU_solver(x.getValue(), y.getValue()))
    ROW = MatrixCallable(lambda x: row_echelon(x.getValue()))
    T = MatrixCallable(lambda x: np.transpose(x.getValue()))

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
    def __mul__(self, other):
        if isinstance(other, Value):
            return self.getValue() * other.getValue()
        return self.getValue() * other
    __rmul__ = __mul__
    def __truediv__(self, other):
        if isinstance(other, Value):
            return self.getValue() / other.getValue()
        return self.getValue() / other
    def __add__(self, other):
        if isinstance(other, Value):
            return self.getValue() + other.getValue()
        return self.getValue() + other
    __radd__ = __add__

    def __sub__(self, other):
        if isinstance(other, Value):
            return self.getValue() - other.getValue()
        return self.getValue() - other
    def __pow__(self, other):
        if isinstance(other, Value):
            return self.getValue()**other.getValue()
        return self.getValue()**other

class Number(Value):
    def __init__(self, value):
        super().__init__()
        self.value = float(value)
    def getValue(self):
        return self.value
class Matrix(Value):
    def __init__(self, rows):
        super().__init__()
        self.value = np.array(rows, dtype=float)
    def getValue(self):
        return self.value
    def __mul__ (self, other):
        if isMatrix(other):
            return np.matmul(self.value, other.getValue())
        return super().__mul__(other)
    __rmul__ = __mul__
    def __add__(self, other):
        if isMatrix(other):
            return np.add(self.value, other.getValue())
        return super().__add__(other)
    def __sub__(self, other):
        if isMatrix(other):
            return np.subtract(self.value, other.getValue())
        return super().__sub__(other)
    __rsub__ = __sub__
    def __truediv__(self, other):
        #A/B can be seen as A*B^-1
        if isMatrix(other):
            return np.matmul(self.value, np.linalg.inv(other.getValue()))
        return super().__truediv__(other)
    def __rtruediv__(self, other):
        #A/B can be seen as A*B^-1
        if isMatrix(other):
            return np.matmul(self.value, np.linalg.inv(other.getValue()))
        return super().__truediv__(other)
    def __pow__(self,other):
        #We can't do matrix to another power
        if isMatrix(other):
            raise Exception("Cannot raise a matrix to the power of another matrix... yet.")  
        #If they are raising a matrix to -1 (or a multiple), then take the inverse          
        value = other
        if isinstance(other, Value):
            value = other.getValue()
        if value < 0:
            value = np.abs(value)
            return np.linalg.inv(self**value)

        return super().__pow__(other)

class Function(Value):
    def __init__(self, value : Value, value2 : Value, type : OperatorType):
        super().__init__()
        self.value = value
        self.value2 = value2
        self.type = type
    def getValue(self):
        if self.value2:
            return self.type.value(self.value, self.value2)
        return self.type.value(self.value)

class Computation(Value):
    def __init__(self, leftValue : Value, rightValue : Value, type : OperatorType):
        super().__init__()
        self.leftValue = leftValue
        self.rightValue = rightValue
        self.type = type
    def getValue(self):
        return self.type.value(self.leftValue, self.rightValue)
        
    
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
    def __mul__(self, other):
        return 0

class Print():
    def __init__(self, _str : str, vals):
        self.string = _str
        self.vals = vals
    def print(self):
        params = re.findall(TokenType.PARAMALL.value, self.string)

        for i in range(len(params)):
            val = self.vals[i]
            self.string = self.string.replace(params[i], str(val.getValue()))
        print(self.string)

        #print(str(self.value.getValue()))


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
    