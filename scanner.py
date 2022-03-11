from tokens import TokenType
from tokens import Token
import re 

class Scanner:
    def __init__(self, input, line = 1):
        self.curr = None
        self.input = input
        self.tokens = []
        self.line = line
    
    def scanNext(self):
        while (self.scan(TokenType.WHITESPACE) or self.scan(TokenType.NEWLINE)):
            pass

        for tokenType in TokenType:
            if tokenType.value[0] != '^':
                continue
            token = self.scan(tokenType)

            if (token != None):
                self.tokens.append(token)
                self.curr = token
                return None

        raise Exception("Cannot scan current token")

    def scan(self, token):
        match = re.search(token.value, self.input)
        if (match):
            self.input = self.input[match.span()[1]:]
            _token = Token(token, match.group(), self.line)
            #print("Matched " + str(_token))
            if token == TokenType.NEWLINE:
                self.line = self.line + 1
            return _token
        return None
    
    def scanAll(self):
        while(self.curr == None or self.curr.token != TokenType.EOF):
            self.scanNext()
        return None

    def print(self):
        for x in self.tokens:
            print(x)
        return None