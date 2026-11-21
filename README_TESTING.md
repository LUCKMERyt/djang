# Проверки и тестирование

> **Зачем этот файл:** воспроизводимый набор проверок перед коммитом и быстрый
> smoke-тест в браузере. Основной [`README.md`](README.md) даёт только три команды;
> здесь — что именно ожидать и на что смотреть.

## Автоматические проверки

Из каталога `D:\djang\Al_Ven`:

```powershell
$env:DB_ENGINE = "sqlite"
..\.venv\Scripts\python.exe manage.py check
..\.venv\Scripts\python.exe manage.py test hello.tests
..\.venv\Scripts\python.exe manage.py makemigrations --check --dry-run
```

Ожидаемо:

- `System check identified no issues (0 silenced).`
- `Ran 9 tests ... OK`
- `No changes detected`

Проверка JavaScript:

```powershell
node --check D:\djang\Al_Ven\hello\static\js\modal.js
node --check D:\djang\Al_Ven\hello\static\js\motion.js
```

Обе команды должны завершиться без вывода.

## Возможные артефакты

Тест `ProductModalTests` создаёт товар с `SimpleUploadedFile`. После прогона
проверьте `git status`: если в `media/products/` появился временный файл —
удалите его.

Если в самописном скрипте используется `django.test.Client`, добавьте:

```python
from django.conf import settings
settings.ALLOWED_HOSTS += ["testserver"]
```

Иначе Django вернёт `DisallowedHost`.

## Smoke-тест в браузере

| URL | Что проверить |
| --- | --- |
| `/` | полоса прогресса, штамп `В НАЛИЧИИ`, счётчик остатков, фото категорий |
| `/products/` | фильтры, поиск, сортировка со стрелкой, модалка товара, цена после фильтра |
| `/news/` | таблица сотрудников, контакты, модалка с монограммой |
| `/blog/` | штамп «Журнал», линии между записями, заголовки |
| `/reviews/` | форма с CSRF, звёзды, карточки отзывов |
| `/reg/`, `/vhod/` | поля появляются по очереди, индикатор пароля |
| `/account/` | аватар, карточки редактирования, смена имени/логина/пароля |
| `/weo/` | условия поставки, полосы разделов |
| `/admin/` | кастомный дашборд, быстрые действия |

## Проверка доступности

Включите в браузере `prefers-reduced-motion: reduce`: анимации и переходы
должны исчезнуть, а полоса прогресса — скрыться. Это не декоративный пункт,
а часть контракта интерфейса.

## Definition of done

1. `manage.py check`, тесты и `makemigrations --check` зелёные.
2. `node --check` для обоих JS-файлов без ошибок.
3. Smoke-тест по таблице выше пройден.
4. `git status` не содержит случайных временных файлов.
5. При изменении поведения обновлены [`README.md`](README.md) и
   [`AI_CONTEXT.md`](AI_CONTEXT.md).

Связанные документы: [`README_DEPLOY.md`](README_DEPLOY.md),
[`README_ANIMATIONS.md`](README_ANIMATIONS.md).
