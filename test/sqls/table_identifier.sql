SELECT STRAIGHT_JOIN A, B
FROM TABLE1 A1
INNER JOIN [BROADCAST] ABC.12TABLE3 A3 ON (A1.COL1=A3.COL2)