import os
import sys

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Al_Ven.settings')
os.environ['DB_ENGINE'] = 'sqlite'
os.environ['DJANGO_ALLOWED_HOSTS'] = 'testserver,localhost,127.0.0.1'
sys.path.insert(0, r'D:\djang/Al_Ven')

import django
django.setup()

from django.conf import settings
from django.test import Client
from hello.models import Products, Person

client = Client()
print('MEDIA_ROOT:', settings.MEDIA_ROOT)
print('MEDIA_URL:', settings.MEDIA_URL)

paths = []
for p in Products.objects.all():
    if p.image:
        paths.append((p.image.url, str(p.image)))
for person in Person.objects.all():
    if person.image:
        paths.append((person.image.url, str(person.image)))

bad = []
good = 0
for url, fs_path in paths:
    r = client.get(url)
    exists = os.path.exists(r'D:\djang/Al_Ven/' + fs_path) if not fs_path.startswith('/media') else True
    if r.status_code == 200:
        good += 1
    else:
        bad.append((url, fs_path, r.status_code))
print(f'GOOD: {good} / {len(paths)}')
for b in bad:
    print('BAD:', b)
