from queryparser import parse
from Query import *
import unittest


class TestCalc(unittest.TestCase):

    def test_simple_select(self):
        text = '''  SELECT T1.*,
                    T1.COL1,
                    T1.COL2
                    FROM DB1.TABLE1 T1
                    '''
        query = parse(text)

        test_tables = [Table("DB1", "TABLE1", "T1")]
        columns = set(["DB1.TABLE1.*", "DB1.TABLE1.COL1", "DB1.TABLE1.COL2"])

        assert query.tables == test_tables
        #assert query.columns == columns
        assert len(query.predicates) == 0
        assert len(query.relations) == 0
        assert len(query.functions) == 0
        assert len(query.aggregates) == 0

    def test_simple_joins(self):
        text = '''  SELECT T1.*,
                    T1.COL1,
                    T1.COL2
                    FROM DB1.TABLE1 T1 
                    INNER JOIN DB1.TABLE2 T2 ON (T1.COL1 = T2.COL1 AND T1.COL2=T2.COL2)
                    LEFT  OUTER JOIN DB2.TABLE3 T3 ON (T1.COL1 = T3.COL1 AND T1.COL2=T3.COL2)
                    RIGHT OUTER JOIN DB2.TABLE4 T4 ON (T1.COL1 = T4.COL1 AND T1.COL2=T4.COL2)
                    FULL  OUTER JOIN DB2.TABLE5 T5 ON (T1.COL1 > T5.COL1 AND T1.COL2<T5.COL2)
                    '''
        query = parse(text)

        test_tables = [Table("DB1", "TABLE1", "T1"),
                       Table("DB1", "TABLE2", "T2"),
                       Table("DB2", "TABLE3", "T3"),
                       Table("DB2", "TABLE4", "T4"),
                       Table("DB2", "TABLE5", "T5")]
        columns = set(["DB1.TABLE1.*",
                       "DB1.TABLE1.COL1",
                       "DB1.TABLE1.COL2",
                       "DB1.TABLE2.COL1",
                       "DB1.TABLE2.COL2",
                       "DB2.TABLE3.COL1",
                       "DB2.TABLE3.COL2",
                       "DB2.TABLE4.COL1",
                       "DB2.TABLE4.COL2",
                       "DB2.TABLE5.COL1",
                       "DB2.TABLE5.COL2"])
        relations = [ Relation("INNER", "DB1.TABLE1", "DB1.TABLE2",     "DB1.TABLE1.COL1=DB1.TABLE2.COL1:DB1.TABLE1.COL2=DB1.TABLE2.COL2", None),
                      Relation("LEFTOUTER", "DB1.TABLE1", "DB2.TABLE3", "DB1.TABLE1.COL1=DB2.TABLE3.COL1:DB1.TABLE1.COL2=DB2.TABLE3.COL2", None),
                      Relation("RIGHTOUTER", "DB1.TABLE1", "DB2.TABLE4","DB1.TABLE1.COL1=DB2.TABLE4.COL1:DB1.TABLE1.COL2=DB2.TABLE4.COL2", None),
                      Relation("FULLOUTER", "DB1.TABLE1", "DB2.TABLE5", "DB1.TABLE1.COL1>DB2.TABLE5.COL1:DB1.TABLE1.COL2<DB2.TABLE5.COL2", None)
                     ]

        assert query.tables == test_tables
        assert query.relations == relations
        assert query.columns == columns
        assert len(query.predicates) == 0
        assert len(query.functions) == 0
        assert len(query.aggregates) == 0


    def test_predicates(self):
        text = '''  SELECT T1.*
                    FROM DB1.TABLE1 T1
                    WHERE T1.COL1="TEST1"
                    AND T1.COL2 BETWEEN "A" AND "B"
                    AND T1.COL3 > "GT" AND T1.COL4<"LT"
                    AND T1.COL5 IN ("C","D") 
               '''
        query = parse(text)

        test_tables = [Table("DB1","TABLE1","T1")]
        assert query.tables == test_tables

        columns = set(["DB1.TABLE1.*",
                       "DB1.TABLE1.COL1",
                       "DB1.TABLE1.COL2",
                       "DB1.TABLE1.COL3",
                       "DB1.TABLE1.COL4",
                       "DB1.TABLE1.COL5"])
        assert query.columns == columns
        assert len(query.relations) == 0
        predicates = [Predicate("DB1.TABLE1.COL1", "EQUALS", "TEST1"),
                      Predicate("DB1.TABLE1.COL2", "BETWEEN", "A:B"),
                      Predicate("DB1.TABLE1.COL3", "INEQUALITY", "GT"),
                      Predicate("DB1.TABLE1.COL4", "INEQUALITY", "LT"),
                      Predicate("DB1.TABLE1.COL5", "IN", "C:D")

                     ]
        assert query.predicates == predicates
        assert len(query.functions) == 0
        assert len(query.aggregates) == 0

    def test_aggregates(self):
        text = '''  SELECT T1.COL1,
                    T1.COL2
                    FROM DB1.TABLE1 T1
                    GROUP BY T1.COL1, 2
               '''
        query = parse(text)

        test_tables = [Table("DB1", "TABLE1", "T1")]
        assert query.tables == test_tables
        columns = set(["DB1.TABLE1.COL1","DB1.TABLE1.COL2"])

        assert query.columns == columns
        assert len(query.relations) == 0
        assert len(query.predicates) == 0
        assert len(query.functions) == 0
        aggregates = ['DB1.TABLE1.COL1', 'DB1.TABLE1.COL2']
        assert query.aggregates == aggregates

    def test_unaliased_query(self):
        text = '''  SELECT COL1,
                    COL2
                    FROM TABLE1
                    GROUP BY COL1, 2
               '''
        query = parse(text)

        test_tables = [Table("", "TABLE1", "")]
        for tab in query.tables:
            print(tab)
        assert query.tables == test_tables
        columns = set(["COL1", "COL2"])
        print(query.columns)
        assert query.columns == columns
        assert len(query.relations) == 0
        assert len(query.predicates) == 0
        assert len(query.functions) == 0
        aggregates = ['COL1', 'COL2']
        assert query.aggregates == aggregates


if __name__=="__main__":
    unittest.main(argv=['first-arg-is-ignored'], exit=False)