from tokens import TokenType, Token
from emtrix import ObjectType, Value, Number, Variable, Emtrix

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
        value = self.VALUE(idToken)
        self.match(TokenType.SEMICOLON)
        self.emtrix.addVariable(value)
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
    def VALUE(self, idToken):
        if self.curr.token == TokenType.OPEN_BRACKET:
            self.match(TokenType.OPEN_BRACKET)
            row = self.ROW()
            rows = self.ROWLIST()
            self.match(TokenType.CLOSE_BRACKET)

            variable = Variable(idToken.value, ObjectType.Matrix)
            variable.addValue(row)
            for _row in rows:
                variable.addValue(_row)

            return variable
        elif self.curr.token == TokenType.ID or self.curr.token == TokenType.NUM:
            var = self.SEQUENCE()
            self.OPERATION()

            variable = Variable(idToken.value, ObjectType.Int)
            variable.addValue(var)

            return variable
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
# Declaration -> id = VALUE ;
# DeclarationList -> Declaration DeclarationList | lambda
# ExpressionList -> Expression DeclarationList ExpressionList  | lambda
# Expression -> FUNC openParen ID closeParen ;
# FUNC -> det
# VALUE -> openBracket ROW ROWLIST closeBracket | SEQUENCE OPERATION
# ROW -> SEQUENCE SEQUENCELIST .
# ROWLIST -> ROW ROWLIST | lambda
# OPERATION -> * SEQUENCE | - SEQUENCE | + SEQUENCE | / SEQUENCE | lambda 
# SEQUENCE -> id | num
# SEQUENCELIST -> SEQUENCE SEQUENCELIST | SEQUENCE '|' SEQUENCELIST | lambda