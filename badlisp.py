from pyparsing import nestedExpr
import re

def parse(source):
    return nestedExpr().parseString(source, parseAll=True).asList()[0]

def evaluate(tree):
    head = tree[0]
    tail = tree[1:]
    if re.match(r'[0-9]+', head):
        ret = [int(head)]
        for i in tail:
            ret.extend(evaluate(i))
        return ret
    else:
        return 'Failure'
    
if __name__ == '__main__':
    evaluate(['3'])
