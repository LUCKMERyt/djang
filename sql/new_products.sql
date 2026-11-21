-- Новые товары для SOPHISTICATED (60 шт.). Работает в SQLite и MySQL.
-- Файл создан командой: python manage.py seed_products --sql ../sql/new_products.sql
-- Не правьте его вручную: меняйте список PRODUCTS в seed_products.py.
-- Файл можно запускать повторно: уже существующие товары пропускаются.
-- Запуск SQLite:  sqlite3 Al_Ven/db.sqlite3 < sql/new_products.sql
-- Запуск MySQL:   mysql -u USER -p DB_NAME < sql/new_products.sql

-- 1. Категории (если ещё нет)
INSERT INTO hello_category (name, coment)
SELECT 'Украшения', 'Изящные украшения и акценты для повседневных и особенных образов.'
FROM (SELECT 1 AS x) AS t
WHERE NOT EXISTS (SELECT 1 FROM hello_category WHERE name = 'Украшения');
INSERT INTO hello_category (name, coment)
SELECT 'Аксессуары', 'Стильные аксессуары, которые дополняют образ и делают его выразительнее.'
FROM (SELECT 1 AS x) AS t
WHERE NOT EXISTS (SELECT 1 FROM hello_category WHERE name = 'Аксессуары');
INSERT INTO hello_category (name, coment)
SELECT 'Подарки', 'Эстетичные подарки для близких, друзей и важных событий.'
FROM (SELECT 1 AS x) AS t
WHERE NOT EXISTS (SELECT 1 FROM hello_category WHERE name = 'Подарки');

-- 2. Товары

-- Украшения
INSERT INTO hello_products (name, sale, material, date_prod, conter, cat_id_id, image, description)
SELECT 'Кольцо «Северная звезда»', 3290, 'Серебро 925', '2025-10-12', 74, (SELECT id FROM hello_category WHERE name = 'Украшения' LIMIT 1), '', 'Кольцо с огранкой в форме звезды и матовым ободком.'
FROM (SELECT 1 AS x) AS t
WHERE NOT EXISTS (SELECT 1 FROM hello_products WHERE name = 'Кольцо «Северная звезда»' AND cat_id_id = (SELECT id FROM hello_category WHERE name = 'Украшения' LIMIT 1));
INSERT INTO hello_products (name, sale, material, date_prod, conter, cat_id_id, image, description)
SELECT 'Кольцо «Тонкая нить»', 1890, 'Позолоченное серебро', '2025-11-03', 120, (SELECT id FROM hello_category WHERE name = 'Украшения' LIMIT 1), '', 'Тонкое кольцо, которое удобно носить в стеке с другими.'
FROM (SELECT 1 AS x) AS t
WHERE NOT EXISTS (SELECT 1 FROM hello_products WHERE name = 'Кольцо «Тонкая нить»' AND cat_id_id = (SELECT id FROM hello_category WHERE name = 'Украшения' LIMIT 1));
INSERT INTO hello_products (name, sale, material, date_prod, conter, cat_id_id, image, description)
SELECT 'Кольцо «Опал Луны»', 4490, 'Серебро и опал', '2026-02-18', 38, (SELECT id FROM hello_category WHERE name = 'Украшения' LIMIT 1), '', 'Кольцо с молочным опалом в гладкой оправе.'
FROM (SELECT 1 AS x) AS t
WHERE NOT EXISTS (SELECT 1 FROM hello_products WHERE name = 'Кольцо «Опал Луны»' AND cat_id_id = (SELECT id FROM hello_category WHERE name = 'Украшения' LIMIT 1));
INSERT INTO hello_products (name, sale, material, date_prod, conter, cat_id_id, image, description)
SELECT 'Кулон «Капля росы»', 2690, 'Серебро 925', '2025-09-22', 88, (SELECT id FROM hello_category WHERE name = 'Украшения' LIMIT 1), '', 'Каплевидный кулон с мягким блеском.'
FROM (SELECT 1 AS x) AS t
WHERE NOT EXISTS (SELECT 1 FROM hello_products WHERE name = 'Кулон «Капля росы»' AND cat_id_id = (SELECT id FROM hello_category WHERE name = 'Украшения' LIMIT 1));
INSERT INTO hello_products (name, sale, material, date_prod, conter, cat_id_id, image, description)
SELECT 'Кулон «Созвездие»', 3190, 'Ювелирная сталь', '2026-03-05', 66, (SELECT id FROM hello_category WHERE name = 'Украшения' LIMIT 1), '', 'Кулон с гравировкой созвездия на тонкой цепочке.'
FROM (SELECT 1 AS x) AS t
WHERE NOT EXISTS (SELECT 1 FROM hello_products WHERE name = 'Кулон «Созвездие»' AND cat_id_id = (SELECT id FROM hello_category WHERE name = 'Украшения' LIMIT 1));
INSERT INTO hello_products (name, sale, material, date_prod, conter, cat_id_id, image, description)
SELECT 'Кулон «Лабрадор»', 4890, 'Серебро и лабрадорит', '2026-04-14', 29, (SELECT id FROM hello_category WHERE name = 'Украшения' LIMIT 1), '', 'Камень с переливами от синего до зелёного.'
FROM (SELECT 1 AS x) AS t
WHERE NOT EXISTS (SELECT 1 FROM hello_products WHERE name = 'Кулон «Лабрадор»' AND cat_id_id = (SELECT id FROM hello_category WHERE name = 'Украшения' LIMIT 1));
INSERT INTO hello_products (name, sale, material, date_prod, conter, cat_id_id, image, description)
SELECT 'Серьги «Жемчужная нить»', 2990, 'Серебро и пресноводный жемчуг', '2025-12-08', 82, (SELECT id FROM hello_category WHERE name = 'Украшения' LIMIT 1), '', 'Лёгкие серьги с нитью из пресноводного жемчуга.'
FROM (SELECT 1 AS x) AS t
WHERE NOT EXISTS (SELECT 1 FROM hello_products WHERE name = 'Серьги «Жемчужная нить»' AND cat_id_id = (SELECT id FROM hello_category WHERE name = 'Украшения' LIMIT 1));
INSERT INTO hello_products (name, sale, material, date_prod, conter, cat_id_id, image, description)
SELECT 'Серьги-кольца «Орбита»', 2390, 'Ювелирная сталь', '2025-10-27', 105, (SELECT id FROM hello_category WHERE name = 'Украшения' LIMIT 1), '', 'Гладкие кольца среднего диаметра на каждый день.'
FROM (SELECT 1 AS x) AS t
WHERE NOT EXISTS (SELECT 1 FROM hello_products WHERE name = 'Серьги-кольца «Орбита»' AND cat_id_id = (SELECT id FROM hello_category WHERE name = 'Украшения' LIMIT 1));
INSERT INTO hello_products (name, sale, material, date_prod, conter, cat_id_id, image, description)
SELECT 'Серьги «Мини-квадрат»', 1590, 'Позолоченная сталь', '2026-01-20', 140, (SELECT id FROM hello_category WHERE name = 'Украшения' LIMIT 1), '', 'Небольшие серьги-гвоздики геометричной формы.'
FROM (SELECT 1 AS x) AS t
WHERE NOT EXISTS (SELECT 1 FROM hello_products WHERE name = 'Серьги «Мини-квадрат»' AND cat_id_id = (SELECT id FROM hello_category WHERE name = 'Украшения' LIMIT 1));
INSERT INTO hello_products (name, sale, material, date_prod, conter, cat_id_id, image, description)
SELECT 'Серьги «Кварц»', 3490, 'Серебро и розовый кварц', '2026-05-11', 47, (SELECT id FROM hello_category WHERE name = 'Украшения' LIMIT 1), '', 'Серьги с розовым кварцем в тонкой оправе.'
FROM (SELECT 1 AS x) AS t
WHERE NOT EXISTS (SELECT 1 FROM hello_products WHERE name = 'Серьги «Кварц»' AND cat_id_id = (SELECT id FROM hello_category WHERE name = 'Украшения' LIMIT 1));
INSERT INTO hello_products (name, sale, material, date_prod, conter, cat_id_id, image, description)
SELECT 'Браслет «Нить судьбы»', 1490, 'Хлопок и сталь', '2025-09-30', 150, (SELECT id FROM hello_category WHERE name = 'Украшения' LIMIT 1), '', 'Тонкий плетёный браслет с регулируемой застёжкой.'
FROM (SELECT 1 AS x) AS t
WHERE NOT EXISTS (SELECT 1 FROM hello_products WHERE name = 'Браслет «Нить судьбы»' AND cat_id_id = (SELECT id FROM hello_category WHERE name = 'Украшения' LIMIT 1));
INSERT INTO hello_products (name, sale, material, date_prod, conter, cat_id_id, image, description)
SELECT 'Браслет «Звенья»', 3390, 'Серебро 925', '2026-02-02', 61, (SELECT id FROM hello_category WHERE name = 'Украшения' LIMIT 1), '', 'Браслет с крупными звеньями и надёжным замком.'
FROM (SELECT 1 AS x) AS t
WHERE NOT EXISTS (SELECT 1 FROM hello_products WHERE name = 'Браслет «Звенья»' AND cat_id_id = (SELECT id FROM hello_category WHERE name = 'Украшения' LIMIT 1));
INSERT INTO hello_products (name, sale, material, date_prod, conter, cat_id_id, image, description)
SELECT 'Браслет «Лунный камень»', 3990, 'Серебро и лунный камень', '2026-06-09', 34, (SELECT id FROM hello_category WHERE name = 'Украшения' LIMIT 1), '', 'Браслет с лунным камнем, который переливается на свету.'
FROM (SELECT 1 AS x) AS t
WHERE NOT EXISTS (SELECT 1 FROM hello_products WHERE name = 'Браслет «Лунный камень»' AND cat_id_id = (SELECT id FROM hello_category WHERE name = 'Украшения' LIMIT 1));
INSERT INTO hello_products (name, sale, material, date_prod, conter, cat_id_id, image, description)
SELECT 'Колье «Лунная дорожка»', 5290, 'Серебро и фианит', '2026-03-24', 25, (SELECT id FROM hello_category WHERE name = 'Украшения' LIMIT 1), '', 'Колье с дорожкой из фианитов для вечернего образа.'
FROM (SELECT 1 AS x) AS t
WHERE NOT EXISTS (SELECT 1 FROM hello_products WHERE name = 'Колье «Лунная дорожка»' AND cat_id_id = (SELECT id FROM hello_category WHERE name = 'Украшения' LIMIT 1));
INSERT INTO hello_products (name, sale, material, date_prod, conter, cat_id_id, image, description)
SELECT 'Колье «Чокер Velour»', 1790, 'Бархат и сталь', '2025-11-17', 96, (SELECT id FROM hello_category WHERE name = 'Украшения' LIMIT 1), '', 'Бархатный чокер с металлической застёжкой.'
FROM (SELECT 1 AS x) AS t
WHERE NOT EXISTS (SELECT 1 FROM hello_products WHERE name = 'Колье «Чокер Velour»' AND cat_id_id = (SELECT id FROM hello_category WHERE name = 'Украшения' LIMIT 1));
INSERT INTO hello_products (name, sale, material, date_prod, conter, cat_id_id, image, description)
SELECT 'Цепочка «Волна»', 3790, 'Серебро 925', '2026-01-08', 52, (SELECT id FROM hello_category WHERE name = 'Украшения' LIMIT 1), '', 'Цепочка волнообразного плетения, подходит для кулонов.'
FROM (SELECT 1 AS x) AS t
WHERE NOT EXISTS (SELECT 1 FROM hello_products WHERE name = 'Цепочка «Волна»' AND cat_id_id = (SELECT id FROM hello_category WHERE name = 'Украшения' LIMIT 1));
INSERT INTO hello_products (name, sale, material, date_prod, conter, cat_id_id, image, description)
SELECT 'Цепочка «Классика»', 2990, 'Ювелирная сталь', '2025-10-05', 110, (SELECT id FROM hello_category WHERE name = 'Украшения' LIMIT 1), '', 'Универсальная цепочка классического плетения.'
FROM (SELECT 1 AS x) AS t
WHERE NOT EXISTS (SELECT 1 FROM hello_products WHERE name = 'Цепочка «Классика»' AND cat_id_id = (SELECT id FROM hello_category WHERE name = 'Украшения' LIMIT 1));
INSERT INTO hello_products (name, sale, material, date_prod, conter, cat_id_id, image, description)
SELECT 'Брошь «Полумесяц»', 1990, 'Эмаль и сталь', '2026-04-02', 72, (SELECT id FROM hello_category WHERE name = 'Украшения' LIMIT 1), '', 'Брошь в форме полумесяца с глянцевой эмалью.'
FROM (SELECT 1 AS x) AS t
WHERE NOT EXISTS (SELECT 1 FROM hello_products WHERE name = 'Брошь «Полумесяц»' AND cat_id_id = (SELECT id FROM hello_category WHERE name = 'Украшения' LIMIT 1));
INSERT INTO hello_products (name, sale, material, date_prod, conter, cat_id_id, image, description)
SELECT 'Набор «Мини-стек» (3 кольца)', 4190, 'Позолоченное серебро', '2026-07-15', 44, (SELECT id FROM hello_category WHERE name = 'Украшения' LIMIT 1), '', 'Три тонких кольца разной фактуры в одном наборе.'
FROM (SELECT 1 AS x) AS t
WHERE NOT EXISTS (SELECT 1 FROM hello_products WHERE name = 'Набор «Мини-стек» (3 кольца)' AND cat_id_id = (SELECT id FROM hello_category WHERE name = 'Украшения' LIMIT 1));
INSERT INTO hello_products (name, sale, material, date_prod, conter, cat_id_id, image, description)
SELECT 'Набор «Кристалл» для пирсинга', 1390, 'Хирургическая сталь', '2026-08-21', 130, (SELECT id FROM hello_category WHERE name = 'Украшения' LIMIT 1), '', 'Набор гвоздиков с кристаллами для ушей.'
FROM (SELECT 1 AS x) AS t
WHERE NOT EXISTS (SELECT 1 FROM hello_products WHERE name = 'Набор «Кристалл» для пирсинга' AND cat_id_id = (SELECT id FROM hello_category WHERE name = 'Украшения' LIMIT 1));

-- Аксессуары
INSERT INTO hello_products (name, sale, material, date_prod, conter, cat_id_id, image, description)
SELECT 'Сумка «Mini Crescent»', 5490, 'Экокожа', '2026-02-10', 42, (SELECT id FROM hello_category WHERE name = 'Аксессуары' LIMIT 1), '', 'Компактная сумка полукруглой формы с регулируемым ремешком.'
FROM (SELECT 1 AS x) AS t
WHERE NOT EXISTS (SELECT 1 FROM hello_products WHERE name = 'Сумка «Mini Crescent»' AND cat_id_id = (SELECT id FROM hello_category WHERE name = 'Аксессуары' LIMIT 1));
INSERT INTO hello_products (name, sale, material, date_prod, conter, cat_id_id, image, description)
SELECT 'Рюкзак «City Slim»', 7290, 'Нейлон', '2026-03-19', 36, (SELECT id FROM hello_category WHERE name = 'Аксессуары' LIMIT 1), '', 'Тонкий городской рюкзак с отделением для ноутбука.'
FROM (SELECT 1 AS x) AS t
WHERE NOT EXISTS (SELECT 1 FROM hello_products WHERE name = 'Рюкзак «City Slim»' AND cat_id_id = (SELECT id FROM hello_category WHERE name = 'Аксессуары' LIMIT 1));
INSERT INTO hello_products (name, sale, material, date_prod, conter, cat_id_id, image, description)
SELECT 'Шопер «Linen Day»', 1990, 'Лён', '2025-10-14', 135, (SELECT id FROM hello_category WHERE name = 'Аксессуары' LIMIT 1), '', 'Вместительная сумка из плотного льна на каждый день.'
FROM (SELECT 1 AS x) AS t
WHERE NOT EXISTS (SELECT 1 FROM hello_products WHERE name = 'Шопер «Linen Day»' AND cat_id_id = (SELECT id FROM hello_category WHERE name = 'Аксессуары' LIMIT 1));
INSERT INTO hello_products (name, sale, material, date_prod, conter, cat_id_id, image, description)
SELECT 'Клатч «Evening»', 4290, 'Атлас', '2026-05-06', 31, (SELECT id FROM hello_category WHERE name = 'Аксессуары' LIMIT 1), '', 'Вечерний клатч с магнитной застёжкой и цепочкой.'
FROM (SELECT 1 AS x) AS t
WHERE NOT EXISTS (SELECT 1 FROM hello_products WHERE name = 'Клатч «Evening»' AND cat_id_id = (SELECT id FROM hello_category WHERE name = 'Аксессуары' LIMIT 1));
INSERT INTO hello_products (name, sale, material, date_prod, conter, cat_id_id, image, description)
SELECT 'Кошелёк «Origami»', 2790, 'Натуральная кожа', '2025-12-12', 77, (SELECT id FROM hello_category WHERE name = 'Аксессуары' LIMIT 1), '', 'Кошелёк со складным корпусом и отделением для монет.'
FROM (SELECT 1 AS x) AS t
WHERE NOT EXISTS (SELECT 1 FROM hello_products WHERE name = 'Кошелёк «Origami»' AND cat_id_id = (SELECT id FROM hello_category WHERE name = 'Аксессуары' LIMIT 1));
INSERT INTO hello_products (name, sale, material, date_prod, conter, cat_id_id, image, description)
SELECT 'Картхолдер «Slim»', 1690, 'Натуральная кожа', '2026-01-27', 118, (SELECT id FROM hello_category WHERE name = 'Аксессуары' LIMIT 1), '', 'Тонкий картхолдер на шесть карт.'
FROM (SELECT 1 AS x) AS t
WHERE NOT EXISTS (SELECT 1 FROM hello_products WHERE name = 'Картхолдер «Slim»' AND cat_id_id = (SELECT id FROM hello_category WHERE name = 'Аксессуары' LIMIT 1));
INSERT INTO hello_products (name, sale, material, date_prod, conter, cat_id_id, image, description)
SELECT 'Ремень «Classic Line»', 3190, 'Кожа', '2025-11-22', 69, (SELECT id FROM hello_category WHERE name = 'Аксессуары' LIMIT 1), '', 'Классический ремень с металлической пряжкой.'
FROM (SELECT 1 AS x) AS t
WHERE NOT EXISTS (SELECT 1 FROM hello_products WHERE name = 'Ремень «Classic Line»' AND cat_id_id = (SELECT id FROM hello_category WHERE name = 'Аксессуары' LIMIT 1));
INSERT INTO hello_products (name, sale, material, date_prod, conter, cat_id_id, image, description)
SELECT 'Ремень «Chain»', 3590, 'Кожа и металл', '2026-06-03', 48, (SELECT id FROM hello_category WHERE name = 'Аксессуары' LIMIT 1), '', 'Ремень с цепочкой в качестве акцента.'
FROM (SELECT 1 AS x) AS t
WHERE NOT EXISTS (SELECT 1 FROM hello_products WHERE name = 'Ремень «Chain»' AND cat_id_id = (SELECT id FROM hello_category WHERE name = 'Аксессуары' LIMIT 1));
INSERT INTO hello_products (name, sale, material, date_prod, conter, cat_id_id, image, description)
SELECT 'Платок «Aurora»', 2490, 'Шёлк', '2026-04-09', 58, (SELECT id FROM hello_category WHERE name = 'Аксессуары' LIMIT 1), '', 'Лёгкий платок с градиентным принтом.'
FROM (SELECT 1 AS x) AS t
WHERE NOT EXISTS (SELECT 1 FROM hello_products WHERE name = 'Платок «Aurora»' AND cat_id_id = (SELECT id FROM hello_category WHERE name = 'Аксессуары' LIMIT 1));
INSERT INTO hello_products (name, sale, material, date_prod, conter, cat_id_id, image, description)
SELECT 'Шарф «Haze»', 3290, 'Шерсть и шёлк', '2025-09-18', 40, (SELECT id FROM hello_category WHERE name = 'Аксессуары' LIMIT 1), '', 'Мягкий шарф с матовой текстурой.'
FROM (SELECT 1 AS x) AS t
WHERE NOT EXISTS (SELECT 1 FROM hello_products WHERE name = 'Шарф «Haze»' AND cat_id_id = (SELECT id FROM hello_category WHERE name = 'Аксессуары' LIMIT 1));
INSERT INTO hello_products (name, sale, material, date_prod, conter, cat_id_id, image, description)
SELECT 'Палантин «Fog»', 4590, 'Кашемир', '2025-10-30', 22, (SELECT id FROM hello_category WHERE name = 'Аксессуары' LIMIT 1), '', 'Тёплый палантин серого оттенка.'
FROM (SELECT 1 AS x) AS t
WHERE NOT EXISTS (SELECT 1 FROM hello_products WHERE name = 'Палантин «Fog»' AND cat_id_id = (SELECT id FROM hello_category WHERE name = 'Аксессуары' LIMIT 1));
INSERT INTO hello_products (name, sale, material, date_prod, conter, cat_id_id, image, description)
SELECT 'Очки «Clear Lens»', 3890, 'Ацетат', '2026-05-20', 60, (SELECT id FROM hello_category WHERE name = 'Аксессуары' LIMIT 1), '', 'Очки с прозрачной оправой и защитой от ультрафиолета.'
FROM (SELECT 1 AS x) AS t
WHERE NOT EXISTS (SELECT 1 FROM hello_products WHERE name = 'Очки «Clear Lens»' AND cat_id_id = (SELECT id FROM hello_category WHERE name = 'Аксессуары' LIMIT 1));
INSERT INTO hello_products (name, sale, material, date_prod, conter, cat_id_id, image, description)
SELECT 'Очки «Retro Round»', 4190, 'Металл', '2026-07-02', 53, (SELECT id FROM hello_category WHERE name = 'Аксессуары' LIMIT 1), '', 'Круглые очки в тонкой металлической оправе.'
FROM (SELECT 1 AS x) AS t
WHERE NOT EXISTS (SELECT 1 FROM hello_products WHERE name = 'Очки «Retro Round»' AND cat_id_id = (SELECT id FROM hello_category WHERE name = 'Аксессуары' LIMIT 1));
INSERT INTO hello_products (name, sale, material, date_prod, conter, cat_id_id, image, description)
SELECT 'Шапка «Grey Knit»', 2190, 'Шерсть', '2025-11-08', 92, (SELECT id FROM hello_category WHERE name = 'Аксессуары' LIMIT 1), '', 'Вязаная шапка с отворотом.'
FROM (SELECT 1 AS x) AS t
WHERE NOT EXISTS (SELECT 1 FROM hello_products WHERE name = 'Шапка «Grey Knit»' AND cat_id_id = (SELECT id FROM hello_category WHERE name = 'Аксессуары' LIMIT 1));
INSERT INTO hello_products (name, sale, material, date_prod, conter, cat_id_id, image, description)
SELECT 'Перчатки «Night Walk»', 2890, 'Кожа и флис', '2025-12-01', 64, (SELECT id FROM hello_category WHERE name = 'Аксессуары' LIMIT 1), '', 'Перчатки на флисовой подкладке для холодной погоды.'
FROM (SELECT 1 AS x) AS t
WHERE NOT EXISTS (SELECT 1 FROM hello_products WHERE name = 'Перчатки «Night Walk»' AND cat_id_id = (SELECT id FROM hello_category WHERE name = 'Аксессуары' LIMIT 1));
INSERT INTO hello_products (name, sale, material, date_prod, conter, cat_id_id, image, description)
SELECT 'Зонт «Storm Mini»', 2390, 'Полиэстер', '2026-03-30', 87, (SELECT id FROM hello_category WHERE name = 'Аксессуары' LIMIT 1), '', 'Компактный зонт, который помещается в сумку.'
FROM (SELECT 1 AS x) AS t
WHERE NOT EXISTS (SELECT 1 FROM hello_products WHERE name = 'Зонт «Storm Mini»' AND cat_id_id = (SELECT id FROM hello_category WHERE name = 'Аксессуары' LIMIT 1));
INSERT INTO hello_products (name, sale, material, date_prod, conter, cat_id_id, image, description)
SELECT 'Заколка «Pearl Clip»', 990, 'Акрил и жемчуг', '2026-02-25', 145, (SELECT id FROM hello_category WHERE name = 'Аксессуары' LIMIT 1), '', 'Заколка с имитацией жемчуга для аккуратной укладки.'
FROM (SELECT 1 AS x) AS t
WHERE NOT EXISTS (SELECT 1 FROM hello_products WHERE name = 'Заколка «Pearl Clip»' AND cat_id_id = (SELECT id FROM hello_category WHERE name = 'Аксессуары' LIMIT 1));
INSERT INTO hello_products (name, sale, material, date_prod, conter, cat_id_id, image, description)
SELECT 'Набор резинок «Silk» (3 шт.)', 890, 'Шёлк', '2025-12-18', 150, (SELECT id FROM hello_category WHERE name = 'Аксессуары' LIMIT 1), '', 'Три шёлковые резинки для волос в разных оттенках.'
FROM (SELECT 1 AS x) AS t
WHERE NOT EXISTS (SELECT 1 FROM hello_products WHERE name = 'Набор резинок «Silk» (3 шт.)' AND cat_id_id = (SELECT id FROM hello_category WHERE name = 'Аксессуары' LIMIT 1));
INSERT INTO hello_products (name, sale, material, date_prod, conter, cat_id_id, image, description)
SELECT 'Часы «Minimal Black»', 5990, 'Сталь и минеральное стекло', '2026-08-08', 27, (SELECT id FROM hello_category WHERE name = 'Аксессуары' LIMIT 1), '', 'Часы с чёрным циферблатом без лишних элементов.'
FROM (SELECT 1 AS x) AS t
WHERE NOT EXISTS (SELECT 1 FROM hello_products WHERE name = 'Часы «Minimal Black»' AND cat_id_id = (SELECT id FROM hello_category WHERE name = 'Аксессуары' LIMIT 1));
INSERT INTO hello_products (name, sale, material, date_prod, conter, cat_id_id, image, description)
SELECT 'Брелок «Moon Charm»', 790, 'Металл и эмаль', '2026-01-14', 126, (SELECT id FROM hello_category WHERE name = 'Аксессуары' LIMIT 1), '', 'Брелок в форме луны для ключей или сумки.'
FROM (SELECT 1 AS x) AS t
WHERE NOT EXISTS (SELECT 1 FROM hello_products WHERE name = 'Брелок «Moon Charm»' AND cat_id_id = (SELECT id FROM hello_category WHERE name = 'Аксессуары' LIMIT 1));

-- Подарки
INSERT INTO hello_products (name, sale, material, date_prod, conter, cat_id_id, image, description)
SELECT 'Свеча «Amber Rain»', 1790, 'Соевый воск', '2026-02-06', 86, (SELECT id FROM hello_category WHERE name = 'Подарки' LIMIT 1), '', 'Ароматическая свеча с нотами янтаря и дождя.'
FROM (SELECT 1 AS x) AS t
WHERE NOT EXISTS (SELECT 1 FROM hello_products WHERE name = 'Свеча «Amber Rain»' AND cat_id_id = (SELECT id FROM hello_category WHERE name = 'Подарки' LIMIT 1));
INSERT INTO hello_products (name, sale, material, date_prod, conter, cat_id_id, image, description)
SELECT 'Свеча «Cedar Night»', 1990, 'Соевый воск', '2026-03-11', 73, (SELECT id FROM hello_category WHERE name = 'Подарки' LIMIT 1), '', 'Свеча с древесным ароматом кедра и мускуса.'
FROM (SELECT 1 AS x) AS t
WHERE NOT EXISTS (SELECT 1 FROM hello_products WHERE name = 'Свеча «Cedar Night»' AND cat_id_id = (SELECT id FROM hello_category WHERE name = 'Подарки' LIMIT 1));
INSERT INTO hello_products (name, sale, material, date_prod, conter, cat_id_id, image, description)
SELECT 'Набор свечей «Trio»', 3990, 'Соевый воск', '2025-11-25', 45, (SELECT id FROM hello_category WHERE name = 'Подарки' LIMIT 1), '', 'Три небольшие свечи с разными ароматами в подарочной коробке.'
FROM (SELECT 1 AS x) AS t
WHERE NOT EXISTS (SELECT 1 FROM hello_products WHERE name = 'Набор свечей «Trio»' AND cat_id_id = (SELECT id FROM hello_category WHERE name = 'Подарки' LIMIT 1));
INSERT INTO hello_products (name, sale, material, date_prod, conter, cat_id_id, image, description)
SELECT 'Диффузор «Silk Garden»', 2290, 'Стекло и ароматическая композиция', '2026-04-22', 62, (SELECT id FROM hello_category WHERE name = 'Подарки' LIMIT 1), '', 'Диффузор с цветочным ароматом и тонкой нотой шёлка.'
FROM (SELECT 1 AS x) AS t
WHERE NOT EXISTS (SELECT 1 FROM hello_products WHERE name = 'Диффузор «Silk Garden»' AND cat_id_id = (SELECT id FROM hello_category WHERE name = 'Подарки' LIMIT 1));
INSERT INTO hello_products (name, sale, material, date_prod, conter, cat_id_id, image, description)
SELECT 'Аромасаше «Lavender»', 690, 'Хлопок и лаванда', '2025-10-09', 140, (SELECT id FROM hello_category WHERE name = 'Подарки' LIMIT 1), '', 'Мешочек с лавандой для шкафа или ящика.'
FROM (SELECT 1 AS x) AS t
WHERE NOT EXISTS (SELECT 1 FROM hello_products WHERE name = 'Аромасаше «Lavender»' AND cat_id_id = (SELECT id FROM hello_category WHERE name = 'Подарки' LIMIT 1));
INSERT INTO hello_products (name, sale, material, date_prod, conter, cat_id_id, image, description)
SELECT 'Подарочный бокс «Уют»', 4490, 'Комбинированный', '2025-12-05', 38, (SELECT id FROM hello_category WHERE name = 'Подарки' LIMIT 1), '', 'Бокс со свечой, чаем и мягким носком для спокойного вечера.'
FROM (SELECT 1 AS x) AS t
WHERE NOT EXISTS (SELECT 1 FROM hello_products WHERE name = 'Подарочный бокс «Уют»' AND cat_id_id = (SELECT id FROM hello_category WHERE name = 'Подарки' LIMIT 1));
INSERT INTO hello_products (name, sale, material, date_prod, conter, cat_id_id, image, description)
SELECT 'Подарочный бокс «Новый год»', 5290, 'Комбинированный', '2025-11-30', 56, (SELECT id FROM hello_category WHERE name = 'Подарки' LIMIT 1), '', 'Праздничный набор с украшением для ёлки и сладостями.'
FROM (SELECT 1 AS x) AS t
WHERE NOT EXISTS (SELECT 1 FROM hello_products WHERE name = 'Подарочный бокс «Новый год»' AND cat_id_id = (SELECT id FROM hello_category WHERE name = 'Подарки' LIMIT 1));
INSERT INTO hello_products (name, sale, material, date_prod, conter, cat_id_id, image, description)
SELECT 'Подарочный бокс «Для неё»', 4790, 'Комбинированный', '2026-02-12', 41, (SELECT id FROM hello_category WHERE name = 'Подарки' LIMIT 1), '', 'Набор из аксессуара, косметики и открытки.'
FROM (SELECT 1 AS x) AS t
WHERE NOT EXISTS (SELECT 1 FROM hello_products WHERE name = 'Подарочный бокс «Для неё»' AND cat_id_id = (SELECT id FROM hello_category WHERE name = 'Подарки' LIMIT 1));
INSERT INTO hello_products (name, sale, material, date_prod, conter, cat_id_id, image, description)
SELECT 'Набор «Чайная церемония»', 3290, 'Чай и керамика', '2026-01-16', 50, (SELECT id FROM hello_category WHERE name = 'Подарки' LIMIT 1), '', 'Керамический чайник, две чашки и сбор из листового чая.'
FROM (SELECT 1 AS x) AS t
WHERE NOT EXISTS (SELECT 1 FROM hello_products WHERE name = 'Набор «Чайная церемония»' AND cat_id_id = (SELECT id FROM hello_category WHERE name = 'Подарки' LIMIT 1));
INSERT INTO hello_products (name, sale, material, date_prod, conter, cat_id_id, image, description)
SELECT 'Набор мыла «Botanica»', 1390, 'Растительные масла', '2025-09-27', 98, (SELECT id FROM hello_category WHERE name = 'Подарки' LIMIT 1), '', 'Три куска натурального мыла с травами.'
FROM (SELECT 1 AS x) AS t
WHERE NOT EXISTS (SELECT 1 FROM hello_products WHERE name = 'Набор мыла «Botanica»' AND cat_id_id = (SELECT id FROM hello_category WHERE name = 'Подарки' LIMIT 1));
INSERT INTO hello_products (name, sale, material, date_prod, conter, cat_id_id, image, description)
SELECT 'Плед «Cloud»', 5990, 'Флис и хлопок', '2025-10-20', 28, (SELECT id FROM hello_category WHERE name = 'Подарки' LIMIT 1), '', 'Мягкий плед для дивана или кресла.'
FROM (SELECT 1 AS x) AS t
WHERE NOT EXISTS (SELECT 1 FROM hello_products WHERE name = 'Плед «Cloud»' AND cat_id_id = (SELECT id FROM hello_category WHERE name = 'Подарки' LIMIT 1));
INSERT INTO hello_products (name, sale, material, date_prod, conter, cat_id_id, image, description)
SELECT 'Кружка «Moon»', 990, 'Керамика', '2026-03-02', 130, (SELECT id FROM hello_category WHERE name = 'Подарки' LIMIT 1), '', 'Керамическая кружка с матовой глазурью.'
FROM (SELECT 1 AS x) AS t
WHERE NOT EXISTS (SELECT 1 FROM hello_products WHERE name = 'Кружка «Moon»' AND cat_id_id = (SELECT id FROM hello_category WHERE name = 'Подарки' LIMIT 1));
INSERT INTO hello_products (name, sale, material, date_prod, conter, cat_id_id, image, description)
SELECT 'Термос «Day & Night»', 2790, 'Нержавеющая сталь', '2026-05-14', 66, (SELECT id FROM hello_category WHERE name = 'Подарки' LIMIT 1), '', 'Термос на 500 мл, который сохраняет тепло до двенадцати часов.'
FROM (SELECT 1 AS x) AS t
WHERE NOT EXISTS (SELECT 1 FROM hello_products WHERE name = 'Термос «Day & Night»' AND cat_id_id = (SELECT id FROM hello_category WHERE name = 'Подарки' LIMIT 1));
INSERT INTO hello_products (name, sale, material, date_prod, conter, cat_id_id, image, description)
SELECT 'Блокнот «Noir»', 890, 'Бумага и экокожа', '2025-12-15', 115, (SELECT id FROM hello_category WHERE name = 'Подарки' LIMIT 1), '', 'Блокнот в чёрной обложке с плотной бумагой.'
FROM (SELECT 1 AS x) AS t
WHERE NOT EXISTS (SELECT 1 FROM hello_products WHERE name = 'Блокнот «Noir»' AND cat_id_id = (SELECT id FROM hello_category WHERE name = 'Подарки' LIMIT 1));
INSERT INTO hello_products (name, sale, material, date_prod, conter, cat_id_id, image, description)
SELECT 'Набор открыток «Constellation» (12 шт.)', 690, 'Дизайнерская бумага', '2026-06-12', 142, (SELECT id FROM hello_category WHERE name = 'Подарки' LIMIT 1), '', 'Двенадцать открыток с иллюстрациями созвездий.'
FROM (SELECT 1 AS x) AS t
WHERE NOT EXISTS (SELECT 1 FROM hello_products WHERE name = 'Набор открыток «Constellation» (12 шт.)' AND cat_id_id = (SELECT id FROM hello_category WHERE name = 'Подарки' LIMIT 1));
INSERT INTO hello_products (name, sale, material, date_prod, conter, cat_id_id, image, description)
SELECT 'Ароматический спрей «Linen»', 1190, 'Парфюмерная композиция', '2026-07-07', 90, (SELECT id FROM hello_category WHERE name = 'Подарки' LIMIT 1), '', 'Спрей для текстиля со свежим ароматом белья.'
FROM (SELECT 1 AS x) AS t
WHERE NOT EXISTS (SELECT 1 FROM hello_products WHERE name = 'Ароматический спрей «Linen»' AND cat_id_id = (SELECT id FROM hello_category WHERE name = 'Подарки' LIMIT 1));
INSERT INTO hello_products (name, sale, material, date_prod, conter, cat_id_id, image, description)
SELECT 'Шкатулка «Pearl»', 3990, 'Дерево и эмаль', '2026-04-28', 33, (SELECT id FROM hello_category WHERE name = 'Подарки' LIMIT 1), '', 'Шкатулка для украшений с перламутровой отделкой.'
FROM (SELECT 1 AS x) AS t
WHERE NOT EXISTS (SELECT 1 FROM hello_products WHERE name = 'Шкатулка «Pearl»' AND cat_id_id = (SELECT id FROM hello_category WHERE name = 'Подарки' LIMIT 1));
INSERT INTO hello_products (name, sale, material, date_prod, conter, cat_id_id, image, description)
SELECT 'Фоторамка «Gallery»', 1590, 'Дерево', '2025-10-24', 79, (SELECT id FROM hello_category WHERE name = 'Подарки' LIMIT 1), '', 'Деревянная рамка формата А5 со стеклом.'
FROM (SELECT 1 AS x) AS t
WHERE NOT EXISTS (SELECT 1 FROM hello_products WHERE name = 'Фоторамка «Gallery»' AND cat_id_id = (SELECT id FROM hello_category WHERE name = 'Подарки' LIMIT 1));
INSERT INTO hello_products (name, sale, material, date_prod, conter, cat_id_id, image, description)
SELECT 'Сертификат SOPHISTICATED 5000', 5000, 'Электронный сертификат', '2026-01-15', 70, (SELECT id FROM hello_category WHERE name = 'Подарки' LIMIT 1), '', 'Подарочный сертификат номиналом 5000 рублей.'
FROM (SELECT 1 AS x) AS t
WHERE NOT EXISTS (SELECT 1 FROM hello_products WHERE name = 'Сертификат SOPHISTICATED 5000' AND cat_id_id = (SELECT id FROM hello_category WHERE name = 'Подарки' LIMIT 1));
INSERT INTO hello_products (name, sale, material, date_prod, conter, cat_id_id, image, description)
SELECT 'Подарочная упаковка «Silk»', 390, 'Бумага и лента', '2026-02-27', 150, (SELECT id FROM hello_category WHERE name = 'Подарки' LIMIT 1), '', 'Упаковочная бумага и атласная лента для небольшого подарка.'
FROM (SELECT 1 AS x) AS t
WHERE NOT EXISTS (SELECT 1 FROM hello_products WHERE name = 'Подарочная упаковка «Silk»' AND cat_id_id = (SELECT id FROM hello_category WHERE name = 'Подарки' LIMIT 1));

-- 3. Фотографии (файлы photo_16.jpg … photo_75.jpg лежат в Al_Ven/media/products/)
UPDATE hello_products SET image = 'products/photo_16.jpg' WHERE name = 'Кольцо «Северная звезда»' AND (image IS NULL OR image = '');
UPDATE hello_products SET image = 'products/photo_17.jpg' WHERE name = 'Кольцо «Тонкая нить»' AND (image IS NULL OR image = '');
UPDATE hello_products SET image = 'products/photo_18.jpg' WHERE name = 'Кольцо «Опал Луны»' AND (image IS NULL OR image = '');
UPDATE hello_products SET image = 'products/photo_19.jpg' WHERE name = 'Кулон «Капля росы»' AND (image IS NULL OR image = '');
UPDATE hello_products SET image = 'products/photo_20.jpg' WHERE name = 'Кулон «Созвездие»' AND (image IS NULL OR image = '');
UPDATE hello_products SET image = 'products/photo_21.jpg' WHERE name = 'Кулон «Лабрадор»' AND (image IS NULL OR image = '');
UPDATE hello_products SET image = 'products/photo_22.jpg' WHERE name = 'Серьги «Жемчужная нить»' AND (image IS NULL OR image = '');
UPDATE hello_products SET image = 'products/photo_23.jpg' WHERE name = 'Серьги-кольца «Орбита»' AND (image IS NULL OR image = '');
UPDATE hello_products SET image = 'products/photo_24.jpg' WHERE name = 'Серьги «Мини-квадрат»' AND (image IS NULL OR image = '');
UPDATE hello_products SET image = 'products/photo_25.jpg' WHERE name = 'Серьги «Кварц»' AND (image IS NULL OR image = '');
UPDATE hello_products SET image = 'products/photo_26.jpg' WHERE name = 'Браслет «Нить судьбы»' AND (image IS NULL OR image = '');
UPDATE hello_products SET image = 'products/photo_27.jpg' WHERE name = 'Браслет «Звенья»' AND (image IS NULL OR image = '');
UPDATE hello_products SET image = 'products/photo_28.jpg' WHERE name = 'Браслет «Лунный камень»' AND (image IS NULL OR image = '');
UPDATE hello_products SET image = 'products/photo_29.jpg' WHERE name = 'Колье «Лунная дорожка»' AND (image IS NULL OR image = '');
UPDATE hello_products SET image = 'products/photo_30.jpg' WHERE name = 'Колье «Чокер Velour»' AND (image IS NULL OR image = '');
UPDATE hello_products SET image = 'products/photo_31.jpg' WHERE name = 'Цепочка «Волна»' AND (image IS NULL OR image = '');
UPDATE hello_products SET image = 'products/photo_32.jpg' WHERE name = 'Цепочка «Классика»' AND (image IS NULL OR image = '');
UPDATE hello_products SET image = 'products/photo_33.jpg' WHERE name = 'Брошь «Полумесяц»' AND (image IS NULL OR image = '');
UPDATE hello_products SET image = 'products/photo_34.jpg' WHERE name = 'Набор «Мини-стек» (3 кольца)' AND (image IS NULL OR image = '');
UPDATE hello_products SET image = 'products/photo_35.jpg' WHERE name = 'Набор «Кристалл» для пирсинга' AND (image IS NULL OR image = '');
UPDATE hello_products SET image = 'products/photo_36.jpg' WHERE name = 'Сумка «Mini Crescent»' AND (image IS NULL OR image = '');
UPDATE hello_products SET image = 'products/photo_37.jpg' WHERE name = 'Рюкзак «City Slim»' AND (image IS NULL OR image = '');
UPDATE hello_products SET image = 'products/photo_38.jpg' WHERE name = 'Шопер «Linen Day»' AND (image IS NULL OR image = '');
UPDATE hello_products SET image = 'products/photo_39.jpg' WHERE name = 'Клатч «Evening»' AND (image IS NULL OR image = '');
UPDATE hello_products SET image = 'products/photo_40.jpg' WHERE name = 'Кошелёк «Origami»' AND (image IS NULL OR image = '');
UPDATE hello_products SET image = 'products/photo_41.jpg' WHERE name = 'Картхолдер «Slim»' AND (image IS NULL OR image = '');
UPDATE hello_products SET image = 'products/photo_42.jpg' WHERE name = 'Ремень «Classic Line»' AND (image IS NULL OR image = '');
UPDATE hello_products SET image = 'products/photo_43.jpg' WHERE name = 'Ремень «Chain»' AND (image IS NULL OR image = '');
UPDATE hello_products SET image = 'products/photo_44.jpg' WHERE name = 'Платок «Aurora»' AND (image IS NULL OR image = '');
UPDATE hello_products SET image = 'products/photo_45.jpg' WHERE name = 'Шарф «Haze»' AND (image IS NULL OR image = '');
UPDATE hello_products SET image = 'products/photo_46.jpg' WHERE name = 'Палантин «Fog»' AND (image IS NULL OR image = '');
UPDATE hello_products SET image = 'products/photo_47.jpg' WHERE name = 'Очки «Clear Lens»' AND (image IS NULL OR image = '');
UPDATE hello_products SET image = 'products/photo_48.jpg' WHERE name = 'Очки «Retro Round»' AND (image IS NULL OR image = '');
UPDATE hello_products SET image = 'products/photo_49.jpg' WHERE name = 'Шапка «Grey Knit»' AND (image IS NULL OR image = '');
UPDATE hello_products SET image = 'products/photo_50.jpg' WHERE name = 'Перчатки «Night Walk»' AND (image IS NULL OR image = '');
UPDATE hello_products SET image = 'products/photo_51.jpg' WHERE name = 'Зонт «Storm Mini»' AND (image IS NULL OR image = '');
UPDATE hello_products SET image = 'products/photo_52.jpg' WHERE name = 'Заколка «Pearl Clip»' AND (image IS NULL OR image = '');
UPDATE hello_products SET image = 'products/photo_53.jpg' WHERE name = 'Набор резинок «Silk» (3 шт.)' AND (image IS NULL OR image = '');
UPDATE hello_products SET image = 'products/photo_54.jpg' WHERE name = 'Часы «Minimal Black»' AND (image IS NULL OR image = '');
UPDATE hello_products SET image = 'products/photo_55.jpg' WHERE name = 'Брелок «Moon Charm»' AND (image IS NULL OR image = '');
UPDATE hello_products SET image = 'products/photo_56.jpg' WHERE name = 'Свеча «Amber Rain»' AND (image IS NULL OR image = '');
UPDATE hello_products SET image = 'products/photo_57.jpg' WHERE name = 'Свеча «Cedar Night»' AND (image IS NULL OR image = '');
UPDATE hello_products SET image = 'products/photo_58.jpg' WHERE name = 'Набор свечей «Trio»' AND (image IS NULL OR image = '');
UPDATE hello_products SET image = 'products/photo_59.jpg' WHERE name = 'Диффузор «Silk Garden»' AND (image IS NULL OR image = '');
UPDATE hello_products SET image = 'products/photo_60.jpg' WHERE name = 'Аромасаше «Lavender»' AND (image IS NULL OR image = '');
UPDATE hello_products SET image = 'products/photo_61.jpg' WHERE name = 'Подарочный бокс «Уют»' AND (image IS NULL OR image = '');
UPDATE hello_products SET image = 'products/photo_62.jpg' WHERE name = 'Подарочный бокс «Новый год»' AND (image IS NULL OR image = '');
UPDATE hello_products SET image = 'products/photo_63.jpg' WHERE name = 'Подарочный бокс «Для неё»' AND (image IS NULL OR image = '');
UPDATE hello_products SET image = 'products/photo_64.jpg' WHERE name = 'Набор «Чайная церемония»' AND (image IS NULL OR image = '');
UPDATE hello_products SET image = 'products/photo_65.jpg' WHERE name = 'Набор мыла «Botanica»' AND (image IS NULL OR image = '');
UPDATE hello_products SET image = 'products/photo_66.jpg' WHERE name = 'Плед «Cloud»' AND (image IS NULL OR image = '');
UPDATE hello_products SET image = 'products/photo_67.jpg' WHERE name = 'Кружка «Moon»' AND (image IS NULL OR image = '');
UPDATE hello_products SET image = 'products/photo_68.jpg' WHERE name = 'Термос «Day & Night»' AND (image IS NULL OR image = '');
UPDATE hello_products SET image = 'products/photo_69.jpg' WHERE name = 'Блокнот «Noir»' AND (image IS NULL OR image = '');
UPDATE hello_products SET image = 'products/photo_70.jpg' WHERE name = 'Набор открыток «Constellation» (12 шт.)' AND (image IS NULL OR image = '');
UPDATE hello_products SET image = 'products/photo_71.jpg' WHERE name = 'Ароматический спрей «Linen»' AND (image IS NULL OR image = '');
UPDATE hello_products SET image = 'products/photo_72.jpg' WHERE name = 'Шкатулка «Pearl»' AND (image IS NULL OR image = '');
UPDATE hello_products SET image = 'products/photo_73.jpg' WHERE name = 'Фоторамка «Gallery»' AND (image IS NULL OR image = '');
UPDATE hello_products SET image = 'products/photo_74.jpg' WHERE name = 'Сертификат SOPHISTICATED 5000' AND (image IS NULL OR image = '');
UPDATE hello_products SET image = 'products/photo_75.jpg' WHERE name = 'Подарочная упаковка «Silk»' AND (image IS NULL OR image = '');
