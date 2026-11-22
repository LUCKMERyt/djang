import os
import pymysql

conn = pymysql.connect(host=os.environ.get('DB_HOST', '127.0.0.1'),
                       port=int(os.environ.get('DB_PORT', '3306')),
                       user=os.environ['DB_USER'],
                       password=os.environ['DB_PASSWORD'],
                       database=os.environ['DB_NAME'], charset='utf8mb4',
                       cursorclass=pymysql.cursors.DictCursor)
cur = conn.cursor()
cur.execute("SELECT COUNT(*) AS total FROM hello_products")
print('Всего товаров:', cur.fetchone())
cur.execute("SELECT COUNT(*) AS empty_slugs FROM hello_products WHERE slug IS NULL OR slug = ''")
print('Пустых слагов:', cur.fetchone())
cur.execute("SELECT COUNT(DISTINCT slug) AS uniq, COUNT(*) AS total FROM hello_products WHERE slug IS NOT NULL AND slug != ''")
print('Уникальных / всего слагов:', cur.fetchone())
conn.close()
