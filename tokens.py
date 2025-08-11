from lib import ProjectError, isNum, isAlphaNum, isCharComparison

from typing import Self

precedenceDict: dict[str, int] = {'=': 1, ':=': 1, '|': 2, "^^": 3, '&': 4, "==": 5, "!=": 5, '<': 6, '>': 6, "<=": 6, ">=": 6, '+': 7, "b-": 7, "*": 8, "/": 8, "%": 8, "u-": 9, "^": 10, "!": 11, "~": 11, "(": -1, ")": -1, ",": -1}

"""
* ! ~
* ^
* u- # unary negation
* \\* / %
* \\+ b- # b- binary subtraction
* < <= >= >
* == !=
* &
* ^^ # bitwise XOR
* \\|
* = := # both assignment
"""

class Token:
    """
    A base token value, like a number or operator
    """
    def canJoin(self, arg: str) -> bool:
        raise ProjectError("Cannot call canJoin on Abstract Token class")
    def join(self, arg: str) -> Self: # type: ignore why the hell can't the class see itself????
        raise ProjectError("Cannot call join method on Abstract Token class")
    def __repr__(self) -> str:
        return self.__str__()

class Number(Token):
    val: float
    mult: float
    def __init__(self, arg: float):
        self.val = arg
        self.mult = 1
    def canJoin(self, arg: str):
        return isNum(arg) or arg == '.' and self.val % 1 == 0
    def join(self, arg: str):
        sign = -1 if self.val < 0 else 1
        self.val *= sign
        if arg == ".":
            self.mult = 0.1
            return self            
        if self.mult == 1:
            self.val = self.val * 10 + float(arg)
        else:
            self.val += self.mult * float(arg)
            self.mult *= 0.1
        self.val *= sign
        return self
    def __str__(self) -> str:
        return f"[Number: {self.val}]"

class Identifier(Token):
    val: str
    def __init__(self, arg: str):
        self.val = arg
    def canJoin(self, arg: str):
        return isAlphaNum(arg)
    def join(self, arg: str):
        self.val += arg
        return self
    def __str__(self) -> str:
        return f"[Name: {self.val}]"

class Operator(Token):
    precedence: int
    val: str
    isUnary: bool
    isLeft: bool
    def __init__(self, char: str, isNeg: bool):
        if char == '-': char = "u-" if isNeg else "b-"
        self.val = char
        self.precedence = precedenceDict[char]
        self.isLeft = char != ')' and char != '^'
        self.isUnary = char == 'u-' or char == '!'
    def isBrack(self):
        return self.val == '(' or self.val == ')'
    def canJoin(self, arg: str) -> bool:
        if arg == "=":
            return len(self.val) == 1 and isCharComparison(self.val)
        if arg == "^":
            return self.val == "^"
        if isNum(arg):
            return self.val == "u-"
        return False
    def join(self, arg: str):
        if self.val == "u-" and isNum(arg):
            return Number(-float(arg))
        self.val += arg
        self.precedence = precedenceDict[self.val]
        return self
    def __str__(self) -> str:
        return f"[Operator: \"{self.val}\", Precedence: {self.precedence}, Unary?: {self.isUnary}, Left?: {self.isLeft}]"

def parseAsToken(arg: str, isNegation: bool) -> Token:
    """
    if isNum(arg) -> float(arg)
    if isAlphaNum(arg) -> str(arg)
    oper(arg)
    """
    if isNum(arg): return Number(float(arg))
    if isAlphaNum(arg): return Identifier(arg)
    return Operator(arg, isNegation)

def tokenize(arg: str) -> list[Token]:
    """
    Takes in user input, and converts that to a list of tokens
    If tokenizing fails, throws ParseException
    """
    expr: list[Token] = []
    i = 0
    while i < len(arg):
        if arg[i] == ' ': ...
        elif len(expr) == 0:
            expr.append(parseAsToken(arg[i], True))
        elif expr[-1].canJoin(arg[i]):
            expr[-1] = expr[-1].join(arg[i])
        else:
            expr.append(parseAsToken(arg[i], isinstance(expr[-1], Operator) and expr[-1].val != ')'))
        i += 1
    return expr