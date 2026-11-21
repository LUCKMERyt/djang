# Анимации и движения

> **Зачем этот файл:** зафиксировать „контракт движения" отдельно от общего
> README. Список эффектов большой (47 `@keyframes`), и без отдельной карты легко
> случайно добавить тяжёлый эффект или сломать `prefers-reduced-motion`.

## Где живёт

- `hello/static/css/style.css`, **раздел 13** — все 47 `@keyframes` и правила.
- `hello/static/js/motion.js` — только JS-зависимые эффекты.
- `hello/static/js/modal.js` — модалки и монограмма сотрудника.
- `base.html` — `body[data-page]`, `.scroll-progress`, `.logo__text`, подключение JS.

## Группы эффектов

| Группа | Примеры | Где видно |
| --- | --- | --- |
| Накладная | `docbar-stamp`, `section-print`, `bar-draw`, `stamp-tilt`, `row-slide`, `row-sweep` | шапка, разделы, таблицы |
| Склад | `header-scan`, `bar-fill`, `low-pulse`, `approval-stamp` | главная, остатки, штамп `В НАЛИЧИИ` |
| Жемчуг | `pearl-shift`, `logo-shine`, `shine`, `pearl-breathe` | кнопки, логотип, градиенты |
| Карточка товара | `thumb-reveal`, `modal-in`, `backdrop-in`, `image-focus`, `detail-line`, `price-flash` | каталог, модалка |
| Команда | `portrait-reveal`, `person-slide`, `contact-slide`, `monogram-pop` | `/news/` |
| Блог и отзывы | `journal-stamp`, `text-reveal`, `star-pop`, `card-rise` | `/blog/`, `/reviews/` |
| Формы | `form-rise`, `field-in`, `error-shake`, `avatar-ring`, `placeholder-sigh` | вход, регистрация, аккаунт |
| Доступность | `focus-pulse`, `message-in`, `message-success` | фокус, сообщения Django |

Полный список определений и использований — в самом `style.css`: каждый
`@keyframes` определён и применён, «мёртвых» анимаций нет.

## Что делает JS

`motion.js` подключён на всех страницах:

1. `--scroll-progress` — ширина верхней полосы.
2. `body.docbar--compact` — сжатие docbar после 80 px скролла.
3. `data-count` — счётчик остатков через `IntersectionObserver`.
4. `.price--tick` — короткая flash-подсветка цены после GET-фильтров.
5. `.password-strength` — индикатор сложности пароля.

`modal.js` подключают только `products.html` и `news.html`.

## Правила

- Новые эффекты — только по отдельному запросу: сайт уже насыщен движениями.
- Без внешних JS-библиотек и тяжёлых переходов.
- Все анимации обязаны работать с `prefers-reduced-motion: reduce`: медиазапрос
  отключает `animation`, `transition` и скрывает `.scroll-progress`.
- Не разбивайте `style.css` на файлы без необходимости: текущая структура
  проста и проверена.
- Проверка после правок: `node --check` для JS, баланс скобок CSS и совпадение
  списка `@keyframes` со списком использований.

Связанные документы: [`README_ARCHITECTURE.md`](README_ARCHITECTURE.md),
[`README_TESTING.md`](README_TESTING.md), [`AI_CONTEXT.md`](AI_CONTEXT.md).
