from enum import Enum
class TokenType(Enum):
    #Keywords
    DET = '^det(?!\w)'

    #Identifieers
    ID = '^[a-zA-Z][a-zA-Z0-9]*'
    NUM = '^[0-9]+'

    #Symbols
    EQUALS = '^='
    OPEN_BRACKET = '^\['
    CLOSE_BRACKET = '^\]'
    PERIOD = '^\.'
    PIPE = '^\|'
    SEMICOLON = '^;'
    OPEN_PAREN = '^\('
    CLOSE_PAREN = '^\)'
    STAR = '^\*'
    MINUS = '^-'
    PLUS = '^\+'
    DIVIDE = '^\/(?!\/\*)(?!\/)'

    #Misc
    #COMMENT = '(\/\*([^*]|[\r\n]|(\*+([^*\/]|[\r\n])))*\*+\/)|(\/\/.*)'
    COMMENT = '^\/\/.*'
    #STRINGBEGIN = '^\>[^{\n]*'
    #STRINGEND = '^}[^\n{]*'
    STRING = '^\>.*?(?=\/\/|\n)'
    PARAMALL = '{[^{}]*}'
    PARAM = '[^{}]+'
    WHITESPACE = '^ +'
    NEWLINE = '^\n'
    UNDEFINED = '^[^a-zA-Z0-9\s\[\]\.\(\)\|\=;\*]+'
    EOF = '^\Z'

class Token():
    def __init__(self, token, value, line):
        self.token = token
        self.value = value
        self.line = line
    def __str__(self):
        return "(" + self.token.name + "," + self.value + "," + str(self.line) + ")"