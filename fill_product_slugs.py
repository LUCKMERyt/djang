"""Заполняет slug для товаров, созданных до добавления поля Products.slug."""
import os
import re
import pymysql

def slugify(s):
    # Повторение django.utils.text.slugify для строк на кириллице.
    s = re.sub(r'[^\w\s-]', '', s).strip().lower()
    return re.sub(r'\s+', '-', s)

conn = pymysql.connect(host=os.environ.get('DB_HOST', '127.0.0.1'),
                       port=int(os.environ.get('DB_PORT', '3306')),
                       user=os.environ['DB_USER'],
                       password=os.environ['DB_PASSWORD'],
                       database=os.environ['DB_NAME'], charset='utf8mb4',
                       cursorclass=pymysql.cursors.DictCursor)
cur = conn.cursor()
try:
    cur.execute("ALTER TABLE hello_products ADD COLUMN slug varchar(50) NULL UNIQUE")
    print("  Колонка slug добавлена.")
except pymysql.err.OperationalError:
    print("  Колонка slug уже есть.")
cur.execute("SELECT id, name, slug FROM hello_products WHERE slug IS NULL OR slug = '' ORDER BY id")
rows = cur.fetchall()
updated = 0
for r in rows:
    base = slugify(r['name']) or f"product-{r['id']}"
    slug = base
    n = 1
    while True:
        cur.execute("SELECT id FROM hello_products WHERE slug = %s AND id != %s", (slug, r['id']))
        if cur.fetchone() is None:
            break
        slug = f'{base}-{n}'
        n += 1
    cur.execute("UPDATE hello_products SET slug = %s WHERE id = %s", (slug, r['id']))
    updated += 1
    print(f"  {r['id']}: {r['name']} -> /products/{slug}/")
conn.commit()
print(f'Обновлено: {updated}')
conn.close()
