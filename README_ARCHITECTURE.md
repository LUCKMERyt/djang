# Архитектура и карта кода

> **Зачем этот файл:** объясняет, как устроен проект и куда идти за изменением.
> [`AI_CONTEXT.md`](AI_CONTEXT.md) — это правила для ассистентов и список
> подводных камней; здесь — спокойная карта слоёв без правил и чеклистов.

## Поток запроса

```text
Al_Ven/Al_Ven/urls.py
        ↓
hello/views.py  →  hello/models.py / hello/forms.py
        ↓
hello/templates/*.html
        ↓
hello/static/css/style.css + static/js/{modal,motion}.js
```

## Слои

| Слой | Файлы | Ответственность |
| --- | --- | --- |
| Настройки | `Al_Ven/Al_Ven/settings.py` | БД, Env, Jazzmin, медиа, безопасность |
| Маршруты | `Al_Ven/Al_Ven/urls.py` | именованные URL, раздача media в DEBUG |
| Данные | `hello/models.py` | `Person`, `Category`, `Products`, `Review` |
| Логика | `hello/views.py` | страницы, фильтры, auth, отзывы, SEO |
| Формы | `hello/forms.py` | регистрация, вход, аккаунт, отзывы |
| Auth | `hello/authentication.py` | вход по email, генерация логина |
| Шаблоны | `hello/templates/` | `base.html` + 9 страниц |
| Стили | `static/css/style.css` | тема «Ночной склад», 47 `@keyframes` |
| JS | `static/js/` | модалки и маленькие движения без библиотек |
| Админка | `hello/admin.py`, `templates/admin/index.html` | кастомный дашборд |

## Устоявшиеся имена

- Модель называется `Products` во множественном числе.
- Поля `conter` (количество), `coment` (описание категории), `cat_id` (FK),
  `sale` (цена) — исторические; не переименовывать без миграции.
- `Review` живёт в таблице `hello_reviews`.
- `reverse('index')` возвращает `/index/` из-за двух маршрутов с именем `index`.

## Модальные окна

`products.html` и `news.html` подключают `modal.js`. Кнопка передаёт данные через
`data-product-*` / `data-person-*`, окно подставляет их через `textContent`.
Так исключается выполнение HTML из базы. Не заменяйте это на `innerHTML`.

## Анимации

`base.html` задаёт `body[data-page]` из имени маршрута. Большинство эффектов —
CSS из раздела 13 `style.css`. `motion.js` подключён везде и отвечает только за
прогресс прокрутки, компактный `docbar`, счётчик остатков, «тик» цены и
индикатор пароля. `prefers-reduced-motion` отключает движения.

Подробнее — [`README_ANIMATIONS.md`](README_ANIMATIONS.md).

## Что НЕ делать без задачи

- Не добавлять тяжёлые JS-библиотеки и frontend-фреймворки.
- Не править `admin.css` и кастомный дашборд админки «заодно».
- Не трогать медиа и `db.sqlite3` без явной необходимости.
- Не восстанавливать удалённые дубли `settings.py`/`urls.py` в корне `Al_Ven`.

Связанные документы: [`README.md`](README.md),
[`README_TESTING.md`](README_TESTING.md), [`AI_CONTEXT.md`](AI_CONTEXT.md).
