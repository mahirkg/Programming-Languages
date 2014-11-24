'''

CS 320 Assignment 2

Mahir Gulrajani

Code based on example code on Lapets' website

Discussed with Laureen Lubin
'''

from math import log, floor
import re

def tokenize(terminals, string):
    regex = "("
    count = 0
    for x in terminals:
        count = count + 1
        if len(x) == 1 and not x.isalpha():
            regex = regex + "\\"
        regex = regex + x
        if (count != len(terminals)):
            regex = regex + "|"
    regex = regex + ")"
    tokens = [t for t in re.split(regex, string)]

    return [t for t in tokens if not t.isspace() and not t == ""]

def number(tokens, extra = 0):
    if re.match(r"^(0||(-?[1-9][0-9]*))$", tokens[0]):
        return (int(tokens[0]), tokens[1:])

def variable(tokens, extra = 0):
    if tokens[0] == 'true' or tokens[0] == 'false':
        return None
    if re.match(r"^([a-z][a-zA-Z0-9]*)$", tokens[0]):
        return (tokens[0], tokens[1:])

def variableWrapped(tokens, extra = 0):
    if tokens[0] == 'true' or tokens[0] == 'false':
        return None
    if re.match(r"^([a-z][a-zA-Z0-9]*)$", tokens[0]):
        return ({'Variable':[tokens[0]]}, tokens[1:])
    
'''
formula = formula XOR formula
        | not ( formula )
        | ( formula )
        | variable
        | true
        | false



leftFormula = not ( formula )
            | ( formula )
            | variable
            | true
            | false
formula = leftFormula XOR formula
        | leftFormula
'''

def formula(tmp):
##    (x, y) = formulaHelper(tmp, True)
##    if y == []:
##        return (x, y)
    return formulaHelper(tmp, True)

def formulaHelper(tmp, top):
    seqs = [\
        ('Xor', [leftFormula, 'xor', formulaHelper]), \
        ('Left', [leftFormula]) \
        ]

    for (label, seq) in seqs:
        tokens = tmp[0:]
        ss = []
        es = []
        for x in seq:
            if len(tokens) == 0:
                break
            if type(x) == type(""):
            
                if tokens[0] == x:
                    tokens = tokens[1:]
                    ss = ss + [x]
                else:
                    break
            else:
                r = x(tokens, False)
                if not r is None:
                    (e, tokens) = r
                    es = es + [e]
        if len(ss) + len(es) == len(seq):
            if not top or len(tokens) == 0:
                if label == 'Left':
                    return (es[0] if len(es) > 0 else label, tokens)
                return ({label:es} if len(es) > 0 else label, tokens)

def leftFormula(tmp, top):
    seqs = [\
        ('True', ['true']), \
        ('False', ['false']), \
        ('Not', ['not', '(', formulaHelper, ')']), \
        ('Variable', [variable]), \
        ('Parens', ['(', formulaHelper, ')']) \
        ]

    for (label, seq) in seqs:
        tokens = tmp[0:]
        ss = []
        es = []
        for x in seq:
            if type(x) == type(""):

                if tokens[0] == x:
                    tokens = tokens[1:]
                    ss = ss + [x]
                else:
                    break
            else:
                r = x(tokens, False)
                if not r is None:
                    (e, tokens) = r
                    es = es + [e]
        if len(ss) + len(es) == len(seq):
            if not top or len(tokens) == 0:
                return ({label:es} if len(es) > 0 else label, tokens)

'''
factor = factor * factor
       | log ( term )
       | ( term )
       | variable
       | number
term = factor + term
     | factor



term = factor + term
     | factor
leftFactor = log ( term )
    | ( term )
    | variable
    | number
factor = leftFactor * factor
    | leftFactor
'''

def term(tmp):
##    (x, y) = termHelper(tmp, True)
##    if y == []:
##        return (x, y)
    return termHelper(tmp, True)

def termHelper(tmp, top):
    seqs = [\
        ('Plus', [factorHelper, '+', termHelper]), \
        ('Factor', [factorHelper]) \
        ]

    for (label, seq) in seqs:
        tokens = tmp[0:]
        ss = []
        es = []
        for x in seq:
            if len(tokens) == 0:
                break
            if type(x) == type(""):

                if tokens[0] == x:
                    tokens = tokens[1:]
                    ss = ss + [x]
                else:
                    break
            else:
                r = x(tokens, False)
                if not r is None:
                    (e, tokens) = r
                    es = es + [e]
        if len(ss) + len(es) == len(seq):
            if not top or len(tokens) == 0:
                if label == 'Factor':
                    return (es[0] if len(es) > 0 else label, tokens)
                return ({label:es} if len(es) > 0 else label, tokens)



def factorHelper(tmp, top):
    seqs = [\
        ('Mult', [leftFactor, '*', factorHelper]), \
        ('Left', [leftFactor]) \
        ]

    for (label, seq) in seqs:
        tokens = tmp[0:]
        ss = []
        es = []
        for x in seq:
            if len(tokens) == 0:
                break
            if type(x) == type(""):
            
                if tokens[0] == x:
                    tokens = tokens[1:]
                    ss = ss + [x]
                else:
                    break
            else:
                r = x(tokens, False)
                if not r is None:
                    (e, tokens) = r
                    es = es + [e]
        if len(ss) + len(es) == len(seq):
            if not top or len(tokens) == 0:
                if label == 'Left':
                    return (es[0] if len(es) > 0 else label, tokens)
                return ({label:es} if len(es) > 0 else label, tokens)

def leftFactor(tmp, top):
    seqs = [\
        ('Log', ['log', '(', termHelper, ')']), \
        ('Number', [number]), \
        ('Variable', [variable]), \
        ('Parens', ['(', termHelper, ')']) \
        ]

    for (label, seq) in seqs:
        tokens = tmp[0:]
        ss = []
        es = []
        for x in seq:
            if type(x) == type(""):
                if tokens[0] == x:
                    tokens = tokens[1:]
                    ss = ss + [x]
                else:
                    break
            else:
                r = x(tokens, False)
                if not r is None:
                    (e, tokens) = r
                    es = es + [e]
        if len(ss) + len(es) == len(seq):
            if not top or len(tokens) == 0:
                return ({label:es} if len(es) > 0 else label, tokens)

'''
program = print expression ; program
    | assign variable := expression ; program
    | if expression { program } program
    | while expression { program } program
    |
expression = formula
    | term
'''

def program(tmp):
    #(x, y) = programHelper(tmp, True)
    #if y == []:
    #    return (x, y)
    return programHelper(tmp, False)

def programHelper(tmp, top):
    seqs = [\
        ('Print', ['print', expression, ';', programHelper]), \
        ('Assign', ['assign', variableWrapped, ':=', expression, ';', programHelper]), \
        ('If', ['if', expression, '{', programHelper, '}', programHelper]), \
        ('While', ['while', expression, '{', programHelper, '}', programHelper]), \
        ('End', []) \
        ]

    for (label, seq) in seqs:
        tokens = tmp[0:]
        ss = []
        es = []
        #print("For label = " + str(label) + " ss = " + str(ss) + " and es = " + str(es))
        for x in seq:
            if type(x) == type(""):
                if len(tokens) == 0:
                    break
                if tokens[0] == x:
                    tokens = tokens[1:]
                    ss = ss + [x]
                else:
                    break
            else:
                r = x(tokens, False)
                if not r is None:
                    (e, tokens) = r
                    es = es + [e]
                #print("r = " + str(r))
                #if len(tokens) == 0:
                #    return ({label:es} if len(es) > 0 else label, tokens)
        if len(ss) + len(es) == len(seq):
            if not top or len(tokens) == 0:
                #print("return value is = " + str(({label:es} if len(es) > 0 else label, tokens)))
                return ({label:es} if len(es) > 0 else label, tokens)

def expression(tmp, top): # this function is the issue
    
    seqs = [\
        ('Formula', [formulaHelper]), \
        ('Term', [termHelper]) \
        ]    
    for (label, seq) in seqs:
        tokens = tmp[0:]
        ss = []
        es = []
        for x in seq:
            if type(x) == type(""):
                if len(tokens) == 0:
                    break
                if tokens[0] == x:
                    tokens = tokens[1:]
                    ss = ss + [x]
                else:
                    break
            else:
                r = x(tokens, False)
                
                if not r is None:
                    (e, tokens) = r
                    es = es + [e]
        if len(ss) + len(es) == len(seq):
            if not top or len(tokens) == 0:
                return (es[0] if len(es) > 0 else label, tokens)
