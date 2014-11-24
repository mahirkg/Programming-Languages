#####################################################################
#
# CAS CS 320, Fall 2014
# Midterm
# interpret.py
#
# Mahir Gulrajani
#
# Credit:
#        - Based off code from lecture and previous homeworks
#

exec(open("parse.py").read())

Node = dict
Leaf = str

def evaluate(env, e):
    if type(e) == Leaf:
        if e == 'True':
            return True
        elif e == 'False':
            return False
    elif type(e) == Node:
        for label in e:
            children = e[label]
            if label == 'Variable': #?
                x = children[0]
                if x in env:
                    return env[x]
                else:
                    print(x + " is unbound.")
                    exit()
            elif label == 'Plus':
                one = int(evaluate(env, children[0]))
                two = int(evaluate(env, children[1]))
                return one + two
            elif label == 'Array': #?
                x = children[0]['Variable'][0]
                k = int(evaluate(env, children[1]))
                if x in env:
                    return env[x][k]
                else:
                    print(x + " is unbound.")
                    exit()
            elif label == 'Number':
                x = children[0]
                return int(x)

def execute(env, s):
    if type(s) == Leaf:
        if s == 'End':
            return (env, [])
    elif type(s) == Node:
        for label in s:
            children = s[label]
            if label == 'Assign':
                x = children[0]['Variable'][0]
                n0 = evaluate(env, children[1])
                n1 = evaluate(env, children[2])
                n2 = evaluate(env, children[3])
                env[x] = [n0, n1, n2]
                return execute(env, children[4])
            elif label == 'Print':
                v = evaluate(env, children[0])
                (env, o) = execute(env, children[1])
                return (env, [v] + o)
            elif label == 'For':
                x = children[0]['Variable'][0]
                p1 = children[1]
                p2 = children[2]
                env[x] = 0
                (env2, o1) = execute(env, p1)
                env2[x] = 1
                (env3, o2) = execute(env2, p1)
                env3[x] = 2
                (env4, o3) = execute(env3, p1)
                (env5, o4) = execute(env4, p2)
                return (env5, o1 + o2 + o3 + o4)
                

# interpret("assign x := [20, 30, 40]; print @ x [ 1 + 1];")
# should return [40]
# interpret("assign x := [20, 30, 40]; print @ x [ 1 + 1]; for x { print x; }")
# should return [40, 0, 1, 2]
# interpret("assign x := [20, 30, 40]; print @ x [ 1 + 1]; for x { print x + 10; }")
# should return [40, 10, 11, 12]
# interpret("assign a := [1+1,2+8,3];for a {print a;}")
# should return [0, 1, 2]
# interpret("assign a := [1+1,2+8,3];for i {print @a[i];}")
# should return [2, 10, 3]
def interpret(s): # interpret a string
    (env, o) = execute({}, tokenizeAndParse(s))
    return o

#eof
