# Быстрый старт

> **Зачем этот файл:** кратчайший путь от пустой консоли до работающего сайта.
> Основной [`README.md`](README.md) — полный справочник; здесь только команды и
> типовые проблемы, чтобы поднять проект локально без чтения всей документации.

## Что понадобится

- Windows + PowerShell.
- Python **3.14.4**.
- Виртуальное окружение `D:\kod\djang-main\.venv` (будет создано, если его нет).

## Команды

```powershell
cd D:\kod\djang-main
if (-not (Test-Path .venv)) { python -m venv .venv }
.\.venv\Scripts\python.exe -m pip install Django==6.1.1 django-jazzmin==3.0.5 mysqlclient==2.3.0 Pillow==13.0.0

cd Al_Ven
$env:DB_ENGINE = "sqlite"
$env:DJANGO_DEBUG = "True"
$env:DJANGO_SSL_REDIRECT = "False"
..\.venv\Scripts\python.exe manage.py migrate
..\.venv\Scripts\python.exe manage.py runserver
```

Откройте:

- сайт — <http://127.0.0.1:8000/>;
- админка — <http://127.0.0.1:8000/admin/>.

Локальная база уже лежит в `Al_Ven/db.sqlite3`, поэтому `migrate` обычно ничего
не меняет, но запускать её безопасно.

## Проверка, что всё живо

```powershell
$env:DB_ENGINE = "sqlite"
..\.venv\Scripts\python.exe manage.py check
..\.venv\Scripts\python.exe manage.py test hello.tests
```

Ожидаемо: `System check identified no issues` и `Ran 28 tests ... OK`.

## Частые проблемы

| Симптом | Причина | Что делать |
| --- | --- | --- |
| Проект пытается подключиться к MySQL | `DB_ENGINE` по умолчанию `mysql` | Выполните `$env:DB_ENGINE = "sqlite"` в той же сессии PowerShell |
| Страница открывается, но нет CSS/JS | Статику не собрал dev-сервер | Убедитесь, что запущен `runserver`, а не `collectstatic`-режим без раздачи |
| HTTPS-ошибки в консоли runserver | Браузер отправляет `https://` на HTTP-порт | Введите `http://127.0.0.1:8000/` явно; HTTPS в режиме разработки выключен |
| Адрес в футере отображается как `РђР...` | Переменная `SITE_ADDRESS` была сохранена в Windows-1251 вместо UTF-8 | Известная форма повреждения исправляется автоматически; для другого текста задайте `SITE_ADDRESS` заново в корректной кодировке |
| Фото товаров не отображаются | `MEDIA_URL` раздаётся только при `DEBUG=True` | Локально оставьте `DJANGO_DEBUG=True`; в production настройте веб-сервер |
| `Invalid HTTP_HOST: testserver` в самописном скрипте | Django не знает тестовый хост | В скрипте добавьте `settings.ALLOWED_HOSTS += ["testserver"]` |

Подробности — в [`README.md`](README.md) и [`AI_CONTEXT.md`](AI_CONTEXT.md).
