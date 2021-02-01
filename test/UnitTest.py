import numpy as np
from antlr4 import *
from SqlBaseLexer import SqlBaseLexer
from SqlBaseListener import SqlBaseListener
from SqlBaseParser import SqlBaseParser
import os
from io import StringIO

def testSelectClause() :
    lexer = SqlBaseLexer(InputStream ("SELECT ANC,ABV1 FROM DB1.TABLE1"))
    stream = CommonTokenStream(lexer)
    stream.fill()
    print('tokens:')
    for tk in stream.tokens:
        print(tk)
    parser = SqlBaseParser(stream)
    tree = parser.singleStatement()
    lisp_tree_str = tree.toStringTree(recog=parser)
    print(lisp_tree_str)


if __name__=="__main__":
    testSelectClause()