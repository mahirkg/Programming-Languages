#####################################################################
#
# CAS CS 320, Fall 2014
# Midterm
# compile.py
#
# Mahir Gulrajani
# Credit: Prof. Lapets' notes
#

from random import randint
exec(open('parse.py').read())
exec(open('interpret.py').read())
exec(open('optimize.py').read()) 
exec(open('machine.py').read())
exec(open('analyze.py').read())


Leaf = str
Node = dict

def freshStr():
    return str(randint(0,10000000))

# takes (environment, tree, heap)
# returns (instructions, address, heap)
def compileExpression(env, e, heap):
    if type(e) == Leaf:
        if e == 'True':
            heap = heap + 1
            return (['set ' + str(heap) + ' 1'], heap, heap)
        elif e == 'False':
            heap = heap + 1
            return (['set ' + str(heap) + ' 0'], heap, heap)
    elif type(e) == Node:
        for label in e:
            children = e[label]
            if label == 'Variable':
                if children[0] in env:
                    return ([], env[children[0]], heap)
                else:
                    print("Unbound!")
                    exit()
            elif label == 'Number':
                n = children[0]
                heap = heap + 1
                return (['set ' + str(heap) + ' ' + str(n)], heap, heap)
            elif label == 'Plus':
                (instsOne, addrOne, heap) = compileExpression(env, children[0], heap)
                (instsTwo, addrTwo, heap) = compileExpression(env, children[1], heap)
                heap = heap + 1
                instructions = instsOne + instsTwo + copy(addrOne, 1) + copy(addrTwo, 2) + \
                               ['add'] + copy(0, heap)
                return (instructions, heap, heap)
            elif label == 'Array':
                x = children[0]
                e = children[1]
                (instsOne, addrOne, heap) = compileExpression(env, e, heap)
                (instsTwo, addrTwo, heap) = compileExpression(env, x, heap)
                instsThree = copy(addrOne, 1) + ['set 2 ' + str(addrTwo), 'add']
                heap = heap + 1
                instsFour = copyFromRef(0, heap)
                return (instsOne + instsTwo + instsThree + instsFour, heap, heap)

# takes (environment, tree, heap)
# returns (environment, instructions, heap)
# simulate(compile("assign x := [10, 20, 30]; for i { print @ x [ i ]; }"))
# should return [10, 20, 30]
# simulate(compile("assign x := [10, 20, 30]; assign y := [10, 20, 30]; for i { print @ x [ i ] + @ y [ i ] ; }"))
# should return [20, 40, 60]
def compileProgram(env, p, heap = 8):
    if type(p) == Leaf:
        if p == 'End':
            return (env, [], heap)
    elif type(p) == Node:
        for label in p:
            children = p[label]
            if label == 'Print':
                [e, prog] = children
                (instsE, addr, heap) = compileExpression(env, e, heap)
                (env, instsP, heap) = compileProgram(env, prog, heap)
                return (env, instsE + copy(addr, 5) + instsP, heap)
            elif label == 'Assign':
                [x, e0, e1, e2, prog] = children
                (instsOne, addrOne, heap) = compileExpression(env, e0, heap)
                (instsTwo, addrTwo, heap) = compileExpression(env, e1, heap)
                (instsThree, addrThree, heap) = compileExpression(env, e2, heap)
                start = heap + 1
                heap = heap + 1
                instsFour = copy(addrOne, heap)
                heap = heap + 1
                instsFour = instsFour + copy(addrTwo, heap)
                heap = heap + 1
                instsFour = instsFour + copy(addrThree, heap)
                env[x['Variable'][0]] = start
                (env, instsFive, heap) = compileProgram(env, prog, heap)
                return (env, instsOne + instsTwo + instsThree + instsFour + instsFive, heap)

def compile(s):
    p = tokenizeAndParse(s)
    if typeProgram({}, p) != 'Void':
        print("Failed type check - returning None!!")
        return None

    p = unrollLoops(foldConstants(p))
    
    (env, insts, heap) = compileProgram({}, p)
    return insts

# compileAndSimulate("print 5; assign x := [2, 2, 2]; for i { print @ x [i]; }")
# should return [5, 2, 2, 2]
def compileAndSimulate(s):
    return simulate(compile(s))

#eof
