from stack import Stack

stack = Stack()
main = {}
stack.push(main)

def add_block(t):
    while(t[2] != 'empty'):
        stack.push(t[2])
        t = t[1]
    stack.push(t[1])

def run_and_pop_block(depth):
    while stack.size() > depth:
        test = stack.pop()
        eval_instruction(test)

def eval_instruction(t):
    if type(t) == int:
        return t
    if type(t) == str:
        if t == 'empty':
            return None
        else:
            return t
    if type(t) == tuple:
        if t[0] == 'block':
            previousStackSize = stack.size()
            add_block(t)
            if(stack.size() <= 1):
                return None
            
            run_and_pop_block(previousStackSize)
        elif t[0] == 'print':
            print_value = eval_expression(t[1])
            print("print >", print_value)
            return print_value
        elif t[0] == 'assign':
            stack.setVariable(t[1], eval_expression(t[2]))
        elif t[0] == 'multiple_assign':
            for (name, value) in t[1]:
                stack.setVariable(name, eval_expression(value))
        elif t[0] == 'incrementone':
            stack.setVariable(t[1], stack.getVariable(t[1]) + 1)
        elif t[0] == 'decrementone':
            stack.setVariable(t[1], stack.getVariable(t[1]) - 1)
        elif t[0] == 'increment':
            stack.setVariable(t[1], stack.getVariable(t[1]) + eval_expression(t[2]))
        elif t[0] == 'decrement':
            stack.setVariable(t[1], stack.getVariable(t[1]) - eval_expression(t[2]))
        elif t[0] == 'get':
            return stack.getVariable(t[1])
        elif t[0] == 'ifelse':
            if eval_expression(t[1]):
                previousStackSize = stack.size()
                add_block(t[2])
                run_and_pop_block(previousStackSize)
            else:
                if t[3] is None:  # no else
                    return
                previousStackSize = stack.size()
                add_block(t[3])
                run_and_pop_block(previousStackSize)
        elif t[0] == 'while':
            while eval_expression(t[1]):
                previousStackSize = stack.size()
                add_block(t[2])
                run_and_pop_block(previousStackSize)

        elif t[0] == 'dowhile':
            previousStackSize = stack.size()
            add_block(t[1])
            run_and_pop_block(previousStackSize)
            while eval_expression(t[2]):
                previousStackSize = stack.size()
                add_block(t[1])
                run_and_pop_block(previousStackSize)
        elif t[0] == 'for':
            eval_instruction(t[1])
            while eval_expression(t[2]):
                previousStackSize = stack.size()
                add_block(t[4])
                run_and_pop_block(previousStackSize)
                eval_instruction(t[3])
        elif t[0] == 'function_declaration':
            function_name = t[1]
            parameters = t[2]
            body = t[3]
            # TODO: add the function to the stack
        elif t[0] == 'function_call':
            # TODO: replace this with the stack thingy
            function_name = t[1]
            args = t[2]
            if function_name in env['functions']:
                params, body = env['functions'][function_name]
                new_env = {'names': {name: eval_expression(arg) for name, arg in zip(params, args)}, 'functions': env['functions']}
                eval_instruction(body, new_env)
            
    else:
        print("Unknown expression type:", t)
        return None

def eval_expression(t):
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
            return stack.getVariable(t[1])
    else:
        print("Unknown expression type:", t)
        return None