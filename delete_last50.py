import os
import pymysql

conn = pymysql.connect(host='127.0.0.1', port=3306, user='myuser',
                       password='1234', database='djangoo', charset='utf8mb4')
cur = conn.cursor()

MEDIA = r'D:\djang\Al_Ven\media'

cur.execute("SELECT id, name, image FROM hello_products ORDER BY id ASC")
rows = cur.fetchall()
total = len(rows)
keep_ids = {r[0] for r in rows[:50]}
to_delete = [r for r in rows if r[0] not in keep_ids]

print(f'Всего товаров: {total}')
print(f'Оставляем первые 50: {len(rows[:50])} (id от {rows[0][0]} до {rows[49][0]})')
print(f'Удаляем: {len(to_delete)} (id от {to_delete[0][0] if to_delete else "—"} до {to_delete[-1][0] if to_delete else "—"})')

deleted_files = 0
for pid, name, image in to_delete:
    if image:
        p = os.path.join(MEDIA, image)
        if os.path.exists(p):
            os.remove(p)
            deleted_files += 1

if to_delete:
    ids = [r[0] for r in to_delete]
    cur.execute("DELETE FROM hello_products WHERE id IN (%s)" % ",".join(str(i) for i in ids))
    conn.commit()
    print(f'Удалено из БД: {len(ids)}')

print(f'Удалено файлов изображений: {deleted_files}')

cur.execute("SELECT COUNT(*) FROM hello_products")
print(f'После удаления — товаров: {cur.fetchone()[0]}')

conn.close()
