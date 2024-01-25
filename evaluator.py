from stack import Stack

stack = Stack()
main = {}
stack.push(main)

RAX = None
variablesToReassign = []


def add_block(t):
    while (t[2] != 'empty'):
        stack.push(t[2])
        t = t[1]
    stack.push(t[1])


def run_and_pop_block(depth):
    while stack.size() > depth:
        instruction = stack.pop()
        eval_instruction(instruction)


def eval_instruction(t):
    global RAX, variablesToReassign

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
            if (stack.size() <= 1):
                return None

            run_and_pop_block(previousStackSize)
        elif t[0] == 'print':
            print_value = ""
            for element in t[1]:
                print_value += str(eval_expression(element))
            print("print >", print_value)
            return print_value
        elif t[0] == 'assign':
            stack.setVariable(t[1], eval_expression(t[2]))
        elif t[0] == 'array_decl':
            array_name = t[1]
            tab = []
            for element in t[2]:  # Iterate over each element in the array
                tab.append(eval_expression(element))
            stack.setVariable(array_name, tab)  # Initializes an array with default values (e.g., 0)
        elif t[0] == 'array_assign':
            array_name = t[1]
            index = eval_expression(t[2])
            value = eval_expression(t[3])
            array = stack.getVariable(array_name)
            if array is None:
                print("Array not declared")
                return
            array[index] = value
            stack.setVariable(array_name, array)
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
            createdFn = (parameters, body)
            stack.setVariable(function_name, createdFn)
        elif t[0] == 'function_call':
            function_name = t[1]
            args = t[2]

            # create a dict with the variables in params and their values passed in args
            params, body = stack.getVariable(function_name)
            new_args = []
            for i in range(len(args)):
                if args[i][1][0] == '#':
                    variablesToReassign += [(params[i], args[i][1])]
                    new_args += [eval_expression(('get', args[i][1][1:]))]
                else:
                    new_args += [eval_expression(args[i])]
            new_env = dict(zip(params, new_args))

            stack.push(new_env)

            # execute body
            previousStackSize = stack.size()
            add_block(body)
            run_and_pop_block(previousStackSize)

            # reassign referenced arguments
            if variablesToReassign:
                for variableToReassign in variablesToReassign:
                    stack.items[0][variableToReassign[1][1:]] = stack.getVariable(variableToReassign[0])

            # remove variables of this function from the stack
            stack.pop()

            if (RAX != None):
                return_value = RAX
            else:
                return_value = None

            RAX = None
            variablesToReassign = []

            return return_value

        elif t[0] == 'return':
            RAX = eval_expression(t[1])
            last_env = stack.lastEnv()
            print("last_env", last_env)
            stack.flush()

    else:
        print("Unknown expression type:", t)
        return None


def eval_expression(t):
    global RAX, variablesToReassign

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
        elif t[0] == 'isequal':
            return eval_expression(t[1]) == eval_expression(t[2])
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
        elif t[0] == 'array_access':
            array_name = t[1]
            index = eval_expression(t[2])
            array = stack.getVariable(array_name)
            if array is None:
                print("Array not declared")
                return None
            if 0 > index > len(array):
                print("Index out of bounds error")
                return None

            return array[index]

        elif t[0] == 'function_call':
            function_name = t[1]
            args = t[2]

            # create a dict with the variables in params and their values passed in args
            params, body = stack.getVariable(function_name)
            new_args = []
            for i in range(len(args)):
                if args[i][1][0] == '#':
                    variablesToReassign += [(params[i], args[i][1])]
                    new_args += [eval_expression(('get', args[i][1][1:]))]
                else:
                    new_args += [eval_expression(args[i])]
            new_env = dict(zip(params, new_args))

            stack.push(new_env)

            # execute body
            previousStackSize = stack.size()
            add_block(body)
            run_and_pop_block(previousStackSize)

            # reassign referenced arguments
            if variablesToReassign:
                for variableToReassign in variablesToReassign:
                    stack.items[0][variableToReassign[1][1:]] = stack.getVariable(variableToReassign[0])

            # remove variables of this function from the stack
            stack.pop()

            if (RAX != None):
                return_value = RAX
            else:
                return_value = None

            RAX = None
            variablesToReassign = []

            return return_value
    else:
        print("Unknown expression type:", t)
        return None
