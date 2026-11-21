import os
import sqlite3
import json

DB = r'D:\djang\Al_Ven\db.sqlite3'
MEDIA = r'D:\djang\Al_Ven\media'

def kind(path):
    with open(path, 'rb') as f:
        head = f.read(12)
    if head.startswith(b'\xff\xd8\xff'):
        return 'JPEG'
    if head.startswith(b'\x89PNG\r\n\x1a\n'):
        return 'PNG'
    if head.startswith(b'GIF8'):
        return 'GIF'
    if head.startswith(b'RIFF') and head[8:12] == b'WEBP':
        return 'WEBP'
    return 'UNKNOWN'

conn = sqlite3.connect(DB)
cur = conn.cursor()

products = cur.execute("SELECT id, name, image FROM hello_products ORDER BY id").fetchall()
people = cur.execute("SELECT id, fam, name, image FROM hello_person ORDER BY id").fetchall()
conn.close()

report = []
report.append('=== ПРОВЕРКА ФОТО В БАЗЕ И НА ДИСКЕ ===')
report.append(f'Товаров: {len(products)}')
no_img = [p for p in products if not p[2]]
report.append(f'Без поля image: {len(no_img)}')

bad_products = []
counts = {}
for pid, name, image in products:
    if not image:
        bad_products.append((pid, name, image, 'NO IMAGE'))
        continue
    full = os.path.join(MEDIA, image)
    if not os.path.exists(full):
        bad_products.append((pid, name, image, 'MISSING FILE'))
        continue
    k = kind(full)
    counts[k] = counts.get(k, 0) + 1
    if k == 'UNKNOWN':
        bad_products.append((pid, name, image, 'INVALID FILE'))

report.append(f'Битых/отсутствующих: {len(bad_products)}')
for b in bad_products:
    report.append(f'  id={b[0]} {b[1]} -> {b[2]} ({b[3]})')
report.append(f'Форматы: {counts}')
report.append('')

report.append('=== СОТРУДНИКИ ===')
bad_people = []
for pid, fam, name, image in people:
    full = os.path.join(MEDIA, image) if image else ''
    status = 'OK' if image and os.path.exists(full) else 'MISSING'
    k = kind(full) if image and os.path.exists(full) else '-'
    report.append(f'  id={pid} {fam} {name} -> {image} | {status} | {k}')
    if status != 'OK':
        bad_people.append(pid)

report.append('')
report.append('=== УНИКАЛЬНОСТЬ ===')
imgs = [p[2] for p in products if p[2]]
report.append(f'Уникальных путей у товаров: {len(set(imgs))} из {len(imgs)}')

open(r'D:\djang\check_all_report.txt', 'w', encoding='utf-8').write('\n'.join(report))
print('written')
