# Развёртывание в production

> **Зачем этот файл:** отдельный чеклист выпуска. Основной `README.md` содержит
> общие сведения, а здесь собрано только то, что нужно проверить перед тем, как
> открыть сайт наружу: Env, БД, статику, медиа, безопасность и почту.

## 1. Переменные окружения

| Переменная | Разработка | Production |
| --- | --- | --- |
| `DJANGO_DEBUG` | `True` | `False` |
| `DJANGO_SECRET_KEY` | локальный ключ | обязательно свой, случайный |
| `DJANGO_ALLOWED_HOSTS` | `localhost,127.0.0.1,[::1]` | домен сайта через запятую |
| `DB_ENGINE` | `sqlite` | обычно `mysql` |
| `DB_NAME/USER/PASSWORD/HOST/PORT` | демо-значения | реальные учётные данные |
| `DJANGO_SECURE_COOKIES` | `not DEBUG` | `True` |
| `DJANGO_SSL_REDIRECT` | `not DEBUG` | `True` |
| `DJANGO_HSTS_SECONDS` | `0` | `31536000` после проверки HTTPS |
| `SITE_EMAIL/PHONE/ADDRESS` | демонстрационные | настоящие контакты |
| `SITE_VK/TELEGRAM/YOUTUBE` | заглушки | реальные ссылки или уберите блок |

При `DJANGO_DEBUG=False` без `DJANGO_SECRET_KEY` проект не запустится — это
намеренная проверка в `Al_Ven/Al_Ven/settings.py`.

## 2. База данных

1. Создайте БД заранее; MySQL использует `utf8mb4`.
2. Проверьте переменные подключения **до** миграций.
3. Не применяйте миграции к общей или рабочей БД, пока не подтверждено, какую
   именно базу разрешено менять.
4. Сделайте бэкап перед `migrate`.

```powershell
$env:DB_ENGINE = "mysql"
# задайте DB_NAME/DB_USER/DB_PASSWORD/DB_HOST/DB_PORT
..\.venv\Scripts\python.exe manage.py migrate
```

## 3. Статика и медиа

```powershell
..\.venv\Scripts\python.exe manage.py collectstatic --noinput
```

- `staticfiles/` — отдавайте через веб-сервер или CDN.
- `media/products/` и `media/people/` — через веб-сервер, CDN или object storage.
- Django раздаёт `MEDIA_URL` только при `DEBUG=True`; в production это не работает.

## 4. Безопасность и контент

- [ ] Ротировать пароли и ключи, которые когда-то хранились в `dsdsd.txt` и
      остались в истории Git.
- [ ] Убедиться, что в Git нет открытых учётных данных.
- [ ] Заменить `EMAIL_BACKEND = console.EmailBackend` на реальный SMTP/сервис.
- [ ] Указать настоящий домен в `robots.txt` и `sitemap.xml`.
- [ ] Проверить, что отзывы публикуются сразу; при нужной модерации — добавить.
- [ ] Проверить ссылки соцсетей и контакты в футере.

## 5. Финальная проверка

```powershell
$env:DB_ENGINE = "mysql"  # или sqlite для staging
..\.venv\Scripts\python.exe manage.py check --deploy
..\.venv\Scripts\python.exe manage.py test hello.tests
..\.venv\Scripts\python.exe manage.py makemigrations --check --dry-run
```

`check --deploy` покажет предупреждения по production-настройкам; их нужно
разобрать до выпуска. Связка файлов — [`README.md`](README.md),
[`README_TESTING.md`](README_TESTING.md), [`AI_CONTEXT.md`](AI_CONTEXT.md).
