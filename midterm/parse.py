#####################################################################
#
# CAS CS 320, Fall 2014
# Midterm
# parse.py
#
# Mahir Gulrajani
#
# Credits: - Given skeleton code
#          - Solutions based off of code snippets in lecture notes
#            (I modified a lot of it though)
#

import re


def number(tokens, top = True):
    if re.compile(r"(-(0|[1-9][0-9]*)|(0|[1-9][0-9]*))").match(tokens[0]):
        return ({"Number": [int(tokens[0])]}, tokens[1:])

def variable(tokens, top = True):
    if re.compile(r"[a-z][A-Za-z0-9]*").match(tokens[0]) and tokens[0] not in ['true', 'false']:
        return ({"Variable": [tokens[0]]}, tokens[1:])

def expression(tmp, top = True):
    seqs = [\
        ('Plus', [leftExpression, '+', expression]), \
        ('Left', [leftExpression]) \
        ]
    
    for (label, seq) in seqs:
        tokens = tmp[0:]
        ss = []
        es = []
        
        for x in seq:

            # need this because of left factoring
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

def leftExpression(tmp, top = True):
    seqs = [\
        ('True', ['true']), \
        ('False', ['false']), \
        ('Number', [number]), \
        ('Variable', [variable]), \
        ('Array', ['@', variable, '[', expression, ']']) \
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
                if label == 'Variable' or label == 'Number':
                    return (es[0] if len(es) > 0 else label, tokens)
                return ({label:es} if len(es) > 0 else label, tokens)

def program(tmp, top = True):
    seqs = [\
        ('Assign', ['assign', variable, ':=', '[', expression, ',', expression, ',', expression, ']', \
                    ';', program]), \
        ('Print', ['print', expression, ';', program]), \
        ('For', ['for', variable, '{', program, '}', program]), \
        ('End', []) \
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
                
                continue


            r = x(tokens, False)
            if not r is None:
                (e, tokens) = r
                es = es + [e]

        if len(ss) + len(es) == len(seq):
            if not top or len(tokens) == 0:
                return ({label:es} if len(es) > 0 else label, tokens)

def tokenize(s):
    tokens = re.split(r"(\s+|assign|:=|\[|\]|,|print|;|for|{|}|true|false|\+|@)", s)
    tokens = [t for t in tokens if not t.isspace() and not t == ""]
    return tokens
                
def tokenizeAndParse(s):
    tokens = tokenize(s)
    p = program(tokens, True)

    # check to see if it evaluated correctly
    if p == None:
        print("Program didn't follow grammar correctly - returning None.")
        return None

    # need nothing left
    if len(p[1]) > 0:
        return None
    else:
        return p[0]

#eof
