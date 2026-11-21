import pymysql

conn = pymysql.connect(host='127.0.0.1', port=3306, user='myuser',
                       password='1234', database='djangoo', charset='utf8mb4')
cur = conn.cursor()
cur.execute("SHOW TABLES")
tables = [r[0] for r in cur.fetchall()]
print('tables:', tables)

if 'hello_products' in tables:
    cur.execute("SELECT COUNT(*) FROM hello_products")
    print('hello_products count:', cur.fetchone()[0])
    cur.execute("SELECT id, name, image FROM hello_products ORDER BY id ASC")
    rows = cur.fetchall()
    print('first 5:', [(r[0], (r[1] or '')[:35], (r[2] or '')) for r in rows[:5]])
    print('last 10:', [(r[0], (r[1] or '')[:35], (r[2] or '')) for r in rows[-10:]])
conn.close()
