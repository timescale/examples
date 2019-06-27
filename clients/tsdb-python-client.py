from psycopg2.extras import RealDictCursor
import psycopg2

uri = "postgres://YOUR-USER:YOUR-PASSWORD@YOUR-SERVICE.a.timescaledb.io:26479/defaultdb?sslmode=require"

db_conn = psycopg2.connect(uri)
c = db_conn.cursor(cursor_factory=RealDictCursor)

c.execute("SELECT 1 = 1")
result = c.fetchone()
