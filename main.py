from tokens import tokenize
from sya import shuntingYardAlgorithm
from parse import parse, variables
from lib import ParseException, clear, help, formatNum

def interpret(arg: str) -> str:
    """
    Function that responds to an expression given.
    """
    try:
        tokens = tokenize(arg)
        expr = shuntingYardAlgorithm(tokens)
        result = parse(expr)
        return result
    except ParseException as e:
        return str(e)

print("Welcome, you may start calculating, or type 'help' for help")

while True:
    userInput = input("> ").lower()
    if userInput == "exit":
        break
    elif userInput == "clear":
        clear()
    elif userInput == "help":
        print(help)
    elif userInput == "vars":
        if not variables:
            print("No user vars")
        else:
            print("User variables:")
            for key in variables:
                print(f"{key}: {formatNum(variables[key])}")
    else:
        print(interpret(userInput))

print("Goodbye")