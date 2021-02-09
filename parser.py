from antlr4 import *
from SqlBaseLexer import SqlBaseLexer
from SqlBaseParser import SqlBaseParser
from SQLParserListenerImpl import SQLParserListenerImpl
import os


def pre_process(query_string):
    substitution_strings = ["STRAIGHT_JOIN"]
    for replace_str in substitution_strings:
        query_string = query_string.replace(replace_str,"")
    return query_string


def parse(query_string):
    processed_query_string = pre_process(query_string)
    print(processed_query_string)
    lexer = SqlBaseLexer(InputStream(processed_query_string))
    stream = CommonTokenStream(lexer)
    stream.fill()
    parser = SqlBaseParser(stream)
    ast = parser.singleStatement()
    ast_str = ast.toStringTree(recog=parser)
    print(ast_str)
    sql_listener = SQLParserListenerImpl()
    sql_listener.initialize()
    ast_visitor = ParseTreeWalker()
    ast_visitor.walk(sql_listener, ast)
    return sql_listener.get_query_metadata()


if __name__ == "__main__":
    sql_files = []
    path = 'C:\\Users\\csaga\\PycharmProjects\\SQLParser\\test\sqls\\'
    for root, directories, files in os.walk(path, topdown=False):
        for name in files:
            sql_files.append(os.path.join(root, name))
    #sql_files = ["C:\\Users\\csaga\\PycharmProjects\\SQLParser\\test\\sqls\\ctas.sql"]
    for f in sql_files:
        print("***********{}****************".format(f))
        file = FileStream(f)
        sql = ""
        with open(f, 'r') as sql_file:
            sql =sql_file.read().upper()
        print(parse(sql))



