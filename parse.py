from tokens import Token, Number, Identifier, Operator
from lib import ParseException, formatNum
from typing import Callable
import math

def pow(a, b):
    try:
        return a ** b
    except:
        raise ParseException("Value out of Range")

constants = {"pi": 3.141592653589793, "e": 2.718281828459045, "tau": 6.283185307179586}
variables: dict[str, float] = {}
functions: dict[str, tuple[Callable, int]] = {
    "sin": (math.sin, 1),
    "cos": (math.cos, 1),
    "tan": (math.tan, 1),
    "csc": (lambda x: 1 / math.sin(x), 1),
    "sec": (lambda x: 1 / math.cos(x), 1),
    "cot": (lambda x: 1 / math.tan(x), 1),
    "arcsin": (math.asin, 1),
    "arccos": (math.acos, 1),
    "arctan": (math.atan, 1),
    "arccsc": (lambda x: 1 / math.asin(x), 1),
    "arcsec": (lambda x: 1 / math.acos(x), 1),
    "arccot": (lambda x: 1 / math.atan(x), 1),
    "exp": (math.exp, 1),
    "ln": (math.log, 1),
    "log": (math.log, 2),
    "max": (max, 2),
    "min": (min, 2),
    "sqrt": (math.sqrt, 1),
    "cbrt": (math.cbrt, 1),
    "nthrt": (lambda a, b: pow(a, 1 / b), 2),
}

def access(arg: float | str) -> float:
    if isinstance(arg, str):
        if arg in constants:
            return constants[arg]
        if arg in variables:
            return variables[arg]
        raise ParseException("Variable doesn't exist", arg)
    return arg

def parse(expr: list[Token]) -> str:
    """
    Reads in an expresson in Reverse Polish Notation, uses data to access or store variables,
    and returns its result as a string
    """
    stack: list[float | str] = []
    def getStack() -> float | str:
        if not stack:
            raise ParseException("Cannot parse expression")
        return stack.pop()
    expr = expr[::-1]
    while expr:
        token = expr.pop()
        if isinstance(token, Number):
            stack.append(token.val)
        elif isinstance(token, Identifier) and token.val in functions:
            func, argCount = functions[token.val]
            args = []
            for i in range(argCount):
                args.append(access(getStack()))
            args.reverse()
            stack.append(func(*args))
        elif isinstance(token, Identifier):
            stack.append(token.val)
        elif isinstance(token, Operator):
            match token.val:
                case "+":
                    second = access(getStack())
                    first = access(getStack())
                    stack.append(first + second)
                case "b-":
                    second = access(getStack())
                    first = access(getStack())
                    stack.append(first - second)
                case "*":
                    second = access(getStack())
                    first = access(getStack())
                    stack.append(first * second)
                case "/":
                    second = access(getStack())
                    first = access(getStack())
                    try:
                        stack.append(first / second)
                    except ZeroDivisionError:
                        raise ParseException("Cannot divide by 0")
                case "%":
                    second = access(getStack())
                    first = access(getStack())
                    stack.append(first % second)
                case "^":
                    second = access(getStack())
                    first = access(getStack())
                    stack.append(pow(first, second))
                case "!":
                    first = access(getStack())
                    stack.append(1 if first == 0 else 0)
                case "~":
                    first = access(getStack())
                    stack.append(~int(first))
                case "&":
                    second = access(getStack())
                    first = access(getStack())
                    stack.append(int(first) & int(second))
                case "|":
                    second = access(getStack())
                    first = access(getStack())
                    stack.append(int(first) | int(second))
                case "u-":
                    first = access(getStack())
                    stack.append(-first)
                case "^^":
                    second = access(getStack())
                    first = access(getStack())
                    stack.append(int(first) ^ int(second))
                case "==":
                    second = access(getStack())
                    first = access(getStack())
                    stack.append(float(second == first))
                case "!=":
                    second = access(getStack())
                    first = access(getStack())
                    stack.append(float(second != first))
                case "<":
                    second = access(getStack())
                    first = access(getStack())
                    stack.append(float(first < second))
                case ">":
                    second = access(getStack())
                    first = access(getStack())
                    stack.append(float(first > second))
                case "<=":
                    second = access(getStack())
                    first = access(getStack())
                    stack.append(float(first <= second))
                case ">=":
                    second = access(getStack())
                    first = access(getStack())
                    stack.append(float(first >= second))
                case "=" | ":=":
                    second = access(getStack())
                    first = getStack()
                    if not isinstance(first, str):
                        raise ParseException("Cannot assign to value", str(first))
                    if first in constants:
                        raise ParseException("Cannot reassign a constant", first)
                    variables[first] = second
    if len(stack) > 1:
        raise ParseException("Unexpected argument format")
    if not stack: return "Done"
    return formatNum(access(stack.pop()))