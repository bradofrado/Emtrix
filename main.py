from scanner import Scanner
from parser import Parser

def readFromFile(fileName):
    input = ''
    with open(fileName) as f:
        lines = f.readlines()
        for line in lines:
            input += line
    return input


input = readFromFile('test.txt')

scanner = Scanner(input)
scanner.scanAll()

parser = Parser(scanner.tokens)

if parser.parse():
    print("Success!")
    print(parser.emtrix)
else:
    print("Failure")
    print(parser.errorToken)