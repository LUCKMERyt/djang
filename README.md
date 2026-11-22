# SOPHISTICATED

**Оптовый склад украшений, аксессуаров и подарков для магазинов, маркетплейсов и корпоративных закупок.**

Это русскоязычный Django-проект B2B-витрины. Он показывает товары в наличии,
цены, материалы, даты производства и остатки, а страницы оформлены как накладные:
шапка документа, разделы с полосами-заголовками и таблицы позиций.

| Кратко | Значение |
| --- | --- |
| Назначение | витрина оптового склада, а не розничный магазин |
| Стек | Python 3.14.4, Django 6.1.1, SQLite или MySQL |
| Админка | Django Admin + `django-jazzmin` |
| Вход | по email через собственный `EmailBackend` |
| Анимации | 47 `@keyframes` в `style.css` + небольшой `motion.js` |
| Тесты | 23 теста в `hello.tests` |
| Запуск | PowerShell, команды из каталога `Al_Ven` |

## Содержание

- [Что есть на сайте](#что-есть-на-сайте)
- [Быстрый старт](#быстрый-старт)
- [Переменные окружения](#переменные-окружения)
- [Проверки](#проверки)
- [Куда смотреть в коде](#куда-смотреть-в-коде)
- [Технологии](#технологии)
- [Анимации](#анимации)
- [Структура проекта](#структура-проекта)
- [Известные ограничения](#известные-ограничения)
- [Перед публикацией](#перед-публикацией)

## Что есть на сайте

- **Главная** (`/`) — позиционирование склада, панель остатков (4 случайных
  товара с `conter > 0`, шкала до 100 шт.), карточки категорий, условия поставки
  и три последних отзыва.
- **Оптовый каталог** (`/products/`) — таблица позиций с поиском по названию и
  описанию (`q`), фильтрами по категории (`category_id`), материалу (`material`),
  наличию (`stock=available`) и сортировкой (`sort`: `name`, `sale`, `-sale`,
  `date_prod`). По кнопке «Подробнее» открывается модальное окно `<dialog>`.
- **Команда** (`/news/`) — таблица сотрудников с фото, должностью, возрастом и
  контактами; карточка сотрудника также открывается в модальном окне.
- **Для бизнеса** (`/blog/`) — три статические статьи о закупках, ассортименте и
  перепродаже. Ссылки «Читать далее» пока ведут на `#`.
- **О складе** (`/weo/`) — условия работы, преимущества и что получает партнёр.
- **Отзывы** (`/reviews/`) — форма с CSRF-защитой и лента, новые отзывы сверху.
- **Аккаунт** — регистрация (`/reg/`), вход по email (`/vhod/`), личный кабинет
  (`/account/`) с изменением имени, логина и пароля, выход через POST (`/vyhod/`).
- **Служебные страницы** — `/robots.txt` и `/sitemap.xml` (статические).
- **Админка** — `/admin/`, оформлена через Jazzmin. Главная админки — кастомный
  дашборд в стиле «накладной» с быстрыми действиями: добавить товар, категорию,
  сотрудника и перейти к отзывам.
- **Анимации** — интерфейс оживляют 47 `@keyframes` в разделе 13 `style.css` и
  маленький `motion.js` без библиотек. `prefers-reduced-motion` отключает все
  анимации и переходы, а также скрывает полосу прогресса.

## Быстрый старт

Команды выполняются из `D:\kod\djang-main\Al_Ven`. Виртуальное окружение уже
находится в `D:\kod\djang-main\.venv`.

Если окружение нужно восстановить с нуля:

```powershell
python -m venv ..\.venv
..\.venv\Scripts\python.exe -m pip install Django==6.1.1 django-jazzmin==3.0.5 mysqlclient==2.3.0 Pillow==13.0.0
```

Локальная работа на SQLite (файл `db.sqlite3` уже есть в репозитории):

```powershell
$env:DB_ENGINE = "sqlite"
..\.venv\Scripts\python.exe manage.py migrate
..\.venv\Scripts\python.exe manage.py runserver
```

Работа на MySQL. Создайте базу и отдельного пользователя MySQL с правами только
на эту базу. Имя базы, пользователя и пароль задайте переменными среды; пароля
по умолчанию в исходниках нет:

```powershell
$env:DB_ENGINE = "mysql"
# DB_NAME, DB_USER и DB_PASSWORD должны быть заранее заданы
# в переменных среды Windows, а не сохранены в файле проекта.
$env:DB_HOST = "127.0.0.1"
$env:DB_PORT = "3306"
..\.venv\Scripts\python.exe manage.py migrate
..\.venv\Scripts\python.exe manage.py runserver
```

База должна существовать заранее. Не применяйте миграции к общей или рабочей
БД, пока не подтверждено, какую именно базу можно менять.

## Переменные окружения

| Переменная | По умолчанию | Назначение |
| --- | --- | --- |
| `DB_ENGINE` | `mysql` | `mysql` или `sqlite` |
| `DB_NAME`, `DB_USER`, `DB_PASSWORD`, `DB_HOST`, `DB_PORT` | имя/пользователь/пароль обязательны для MySQL; `127.0.0.1`, `3306` | подключение к MySQL |
| `DJANGO_DEBUG` | `True` | режим отладки; в production — `False` |
| `DJANGO_SECRET_KEY` | генерируется случайно только при `DEBUG=True` | production требует ключ из переменной среды |
| `DJANGO_ALLOWED_HOSTS` | `localhost,127.0.0.1,[::1]` | список хостов через запятую |
| `DJANGO_SECURE_COOKIES` | `not DEBUG` | флаги `Secure` для session/CSRF-кук |
| `DJANGO_SSL_REDIRECT` | `not DEBUG` | принудительный HTTPS |
| `DJANGO_HSTS_SECONDS` | `0` | время HSTS в секундах |
| `DJANGO_TRUST_PROXY_SSL_HEADER` | `False` | включать только за доверенным HTTPS-прокси/туннелем |
| `SITE_EMAIL`, `SITE_PHONE`, `SITE_ADDRESS` | демонстрационные | контакты в футере |
| `SITE_VK`, `SITE_TELEGRAM`, `SITE_YOUTUBE` | заглушки | ссылки на соцсети |

## Проверки

```powershell
$env:DB_ENGINE = "sqlite"
..\.venv\Scripts\python.exe manage.py check
..\.venv\Scripts\python.exe manage.py test hello.tests
..\.venv\Scripts\python.exe manage.py makemigrations --check --dry-run
```

Ожидаемый результат: `System check identified no issues`, `Ran 23 tests ... OK`,
`No changes detected`. Тест модалки создаёт временный файл в
`media/products/` — после прогона его нужно удалить, если он появился в
`git status`.

## Куда смотреть в коде

| Задача | Файл |
| --- | --- |
| Изменить тексты главной | `hello/templates/index.html` |
| Добавить/изменить фильтр каталога | `hello/views.py` (`products`) и `hello/templates/products.html` |
| Изменить текст страницы «О складе» | `hello/templates/weo.html` |
| Изменить контакты | `Al_Ven/Al_Ven/settings.py` (`SITE_*`) и `hello/context_processors.py` |
| Изменить правила отзыва | `hello/forms.py` (`ReviewForm`) и `hello/models.py` (`Review`) |
| Добавить товар, категорию, сотрудника | админка `/admin/` |
| Изменить главную админки | `Al_Ven/templates/admin/index.html` |
| Изменить стили сайта | `hello/static/css/style.css` |
| Изменить анимации и JS-эффекты | `style.css` (раздел 13) и `hello/static/js/motion.js` |
| Изменить поведение модалок | `hello/static/js/modal.js` и `data-*` в шаблонах |
| Добавить страницу | view в `hello/views.py`, путь в `Al_Ven/Al_Ven/urls.py`, шаблон, пункт меню в `base.html` |

Подробная карта для ассистентов — в [`AI_CONTEXT.md`](AI_CONTEXT.md).

### Дополнительные руководства

- [`README_QUICKSTART.md`](README_QUICKSTART.md) — только команды для локального запуска.
- [`README_DEPLOY.md`](README_DEPLOY.md) — чеклист выпуска в production.
- [`README_CONTENT.md`](README_CONTENT.md) — работа с товарами и сотрудниками через админку.
- [`README_ARCHITECTURE.md`](README_ARCHITECTURE.md) — карта слоёв и потока запроса.
- [`README_TESTING.md`](README_TESTING.md) — автоматические и ручные проверки.
- [`README_ANIMATIONS.md`](README_ANIMATIONS.md) — контракт анимаций и доступности.
- [`README_FILES.md`](README_FILES.md) — карта всех файлов: зачем нужен каждый файл и каталог.

## Технологии

- Python 3.14.4 и Django 6.1.1;
- SQLite для локальной разработки, MySQL через `mysqlclient` для рабочего окружения;
- `Pillow` для полей `ImageField`;
- Django ORM и стандартная модель пользователя `User`;
- HTML-шаблоны Django, CSS и небольшой JavaScript без frontend-фреймворка;
- `django-jazzmin` для админки;
- Oswald, IBM Plex Sans и IBM Plex Mono подключаются через Google Fonts.

## Анимации

Анимации собраны в разделе 13 `hello/static/css/style.css` — сейчас это 47
`@keyframes`. Большинство эффектов работают на чистом CSS и привязаны к
`data-page`, который `base.html` берёт из имени текущего маршрута.

Небольшой `hello/static/js/motion.js` подключён на всех страницах и отвечает
только за эффекты, которым нужен JS:

- полоса прогресса прокрутки;
- сжатие и «прилипание» `.docbar` после 80 px скролла;
- счётчик остатков на главной через `IntersectionObserver`;
- короткий «тик» цены после GET-фильтрации каталога;
- индикатор сложности пароля в `reg`, `vhod` и смене пароля.

`hello/static/js/modal.js` подключён в каталоге и команде: он заполняет нативные
`<dialog>` через `data-*` и `textContent`, а также делает pop-анимацию монограммы
сотрудника. Медиазапрос `prefers-reduced-motion: reduce` отключает анимации,
переходы и полосу прогресса.

## Структура проекта

```text
корень/
├── README.md, AI_CONTEXT.md
├── sql/new_products.sql       # сгенерированный SQL для загрузки товаров
└── Al_Ven/
    ├── manage.py
    ├── db.sqlite3             # локальная база SQLite (в репозитории)
    ├── Al_Ven/                # рабочие настройки и маршруты
    │   ├── settings.py        # БД, окружение, Jazzmin
    │   ├── urls.py            # маршруты и раздача media в DEBUG
    │   ├── templates/admin/index.html # кастомный дашборд админки
    │   ├── asgi.py, wsgi.py
    │   └── __init__.py
    ├── hello/
    │   ├── models.py          # Person, Category, Products, Review
    │   ├── views.py           # страницы, фильтры, auth, отзывы, SEO
    │   ├── forms.py           # регистрация, вход, аккаунт, отзывы
    │   ├── authentication.py  # EmailBackend и username_for_email
    │   ├── context_processors.py # SITE_CONTACTS
    │   ├── admin.py           # Django Admin + Jazzmin
    │   ├── tests.py           # 23 теста
    │   ├── management/commands/seed_products.py # загрузка товаров
    │   ├── migrations/        # 0001–0012
    │   ├── templates/         # 10 шаблонов: base + 9 страниц
    │   └── static/
    │       ├── css/style.css  # основной сайт: 2226 строк, 47 @keyframes
    │       ├── css/admin.css  # только админка
    │       ├── js/modal.js    # модальные окна каталога и команды
    │       └── js/motion.js   # прогресс, docbar, счётчик, цена, пароль
    ├── media/
    │   ├── products/          # фото товаров
    │   └── people/            # фото сотрудников
    └── islands_app/           # заготовка, не в INSTALLED_APPS
```

Рабочие настройки и маршруты находятся только в `Al_Ven/Al_Ven/`. Старые
`Al_Ven/settings.py`, `Al_Ven/urls.py` и `django-admin` были удалены как дубли;
не восстанавливайте их без отдельного запроса.

## Известные ограничения

- `/index/` дублирует главную и имеет то же имя `index`, поэтому
  `reverse('index')` возвращает `/index/`, а не `/`. Маршрут оставлен как есть.
- У товаров нет отдельных страниц: подробности показывает модалка.
- Корзины, заказа и оплаты нет — это витрина, а не магазин.
- Статьи `/blog/` статические, их ссылки «Читать далее» не ведут на контент.
- `robots.txt` и `sitemap.xml` содержат относительные URL и заглушку домена.
- Контакты демонстрационные; письма выводятся в консоль
  (`console.EmailBackend`).
- Отзывы публикуются сразу без модерации; при необходимости её нужно добавить.
- `requirements.txt` нет — версии зафиксированы в команде установки выше; при
  обновлении зависимостей обновляйте и эту команду.
- В корне репозитория есть пользовательские скрипты загрузки фото
  (`download_photos*.ps1`, `gen_plan*.py`, `update_db.py` и др.). Это не часть
  приложения: не удаляйте их и не считайте стабильным интерфейсом без запроса.

## Перед публикацией

- [ ] задать `DJANGO_SECRET_KEY`, `DJANGO_ALLOWED_HOSTS`, `DJANGO_DEBUG=False`;
- [ ] проверить `DJANGO_SECURE_COOKIES`, `DJANGO_SSL_REDIRECT`,
      `DJANGO_HSTS_SECONDS` и наличие HTTPS;
- [ ] заменить демонстрационные контакты и соцсети через `SITE_*`;
- [ ] заменить `EMAIL_BACKEND` на реальный SMTP/сервис;
- [ ] указать настоящий домен в `robots.txt` и `sitemap.xml`;
- [ ] настроить отдачу `staticfiles/` и `media/` веб-сервером, CDN или object storage;
- [ ] решить вопрос с модерацией отзывов;
- [ ] убедиться, что секреты и пароли не попали в Git;
- [ ] ротировать учётные данные, которые раньше хранились в `dsdsd.txt` и
      остались в истории Git.

Секреты и пароли не должны попадать в Git.
