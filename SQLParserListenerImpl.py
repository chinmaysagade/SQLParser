# Generated from SqlBase.g4 by ANTLR 4.9.1
from antlr4 import *
if __name__ is not None and "." in __name__:
    from .SqlBaseParser import SqlBaseParser
else:
    from SqlBaseParser import SqlBaseParser
    from SqlBaseLexer import SqlBaseLexer
    from Query import Query,Table, Relation, Filter


# This class defines a complete listener for a parse tree produced by SqlBaseParser.
class SQLParserListenerImpl(ParseTreeListener):

    def initialize(self):
        self.table_stack = []
        self.relation_stack = []
        self.query = Query()

    def get_query_metadata(self):
        return self.query

    def substitute_alias_with_name(self, expr):
        for table in self.query.tables:
            if len(table.alias) > 1:
                return expr.replace(table.alias, table.name)
            else:
                return expr

    # Enter a parse tree produced by SqlBaseParser#joinRelation.
    def enterJoinRelation(self, ctx:SqlBaseParser.JoinRelationContext):
        #print("enterJoinRelation:", ctx.getText())
        relation = Relation()
        relation.set_left_table(self.table_stack.pop())
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
        db_name=""
        if "SELECT" not in table_name:
            if "." in table_name:
                parts = table_name.split(".")
                db_name = parts[0]
                table_name = parts[1]
            if len(alias_name) > 0:
                table_name = table_name.replace(alias_name, '')
            self.query.add_table(Table(db_name, table_name, alias_name))
            self.table_stack.append(table_name)
            if len(self.relation_stack) == 1:
                relation = self.relation_stack.pop()
                relation.set_right_table(table_name)
                self.relation_stack.append(relation)

    # Enter a parse tree produced by SqlBaseParser#expression.
    def enterExpression(self, ctx:SqlBaseParser.ExpressionContext):
        if len(self.relation_stack)>0:
            relation = self.relation_stack.pop()
            expr = self.substitute_alias_with_name(ctx.getText())
            relation.set_expression(expr)
            self.query.add_relation(relation)

    # Enter a parse tree produced by SqlBaseParser#joinCriteria.
    def enterJoinCriteria(self, ctx:SqlBaseParser.JoinCriteriaContext):
        if len(self.relation_stack) > 0:
            relation = self.relation_stack.pop()
            expr = self.substitute_alias_with_name(ctx.getText())
            relation.set_expression(expr)
            self.query.add_relation(relation)

    # Enter a parse tree produced by SqlBaseParser#functionName.
    def enterFunctionName(self, ctx:SqlBaseParser.FunctionNameContext):
        self.query.add_function(ctx.getText())


    # Enter a parse tree produced by SqlBaseParser#joinHint.
    def enterJoinHint(self, ctx:SqlBaseParser.JoinHintContext):
        relation = self.relation_stack.pop()
        relation.set_join_hint(ctx.getText().replace("]","").replace("[",""))
        self.relation_stack.append(relation)

    def enterAggregationClause(self, ctx:SqlBaseParser.AggregationClauseContext):
        #print("enterAggregationClause",ctx.getText())
        grp_expr = ctx.getText().replace("GROUPBY","")
        grp_cols = grp_expr.split(",")
        for col in grp_cols:
            self.query.add_aggregates(self.substitute_alias_with_name(col))
        pass

    def extract_filter(self, expr):
        lexer = SqlBaseLexer(InputStream(expr))
        stream = CommonTokenStream(lexer)
        stream.fill()
        filter_cond = Filter()
        for tk in stream.tokens:
            print(tk)
            val = expr[tk.start:tk.stop + 1].strip()
            print("val:", val)
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
            fexpr = ""
            for tk in stream.tokens:
                if tk.type == 282:
                    fexpr = expr + expr[tk.start:tk.stop + 1].strip() + ";"
            filter_cond.set_filter_expr(fexpr)

        if filter_cond.type == "EQUALS" or filter_cond.type == "INEQUALITY":
            fexpr = ""
            for tk in stream.tokens:
                if tk.type == 282:
                    fexpr = expr[tk.start:tk.stop + 1].strip()
            filter_cond.set_filter_expr(fexpr)

        return filter_cond

    def enterWhereClause(self, ctx:SqlBaseParser.WhereClauseContext):
        where_clause = ctx.getText().replace("WHERE","")
        where_parts = where_clause.split('AND')
        for part in where_parts:
            print(part)
            self.query.add_filters(self.extract_filter(self.substitute_alias_with_name(part)))

    def enterColumnReference(self, ctx:SqlBaseParser.ColumnReferenceContext):
        self.query.add_columns(self.substitute_alias_with_name(ctx.getText()))

del SqlBaseParser