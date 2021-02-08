import json
from lexer import select_stmt
tests = [
    "select * from table1 where z > 100",
    "select count(abc) from table1 where date = '2021-01-01'",
    "select col1,col2 from table1 where col > 100",
    "select a.col1, b.col2 from a.table1 inner join b.table2 where a.col > 100",
    "select a.col1, b.col2 from a.table1 inner join b.table2 on (a.b=c.d) inner join table3 on (d.x=y.z) where a.col > 100",
    "create table table3 as select a.col1, b.col2 from a.table1 inner join b.table2 where a.col > 100",
    "create table d.table3 as select a.col1, b.col2 from a.table1 inner join b.table2 where a.col > 100",
    "create table d.table3 as select count(a.abc) from a.table1 where a.col > 100 GROUP BY b.col2",
]

if __name__ == "__main__":
    #main()
    for sql in tests:
        print("Testing SQL:", sql)
        print(json.dumps(select_stmt.parseString(sql).asDict()))
    #for t, start, end in select_stmt.scanString(statement):
    #    print(' ' * start + '^' * (end - start))
    #    print(' '*start + t[0])