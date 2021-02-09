import numpy as np
from antlr4 import *
from SqlBaseLexer import SqlBaseLexer
from SqlBaseListener import SqlBaseListener
from SqlBaseParser import SqlBaseParser
import os
from io import StringIO
from Query import  Filter
def testSelectClause() :
    text = "TABLE1.COL1='42424' "
    lexer = SqlBaseLexer(InputStream (text))
    stream = CommonTokenStream(lexer)
    stream.fill()
    print('tokens:')
    ignore_list=["","(",")"]
    #IN=113
    #identifier=292
    filter_cond = Filter()
    for tk in stream.tokens:
        print(tk)
        val = text[tk.start:tk.stop+1].strip()
        if tk.type == 292:
            filter_cond.set_filter_column(val)
        elif tk.type == 113:
            filter_cond.set_filter_type("IN")
        elif tk.type == 26:
            filter_cond.set_filter_type("BETWEEN")
        elif tk.type == 264:
            filter_cond.set_filter_type("EQUALS")
        elif tk.type == 271 or tk.type == 269 or tk.type == 268 or tk.type == 270:
            filter_cond.set_filter_type("INEQUALITY")

    if filter_cond.type == "BETWEEN":
        expr=""
        for tk in stream.tokens:
            val = text[tk.start:tk.stop + 1].strip()
            if tk.type == 282:
                expr = expr+val+";"
        filter_cond.set_filter_expr(expr)

    if filter_cond.type == "EQUALS" or filter_cond.type == "INEQUALITY":
        expr = ""
        for tk in stream.tokens:
            val = text[tk.start:tk.stop + 1].strip()
            if tk.type == 282:
                expr = val
        filter_cond.set_filter_expr(expr)
    print(filter_cond)


if __name__=="__main__":
    testSelectClause()