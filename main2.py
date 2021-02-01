import numpy as np
from antlr4 import *
from SimpleExpr1Lexer import SimpleExpr1Lexer
from SimpleExpr1Parser import SimpleExpr1Parser
def beautify_lisp_string(in_string):
    indent_size = 3
    add_indent = ' '*indent_size
    out_string = in_string[0]  # no indent for 1st (
    indent = ''
    for i in range(1, len(in_string)):
        if in_string[i] == '(' and in_string[i+1] != ' ':
            indent += add_indent
            out_string += "\n" + indent + '('
        elif in_string[i] == ')':
            out_string += ')'
            if len(indent) > 0:
                indent = indent.replace(add_indent, '', 1)
        else:
            out_string += in_string[i]
    return out_string

file = FileStream("test1.txt")
lexer = SimpleExpr1Lexer(file)
stream = CommonTokenStream(lexer)
stream.fill()
print('tokens:')
for tk in stream.tokens:
    print(tk)
parser = SimpleExpr1Parser(stream)
tree = parser.stat()
print("tree")
lisp_tree_str = tree.toStringTree(recog=parser)
print(beautify_lisp_string(lisp_tree_str))


