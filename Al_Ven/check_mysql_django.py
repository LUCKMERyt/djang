import os
import sys

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Al_Ven.settings')
sys.path.insert(0, r'D:/djang/Al_Ven')

import django
django.setup()

from django.conf import settings
from hello.models import Products, Person

print('DB ENGINE:', settings.DATABASES['default']['ENGINE'])
print('DB NAME:', settings.DATABASES['default']['NAME'])
print('Products:', Products.objects.count())
print('Persons:', Person.objects.count())

for p in Products.objects.all()[:100]:
    img = str(p.image) if p.image else ''
    print(f'  {p.id} | {p.name} | {img}')

for person in Person.objects.all():
    print(f'  PERSON {person.id} | {person.name} {person.fam} | {person.image}')
