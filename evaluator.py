from genereTreeGraphviz2 import printTreeGraph

names = {}

def eval(t):
    if type(t) == int:
        return t
    if type(t) == str:
        if t == 'empty':
            return None
        else:
            return t
    if type(t) == tuple:
        if t[0] == 'block':
            eval(t[1])
            eval(t[2])
        elif t[0] == 'add':
            return eval(t[1]) + eval(t[2])
        elif t[0] == 'substract':
            return eval(t[1]) - eval(t[2])
        elif t[0] == 'multiply':
            return eval(t[1]) * eval(t[2])
        elif t[0] == 'divide':
            if eval(t[2]) != 0:
                return eval(t[1]) / eval(t[2])
            else:
                print("Error: Division by zero")
                return None
        elif t[0] == 'print':
            print_value = eval(t[1])
            print("print >", print_value)
            return print_value
        elif t[0] == 'smaller':
            return eval(t[1]) < eval(t[2])
        elif t[0] == 'greater':
            return eval(t[1]) > eval(t[2])
        elif t[0] == 'smallerequal':
            return eval(t[1]) <= eval(t[2])
        elif t[0] == 'greaterequal':
            return eval(t[1]) >= eval(t[2])
        elif t[0] == 'and':
            return eval(t[1]) and eval(t[2])
        elif t[0] == 'or':
            return eval(t[1]) or eval(t[2])
        elif t[0] == 'assign':
            names[t[1]] = eval(t[2])
        elif t[0] == 'incrementone':
            names[t[1]] += 1
        elif t[0] == 'decrementone':
            names[t[1]] -= 1
        elif t[0] == 'increment':
            names[t[1]] += eval(t[2])
        elif t[0] == 'decrement':
            names[t[1]] -= eval(t[2])
        elif t[0] == 'get':
            return names.get(t[1])
        elif t[0] == 'ifelse':
            if t[1]:
                eval(t[2])
            else:
                if t[3] is None:  # no else
                    return
                eval(t[3])
        elif t[0] == 'while':
            while eval(t[1]):
                eval(t[2])
        elif t[0] == 'dowhile':
            eval(t[1])
            while eval(t[2]):
                eval(t[1])
        elif t[0] == 'for':
            eval(t[1])
            while eval(t[2]):
                eval(t[4])
                eval(t[3])
    else:
        print("Unknown expression type:", t)
        return None
