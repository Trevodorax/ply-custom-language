main_env = {'names': {}, 'functions': {}}

def eval_instruction(t, env = main_env):
    if type(t) == int:
        return t
    if type(t) == str:
        if t == 'empty':
            return None
        else:
            return t
    if type(t) == tuple:
        if t[0] == 'block':
            eval_instruction(t[1])
            eval_instruction(t[2])
        elif t[0] == 'print':
            print_value = eval_expression(t[1])
            print("print >", print_value)
            return print_value
        elif t[0] == 'assign':
            env['names'][t[1]] = eval_expression(t[2])
        elif t[0] == 'incrementone':
            env['names'][t[1]] += 1
        elif t[0] == 'decrementone':
            env['names'][t[1]] -= 1
        elif t[0] == 'increment':
            env['names'][t[1]] += eval_expression(t[2])
        elif t[0] == 'decrement':
            env['names'][t[1]] -= eval_expression(t[2])
        elif t[0] == 'get':
            return env['names'].get(t[1])
        elif t[0] == 'ifelse':
            if t[1]:
                eval_instruction(t[2])
            else:
                if t[3] is None:  # no else
                    return
                eval_instruction(t[3])
        elif t[0] == 'while':
            while eval_expression(t[1]):
                eval_instruction(t[2])
        elif t[0] == 'dowhile':
            eval_instruction(t[1])
            while eval_expression(t[2]):
                eval_instruction(t[1])
        elif t[0] == 'for':
            eval_instruction(t[1])
            while eval_expression(t[2]):
                eval_instruction(t[4])
                eval_instruction(t[3])
        elif t[0] == 'function_declaration':
            function_name = t[1]
            parameters = t[2]
            body = t[3]
            env['functions'][function_name] = (parameters, body)
        elif t[0] == 'function_call':
            function_name = t[1]
            args = t[2]
            if function_name in env['functions']:
                params, body = env['functions'][function_name]
                new_env = {'names': {name: eval_expression(arg, env) for name, arg in zip(params, args)}, 'functions': env['functions']}
                eval_instruction(body, new_env)
    else:
        print("Unknown expression type:", t)
        return None

def eval_expression(t, env = main_env):
    if type(t) == int:
        return t
    if type(t) == str:
        if t == 'empty':
            return None
        else:
            return t
    if type(t) == tuple:
        if t[0] == 'add':
            return eval_expression(t[1]) + eval_expression(t[2])
        elif t[0] == 'substract':
            return eval_expression(t[1]) - eval_expression(t[2])
        elif t[0] == 'multiply':
            return eval_expression(t[1]) * eval_expression(t[2])
        elif t[0] == 'divide':
            if eval_expression(t[2]) != 0:
                return eval_expression(t[1]) / eval_expression(t[2])
            else:
                print("Error: Division by zero")
                return None
        elif t[0] == 'smaller':
            return eval_expression(t[1]) < eval_expression(t[2])
        elif t[0] == 'greater':
            return eval_expression(t[1]) > eval_expression(t[2])
        elif t[0] == 'smallerequal':
            return eval_expression(t[1]) <= eval_expression(t[2])
        elif t[0] == 'greaterequal':
            return eval_expression(t[1]) >= eval_expression(t[2])
        elif t[0] == 'and':
            return eval_expression(t[1]) and eval_expression(t[2])
        elif t[0] == 'or':
            return eval_expression(t[1]) or eval_expression(t[2])
        elif t[0] == 'get':
            return env['names'].get(t[1])
    else:
        print("Unknown expression type:", t)
        return None