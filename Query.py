
class Table():

    def __init__(self,db, name, alias):
        self.db= db
        self.name = name
        self.alias = alias

    def __str__(self):
        return "{}.{}=>{}".format(self.db, self.name, self.alias)


class Relation():

    def __init__(self):
        self.type = None
        self.left_table = None
        self.right_table = None
        self.expression = None
        self.join_hint = None

    def set_join_type(self, type):
        self.type = type

    def set_left_table(self, left_table):
        self.left_table = left_table

    def set_right_table(self, right_table):
        self.right_table = right_table

    def set_expression(self, expression):
        self.expression = expression

    def set_join_hint(self, join_hint):
        self.join_hint = join_hint

    def __str__(self):
        return "Relation : {},{},{},{},{}".format(self.type, self.left_table, self.right_table, self.expression, self.join_hint)

class Query():

    def __init__(self):
        self.tables = []
        self.relations = []
        self.functions = []
        self.is_aggregate = False

    def add_table(self, table):
        self.tables.append(table)

    def add_relation(self, relation):
        self.relations.append(relation)

    def set_is_aggregate(self, is_aggregate):
        self.is_aggregate = is_aggregate

    def add_function(self, function):
        self.functions.append(function)

    def get_table_name_by_alias(self, alias):
        for table in self.tables:
            if table.alias == alias:
                return table.name
        return "None"

    def __str__(self):
        return ",".join([ str(x) for x in self.tables ])+" "+",".join([ str(x) for x in self.relations ])+",functions:"+",".join([ str(x) for x in self.functions ])
