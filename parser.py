from tokens import TokenType
from emtrix import ObjectType, Variable, Emtrix

class Parser():
    def __init__(self, tokens):
        if (len(tokens) == 0):
            raise Exception("No tokens were given")
        self.tokens = tokens
        self.curr = tokens[0]
        self.errorToken = None
 
        return None

    def parse(self):
        try:
            self.Emtrix()
            return True
        except Exception as token:
            self.errorToken = token
            return False

    def moveNext(self):
        if self.curr.token != TokenType.EOF:
                self.tokens = self.tokens[1:]
                self.curr = self.tokens[0]
        if self.curr.token == TokenType.COMMENT:
            self.moveNext()

    def match(self, token):
        if self.curr.token == token:
            self.moveNext()
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
        self.match(TokenType.ID)
        self.match(TokenType.EQUALS)
        self.VALUE()
        self.match(TokenType.SEMICOLON)
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
    def VALUE(self):
        if self.curr.token == TokenType.OPEN_BRACKET:
            self.match(TokenType.OPEN_BRACKET)
            self.ROW()
            self.ROWLIST()
            self.match(TokenType.CLOSE_BRACKET)
        elif self.curr.token == TokenType.ID or self.curr.token == TokenType.NUM:
            self.SEQUENCE()
            self.OPERATION()
        else:
            self.throwException()
        return None
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
            self.SEQUENCE()
            self.SEQUENCELIST()
            self.match(TokenType.PERIOD)
        else:
            self.throwException()
        return None
    def ROWLIST(self):
        if self.curr.token == TokenType.ID or self.curr.token == TokenType.NUM:
            self.ROW()
            self.ROWLIST()
        else:
            #lambda
            pass
        return None
    def SEQUENCE(self):
        if self.curr.token == TokenType.ID:
            self.match(TokenType.ID)
        elif self.curr.token == TokenType.NUM:
            self.match(TokenType.NUM)
        else:
            self.throwException()
        return None
    def SEQUENCELIST(self):
        if self.curr.token == TokenType.ID or self.curr.token == TokenType.NUM:
            self.SEQUENCE()
            if self.curr.token == TokenType.PIPE:
                self.match(TokenType.PIPE)
            self.SEQUENCELIST()
        else:
            #lambda
            pass
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