from scanner import Scanner
from parser import Parser

import sys

def readFromFile(fileName):
    input = ''
    with open(fileName) as f:
        lines = f.readlines()
        for line in lines:
            input += line
    return input

fileName = "homework.txt"
if len(sys.argv) > 1:
    fileName = sys.argv[1]
else:
    raise Exception("No input files")

input = readFromFile(fileName)

scanner = Scanner(input)
scanner.scanAll()

parser = Parser(scanner.tokens)

if parser.parse():
    parser.emtrix.printAll()
else:
    print("Failure")
    print(parser.errorToken)