import sys
from pyparsing import *

ParserElement.enablePackrat()


def map_keywords():
    keywords = {}
    with open("keywords.txt") as f:
        tokens = f.readlines()
        for token in tokens:
            keywords[token.strip()] = CaselessKeyword(token.replace('\n','').strip())
    return keywords


def map_aggregate_functions():
    functions = "COUNT|SUM|AVG|"
    return {
        k.strip(): CaselessKeyword(k.strip())
        for k in functions.split("|")
    }


keywords = map_keywords()
vars().update(keywords)
aggregate_functions = map_aggregate_functions()
vars().update(aggregate_functions)

LPAR, RPAR, COMMA = map(Suppress, "(),")
DOT, STAR = map(Literal, ".*")
UNARY, BINARY, TERNARY = 1, 2, 3
any_keyword = MatchFirst(keywords.values())
quoted_identifier = QuotedString('"', escQuote='""')
comment = "--" + restOfLine

identifier = (~any_keyword + Word(alphas, alphanums + "_")).setParseAction(
    pyparsing_common.downcaseTokens
) | quoted_identifier

collation_name = identifier.copy()
column_name = identifier.copy()
column_alias = identifier.copy()
table_name = identifier.copy()
table_alias = identifier.copy()
index_name = identifier.copy()
function_name = identifier.copy()
parameter_name = identifier.copy()
database_name = identifier.copy()
bind_parameter = Word("?", nums) | Combine(oneOf(": @ $") + parameter_name)
numeric_literal = pyparsing_common.number
string_literal = QuotedString("'", escQuote="''")
blob_literal = Regex(r"[xX]'[0-9A-Fa-f]+'")
literal_value = (
    numeric_literal
    | string_literal
    | blob_literal
    | TRUE
    | FALSE
    | NULL
    | CURRENT_TIME
    | CURRENT_DATE
    | CURRENT_TIMESTAMP
)
NOT_NULL = Group(NOT + NULL)
NOT_BETWEEN = Group(NOT + BETWEEN)
NOT_IN = Group(NOT + IN)
NOT_LIKE = Group(NOT + LIKE)
NOT_MATCH = Group(NOT + MATCH)
NOT_GLOB = Group(NOT + GLOB)
NOT_REGEXP = Group(NOT + REGEXP)
type_name = oneOf("TEXT BIGINT BOOLEAN CHAR DATE DECIMAL DOUBLE FLOAT INT MAP REAL SMALLINT STRING STRUCT TIMESTAMP TINYINT VARCHAR NULL")
expr = Forward().setName("expression")
select_stmt = Forward().setName("select statement")
cast_expr = CAST + LPAR + expr + AS + type_name + RPAR
db_aggregate_functions = MatchFirst(aggregate_functions.values())
function_expr = (db_aggregate_functions + LPAR
    + Optional(STAR | literal_value| identifier | Group(identifier("col_tab") + DOT + identifier("col")))
    + RPAR).setName("column_aggregate")
expr_term = (
    cast_expr
    | EXISTS + LPAR + select_stmt + RPAR
    | function_name.setName("function_name")+ LPAR+ Optional(STAR | delimitedList(expr))+ RPAR
    | literal_value
    | bind_parameter
    | Group(
        identifier("col_db") + DOT + identifier("col_tab") + DOT + identifier("col")
    )
    | Group(identifier("col_tab") + DOT + identifier("col"))
    | Group(identifier("col"))
)

expr << infixNotation(
    expr_term,
    [
        (oneOf("- + ~") | NOT, UNARY, opAssoc.RIGHT),
        (ISNULL | NOTNULL | NOT_NULL, UNARY, opAssoc.LEFT),
        ("||", BINARY, opAssoc.LEFT),
        (oneOf("* / %"), BINARY, opAssoc.LEFT),
        (oneOf("+ -"), BINARY, opAssoc.LEFT),
        (oneOf("<< >> & |"), BINARY, opAssoc.LEFT),
        (oneOf("< <= > >="), BINARY, opAssoc.LEFT),
        (
   oneOf("= == != <>")
   | IS
   | IN
   | LIKE
   | GLOB
   | MATCH
   | REGEXP
   | NOT_IN
   | NOT_LIKE
   | NOT_GLOB
   | NOT_MATCH
   | NOT_REGEXP,
   BINARY,
   opAssoc.LEFT,
        ),
        ((BETWEEN | NOT_BETWEEN, AND), TERNARY, opAssoc.LEFT),
        (
   (IN | NOT_IN) + LPAR + Group(select_stmt | delimitedList(expr)) + RPAR,
   UNARY,
   opAssoc.LEFT,
        ),
        (AND, BINARY, opAssoc.LEFT),
        (OR, BINARY, opAssoc.LEFT),
    ],
)

compound_operator = UNION + Optional(ALL) | INTERSECT | EXCEPT

ordering_term = Group(
    expr("order_key")
    + Optional(COLLATE + collation_name("collate"))
    + Optional(ASC | DESC)("direction")
)

join_constraint = Group(
    Optional(ON + expr | USING + LPAR + Group(delimitedList(column_name)) + RPAR)
)

join_op = COMMA | Group(
    Optional(NATURAL) + Optional(INNER | CROSS | LEFT + OUTER | LEFT | OUTER) + JOIN
)

join_source = Forward()
single_source = (
    Group(database_name("database") + DOT + table_name("table*") | table_name("table*"))
    + Optional(Optional(AS) + table_alias("table_alias*"))
    + Optional(INDEXED + BY + index_name("name") | NOT + INDEXED)("index")
    | (LPAR + select_stmt + RPAR + Optional(Optional(AS) + table_alias))
    | (LPAR + join_source + RPAR)
)

join_source <<= (
    Group(single_source + OneOrMore(join_op + single_source + join_constraint))
    | single_source
)

# result_column = "*" | table_name + "." + "*" | Group(expr + Optional(Optional(AS) + column_alias))
result_column = Group(
    STAR("col")
    | function_expr
    | table_name("col_table") + DOT + STAR("col")
    | expr("col") + Optional(Optional(AS) + column_alias("alias"))
)

select_core = (
    (SELECT |(CREATE+TABLE+Group(database_name("database") + DOT + table_name("table*") | table_name("table*"))+ AS + SELECT))
    + Optional(DISTINCT | ALL)
    + Group(delimitedList(result_column))("columns")
    + Optional(FROM + join_source("from*"))
    + Optional(WHERE + expr("where_expr"))
    + Optional(
        GROUP
        + BY
        + Group(delimitedList(ordering_term))("group_by_terms")
        + Optional(HAVING + expr("having_expr"))
    )
)

select_stmt << (
    select_core
    + ZeroOrMore(compound_operator + select_core)
    + Optional(ORDER + BY + Group(delimitedList(ordering_term))("order_by_terms"))
    + Optional(
        LIMIT
        + (Group(expr + OFFSET + expr) | Group(expr + COMMA + expr) | expr)("limit")
    )
)

select_stmt.ignore(comment)



