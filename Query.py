
class Table():

    def __init__(self,db, name, alias):
        self.db= db
        self.name = name
        self.alias = alias

    def __str__(self):
        return "{}.{}.{}".format(self.db, self.name,self.alias)

    def __eq__(self, other):
        if not isinstance(other, Table):
            return NotImplemented
        return self.db == other.db and self.name == other.name and self.alias == other.alias


class Predicate():

    def __init__(self, column="", type="", expr=""):
        self.column= column
        self.type = type
        self.expr = expr

    def set_predicate_type(self, type):
        self.type=type

    def set_predicate_column(self, column):
        self.column=column

    def set_predicate_expr(self, expr):
        self.expr=expr

    def __str__(self):
        return "({},{},{})".format(self.column, self.type, self.expr)

    def __eq__(self, other):
        if not isinstance(other, Predicate):
            return NotImplemented
        return self.column == other.column and self.type == other.type and self.expr == other.expr

class Relation():

    def __init__(self, type=None, left_table=None, right_table=None, expression=None, join_hint=None):
        self.type = type
        self.left_table = left_table
        self.right_table = right_table
        self.expression = expression
        self.join_hint = join_hint

    def set_join_type(self, type):
        self.type = type

    def set_left_table(self, left_table):
        self.left_table = left_table

    def set_right_table(self, right_table):
        self.right_table = right_table

    def set_expression(self, expression):
        #print("set_expression:", str(self))
        self.expression = expression

    def set_join_hint(self, join_hint):
        self.join_hint = join_hint

    def __str__(self):
        return " {},{},{},{},{}".format(self.type, self.left_table, self.right_table, self.expression, self.join_hint)

    def __eq__(self, other):
        if not isinstance(other, Relation):
            return NotImplemented
        return self.type == other.type \
               and self.left_table == other.left_table \
               and self.right_table == other.right_table \
               and self.expression == other.expression \
               and self.join_hint == other.join_hint

class Query():

    def __init__(self):
        self.tables = []
        self.relations = []
        self.functions = set()
        self.aggregates = []
        self.predicates = []
        self.columns = set()

    def add_table(self, table):
        self.tables.append(table)

    def add_relation(self, relation):
        self.relations.append(relation)

    def add_function(self, function):
        self.functions.add(function)

    def add_aggregates(self, aggregate):
        self.aggregates.append(aggregate)

    def add_predicates(self, predicate):
        self.predicates.append(predicate)

    def add_columns(self, column):
        if column is not None:
            self.columns.add(column)

    def get_table_name_by_alias(self, alias):
        for table in self.tables:
            if table.alias == alias:
                return table.db+"."+table.name
        return "None"

    def get_alias_by_table_name(self, name):
        for table in self.tables:
            if table.name == name:
                return table.alias
        return "None"

    def __str__(self):
        return "Tables:"+" ;".join(["("+str(x)+")"for x in self.tables ]) \
               + "\nColumns:" + " ;".join([str(x) for x in self.columns])\
               +"\nRelations: "+"\n".join([ "("+str(x)+")" for x in self.relations ])\
               +"\nFunctions:"+" ;".join([ str(x) for x in self.functions ])\
               +"\nPredicates:" + " ;".join([str(x) for x in self.predicates])\
               +"\nAggregates:" + " ;".join([str(x) for x in self.aggregates])


