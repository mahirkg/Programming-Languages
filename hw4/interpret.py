#####################################################################
#
# CAS CS 320, Fall 2014
# Assignment 4
# interpret.py
#
# Mahir Gulrajani
# Collaborated with Ann Ming Samborski, Sana Nagar and Anbita Siregar
# Credits: Professor Lapets
#

exec(open("parse.py").read())

def subst(s, a):
    if type(a) == Node:
        for label in a:
            children = a[label]
            if label == 'Variable':
                if s != None:
                    if children[0] in s:
                        return s[children[0]]
                    else:
                        return a
            else:
                return {label: [subst(s, b) for b in children]}
    elif type(a) == Leaf:
        return a

def unify(a, b):
    if type(a) == Leaf and a == b:
        return {}
    elif type(a) == Node and type(b) == Node:
        for labelA in a:
            for labelB in b:
                childrenA = a[labelA]
                childrenB = b[labelB]
                if 'Variable' == labelA:
                    return {childrenA[0]: b}
                if 'Variable' == labelB:
                    return {childrenB[0]: a}
                if labelA == labelB and len(childrenA) == len(childrenB):
                    combinedSubstitution = []
                    for (c, d) in zip(childrenA, childrenB):
                        if unify(c, d) != None:
                            for x in unify(c, d):
                                combinedSubstitution += [(x, unify(c, d)[x])]
                    return dict(combinedSubstitution)

def build(m, d):
    if type(d) == Node:
        for label in d:
            children = d[label]
            if label == 'Function':
                f = children[0]['Variable'][0]
                p = children[1]
                e = children[2]
                if f in m:
                    m[f] = m[f] + [(p, e)]
                else:
                    m[f] = [(p, e)]
                return build(m, children[3])
    elif type(d) == Leaf:
        if d == 'End':
            return m

# evaluate({}, {}, {'Number':[{'Plus':[{'Number':[25]}, {'Number':[30]}]}]})
# should return 55
def evaluate(m, env, e):
    if type(e) == Node:
        for label in e:
            children = e[label]
            if label == 'ConInd':
                v1 = evaluate(m, env, children[1])
                v2 = evaluate(m, env, children[2])
                return {'ConInd': [children[0], v1, v2]}
            elif label == 'ConBase':
                return {'ConBase': children}
            elif label == 'Number':
                return evaluate(m, env, children[0])
            elif label == 'Variable':
                if children[0] in env:
                    return env[children[0]]
                else:
                    # Usually 'Apply' w/ unknown hits this case
                    continue
            elif label == 'Plus':
                n1 = evaluate(m, env, children[0])
                n2 = evaluate(m, env, children[1])
                return n1 + n2
            elif label == 'Apply':
                f = children[0]['Variable'][0]
                v1 = evaluate(m, env, children[1])
                for (p, e2) in m[f]:
                    print("p:",p)
                    print("e2:",e2)
                    print("unify(p, v1):", unify(p, v1))
                    print("subst(unify(p, v1), p):",subst(unify(p, v1), p))
                    print("subst(unify(p, v1), v1):",subst(unify(p, v1), v1))
                    if subst(unify(p, v1), p) == subst(unify(p, v1), v1):
                        return evaluate(m, unify(p, v1), e2)
    elif type(e) == Leaf:
        return e
    elif type(e) == int:
        return e

def interact(s):
    # Build the module definition.
    m = build({}, parser(grammar, 'declaration')(s))

    # Interactive loop.
    while True:
        # Prompt the user for a query.
        s = input('> ') 
        if s == ':quit':
            break
        
        # Parse and evaluate the query.
        e = parser(grammar, 'expression')(s)
        if not e is None:
            print(evaluate(m, {}, e))
        else:
            print("Unknown input.")

#eof
