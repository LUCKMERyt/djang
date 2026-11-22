# Развёртывание в production

> **Зачем этот файл:** отдельный чеклист выпуска. Основной `README.md` содержит
> общие сведения, а здесь собрано только то, что нужно проверить перед тем, как
> открыть сайт наружу: Env, БД, статику, медиа, безопасность и почту.

## 1. Переменные окружения

| Переменная | Разработка | Production |
| --- | --- | --- |
| `DJANGO_DEBUG` | `True` | `False` |
| `DJANGO_SECRET_KEY` | временный случайный только при `DEBUG=True` | задать свой случайный через среду |
| `DJANGO_ALLOWED_HOSTS` | `localhost,127.0.0.1,[::1]` | домен сайта через запятую |
| `DB_ENGINE` | `sqlite` | обычно `mysql` |
| `DB_NAME/USER/PASSWORD/HOST/PORT` | MySQL требует имя/пользователя/пароль из среды | реальные учётные данные; host/port по необходимости |
| `DJANGO_SECURE_COOKIES` | `not DEBUG` | `True` |
| `DJANGO_SSL_REDIRECT` | `not DEBUG` | `True` |
| `DJANGO_HSTS_SECONDS` | `0` | `31536000` после проверки HTTPS |
| `DJANGO_TRUST_PROXY_SSL_HEADER` | `False` | `True` только за доверенным HTTPS-прокси/туннелем |
| `SITE_EMAIL/PHONE/ADDRESS` | демонстрационные | настоящие контакты |
| `SITE_VK/TELEGRAM/YOUTUBE` | заглушки | реальные ссылки или уберите блок |

При `DJANGO_DEBUG=False` без `DJANGO_SECRET_KEY` проект не запустится — это
намеренная проверка в `Al_Ven/Al_Ven/settings.py`.
Секреты задавайте переменными среды Windows; не сохраняйте их в исходниках,
`.env` или файлах проекта. `DJANGO_TRUST_PROXY_SSL_HEADER=True` задавайте
только если перед Django стоит доверенный прокси/туннель, который сам
перезаписывает заголовок `X-Forwarded-Proto`.

## 2. База данных

1. Создайте БД заранее; MySQL использует `utf8mb4`.
2. Проверьте переменные подключения **до** миграций.
3. Не применяйте миграции к общей или рабочей БД, пока не подтверждено, какую
   именно базу разрешено менять.
4. Сделайте бэкап перед `migrate`.
5. Оставьте MySQL доступным только локальному компьютеру: задайте
   `bind-address=127.0.0.1` в конфигурации MySQL и никогда не пробрасывайте
   порты `3306`/`33060` на роутере.

```powershell
$env:DB_ENGINE = "mysql"
# задайте DB_NAME/DB_USER/DB_PASSWORD/DB_HOST/DB_PORT
..\.venv\Scripts\python.exe manage.py migrate
```

## 3. Статика и медиа

```powershell
..\.venv\Scripts\python.exe manage.py collectstatic --noinput
```

- Production WSGI-конфигурация использует WhiteNoise для `staticfiles/` и
  `media/`. Для небольшого локального сайта это удобно; при высокой нагрузке
  перенесите раздачу файлов на веб-сервер, CDN или object storage.

## 4. Запуск на Windows

Установите серверные пакеты в виртуальное окружение и соберите статику:

```powershell
..\.venv\Scripts\python.exe -m pip install waitress==3.0.2 whitenoise==6.12.0
..\.venv\Scripts\python.exe manage.py collectstatic --noinput
```

Для локальной проверки запустите WSGI-приложение на loopback-интерфейсе:

```powershell
..\.venv\Scripts\waitress-serve.exe --listen=127.0.0.1:8000 Al_Ven.wsgi:application
```

Не публикуйте `runserver` в Интернет. Настройте внешний HTTPS-прокси/туннель
перед включением `DJANGO_SSL_REDIRECT=True` и HSTS; задавайте
`DJANGO_HSTS_SECONDS=31536000` только после проверки HTTPS на домене.

## 5. Безопасность и контент

- [ ] Ротировать пароли и ключи, которые раньше хранились в удалённых
      `dsdsd.txt` и могли остаться в истории Git.
- [ ] Убедиться, что в Git нет открытых учётных данных.
- [ ] Заменить `EMAIL_BACKEND = console.EmailBackend` на реальный SMTP/сервис.
- [ ] Указать настоящий домен в `robots.txt` и `sitemap.xml`.
- [ ] Проверить, что отзывы публикуются сразу; при нужной модерации — добавить.
- [ ] Проверить ссылки соцсетей и контакты в футере.

## 6. Финальная проверка

```powershell
$env:DB_ENGINE = "mysql"  # или sqlite для staging
..\.venv\Scripts\python.exe manage.py check --deploy
..\.venv\Scripts\python.exe manage.py test hello.tests
..\.venv\Scripts\python.exe manage.py makemigrations --check --dry-run
```

`check --deploy` покажет предупреждения по production-настройкам; их нужно
разобрать до выпуска. Связка файлов — [`README.md`](README.md),
[`README_TESTING.md`](README_TESTING.md), [`AI_CONTEXT.md`](AI_CONTEXT.md).
