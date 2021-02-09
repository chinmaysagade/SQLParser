CREATE TABLE TABLE1
ROW FORMAT DELIMITED FIELDS TERMINATED BY "|"
STORED AS PARQUET
LOCATION 'L1'
SELECT t1.*,
t2.*
FROM DB1.TABLE123 t1
INNER JOIN DB1.TABLE456 t2 ON (t1.COL1=t2.COL2)
WHERE t2.COL3 in ("A","B","C")