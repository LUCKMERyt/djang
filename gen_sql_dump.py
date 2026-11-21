import os
import sys

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Al_Ven.settings')
os.environ['DB_ENGINE'] = 'sqlite'
os.environ['DJANGO_ALLOWED_HOSTS'] = 'testserver,localhost,127.0.0.1'
sys.path.insert(0, r'D:\djang/Al_Ven')

import django
django.setup()

from hello.models import Products

lines = []
lines.append('-- Дамп таблицы hello_products')
lines.append('-- Всего товаров: %d' % Products.objects.count())
lines.append('INSERT INTO hello_products (id, name, sale, material, date_prod, conter, cat_id_id, image, description, slug) VALUES')

rows = list(Products.objects.all().order_by('id').values())
cols = ['id', 'name', 'sale', 'material', 'date_prod', 'conter', 'cat_id_id', 'image', 'description', 'slug']

def sql_str(v):
    if v is None:
        return 'NULL'
    s = str(v).replace("'", "''")
    return "'" + s + "'"

values_sql = []
for r in rows:
    vals = []
    for c in cols:
        v = r.get(c)
        if c in ('id', 'sale', 'conter', 'cat_id_id'):
            vals.append(str(int(v)) if v is not None else 'NULL')
        elif c in ('date_prod',):
            vals.append("'" + str(v) + "'" if v else 'NULL')
        else:
            vals.append(sql_str(v))
    values_sql.append('    (' + ', '.join(vals) + ')')

lines.append(',\n'.join(values_sql) + ';')

with open(r'D:\djang\hello_products_dump.sql', 'w', encoding='utf-8') as f:
    f.write('\n'.join(lines) + '\n')

print('written')
