# Generated from SqlBase.g4 by ANTLR 4.9.1
from antlr4 import *
import re
from antlr4.tree.Tree import TerminalNodeImpl
if __name__ is not None and "." in __name__:
    from .SqlBaseParser import SqlBaseParser
else:
    from SqlBaseParser import SqlBaseParser
    from SqlBaseLexer import SqlBaseLexer
    from Query import Query,Table, Relation, Predicate


# This class defines a complete listener for a parse tree produced by SqlBaseParser.
class SQLParserListenerImpl(ParseTreeListener):

    def initialize(self, query_string):
        self.table_stack = []
        self.relation_stack = []
        self.query = Query()
        self.query_string=query_string
        self.filter_columns = []
        self.column_stack= []

    def get_query_metadata(self):
        final_query = Query()
        for column in self.query.columns:
            final_query.add_columns(self.substitute_alias_with_name(column))
        for predicate in self.query.predicates:
            predicate.set_predicate_column(self.substitute_alias_with_name(predicate.column, debug=False))
            predicate.set_predicate_expr(self.substitute_alias_with_name(predicate.expr, debug=False))
            predicate.set_predicate_type(predicate.type)
            final_query.add_predicates(predicate)
        for relation in self.query.relations:
            relation.set_expression(self.substitute_alias_with_name(relation.expression))
            final_query.add_relation(relation)
        for aggregate in self.query.aggregates:
            final_query.add_aggregates(self.substitute_alias_with_name(aggregate))
        final_query.tables = self.query.tables
        final_query.functions = self.query.functions
        return final_query

    def substitute_alias_with_name(self, expr, debug=False):
        for table in self.query.tables:
            if len(table.alias) > 1:
                #print("expr:{};alias:{};name:{}".format(expr,table.alias,table.name))
                if debug:
                    print(expr, ":", table)
                    print("table.db",table.db)
                    print("replacing {} with {}".format(table.alias, table.db + '.' + table.name))
                if len(table.db) < 1:
                    expr = re.sub(r"\b%s\b" % table.alias, table.db + '.' + table.name, expr)
                else:
                    expr = re.sub(r"\b%s\b" % table.alias, table.db + '.' + table.name, expr)
        return expr

    # Enter a parse tree produced by SqlBaseParser#joinRelation.
    def enterJoinRelation(self, ctx:SqlBaseParser.JoinRelationContext):
        #print("enterJoinRelation:", ctx.getText())
        relation = Relation()
        #relation.set_left_table(self.table_stack.pop())
        self.relation_stack.append(relation)

    def enterJoinType(self, ctx:SqlBaseParser.JoinTypeContext):
        #print("enterJoinType:", ctx.getText())
        relation = self.relation_stack.pop()
        relation.set_join_type(ctx.getText())
        self.relation_stack.append(relation)


    # Enter a parse tree produced by SqlBaseParser#tableAlias.
    def enterTableAlias(self, ctx:SqlBaseParser.TableAliasContext):
        #print("enterTableAlias:", ctx.getText())
        alias_name = ctx.getText()
        table_name = ctx.parentCtx.getText()
        db_name = ""
        if "SELECT" not in table_name:
            if "." in table_name:
                parts = table_name.split(".")
                db_name = parts[0]
                table_name = parts[1]
            if len(alias_name) > 0:
                table_name = ''.join(table_name.rsplit(alias_name, 1))
            self.query.add_table(Table(db_name, table_name, alias_name))
            if len(db_name) < 1:
                self.table_stack.append(table_name)
            else:
                self.table_stack.append(db_name+'.'+table_name)
            if len(self.relation_stack) == 1:
                relation = self.relation_stack.pop()
                if len(db_name) < 1:
                    relation.set_right_table(table_name)
                else:
                    relation.set_right_table(db_name + '.' + table_name)
                self.relation_stack.append(relation)

    # Enter a parse tree produced by SqlBaseParser#expression.
    def enterExpression(self, ctx:SqlBaseParser.ExpressionContext):
        if len(self.relation_stack) > 0:
            relation = self.relation_stack.pop()
            relation.set_expression(":".join(ctx.getText().split("AND")))
            self.relation_stack.append(relation)

    # Enter a parse tree produced by SqlBaseParser#functionName.
    def enterFunctionName(self, ctx:SqlBaseParser.FunctionNameContext):
        self.query.add_function(ctx.getText())


    # Enter a parse tree produced by SqlBaseParser#joinHint.
    def enterJoinHint(self, ctx:SqlBaseParser.JoinHintContext):
        relation = self.relation_stack.pop()
        relation.set_join_hint(ctx.getText().replace("]", "").replace("[", ""))
        self.relation_stack.append(relation)

    def enterAggregationClause(self, ctx:SqlBaseParser.AggregationClauseContext):
        #print("enterAggregationClause",ctx.getText())
        grp_expr = ctx.getText().replace("GROUPBY", "")
        grp_cols = grp_expr.split(",")
        for col in grp_cols:
            if col.isdigit():
                self.query.add_aggregates(self.substitute_alias_with_name(self.column_stack[int(col)-1]))
            else:
                self.query.add_aggregates(self.substitute_alias_with_name(col))
        pass

    def enterWhereClause(self, ctx:SqlBaseParser.WhereClauseContext):
        self.filter_columns = []

    def enterColumnReference(self, ctx:SqlBaseParser.ColumnReferenceContext):
        self.query.add_columns(ctx.getText())
        self.column_stack.append(ctx.getText())
        self.filter_columns.append(ctx.getText())


    def enterPredicate(self, ctx:SqlBaseParser.PredicateContext):
        #print("enterPredicate", ctx.getText())
        text = ctx.getText()
        if "BETWEEN" in text:
            predicate = Predicate()
            column = self.filter_columns.pop()
            predicate.set_predicate_column(column)
            predicate.set_predicate_type("BETWEEN")
            cond = text.replace("BETWEEN", "").replace('"', '').replace("'", '').replace("AND",":")
            predicate.set_predicate_expr(cond)
            self.query.add_predicates(predicate)
        if "IN" in text:
            predicate = Predicate()
            column = self.filter_columns.pop()
            predicate.set_predicate_column(column)
            predicate.set_predicate_type("IN")
            cond = text.replace("IN", "").replace("(","").replace(")","").replace('"', '').replace("'", '')
            predicate.set_predicate_expr(":".join(cond.split(",")))
            self.query.add_predicates(predicate)


    def enterComparison(self, ctx:SqlBaseParser.PredicateContext):

        text = ctx.getText()
        lexer = SqlBaseLexer(InputStream(text))
        stream = CommonTokenStream(lexer)
        stream.fill()
        left_token_type = stream.tokens[0].type
        left_token = stream.tokens[0].text
        operator = stream.tokens[1].type
        right_token_type = stream.tokens[2].type
        right_token = stream.tokens[2].text

        INEQUALITY_OPERATORS = [268, 269, 270, 271]
        STRING_IDENTIFIERS = [282, 286]
        IDENTIFIER = 292

        if left_token_type == IDENTIFIER and operator == 264 and right_token_type in STRING_IDENTIFIERS:
            condition = Predicate()
            condition.set_predicate_column(left_token)
            condition.set_predicate_type("EQUALS")
            condition.set_predicate_expr(right_token.replace("'", '').replace('"',""))
            self.query.add_predicates(condition)

        elif left_token_type == IDENTIFIER and operator in INEQUALITY_OPERATORS and right_token_type in STRING_IDENTIFIERS:
            condition = Predicate()
            condition.set_predicate_column(left_token)
            condition.set_predicate_type("INEQUALITY")
            condition.set_predicate_expr(right_token.replace("'", '').replace('"',""))
            self.query.add_predicates(condition)

        if left_token_type == IDENTIFIER and right_token_type == IDENTIFIER:
            if len(self.relation_stack) > 0:
                relation = self.relation_stack.pop()
                known_table_parts = relation.right_table.split('.')
                expr_first_table = self.query.get_table_name_by_alias(left_token.split('.')[0])
                expr_second_table = self.query.get_table_name_by_alias(right_token.split('.')[0])
                if len(known_table_parts) == 1:
                    known_tables_name = known_table_parts[0]
                    table_alias = self.query.get_alias_by_table_name(known_tables_name)
                    if table_alias != "None":
                        if expr_first_table == table_alias:
                            relation.set_left_table(self.query.get_table_name_by_alias(expr_second_table))
                        else:
                            relation.set_left_table(self.query.get_table_name_by_alias(expr_first_table))
                else:
                    known_tables_name = known_table_parts[1]
                    known_table_alias = self.query.get_alias_by_table_name(known_tables_name)
                    if known_table_alias != "None":
                        if left_token.split('.')[0] == known_table_alias:
                            relation.set_left_table(expr_second_table)
                        else:
                            relation.set_left_table(expr_first_table)

                self.query.add_relation(relation)

del SqlBaseParser