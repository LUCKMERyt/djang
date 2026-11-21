import ast
import json
from datetime import date

SRC = r'D:\djang\Al_Ven\hello\management\commands\seed_products.py'
OUT = r'D:\djang\download_plan.json'
FIRST = 16

src = open(SRC, encoding='utf-8').read()
tree = ast.parse(src)
products_node = None
for node in tree.body:
    if isinstance(node, ast.Assign):
        for t in node.targets:
            if isinstance(t, ast.Name) and t.id == 'PRODUCTS':
                products_node = node.value
products = eval(compile(ast.Expression(products_node), '<seed>', 'eval'), {'date': date})

def q(name):
    n = name.lower()
    rules = [
        ('кольцо', 'ring jewelry'),
        ('серьги-кольца', 'hoop earrings'),
        ('серьги', 'earrings jewelry'),
        ('кулон', 'pendant necklace'),
        ('подвеска', 'pendant necklace'),
        ('колье', 'necklace jewelry'),
        ('цепочка', 'chain necklace'),
        ('браслет', 'bracelet jewelry'),
        ('брошь', 'brooch jewelry'),
        ('набор «мини-стек»', 'rings set jewelry'),
        ('набор «кристалл»', 'ear piercing studs'),
        ('рюкзак', 'backpack'),
        ('шопер', 'tote bag'),
        ('сумка-тоут', 'tote bag'),
        ('сумка', 'handbag'),
        ('клатч', 'clutch bag'),
        ('кошелёк', 'wallet'),
        ('картхолдер', 'card holder wallet'),
        ('ремень', 'leather belt'),
        ('платок', 'silk scarf'),
        ('палантин', 'shawl'),
        ('шарф', 'scarf'),
        ('очки', 'sunglasses'),
        ('шапка', 'knitted hat'),
        ('перчатки', 'gloves'),
        ('зонт', 'umbrella'),
        ('заколка', 'hair clip'),
        ('резинок', 'hair ties'),
        ('часы', 'wristwatch'),
        ('брелок', 'keychain'),
        ('свеч', 'candle'),
        ('диффузор', 'reed diffuser'),
        ('аромасаше', 'lavender sachet'),
        ('подарочный бокс', 'gift box'),
        ('чайная церемония', 'tea set'),
        ('мыла', 'handmade soap'),
        ('плед', 'blanket'),
        ('кружка', 'ceramic mug'),
        ('чашка', 'coffee mug'),
        ('термос', 'thermos'),
        ('блокнот', 'notebook'),
        ('открыток', 'postcards'),
        ('спрей', 'room spray'),
        ('шкатулка', 'jewelry box'),
        ('фоторамка', 'picture frame'),
        ('сертификат', 'gift certificate'),
        ('упаковка', 'gift wrapping'),
        ('ванны', 'bath spa set'),
        ('подставка', 'coasters'),
        ('ароматизатор', 'car air freshener'),
        ('пикника', 'picnic basket'),
    ]
    for key, query in rules:
        if key in n:
            return query
    return 'gift'

plan = []
n = FIRST
for category, items in products.items():
    for item in items:
        name = item[0]
        plan.append({
            'n': n,
            'name': name,
            'category': category,
            'query': q(name),
        })
        n += 1

with open(OUT, 'w', encoding='utf-8') as f:
    json.dump(plan, f, ensure_ascii=False, indent=2)

print(f'plan entries: {len(plan)}, photos {plan[0]["n"]}..{plan[-1]["n"]}')
