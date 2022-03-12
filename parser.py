from scanner import Scanner
from tokens import TokenType, Token
import re
from emtrix import Computation, Function, Matrix, ObjectType, OperatorType, Print, Value, Number, Variable, Emtrix

class Parser():
    def __init__(self, tokens, emtrix = None):
        if (len(tokens) == 0):
            raise Exception("No tokens were given")
        self.tokens = tokens
        self.curr = tokens[0]
        self.errorToken = None
 
        if emtrix == None:
            self.emtrix = Emtrix()
        else:
            self.emtrix = emtrix
        return None

    def parse(self):
        try:
            while self.curr.token == TokenType.COMMENT:
                self.moveNext()
            self.Emtrix()
            return True
        except Exception as token:
            self.errorToken = token
            return False

    def moveNext(self):
        val = None
        if self.curr.token != TokenType.EOF:
                val = self.curr
                self.tokens = self.tokens[1:]
                self.curr = self.tokens[0]
        while self.curr.token == TokenType.COMMENT:
            self.moveNext()

        return val

    def match(self, token : TokenType, idIsDefined : bool = False) -> Token:
        if self.curr.token == token:
            #If this is a variable that should be defined already but isn't,
            #throw an excpetion
            if (idIsDefined and token == TokenType.ID and self.emtrix.containsVariable(self.curr.value) == False):
                self.throwException()
            return self.moveNext()
        else:
            self.throwException() 
        return None

    def throwException(self):
        raise Exception(self.curr)
    
    def switch(self, cases, check) -> bool:
        tokenTypes = [TokenType.ID, TokenType.NUM, TokenType.STAR, TokenType.DIVIDE, TokenType.PLUS, TokenType.MINUS]

        try:
            cases.index(check)
            return True
        except:
            return False

    def parseOperations(self, tokens, tokenTypes):
        index = 0
        hitIndex = -1
        parenDepth = 0
        #can loop through these, until it hits something not in this list
        #this is essentially anything that can be in a computation (including matrix tokens)
        toCheck = [TokenType.ID, TokenType.NUM, TokenType.STAR, TokenType.DIVIDE, TokenType.PLUS, TokenType.MINUS, TokenType.OPEN_BRACKET, TokenType.CLOSE_BRACKET, TokenType.PERIOD, TokenType.PIPE, TokenType.OPEN_PAREN, TokenType.CLOSE_PAREN]
        while index < len(tokens) - 1 and (self.switch(toCheck, tokens[index].token) or self.isFunc(tokens[index].token)):
            # Keep track of how many levels of parenthesis we are in
            if tokens[index].token == TokenType.OPEN_PAREN:
                parenDepth = parenDepth + 1
            elif tokens[index].token == TokenType.CLOSE_PAREN:
                parenDepth = parenDepth - 1

            # If we are one of the given token type and not in parens, save that index
            if self.switch(tokenTypes, tokens[index].token) and parenDepth == 0:
                hitIndex = index
            index = index + 1

        return hitIndex

    def isFunc(self, token):
        funcs = [TokenType.DET, TokenType.EIG]
        return self.switch(funcs, token)

    #Grammars
    def Emtrix(self):
        self.DeclarationList()
        self.PrintList()
        self.match(TokenType.EOF)
        return None
    def Declaration(self):
        idToken = self.match(TokenType.ID)
        self.match(TokenType.EQUALS)
        value = self.COMPUTATION(self.tokens)
        self.match(TokenType.SEMICOLON)

        newVar = Variable(idToken.value, value)
        self.emtrix.addVariable(newVar)
        return None
    def DeclarationList(self):
        if self.curr.token == TokenType.ID:
            self.Declaration()
            self.DeclarationList()
        else:
            #lambda
            pass
        return None
    def Expression(self, tokens) -> Value:
        if (self.isFunc(tokens[0].token)):
            self.FUNC()
            self.match(TokenType.OPEN_PAREN)
            val = self.COMPUTATION(tokens[2:])
            self.match(TokenType.CLOSE_PAREN)

            operator = None
            if tokens[0].token == TokenType.EIG:
                operator = OperatorType.Eig
            elif tokens[0].token == TokenType.DET:
                operator = OperatorType.Det

            if operator == None:
                raise Exception("Something went wrong")
            
            return Function(val, operator)
        else:
            self.throwException()
        return None
    def PrintList(self):
        if (self.curr.token == TokenType.STRING):
            self.Print()
            self.DeclarationList()
            self.PrintList()
        else:
            #lambda
            pass
    def Print(self):
        if self.curr.token == TokenType.STRING:
            _str = self.match(TokenType.STRING)
            params = re.findall(TokenType.PARAMALL.value, _str.value)
            vals = []
            for x in params:
                x = re.search(TokenType.PARAM.value, x).group()
                s = Scanner(x, _str.line)
                s.scanAll()

                p = Parser(s.tokens, self.emtrix)

                vals.append(p.COMPUTATION(p.tokens))
                
            self.emtrix.addPrint(Print(_str.value, vals))
    def FUNC(self):
        if self.isFunc(self.curr.token):
            self.match(self.curr.token)
        else:
            self.throwException()
        return None
    def COMPUTATION(self, tokens) -> Value:
        index = self.parseOperations(tokens, [TokenType.PLUS, TokenType.MINUS])
        if index == -1:
            return self.A(tokens[0:])
        elif tokens[index].token == TokenType.MINUS:
            leftValue = self.COMPUTATION(tokens[0:index])
            self.match(TokenType.MINUS)
            rightValue = self.A(tokens[index+1:])

            return Computation(leftValue, rightValue, OperatorType.Minus)
        elif tokens[index].token == TokenType.PLUS:
            leftValue = self.COMPUTATION(tokens[0:index])
            self.match(TokenType.PLUS)
            rightValue = self.A(tokens[index+1:])

            return Computation(leftValue, rightValue, OperatorType.Plus)
        else:
            self.throwException()
    def A(self, tokens) -> Value:
        index = self.parseOperations(tokens, [TokenType.STAR, TokenType.DIVIDE])
        if index == -1:
            return self.B(tokens)
        elif tokens[index].token == TokenType.STAR:
            leftValue = self.A(tokens[0:index])
            self.match(TokenType.STAR)
            rightValue = self.B(tokens[index+1:])

            return Computation(leftValue, rightValue, OperatorType.Multiply)
        elif tokens[index].token == TokenType.DIVIDE:
            leftValue = self.A(tokens[0:index])
            self.match(TokenType.DIVIDE)
            rightValue = self.B(tokens[index+1:])

            return Computation(leftValue, rightValue, OperatorType.Divide)
        else:
            self.throwException()
        pass
    def B(self, tokens) -> Value:
        if tokens[0].token == TokenType.ID or tokens[0].token == TokenType.NUM:
            return self.SEQUENCE()
        elif tokens[0].token == TokenType.OPEN_BRACKET:
            return self.MATRIX()
        elif tokens[0].token == TokenType.OPEN_PAREN:
            self.match(TokenType.OPEN_PAREN)
            value = self.COMPUTATION(tokens[1:])
            self.match(TokenType.CLOSE_PAREN)

            return value
        elif self.isFunc(tokens[0].token):
            return self.Expression(tokens)
        else:
            self.throwException()
        pass
    def MATRIX(self) -> Value:
        if self.curr.token == TokenType.OPEN_BRACKET:
            self.match(TokenType.OPEN_BRACKET)
            row = self.ROW()
            rows = self.ROWLIST()
            self.match(TokenType.CLOSE_BRACKET)

            rows.insert(0, row)

            return Matrix(rows)
        else:
            self.throwException()
    def OPERATION(self):
        if self.curr.token == TokenType.STAR:
            self.match(TokenType.STAR)
            self.SEQUENCE()
        elif self.curr.token == TokenType.PLUS:
            self.match(TokenType.PLUS)
            self.SEQUENCE()
        elif self.curr.token == TokenType.MINUS:
            self.match(TokenType.MINUS)
            self.SEQUENCE()
        elif self.curr.token == TokenType.DIVIDE:
            self.match(TokenType.DIVIDE)
            self.SEQUENCE()
        else:
            #lambda
            pass
        return None
    def ROW(self):
        if self.curr.token == TokenType.ID or self.curr.token == TokenType.NUM:
            val = self.SEQUENCE()
            vals = self.SEQUENCELIST()
            self.match(TokenType.PERIOD)

            vals.insert(0, val)
            _vals = [x.getValue() for x in vals]

            return _vals
        else:
            self.throwException()
        return None
    def ROWLIST(self):
        if self.curr.token == TokenType.ID or self.curr.token == TokenType.NUM:
            row = self.ROW()
            rows = self.ROWLIST()

            rows.insert(0, row)

            return rows
        else:
            #lambda
            return []
        return None
    def SEQUENCE(self) -> Value:
        if self.curr.token == TokenType.ID:
            idToken = self.match(TokenType.ID, True)

            return self.emtrix.getVariable(idToken.value).value
        elif self.curr.token == TokenType.NUM:
            numToken = self.match(TokenType.NUM)

            return Number(numToken.value)
        else:
            self.throwException()
        return None
    def SEQUENCELIST(self):
        if self.curr.token == TokenType.ID or self.curr.token == TokenType.NUM:
            var = self.SEQUENCE()
            if self.curr.token == TokenType.PIPE:
                self.match(TokenType.PIPE)
            vars = self.SEQUENCELIST()
            vars.insert(0, var)

            return vars
        else:
            #lambda
            return []
        return None
#Grammar
# Emtrix -> DeclarationList PrintList
# Declaration -> id = COMPUTATION ;
# DeclarationList -> Declaration DeclarationList | lambda
# PrintList -> Print DeclarationList PrintList  | lambda
# Print -> string
# Expression -> FUNC openParen COMPUTATION closeParen;
# FUNC -> det
# ROW -> SEQUENCE SEQUENCELIST .
# ROWLIST -> ROW ROWLIST | lambda
# COMPUTATION -> E
# E -> E - A | E + A | A
# A -> A * B | A / B | B
# B -> SEQUENCE | MATRIX | (E) | EXPRESSION
# OPERATION -> * SEQUENCE | - SEQUENCE | + SEQUENCE | / SEQUENCE | lambda 
# SEQUENCE -> id | num
# MATRIX -> openBracket ROW ROWLIST closeBracket
# SEQUENCELIST -> SEQUENCE SEQUENCELIST | SEQUENCE '|' SEQUENCELIST | lambda

# A = (4 + 3) * 8 / 3 + [1 2 3.];
# E + A
# A / B + A
# A * B / B + A
# (E) * B / B + A
# (E + A) * B / B + A
# (4 + 3) * B / B + A
# (4 + 3) * 8 / 3 + A


# Computation
# Left Value, operation, right Value
