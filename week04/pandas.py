import numpy as np
import pandas as pd
import pymysql

conn = pymysql.connect('ip', 'name', 'pass', 'dbname', charset=utf8)
sql = 'select * from data'

# 1. SELECT * FROM data;
example = pd.read_sql(sql, conn)

# 2. SELECT * FROM data LIMIT 10;
example.head(10)

# 3. SELECT id FROM data;  //id 是 data 表的特定一列
example.['id']

# 4. SELECT COUNT(id) FROM data;
example.['id'].count()

# 5. SELECT * FROM data WHERE id<1000 AND age>30;
example[(example['id'] < 1000) & (example['age'] > 30)]

# 6. SELECT id,COUNT(DISTINCT order_id) FROM table1 GROUP BY id;
example.groupby('id').agg({'id':np.size,'order_id':example['order_id'].drop_duplicates().count()})

# 7. SELECT * FROM table1 t1 INNER JOIN table2 t2 ON t1.id = t2.id;
pd.merge(t1,t2,on='id')

# 8. SELECT * FROM table1 UNION SELECT * FROM table2;
pd.concat([table1,table2]).drop_duplicates()

# 9. DELETE FROM table1 WHERE id=10;
table1.ix[~table1['id']=10]

# 10. ALTER TABLE table1 DROP COLUMN column_name;
table1.ix[~table1['column_name']]
