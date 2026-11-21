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

def type_en(name):
    n = name.lower()
    rules = [
        ('серьги-кольца', 'hoop earrings'),
        ('набор «мини-стек»', 'ring set'),
        ('набор «кристалл»', 'ear studs'),
        ('кольцо', 'ring'),
        ('серьги', 'earrings'),
        ('кулон', 'pendant'),
        ('подвеска', 'pendant'),
        ('колье', 'necklace'),
        ('цепочка', 'chain necklace'),
        ('браслет', 'bracelet'),
        ('брошь', 'brooch'),
        ('сумка-тоут', 'tote bag'),
        ('шопер', 'tote bag'),
        ('сумка', 'handbag'),
        ('клатч', 'clutch bag'),
        ('рюкзак', 'backpack'),
        ('кошелёк', 'wallet'),
        ('картхолдер', 'card holder'),
        ('ремень', 'belt'),
        ('платок', 'scarf'),
        ('палантин', 'shawl'),
        ('шарф', 'scarf'),
        ('очки', 'sunglasses'),
        ('шапка', 'beanie hat'),
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
        ('мыла', 'soap'),
        ('плед', 'blanket'),
        ('кружка', 'mug'),
        ('чашка', 'mug'),
        ('термос', 'thermos'),
        ('блокнот', 'notebook'),
        ('открыток', 'postcards'),
        ('спрей', 'room spray'),
        ('шкатулка', 'jewelry box'),
        ('фоторамка', 'picture frame'),
        ('сертификат', 'gift certificate'),
        ('упаковка', 'gift wrapping'),
        ('ванны', 'bath set'),
        ('подставка', 'coaster'),
        ('ароматизатор', 'car air freshener'),
        ('пикника', 'picnic set'),
    ]
    for key, val in rules:
        if key in n:
            return val
    return 'gift'

def material_en(material):
    m = material.lower()
    rules = [
        ('белое золото', 'white gold'),
        ('позолоченное серебро', 'gold plated silver'),
        ('позолоченная сталь', 'gold plated steel'),
        ('нержавеющая сталь', 'stainless steel'),
        ('хирургическая сталь', 'stainless steel'),
        ('ювелирная сталь', 'stainless steel'),
        ('серебро', 'silver'),
        ('золото', 'gold'),
        ('сталь', 'steel'),
        ('экокожа', 'faux leather'),
        ('натуральная кожа', 'leather'),
        ('кожа', 'leather'),
        ('нейлон', 'nylon'),
        ('лён', 'linen'),
        ('атлас', 'satin'),
        ('шёлк', 'silk'),
        ('шерсть', 'wool'),
        ('кашемир', 'cashmere'),
        ('хлопок', 'cotton'),
        ('бархат', 'velvet'),
        ('керамика', 'ceramic'),
        ('стекло', 'glass'),
        ('соевый воск', 'soy wax'),
        ('дерево', 'wooden'),
        ('акрил', 'acrylic'),
        ('полиэстер', 'polyester'),
        ('пвх', 'pvc'),
        ('флис', 'fleece'),
        ('фильц', 'felt'),
        ('бумага', 'paper'),
        ('металл', 'metal'),
        ('аметист', 'amethyst'),
        ('изумруд', 'emerald'),
        ('лабрадорит', 'labradorite'),
        ('лунный камень', 'moonstone'),
        ('опал', 'opal'),
        ('кварц', 'quartz'),
        ('жемчуг', 'pearl'),
        ('фианит', 'cubic zirconia'),
        ('цирконий', 'zirconia'),
        ('алмаз', 'diamond'),
        ('эмаль', 'enamel'),
        ('ацетат', 'acetate'),
        ('поликарбонат', 'polycarbonate'),
        ('спандекс', 'spandex'),
    ]
    found = []
    for key, val in rules:
        if key not in m:
            continue
        # Skip a value that is already covered by a more specific one
        if any(val in existing or existing in val for existing in found):
            continue
        found.append(val)
    return ' '.join(found[:2])

plan = []
n = FIRST
for category, items in products.items():
    for item in items:
        name, sale, material = item[0], item[1], item[2]
        t = type_en(name)
        mat = material_en(material)
        query = (t + ' ' + mat).strip()
        plan.append({
            'n': n,
            'name': name,
            'category': category,
            'material': material,
            'type': t,
            'material_en': mat,
            'query': query,
        })
        n += 1

with open(OUT, 'w', encoding='utf-8') as f:
    json.dump(plan, f, ensure_ascii=False, indent=2)

print(f'plan entries: {len(plan)}, photos {plan[0]["n"]}..{plan[-1]["n"]}')
for p in plan[:5]:
    print(p['n'], '|', p['query'], '|', p['name'])
