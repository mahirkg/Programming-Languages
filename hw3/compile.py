#####################################################################
#
# CAS CS 320, Fall 2014
# Assignment 3
# compile.py
#
# Mahir Gulrajani
#

exec(open("machine.py").read())
exec(open("interpret.py").read())
exec(open("parse.py").read())



'''
Implement a function compileTerm(env, t, heap) that takes three arguments:
env is a mapping from variables to memory addresses, t is a term parse tree,
and heap is the memory address of the current top of the heap. The function
should return a tuple (insts, addr, heap) in which insts is a sequence of
machine language instructions (represented as a Python list of strings) that
perform the computation represented by the parse tree, addr is the address of
the result, and heap is an integer representing the memory of the top of the
heap after the computation is performed.

term ::= number | variable | term + term
'''

def compileTerm(env, t, heap):
    if type(t) == dict:
        for label in t:
            children = t[label]
            if label == 'Number':
                # grow the heap
                heap = heap + 1
                # store the number in the heap and move on
                return (['set ' + str(heap) + ' ' + str(children[0])], heap, heap)
            elif label == 'Variable':
                # do not grow heap because nothing is stored in it in this step
                # return the instruction, address of result and heap
                if children[0] in env:
                    return ([], env[children[0]], heap)
                else:
                    print("Unbound.")
                    exit()
            elif label == 'Plus':
                # the operands are o1 and o2
                o1 = children[0]
                o2 = children[1]
                # evaluate the operands one by one to get the instructions necessary
                (i1, a1, h1) = compileTerm(env, o1, heap)
                (i2, a2, h2) = compileTerm(env, o2, h1)
                instructions = i1 + i2
                heap = h2
                # grow the heap to store the sum
                heap = heap + 1
                # instructions necessary to add up the evaluated operands and store
                # it at the top of the heap
                instructions = instructions + \
                               copy(a1, 1) + \
                               copy(a2, 2) + \
                               ['add'] + \
                               copy(0, heap)
                # return all the instructions, the result location and the heap
                return (instructions, heap, heap)
    else:
        # error handling
        return None

'''
Implement a function compileFormula(env, f, heap). The requirements for this
function are the same as those for compileTerm(env, t, heap), except that it
must handle formula parse trees.

formula ::= true | false | variable | not formula | formula or formula |
            formula and formula
'''

# Based on the compileFormula(f, heap = 3, fresh = 0) example in the notes
def compileFormula(env, f, heap):
    if type(f) == str:
        if f == 'True':
            # grow the heap
            heap = heap + 1
            # Return the instruction, the value and the heap
            return (['set ' + str(heap) + ' 1'], heap, heap)
        if f == 'False':
            # grow the heap
            heap = heap + 1
            # Return the instruction, the value and the heap
            return (['set ' + str(heap) + ' 0'], heap, heap)
    elif type(f) == dict:
        for label in f:
            children = f[label]
            if label == 'Variable':
                # do not grow heap because nothing is stored in it in this step
                # return the instruction, address of result and heap
                if children[0] in env:
                    return ([], env[children[0]], heap)
                else:
                    print("Unbound.")
                    exit()
            elif label == 'Not':
                # compile the subtree to obtain the list of instructions that
                # computes the value represented by f.
                (i, a, heap) = compileFormula(env, children[0], heap)
                # grow the heap to store the result of the not
                heap = heap + 1
                # generate more instructions to change the memory
                # location in accordance with the definition of the
                # Not operation.
                instructions = i + \
                               ['branch NOTsetZero' + str(heap) + ' ' + str(a), \
                                'set ' + str(heap) + ' 1', \
                                'goto NOTfinish' + str(heap), \
                                'label NOTsetZero' + str(heap),\
                                'set ' + str(heap) + ' 0', \
                                'label NOTfinish' + str(heap)]
                # return the instructions and the heap
                return (instructions, heap, heap)
            elif label == 'Or':
                # the operands are o1 and o2
                o1 = children[0]
                o2 = children[1]
                # evaluate the operands one by one to get the instructions necessary
                (i1, a1, h1) = compileFormula(env, o1, heap)
                (i2, a2, h2) = compileFormula(env, o2, h1)
                instructions = i1 + i2
                heap = h2
                # grow the heap to store the result of the Or
                heap = heap + 1
                # add instructions to compute the result of the Or
                instructions = instructions + \
                               copy(a1, 1) + \
                               copy(a2, 2) + \
                               ['add', \
                                'branch ORsetOne' + str(heap) + ' 0', \
                                'goto ORfinish' + str(heap), \
                                'label ORsetOne' + str(heap), \
                                'set 0 1',\
                                'label ORfinish' + str(heap)] + \
                                copy(0, heap)
                # return the instructions, the result and the heap
                return (instructions, heap, heap)
            elif label == 'And':
                # the operands are o1 and o2
                o1 = children[0]
                o2 = children[1]
                # evaluate the operands one by one to get the instructions necessary
                (i1, a1, h1) = compileFormula(env, o1, heap)
                (i2, a2, h2) = compileFormula(env, o2, h1)
                instructions = i1 + i2
                heap = h2
                # grow the heap to store the result of the And
                heap = heap + 1
                # add instructions to compute and store the result of the And
                instructions = instructions + \
                               ['branch ANDcouldBeTrue' + str(heap) + ' ' + str(a1), \
                                'label ANDfalse' + str(heap), \
                                'set ' + str(heap) + ' 0', \
                                'goto ANDdone' + str(heap), \
                                'label ANDcouldBeTrue' + str(heap), \
                                'branch ANDisTrue' + str(heap) + ' ' + str(a2), \
                                'goto ANDfalse' + str(heap), \
                                'label ANDisTrue' + str(heap), \
                                'set ' + str(heap) + ' 1', \
                                'label ANDdone' + str(heap)]
                # return the instructions, the result and the heap
                return (instructions, heap, heap)
    else:
        # error handling
        return None

'''
Implement a function compileProgram(env, s, heap) that takes three arguments:
env is a mapping from variables to memory addresses, s is a program parse tree,
and heap is the memory address of the current top of the heap. The function
should return a tuple (env, insts, heap) in which env is an updated environment,
insts is a sequence of machine language instructions (represented as a Python
list of strings) that perform the computation represented by the parse tree, and
heap is an integer representing the memory of the top of the heap after the
computation is performed.

program ::= print expression ; program
    |	variable := expression ; program
    |	if expression { program } program
    |   while expression { program } program
    |	procedure variable { program } program
    |	call variable ; program
    |	
'''

def compileProgram(env, s, heap):
    if type(s) == str:
        if s == 'End':
            return (env, [], heap)
    elif type(s) == dict:
        for label in s:
            children = s[label]
            if label == 'Print':
                expression = children[0]
                p = children[1]
                # compile the expression
                r = compileFormula(env, expression, heap)
                if r is None:
                    r = compileTerm(env, expression, heap)
                (i1, a1, h1) = r
                # the print instruction
                instructions = i1 + \
                               copy(a1, 5)
                # compile the remainder
                (env, i2, h2) = compileProgram(env, p, h1)
                instructions = instructions + i2
                heap = h2
                # return the instructions to compile expression, print it and
                # then compile the rest, as well as the heap
                return (env, instructions, heap)
            elif label == 'Assign':
                x = children[0]['Variable'][0]
                expression = children[1]
                p = children[2]
                # compile the expression
                r = compileFormula(env, expression, heap)
                if r is None:
                    r = compileTerm(env, expression, heap)
                (i1, a1, h1) = r
                instructions = i1
                # do the actual assign now
                env[x] = a1
                # compile the rest
                (env, i2, h2) = compileProgram(env, p, h1)
                heap = h2
                # return the instructions and the heap
                instructions = instructions + i2
                return (env, instructions, heap)
            elif label == 'If':
                expression = children[0]
                p1 = children[1]
                p2 = children[2]
                # compile the expression
                r = compileFormula(env, expression, heap)
                if r is None:
                    r = compileTerm(env, expression, heap)
                (i1, a1, h1) = r
                # compile the if-true statement
                (env, i2, h2) = compileProgram(env, p1, h1)
                heap = h2
                # add the if-statement instructions
                instructions = i1 +\
                               ['branch ifTrue' + str(heap) + ' ' + str(a1), \
                                'goto done' + str(heap), \
                                'label ifTrue' + str(heap)] + \
                                i2 + \
                                ['label done' + str(heap)]
                # compile the rest
                (env, i3, h3) = compileProgram(env, p2, heap)
                heap = h3
                instructions = instructions + i3
                # return the instructions and the heap
                return (env, instructions, heap)
            elif label == 'While':
                expression = children[0]
                p1 = children[1]
                p2 = children[2]
                # compile the expression
                r = compileFormula(env, expression, heap)
                if r is None:
                    r = compileTerm(env, expression, heap)
                (i1, a1, h1) = r
                # compile the while-true statement
                (env, i2, h2) = compileProgram(env, p1, h1)
                heap = h2
                # add the while-statement instructions
                instructions = i1 + \
                               ['branch whileTrue' + str(heap) + ' ' + str(a1), \
                                'goto done' + str(heap), \
                                'label whileTrue' + str(heap)] + \
                                i2
                # recompile the expression
                r = compileFormula(env, expression, heap)
                if r is None:
                    r = compileTerm(env, expression, heap)
                (i1, a1, h1) = r

                # add more of the while-statement instructions
                instructions = instructions + \
                               ['branch whileTrue' + str(heap) + ' ' + str(a1), \
                                'label done' + str(heap)]
                # compile the rest
                (env, i3, h3) = compileProgram(env, p2, heap)
                heap = h3
                instructions = instructions + i3
                # return the instructions and the heap
                return (env, instructions, heap)
            elif label == 'Procedure':
                name = children[0]['Variable'][0]
                body = children[1]
                rest = children[2]
                # need to get the instructions for the body
                (env, i1, h1) = compileProgram(env, body, heap)
                # get the instructions to set up a procedure with that body
                instructions = procedure(name, i1)
                # compile the rest
                (env, i2, h2) = compileProgram(env, rest, h1)
                heap = h2
                instructions = instructions + i2
                # return the environment, instructions and the heap
                return (env, instructions, heap)
            elif label == 'Call':
                name = children[0]['Variable'][0]
                rest = children[1]
                # get the instructions to call the body
                instructions = call(name)
                # compile the rest
                (env, i1, h1) = compileProgram(env, rest, heap)
                heap = h1
                instructions = instructions + i1
                # return the total instructions and updated heap/environment
                return (env, instructions, heap)
    else:
        # error handling
        return None 


'''
Implement a function compile(s) that takes a single string s that is a
concrete syntax representation of a program in the source programming
language and returns its compiled form: a sequence of instructions in the
target machine language.
'''

def compile(s):
    # get the instructions
    (env, instructions, heap) = compileProgram({}, tokenizeAndParse(s), 7)
    # add an instruction to initialize the stack pointer to 0
    instructions = ['set 7 0'] + instructions
    # return the sequence of instructions in the target machine language
    return instructions
