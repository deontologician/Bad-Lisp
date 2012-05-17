#!/usr/bin/env python2

from pyparsing import nestedExpr
import re
import operator as op

ops = { '+': op.add,
        '-': op.sub,
        '*': op.mul,
        '/': op.div,
        '<': op.lt,
        '>': op.gt,
        '=': op.eq,
        '^': op.pow,
        'and': op.and_,
        'or': op.or_,
        }

def parse(source):
    return nestedExpr().parseString(source, parseAll=True).asList()[0]

def flatten(ls):
    """Flattens a heterogeneous list in the expected way.
    
    >>> flatten([1,2,3])
    [1, 2, 3]
    >>> flatten([1, [2], [3]])
    [1, 2, 3]
    >>> flatten([1, [2, 3]])
    [1, [2, 3]]
    """
    ret = []
    for i in ls:
        if isinstance(i, list):
            flattened = flatten(i)
            if len(flattened) == 1:
                ret.extend(flattened)
            else:
                ret.append(flattened)
        else:
            ret.append(i)
    return ret

def wrap(value):
    'Turns an item into a list if it is not one already'
    return value if isinstance(value, list) and value != [] else [value]

def eval_tail(tail):
    return flatten(evaluate(t) for t in tail)

def evaluate(tree, debug = False):
    tree = wrap(tree)
    wrapped_head = tree[:1]
    tail = tree[1:]
    if wrapped_head == [[]]:
        # empty list case
        return [[]] + eval_tail(tail)
    head = wrapped_head[0]
    if re.match(r'^[0-9,]+$', head):
        # numbers
        ret = [int(head.replace(',', ''))]
        ret.extend(eval_tail(tail))
        return ret
    elif head in ['true', 'false', 't', 'f']:
        # booleans
        boo = True if head in ['true', 't'] else False
        return [boo] + eval_tail(tail)
    elif head in ops:
        # arithmetic and logical operations
        [first_op] = evaluate(tail[0])
        return [reduce(ops[head], eval_tail(tail[1:]), first_op)]
    elif re.match(r"^\'.\'$", head):
        # characters
        char = head.strip("'")
        return [char] + eval_tail(tail)
    elif re.match(r'^\".*\"$', head):
        # strings
        string = list(head.strip('"'))
        return [string] + eval_tail(tail)
    elif head.startswith('`'):
        # quoted variable names
        return [head.lstrip('`')] + eval_tail(tail)
    elif head == 'hd':
        # head function
        return evaluate(tail[0][0])
    elif head == 'tl':
        return eval_tail(tail[0][1:])
    else:
        return 'Undefined variable: {}'.format(head)


def parse_and_eval(program, debug = False):
    try:
        tree = parse(program)
        return evaluate(tree)
    except:
        if debug:
            import traceback
            traceback.print_exc()
        return 'Failed'
        
def hack_string(tree):
    return str(tree).replace('[', '(').replace(']', ')').replace(',', '')

if __name__ == '__main__':
    import sys
    debug = False
    if len(sys.argv) > 1:
        if sys.argv[1] == 'debug':
            debug = True
        else:
            for term in sys.argv[1:]:
                print parse_and_eval(term, debug=debug)
            sys.exit()
    try:
        while True:
            print hack_string(parse_and_eval(raw_input('%: '), debug=debug))
    except (KeyboardInterrupt, EOFError):
        print "Bye!"
