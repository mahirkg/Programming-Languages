#####################################################################
#
# CAS CS 320, Fall 2014
# Midterm (skeleton code)
# analyze.py
#
# Mahir Gulrajani
#
# Assuming that the environment doesn't contain real values, just types
# For example, typeExpression({'lol':'Number'}, {'Plus': [{'Number': [5]}, {'Variable': ['lol']}]})
# would return 'Number', because you're adding a number to a variable that contains a number.
# 
exec(open("parse.py").read())

Node = dict
Leaf = str

# typeExpression({}, {'Plus': [{'Number': [5]}, {'Number': [6]}]})
# should return 'Number'
# typeExpression({'x':'Array'}, {'Array': [{'Variable': ['x']}, {'Number': [0]}]})
# should return 'Number'
# typeExpression({'lol':'Number'}, {'Plus': [{'Number': [5]}, {'Variable': ['lol']}]})
# should return 'Number'
def typeExpression(env, e):
    if type(e) == Leaf:
        if e == 'True' or e == 'False':
            return 'Boolean'
    elif type(e) == Node:
        for label in e:
            children = e[label]
            if label == 'Number':
                return 'Number'
            elif label == 'Variable': # ?
                x = children[0]
                if x in env and env[x] == 'Number':
                    return 'Number'
            elif label == 'Array': # ?
                [x, e] = children
                x = x['Variable'][0]
                if x in env and env[x] == 'Array' and typeExpression(env, e) == 'Number':
                    return 'Number'
            elif label == 'Plus':
                if typeExpression(env, children[0]) == 'Number':
                    if typeExpression(env, children[1]) == 'Number':
                        return 'Number'

# typeProgram({}, tokenizeAndParse("print 5; assign x := [2, 2, 2]; for i { print @ x [i]; }"))
# should return 'Void'
def typeProgram(env, s):
    if type(s) == Leaf:
        if s == 'End':
            return 'Void'
    elif type(s) == Node:
        for label in s:
            if label == 'Print':
                [e, p] = s[label]
                if typeExpression(env, e) == 'Number' or\
                   typeExpression(env, e) == 'Boolean':
                    if typeProgram(env, p) == 'Void':
                        return 'Void'
            elif label == 'Assign':
                [x, e0, e1, e2, p] = s[label]
                x = x['Variable'][0]
                if typeExpression(env, e0) == 'Number' and\
                   typeExpression(env, e1) == 'Number' and\
                   typeExpression(env, e2) == 'Number':
                     env[x] = 'Array'
                     if typeProgram(env, p) == 'Void':
                           return 'Void'

            elif label == 'For':
                [x, p1, p2] = s[label]
                x = x['Variable'][0]
                env[x] = 'Number'
                if typeProgram(env, p1) == 'Void':
                    if typeProgram(env, p2) == 'Void':
                        return 'Void'
#eof
