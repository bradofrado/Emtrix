from tokens import TokenType, Token
from emtrix import Computation, ObjectType, Value, Number, Variable, Emtrix

class Parser():
    def __init__(self, tokens):
        if (len(tokens) == 0):
            raise Exception("No tokens were given")
        self.tokens = tokens
        self.curr = tokens[0]
        self.errorToken = None
 
        self.emtrix = Emtrix()
        return None

    def parse(self):
        try:
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
        if self.curr.token == TokenType.COMMENT:
            return self.moveNext()

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
        while index < len(tokens) - 1 and self.switch(toCheck, tokens[index].token):
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

    #Grammars
    def Emtrix(self):
        if self.curr.token == TokenType.ID:
            self.Declaration()
            self.DeclarationList()
            self.ExpressionList()
            self.match(TokenType.EOF)
        else:
            self.throwException()
        return None
    def Declaration(self):
        idToken = self.match(TokenType.ID)
        self.match(TokenType.EQUALS)
        value = self.COMPUTATION(self.tokens)
        self.match(TokenType.SEMICOLON)
        #self.emtrix.addVariable(value)
        return None
    def DeclarationList(self):
        if self.curr.token == TokenType.ID:
            self.Declaration()
            self.DeclarationList()
        else:
            #lambda
            pass
        return None
    def Expression(self):
        if (self.curr.token == TokenType.DET):
            self.FUNC()
            self.match(TokenType.OPEN_PAREN)
            self.SEQUENCE()
            self.match(TokenType.CLOSE_PAREN)
            self.match(TokenType.SEMICOLON)
        else:
            self.throwException()
        return None
    def ExpressionList(self):
        if (self.curr.token == TokenType.DET):
            self.Expression()
            self.DeclarationList()
            self.ExpressionList()
        else:
            #lambda
            pass
    def FUNC(self):
        if (self.curr.token == TokenType.DET):
            self.match(TokenType.DET)
        else:
            self.throwException()
        return None
    def COMPUTATION(self, tokens):
        index = self.parseOperations(tokens, [TokenType.PLUS, TokenType.MINUS])
        if index == -1:
            self.A(tokens[0:])
        elif tokens[index].token == TokenType.MINUS:
            self.COMPUTATION(tokens[0:index])
            self.match(TokenType.MINUS)
            self.A(tokens[index+1:])
        elif tokens[index].token == TokenType.PLUS:
            self.COMPUTATION(tokens[0:index])
            self.match(TokenType.PLUS)
            self.A(tokens[index+1:])
        # elif index == -1#tokens[0].token == TokenType.ID or tokens[0].token == TokenType.NUM or tokens[0].token == TokenType.OPEN_BRACKET:
        #     self.A(tokens[0:index+1])
        else:
            self.throwException()
        # if self.curr.token == TokenType.OPEN_BRACKET:
        #     self.match(TokenType.OPEN_BRACKET)
        #     row = self.ROW()
        #     rows = self.ROWLIST()
        #     self.match(TokenType.CLOSE_BRACKET)

        #     variable = Variable(idToken.value, ObjectType.Matrix)
        #     variable.addValue(row)
        #     for _row in rows:
        #         variable.addValue(_row)

        #     return variable
        # elif self.curr.token == TokenType.ID or self.curr.token == TokenType.NUM:
        #     var = self.SEQUENCE()
        #     self.OPERATION()

        #     variable = Variable(idToken.value, ObjectType.Int)
        #     variable.addValue(var)

        #     return variable
        # else:
        #     self.throwException()
    def A(self, tokens):
        index = self.parseOperations(tokens, [TokenType.STAR, TokenType.DIVIDE])
        if index == -1:
            self.B(tokens)
        elif tokens[index].token == TokenType.STAR:
            self.A(tokens[0:index])
            self.match(TokenType.STAR)
            self.B(tokens[index+1:])
        elif tokens[index].token == TokenType.DIVIDE:
            self.A(tokens[0:index])
            self.match(TokenType.DIVIDE)
            self.B(tokens[index+1:])
        # elif tokens[0].token == TokenType.ID or tokens[0].token == TokenType.NUM or tokens[0].token == TokenType.OPEN_BRACKET:
        #     self.B()
        else:
            self.throwException()
        pass
    def B(self, tokens):
        if tokens[0].token == TokenType.ID or tokens[0].token == TokenType.NUM:
            self.SEQUENCE()
        elif tokens[0].token == TokenType.OPEN_BRACKET:
            self.MATRIX()
        elif tokens[0].token == TokenType.OPEN_PAREN:
            self.match(TokenType.OPEN_PAREN)
            self.COMPUTATION(tokens[1:])
            self.match(TokenType.CLOSE_PAREN)
        else:
            self.throwException()
        pass
    def MATRIX(self):
        if self.curr.token == TokenType.OPEN_BRACKET:
            self.match(TokenType.OPEN_BRACKET)
            row = self.ROW()
            rows = self.ROWLIST()
            self.match(TokenType.CLOSE_BRACKET)

            rows.insert(0, row)

            return rows
            # variable = Variable(idToken.value, ObjectType.Matrix)
            # variable.addValue(row)
            # for _row in rows:
            #     variable.addValue(_row)

            # return variable
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

            return vals
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

            return self.emtrix.getVariable(idToken.value)
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
# Emtrix -> Declaration DeclarationList ExpressionList
# Declaration -> id = COMPUTATION ;
# DeclarationList -> Declaration DeclarationList | lambda
# ExpressionList -> Expression DeclarationList ExpressionList  | lambda
# Expression -> FUNC openParen ID closeParen ;
# FUNC -> det
# ROW -> SEQUENCE SEQUENCELIST .
# ROWLIST -> ROW ROWLIST | lambda
# COMPUTATION -> E
# E -> E - A | E + A | A
# A -> A * B | A / B | B
# B -> SEQUENCE | MATRIX | (E)
# OPERATION -> * SEQUENCE | - SEQUENCE | + SEQUENCE | / SEQUENCE | lambda 
# SEQUENCE -> id | num
# MATRIX -> openBracket ROW ROWLIST closeBracket
# SEQUENCELIST -> SEQUENCE SEQUENCELIST | SEQUENCE '|' SEQUENCELIST | lambda

# A = (4 + 3) * 8 / 3 + [1 2 3.];

# E + A
# 