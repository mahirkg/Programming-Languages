#
# CAS CS 320, Fall 2014
# Title: Assignment 3
# File: interpret.py
# Author: Mahir Gulrajani
# Credits: Professor Lapets' code examples and skeletons
#

exec(open("parse.py").read())

Node = dict
Leaf = str

# evalTerm({'v':{'Plus': [3, 4]}}, {'Plus': [{'Variable': ['v']}, 2]}) should return 9
# evalTerm({}, {'Plus': [3, 4]}) should return 7
def evalTerm(env, t):
    if type(t) == Node:
        for label in t:
            children = t[label]
            if label == 'Number':
                f = children[0]
                v = evalTerm(env, f)
                return int(v)
            elif label == 'Variable':
                x = children[0]
                if x in env:
                    return evalTerm(env, env[x])
                else:
                    exit()
            elif label == 'Plus':
                f1 = children[0]
                v1 = evalTerm(env, f1)
                f2 = children[1]
                v2 = evalTerm(env, f2)
                return int(v1) + int(v2)
    else:
        return t

# evalFormula({'v':{'Not': ['False']}}, {'Not': [{'Variable': ['v']}]}) should return True
# evalFormula({'v':{'And': ['True', 'True']}}, {'Not': [{'Variable': ['v']}]}) should return False
# evalFormula({'v':{'Or': ['True', 'False']}}, {'Not': [{'Variable': ['v']}]}) should return False
# evalFormula({'v':{'Or': ['False', 'False']}}, {'Not': [{'Variable': ['v']}]}) should return True
def evalFormula(env, f):
    if type(f) == Node:
        for label in f:
            children = f[label]
            if label == 'Not':
                f = children[0]
                v = evalFormula(env, f)
                return not v
            elif label == 'Variable':
                x = children[0]
                if x in env:
                    return evalFormula(env, env[x])
                else:
                    print(x + " is unbound.")
                    exit()
            elif label == 'And':
                f1 = children[0]
                f2 = children[1]
                v1 = evalFormula(env, f1)
                if v1 == False:
                    return v1
                else:
                    return evalFormula(env, f2)
            elif label == 'Or':
                f1 = children[0]
                f2 = children[1]
                v1 = evalFormula(env, f1)
                if v1 == True:
                    return v1
                else:
                    return evalFormula(env, f2)
    elif type(f) == Leaf:
        if f == 'True':
            return True
        if f == 'False':
            return False

# evalExpression({'v':{'Not': ['False']}}, {'Not': [{'Variable': ['v']}]}) should return True
# evalExpression({}, {'Plus': [3, 4]}) should return 7
# evalExpression({'v':{'Plus': [3, 4]}}, {'Plus': [{'Variable': ['v']}, 2]}) should return 9
# evalExpression({'v':{'Or': ['True', 'True']}}, {'Not': [{'Variable': ['v']}]}) should return False
def evalExpression(env, e):
    f = evalFormula(env, e)
    if f == None:
        f = evalTerm(env, e)
    return f

def execProgram(env, s):
    if type(s) == str:
        if s == 'End':
            return (env, [])
    elif type(s) == dict:
        for label in s:
            if label == 'Print':
                children = s[label]
                f = children[0]
                p = children[1]
                v = evalExpression(env, f)
                (env, o) = execProgram(env, p)
                return (env, [v] + o)
            elif label == 'Assign':
                children = s[label]
                x = children[0]['Variable'][0]
                f = children[1]
                p = children[2]
                env[x] = f
                (env, o) = execProgram(env, p)
                return (env, o)
            elif label == 'If':
                children = s[label]
                expression = children[0]
                p1 = children[1]
                p2 = children[2]
                env1 = env
                if evalExpression(env, expression) == True:
                    (env2, o1) = execProgram(env, p1)
                    (env3, o2) = execProgram(env2, p2)
                    return (env3, o1 + o2)
                else:
                    return execProgram(env1, p2)
            elif label == 'While':
                children = s[label]
                expression = children[0]
                p1 = children[1]
                p2 = children[2]
                while evalExpression(env, expression) == True:
                    (env2, o1) = execProgram(env, p1)
                (env3, o2) = execProgram(env, p2)
                return (env3, o2)
            elif label == 'Call':
                children = s[label]
                x = children[0]['Variable'][0]
                p2 = children[1]
                if x in env:
                   (env2, o1) = execProgram(env, env[x])
                   (env3, o2) = execProgram(env2, p2)
                   return (env3, o1 + o2)
                else:
                    print(x + " is unbound.")
                    exit()
            elif label == 'Procedure':
                children = s[label]
                x = children[0]['Variable'][0]
                p1 = children[1]
                env[x] = p1
                p2 = children[2]
                (env, o) = execProgram(env, p2)
                return (env, o)
                

# interpret("print 3 + 4 + 5 + 6; x := 5 + 6; print x;") should return [18, 11]
def interpret(s):
    (env, o) = execProgram({}, tokenizeAndParse(s))
    return o

#eof
