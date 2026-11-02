[Сайт-превью](https://luckmeryt.github.io/djang/index.html)

## Локальный запуск

Из каталога `Al_Ven` выполните:

```powershell
..\.venv\Scripts\python.exe manage.py migrate
..\.venv\Scripts\python.exe manage.py runserver
```

По умолчанию приложение подключается к MySQL на `127.0.0.1:3306`:
`DB_NAME=djangoo`, `DB_USER=root`. Пароль передаётся через переменную окружения
`DB_PASSWORD`, а не хранится в исходниках. В PowerShell задайте свои параметры
перед запуском (пароль вводится скрыто):

```powershell
$env:DB_ENGINE = "mysql"
$env:DB_NAME = "djangoo"
$env:DB_USER = "root"
$env:DB_PASSWORD = Read-Host "Пароль MySQL"
$env:DB_HOST = "127.0.0.1"
$env:DB_PORT = "3306"
..\.venv\Scripts\python.exe manage.py migrate
..\.venv\Scripts\python.exe manage.py runserver
```

База `djangoo` должна быть заранее создана, а указанному MySQL-пользователю
нужны права на неё. Вместо `root` предпочтительно создать отдельного пользователя
для сайта. Для локального SQLite можно явно задать `$env:DB_ENGINE = "sqlite"`.

Для публичного сервера обязательно задайте собственный случайный
`DJANGO_SECRET_KEY`, `DJANGO_ALLOWED_HOSTS` (список доменов через запятую),
`DJANGO_DEBUG=False` и HTTPS. Не используйте тестовый локальный ключ в интернете.
Пример генерации ключа:

```powershell
..\.venv\Scripts\python.exe -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

Новые аккаунты хранятся в стандартной модели Django, а пароль сохраняется только
в виде хеша. Миграция `0005_migrate_registered_users` переносит старые аккаунты
из `RegisteredUser` и удаляет прежнюю таблицу с открытыми паролями.
