from tokens import Token, Operator, Identifier, Number
from lib import ParseException

def shuntingYardAlgorithm(toks: list[Token]) -> list[Token]:
    """
    Takes in a token list, and outputs an expression list by using the shunting yard algorithm
    The result is of the form called Reverse Polish Notation
    """
    result: list[Token] = []
    opers: list[Operator | Identifier] = []
    toks = toks[::-1]
    while toks:
        token = toks.pop()
        if isinstance(token, Number):
            result.append(token)
        elif isinstance(token, Identifier) and toks and isinstance(toks[-1], Operator) and toks[-1].val == "(":
            opers.append(token)
        elif isinstance(token, Identifier):
            result.append(token)
        elif isinstance(token, Operator) and not token.isBrack() and token.val != ",":
            while opers:
                op2 = opers[-1]
                if isinstance(op2, Operator) and op2.val == "(": break
                if isinstance(op2, Operator) and not (op2.precedence > token.precedence or (op2.precedence == token.precedence and token.isLeft)): break
                result.append(opers.pop())
            opers.append(token)
        elif isinstance(token, Operator) and token.val == ",":
            while opers and not (isinstance(opers[-1], Operator) and opers[-1].val == "("):
                result.append(opers.pop())
        elif isinstance(token, Operator) and token.val == "(":
            opers.append(token)
        elif isinstance(token, Operator) and token.val == ")":
            while opers and not (isinstance(opers[-1], Operator) and opers[-1].val == "("):
                result.append(opers.pop())
            if not opers:
                raise ParseException("Mismatched parenthesis")
            opers.pop()
            if opers and isinstance(opers[-1], Identifier):
                result.append(opers.pop())
    while opers:
        if isinstance(opers[-1], Operator) and opers[-1].isBrack():
            raise ParseException("Mismatched parenthesis")
        result.append(opers.pop())
    return result