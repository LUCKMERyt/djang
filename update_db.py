import ast
import sqlite3
from datetime import date

SRC = r'D:\djang\Al_Ven\hello\management\commands\seed_products.py'
DB = r'D:\djang\Al_Ven\db.sqlite3'
FIRST = 16

src = open(SRC, encoding='utf-8').read()
tree = ast.parse(src)

products_node = None
categories_node = None
for node in tree.body:
    if isinstance(node, ast.Assign):
        for t in node.targets:
            if isinstance(t, ast.Name) and t.id == 'PRODUCTS':
                products_node = node.value
            if isinstance(t, ast.Name) and t.id == 'CATEGORY_DESCRIPTIONS':
                categories_node = node.value

PRODUCTS = eval(compile(ast.Expression(products_node), '<seed>', 'eval'), {'date': date})
CATS = eval(compile(ast.Expression(categories_node), '<seed>', 'eval'))

conn = sqlite3.connect(DB)
cur = conn.cursor()

created_products = 0
updated_images = 0
skipped_existing = 0
n = FIRST

for category_name, items in PRODUCTS.items():
    cur.execute("SELECT id FROM hello_category WHERE name = ?", (category_name,))
    row = cur.fetchone()
    if row:
        cat_id = row[0]
    else:
        cur.execute(
            "INSERT INTO hello_category (name, coment) VALUES (?, ?)",
            (category_name, CATS.get(category_name, '')),
        )
        cat_id = cur.lastrowid

    for name, sale, material, date_prod, conter, description in items:
        photo = f'products/photo_{n}.jpg'
        cur.execute(
            "SELECT id, image FROM hello_products WHERE name = ? AND cat_id_id = ?",
            (name, cat_id),
        )
        row = cur.fetchone()
        if row:
            pid, image = row
            if not image:
                cur.execute("UPDATE hello_products SET image = ? WHERE id = ?", (photo, pid))
                updated_images += 1
            else:
                skipped_existing += 1
        else:
            cur.execute(
                "INSERT INTO hello_products (name, sale, material, date_prod, conter, cat_id_id, image, description) "
                "VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
                (name, sale, material, date_prod.isoformat(), conter, cat_id, photo, description),
            )
            created_products += 1
        n += 1

conn.commit()
cur.execute("SELECT COUNT(*) FROM hello_products")
total = cur.fetchone()[0]
cur.execute("SELECT COUNT(*) FROM hello_products WHERE image IS NOT NULL AND image != ''")
with_img = cur.fetchone()[0]

print(f"Created products: {created_products}")
print(f"Updated images on existing: {updated_images}")
print(f"Skipped (already had image): {skipped_existing}")
print(f"Total products in DB: {total}")
print(f"Products with image: {with_img}")
conn.close()
