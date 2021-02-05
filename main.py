import numpy as np
from antlr4 import *
from SqlBaseLexer import SqlBaseLexer
from SqlBaseListener import SqlBaseListener
from SqlBaseParser import SqlBaseParser
import os


if __name__=="__main__":
    sql_files = []
    path = 'C:\\Users\\csaga\\PycharmProjects\\SQLParser\\test\sqls\\'
    for root, directories, files in os.walk(path, topdown=False):
        for name in files:
            sql_files.append(os.path.join(root, name))
    sql_files = ["C:\\Users\\csaga\\PycharmProjects\\SQLParser\\test\\sqls\\ComplexJoin.sql"]
    for f in sql_files:
        print(f)
        file = FileStream(f)
        lexer = SqlBaseLexer(file)
        stream = CommonTokenStream(lexer)
        stream.fill()
        #print('tokens:')
        #for tk in stream.tokens:
        #    print(tk)
        parser = SqlBaseParser(stream)
        tree = parser.singleStatement()
        lisp_tree_str = tree.toStringTree(recog=parser)

        print(lisp_tree_str)
        sqlListener = SqlBaseListener()
        sqlListener.initialize()
        walker = ParseTreeWalker()
        walker.walk(sqlListener, tree)
        print(sqlListener.get_query_metadata())


