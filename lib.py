import os

digits = set("0123456789")

help = """
help: shows this list
clear: clears the screen
vars: prints all variables user has defined
exit: exits the program

Arithmetic operations, bitwise manipulation, and function calls are all supported

Constants: e, pi, tau

Functions:
    All trig functions take 1 argument, has all trig functions aside from hyperbolic ones
    exp: 1 arg, does e ^ x
    ln: 1 arg, does ln(x)
    log: 2 args 'a' and 'b', does log(b) / log(a) or log_a(b)
    max: 2 args
    min: 2 args
    sqrt: 1 arg, does the square root of the value
    cbrt: 1 arg, does the cube root of the value
    nthrt: 2 args 'a' and 'b', does a ^ (1 / b)
""".strip()

def isNum(arg: str):
    return arg in digits

def isAlphaNum(arg: str):
    return arg.isalpha() or arg in digits

def isCharComparison(arg: str):
    return arg == '<' or arg == '>' or arg == '=' or arg == ':' or arg == '!'

def clear():
    if os.name == "nt":
        os.system("cls")
    else:
        os.system("clear")

def formatNum(arg: float) -> str:
    if arg % 1 == 0:
        return str(int(arg))
    return str(arg)

class ParseException(Exception):
    """
    Result of tokenize failing
    """
    def __init__(self, msg: str, *other: str):
        self.msg = msg
        self.other = other
    def __str__(self) -> str:
        return f"{self.msg}\n{'\n'.join(self.other)}"

class ProjectError(Exception):
    """
    If the project fails in some way
    """
    def __str__(self) -> str:
        return "A parsing error occured" # TODO: make message more verbose3