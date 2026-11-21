import os
import sys

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Al_Ven.settings')
sys.path.insert(0, r'D:\djang\Al_Ven')

import django
django.setup()

from django.test import Client
from hello.models import Products, Person

client = Client()
lines = []
errors = []

# --- DB slugs ---
null_slugs = list(Products.objects.filter(slug__isnull=True).values_list('id', 'name'))
empty_slugs = list(Products.objects.filter(slug='').values_list('id', 'name'))
lines.append(f'Products: {Products.objects.count()}, Person: {Person.objects.count()}')
lines.append(f'Null slugs: {len(null_slugs)}, empty slugs: {len(empty_slugs)}')

# --- /products/ page ---
resp = client.get('/products/')
html = resp.content.decode('utf-8', errors='replace')
lines.append(f'GET /products/ -> {resp.status_code}')
if resp.status_code != 200:
    errors.append('/products/ status != 200')

shown = 0
for p in Products.objects.all():
    if p.image and p.image.url in html:
        shown += 1
lines.append(f'Product image URLs present on /products/: {shown} of {Products.objects.count()}')
if shown != Products.objects.count():
    missing = [p.id for p in Products.objects.all() if p.image and p.image.url not in html]
    errors.append(f'/products/ missing image URLs for ids: {missing[:20]}')

# --- detail pages ---
detail_ok = 0
detail_bad = []
for p in Products.objects.all():
    if not p.slug:
        detail_bad.append((p.id, p.name, 'NO SLUG'))
        continue
    r = client.get(f'/products/{p.slug}/')
    if r.status_code == 200 and p.image and p.image.url in r.content.decode('utf-8', errors='replace'):
        detail_ok += 1
    else:
        detail_bad.append((p.id, p.name, f'status={r.status_code}'))
lines.append(f'Detail pages with image OK: {detail_ok} of {Products.objects.count()}')
for b in detail_bad[:20]:
    errors.append(f'detail problem: {b}')

# --- /news/ team page ---
r = client.get('/news/')
html_news = r.content.decode('utf-8', errors='replace')
people_ok = 0
for person in Person.objects.all():
    if person.image and person.image.url in html_news:
        people_ok += 1
lines.append(f'GET /news/ -> {r.status_code}; person images present: {people_ok} of {Person.objects.count()}')
if r.status_code != 200:
    errors.append('/news/ status != 200')
if people_ok != Person.objects.count():
    errors.append('some person images missing on /news/')

# --- media serving ---
media_ok = 0
media_bad = []
for p in Products.objects.all():
    if not p.image:
        continue
    mr = client.get(p.image.url)
    ctype = mr.headers.get('Content-Type', '')
    if mr.status_code == 200 and ctype.startswith('image/'):
        media_ok += 1
    else:
        media_bad.append((p.image.url, mr.status_code, ctype))
for person in Person.objects.all():
    if not person.image:
        continue
    mr = client.get(person.image.url)
    ctype = mr.headers.get('Content-Type', '')
    if mr.status_code == 200 and ctype.startswith('image/'):
        media_ok += 1
    else:
        media_bad.append((person.image.url, mr.status_code, ctype))
lines.append(f'Media files served OK: {media_ok} of {Products.objects.count() + Person.objects.count()}')
for b in media_bad[:20]:
    errors.append(f'media problem: {b}')

# --- index page ---
r = client.get('/')
lines.append(f'GET / -> {r.status_code}')

lines.append('')
lines.append('ERRORS: ' + (str(len(errors))))
for e in errors:
    lines.append('  ' + e)

open(r'D:\djang\site_check_report.txt', 'w', encoding='utf-8').write('\n'.join(lines))
print('written')
