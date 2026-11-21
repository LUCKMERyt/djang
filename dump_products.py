import sqlite3, json

conn = sqlite3.connect(r'D:\djang\Al_Ven\db.sqlite3')
cur = conn.cursor()
cur.execute("SELECT id, name, cat_id_id FROM hello_products ORDER BY id")
rows = [{"id": r[0], "name": r[1], "cat": r[2]} for r in cur.fetchall()]
with open(r'D:\djang\existing_products.json', 'w', encoding='utf-8') as f:
    json.dump(rows, f, ensure_ascii=False, indent=2)
conn.close()
print("written")
