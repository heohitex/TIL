import pandas as pd
import cx_Oracle as oci
conn = oci.connect('HR/hr@localhost:1521/xepdb1')  # 사용자이름/Password 포트/서비스이름
print(conn.version)
df = pd.read_sql("select * from EDA_1",con=conn)
df
