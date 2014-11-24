'''

CS 320 Assignment 2

Mahir Gulrajani

Code based on example code on Lapets' website

Note: Discussed with Laureen Lubin

'''


def evalTerm(env, e):
    if type(e) == dict:
        for label in e:
            children = e[label]
            if label == 'Number':
                f = children[0]
                v = evalTerm(env, f)
                return int(v)
            elif label == 'Parens':
                f = children[0]
                v = evalTerm(env, f)
                return v
            elif label == 'Log':
                f = children[0]
                v = floor(evalTerm(env, f))
                return log(v, 2)
            elif label == 'Variable':
                x = children[0]
                if x in env:
                    return env[x]
                else:
                    print(x + " is unbound.")
                    exit()
            elif label == 'Plus':
                f1 = children[0]
                v1 = evalTerm(env, f1)
                f2 = children[1]
                v2 = evalTerm(env, f2)
                return int(v1 + v2)
            elif label == 'Mult':
                f2 = children[1]
                v2 = evalTerm(env, f2)
                f1 = children[0]
                v1 = evalTerm(env, f1)
                return int(v1 * v2)
    elif type(e) == str:
        return e
    elif type(e) == int:
        return int(e)

def evalFormula(env, e):
    if type(e) == dict:
        for label in e:
            children = e[label]
            if label == 'Not':
                f = children[0]
                v = evalFormula(env, f)
                return not v
            elif label == 'Parens':
                f = children[0]
                v = evalFormula(env, f)
                return v
            elif label == 'Xor':
                f2 = children[1]
                v2 = evalFormula(env, f2)
                f1 = children[0]
                v1 = evalFormula(env, f1)
                return bool(v1) != bool(v2)
            elif label == 'Variable':
                x = children[0]
                if x in env:
                    return env[x]
                else:
                    print(x + " is unbound.")
                    exit()
    elif type(e) == str:
        if e == 'True':
            return True
        if e == 'False':
            return False

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
                v = evalFormula(env, f)
                if v == None:
                    v = evalTerm(env, f)
                (env, o) = execProgram(env, p)
                return (env, [v] + o)
            elif label == 'Assign':
                children = s[label]
                x = children[0]['Variable'][0]
                f = children[1]
                p = children[2]
                v = evalFormula(env, f)
                if v == None:
                    v = evalTerm(env, f)
                env[x] = v
                (env, o) = execProgram(env, p)
                return (env, o)
            elif label == 'If':
                children = s[label]
                expression = children[0]
                p1 = children[1]
                p2 = children[2]
                env1 = env
                if evalFormula(env, expression) == True:
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
                while evalFormula(env, expression) == True:
                    (env2, o1) = execProgram(env, p1)
                (env3, o2) = execProgram(env, p2)
                return (env3, o2)

def interpret(s):
    terminals = ['print', ';', 'assign', ':=', 'if', '(', ')', 'while',
                 'log', '*', '+', 'not', 'xor', 'true', 'false', '\s']
    tokens = tokenize(terminals, s)
    #print("tokens = " + str(tokens))
    (tree, extra) = program(tokens)
    #print(str(tree))
    #print(str(extra))
    if len(extra) != 0:
        return None
    (env, output) = execProgram({}, tree)
    return output

                
                    
